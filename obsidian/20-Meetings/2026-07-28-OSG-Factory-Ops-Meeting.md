---
type: meeting
date: 2026-07-28
participants:
  - Jeff Dost
  - Marco Mascheroni
  - Hyunwoo Kim
  - Luis Simas
topics:
  - gettarballs.py default-version handling for OS/architecture pairs
  - Kubernetes factory patching mechanisms
  - Architecture "auto" / arch map default handling
  - Condor CE site-token migration status
---

# OSG Factory Ops Meeting

## Summary

Marco Mascheroni described a fix he had already started implementing for `gettarballs.py`: rather than a single string, the "default tarball version" configuration becomes a list per OS/architecture pair, with the first available entry in the list used as the default. This was prompted by problems getting new HTCondor tarballs onto the Kubernetes factories, specifically that Alma Linux 10 (EL10) had no default version because the existing default (23018/23.0.18) does not exist for EL10. While working through where to place a manual/temporary fix, Jeff Dost and Marco walked through the several places the Kubernetes factory deployment involves for overriding generated files (config map with a `.base` suffix, the deployment file mount, and init scripts), and discovered that `gettarballs.py` in the image is actually an old, unused leftover — patches to it should instead go through the newer, cleaner `GWS Factory patches` directory mechanism (the same one already used for a Condor startup patch). Marco separately raised that the OSG frontend had tried setting `architecture=auto` (as opposed to a specific architecture or leaving it unset to get the default), which doesn't currently work because the generated tarball arch map only maps `x86_64` to `default`, not `default,x86_64`, unlike the OS map which does list both forms. Marco had manually added `default,x86_64` (and other observed detection strings) to the generated `01_tarballs` file (not the source YAML) as a stopgap for the 25.x series only. Luis Simas reported continued progress on the Condor CE site-token migration.

## Decisions / Conclusions

- The `gettarballs.py` default-tarball-version parameter will change from a single string to a list; the first entry present is used, falling back through the list if earlier entries aren't available for a given OS/architecture pair. Marco had already implemented this fix.
- The factory will not be touched/restarted this week while OSG runs PEARC-related work, to avoid disrupting anything currently working; routine changes like updating entries are still considered fine.
- The `gettarballs.py` file shipped in the Kubernetes factory image/RPM is not actually used anymore (nothing references it); going forward, patches to it should be placed in the `GWS Factory patches` directory (following the same pattern already used for the Condor startup patch) with an accompanying copy command added to the relevant init script, rather than overwriting it via the old config-map/`.base` mechanism.
- The arch map in the tarball-generation YAML needs to be updated so that `x86_64` maps to `default,x86_64` (matching how the OS map already produces both `default` and the specific OS string, e.g. `default,el8`), to support both the frontend `architecture=auto` case and manual overrides. This will be handled once the new `gettarballs.py`/list-based default version fix is in place, rather than as a separate immediate change.
- Marco's manual workaround (adding `default,x86_64`-style entries directly to the generated `01_tarballs` file) was applied only to the 25.x series, deliberately, to avoid affecting other versions; it will become unnecessary once the new `gettarballs.py` and arch map changes are deployed.
- Jeff will diff Marco's manually modified `01_tarballs` file against the saved base file to identify all of Marco's manual changes, so they aren't lost if Jeff has to regenerate/overwrite that area before the fix lands.
- OSG is currently the only factory affected by the auto-tarball-detection mechanism; other factories don't yet have EL10 tarballs.

## Action Items

- [ ] Finish testing the new `gettarballs.py` (list-based default version fix) — Marco Mascheroni (targeting end of day, before going on vacation next week)
- [ ] Once the new `gettarballs.py` is ready, hand it off to Jeff Dost to test on ITB before deploying — Marco Mascheroni
- [ ] Test the new `gettarballs.py` on ITB, then deploy it (placing it via the `GWS Factory patches` mechanism with a copy command in the init scripts) while Marco is on vacation, being careful not to lose Marco's manual `01_tarballs` changes — Jeff Dost
- [ ] Diff Marco's manually edited `01_tarballs` file against the base file to capture all manual changes before doing any regeneration — Jeff Dost
- [ ] Update the arch map so `x86_64` maps to `default,x86_64` (in addition to just `default`), once the new `gettarballs.py` is deployed — Jeff Dost / Marco Mascheroni
- [ ] Ask Brian Lin (or "Med") about why/whether the OSG frontend's use of `architecture=auto` is an intentionally supported configuration, and whether it relates to PEARC preparation — Jeff Dost (informal, next contact)
- [ ] Add EL10 tarball support to the other (non-OSG) factories — Marco Mascheroni / Jeff Dost (no timeline given)
- [ ] Continue Condor CE site-token migration and open tickets this week — Luis Simas

## Discussion

### Default tarball version per OS/architecture pair

Marco explained the existing problem: for each OS/architecture pair, the factory needs a default tarball version to use when the frontend doesn't specify one. Currently there is a single global default version parameter (e.g. `23018` / 23.0.18), but that version doesn't exist for Alma Linux 10 (EL10), so specifying `condor_os=el10` without a version fails, since there is no fallback. Jeff noted that in practice no connected frontend actually omits the version — they all specify one explicitly — but said he'd prefer the system pick either the oldest available version or the latest ".0" release rather than requiring an explicit default at all. Marco confirmed that specifying a list of versions (e.g. `24.0.x`, `23.0.x`) already works today for the frontend-supplied version list, with the first available one picked per OS (e.g. latest 24 series picked when available, falling back to 23 for EL7 where a newer version doesn't exist). Marco's in-progress fix generalizes the same list-based approach to the *default* version setting, changing it from a single string to a list, so the same fallback logic applies when no version is specified at all. Jeff also raised, as an aside/open question rather than a decision, whether at some point OSG should just stop supporting Red Hat/EL7 entirely.

### Locating where to override `gettarballs.py` on the Kubernetes factories

Marco asked how to get a locally-patched `gettarballs.py` (or an EL10 override) onto the running Kubernetes factory (Tiger) ahead of a real fix landing, since directly editing the `01_tarballs` YAML entries caused duplicate-key errors rather than overriding cleanly. Jeff walked through the Kubernetes factory deployment structure live: an "O2 tarballs" file generates the "O1 tarballs" file; overrides are normally added as a `.base`-suffixed config map entry that gets mounted and then copied to the "live" file location by an init script, and separately the file must be referenced in the deployment's customization/config map list. While tracing this for `gettarballs.py`, Jeff discovered that the copy of the script inside the container image (referenced from a `prep tarball` script) is not actually referenced/used anywhere in the current setup — a leftover from before the newer patching approach existed. Jeff also found that a Condor startup file is still being overwritten via this same old mechanism, which surprised him ("I didn't realize we're still overwriting that").

Instead, Jeff recommended treating a `gettarballs.py` override like the existing `GWS Factory patches` mechanism used for the Condor startup patch: files placed in a patches directory are automatically mounted at a fixed path and copied into place by an init script (`40-patch`), without needing to individually list each file in the customization/config map (unlike the `.base`-file approach, which does require explicit listing). This approach also avoids needing to build and roll out a new container image for each patch — patches placed this way take effect without a merged pull request or new image, whereas an image-embedded fix would require both. Marco confirmed this was preferable given the friction of needing a new image for every patch iteration. Jeff suggested making a note to consider removing the unused old `gettarballs.py`/Condor-startup-in-image mechanism at some point, since it now appears to only add confusion.

### `architecture=auto` and the arch map

Marco reported that the OSG frontend had configured `architecture=auto` for entries using ARM (as opposed to leaving architecture unset, which gets a `default` value, or specifying `arc64` explicitly) — this had not previously been tested and did not work. The likely reason: for the OS map, the generated tarball YAML maps a detected OS string (e.g. Alma Linux 8) to both a specific label and `default` (e.g. `default,el8`), but the equivalent arch map only maps `x86_64` to `default`, not to `default,x86_64`. Jeff and Marco worked through the live example Brian Lin had pasted in Slack, where the pilot's self-detected architecture string looked like `x86_64` (with variations Marco had observed, e.g. `x86_64`/`x86-64`), which doesn't match a bare `default` entry. Marco had manually added `default,x86_64`-style entries to the generated `01_tarballs` file (not the source arch-map YAML), scoped only to the 25.x tarball series, as an immediate workaround; he deliberately avoided touching the mapping for all versions to limit blast radius. Both agreed the underlying fix is a YAML-only change (no code change) to the arch map, mirroring how the OS map already lists both the specific and `default` forms, and that it doesn't need to happen immediately — it will be done once the new `gettarballs.py` fix is deployed. Jeff noted this whole area only currently affects OSG, since other factories don't have EL10 tarballs and aren't using the auto-tarball-detection setup yet (though it exists more broadly, it is launched manually).

Jeff also noted OSG appeared to be doing significant work that week in preparation for PEARC, and speculated the `architecture=auto` attempt might be related, though this was not confirmed.

### Condor CE site-token migration (brief update)

Luis Simas said there wasn't much new on factory operations; he is continuing the Condor CE migration to site tokens, having completed Tier-1 sites for CMS and some Tier-2/Tier-3 sites. He expects to open some tickets this week.

### Other updates

Hyunwoo Kim reported nothing to share; factory operations were quiet the previous week.

## Open Questions

- Whether `architecture=auto` is intended to be a fully supported configuration for the glideinWMS/frontend scripts, and why the OSG frontend attempted to use it (possibly related to PEARC preparation) — Jeff planned to ask Brian Lin or "Med."
- When exactly OSG needs the EL10/tarball fixes in place, and whether/when to stop supporting Red Hat 7/EL7 more broadly.
- Whether the unused, image-embedded `gettarballs.py` and Condor-startup overwrite mechanism should simply be removed now that the patch-directory approach is preferred.

## Related

[[OSG]] · [[HTCondor]] · [[glideinWMS]] · [[Factory Operations]] · [[Factory Configuration]] · [[Kubernetes]] · [[Pilot Jobs]]

## Source

meeting_saved_closed_caption.txt (from `2026-07-28 17.07.29 OSG Factory Ops Meeting`)
