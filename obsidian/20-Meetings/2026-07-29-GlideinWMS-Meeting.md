---
type: meeting
date: 2026-07-29
participants:
  - Marco Mascheroni
  - Marco Mambelli
  - Namratha Urs
  - Shreyas Bhat
topics:
  - GLIDEIN_Site attribute fallback logic and a suspected entry-name/glidein-element-name bug
  - ID token generator script location (3.10 vs 3.11)
  - get_tarball script default Condor tarball version fallback list (AlmaLinux 10 vs EL7)
  - Issue #281 PR: ID token path and job token cleanup
  - 6.2.0D release status
---

# GlideinWMS Meeting

## Summary

This transcript is a partial capture of a recurring GlideinWMS meeting (release/testing discussion followed by round-table updates); it begins mid-conversation, so earlier context for the opening topic is missing. The captured portion covers a discussion of the `GLIDEIN_Site` attribute fallback behavior and a possible bug in it, a clarification about which ID-token generator script is used in 3.10 vs 3.11, an update from Marco Mascheroni on a fix to the `get_tarball` script's default Condor version handling, a round-table update from Shreyas Bhat on a PR for issue #281, and a brief exchange about the still-pending 6.2.0D release. A participant labeled `[WH8XE- Quarium]` appears throughout; Namratha Urs addresses this speaker directly as "Steve" once, so this label likely (but not certainly) represents Steve speaking from a shared room/endpoint.

## Decisions / Conclusions

- GlideinWMS itself does not require `GLIDEIN_Site` to be defined on a factory entry; for CMS, the required attribute is `GLIDEIN_CMSSite`. The entry name, by contrast, is always defined, which is the reasoning behind using the entry name as a fallback when `GLIDEIN_Site` is not set.
- Marco Mascheroni suspects the fallback logic has a bug: it appears to use the "glidein element name" instead of the entry name, which he believes caused a key error / "name not found" when he tested it. He is testing a fix as part of a separate factory-operations pull request (not tied to a release).
- In GlideinWMS 3.10, the ID token generator is an internal function; in 3.11, the ID token generator script located in the `plugins` directory is used instead.
- Marco Mascheroni fixed an issue in the `get_tarball` script (used by factory operations to download Condor tarballs from the HTCSS website for worker nodes): the default Condor tarball version was previously a single hard-coded version (e.g., 23.0.18) per OS/architecture, but no single version was available for all supported operating systems (e.g., available for EL7 but not AlmaLinux 10, or vice versa for newer versions). He changed the default tarball version from a single value to a list of fallback versions per OS/architecture pair, so the script tries each in order until one is found, covering all currently supported OS/architecture combinations.
- Shreyas Bhat submitted a PR for issue #281 making two changes related to ID tokens: `ID_TOKENS` now points to the path inside the glidein itself where the ID token is stored, and `JOB_TOKENS` is unset/removed in the glidein because it previously pointed to a file on the factory that no longer exists by the time the glidein starts. The PR is awaiting approval.
- The 6.2.0D release was not yet out as of this meeting (confirmed by Marco Mambelli in response to a question).

## Action Items

- [ ] Test the `GLIDEIN_Site` fallback fix (entry name vs. glidein element name) and report back — Marco Mascheroni

## Discussion

### GLIDEIN_Site fallback logic
The discussion (already in progress when the transcript starts) concerned why `GLIDEIN_Site` is not always defined on factory entries. Marco Mascheroni explained that only `GLIDEIN_CMSSite` is required for CMS, and GlideinWMS itself does not require `GLIDEIN_Site`; the entry name is always defined, which is why the fallback to entry name exists. `[WH8XE- Quarium]`/Steve suggested that other things depend on `GLIDEIN_Site`, implying it might be worth always defining it; Marco Mascheroni agreed this was a good point and noted "Jeff has a plan" for this, and said he might raise it at a future Factory Ops meeting (stated tentatively, not as a firm commitment). Marco Mambelli added that `GLIDEIN_Site` is not enforced but is useful, and that OSG is also looking at this attribute; he proposed that if a `GLIDEIN_CMSSite`-equivalent is set, it could be set equal to `GLIDEIN_Site` to avoid defining it twice, while keeping the fallback in place. Marco Mascheroni then noted a possible bug in the fallback implementation (using glidein element name instead of entry name), which he is testing.

### ID token generator script
In response to a question from Namratha Urs about whether the ID token generator script in the `plugins` directory is still used with 3.11 factories/front ends, Marco Mambelli clarified that 3.10 uses an internal function for this, while 3.11 uses the generator script located in `plugins`.

### get_tarball script default Condor version fix
Marco Mascheroni described a fix to the `get_tarball` script, which factory operations uses to download Condor tarballs from the HTCSS website for use by worker nodes. The script has logic to download tarballs only for certain operating-system/architecture combinations, and falls back to a default tarball version when the front end doesn't specify a Condor version for a given OS/architecture pair. The previous default was a single hard-coded version, which did not exist for all supported operating systems simultaneously (worker nodes currently span multiple OS versions, with no single Condor version available for all of them, including continued support for some EL7 nodes). He changed the default from a single version to a list, so the script iterates through fallback versions per OS/architecture until it finds one that exists, covering all current OS/architecture pairs.

### Issue #281 PR (Shreyas Bhat)
Shreyas Bhat reported submitting a PR for issue #281 with two changes to ID-token-related variables: `ID_TOKENS` now points to the in-glidein path where the ID token is stored, and `JOB_TOKENS` is unset in the glidein, since it previously pointed to a file on the factory that no longer exists by the time the glidein starts. The PR is awaiting approval; he is looking to pick up his next ticket in the meantime.

### Round table
- `[WH8XE- Quarium]`/Steve asked about the status of the 6.2.0D release, expecting it to have been out already. Marco Mambelli said it was not out yet.

## Open Questions

- Should `GLIDEIN_Site` be defined on every factory entry rather than relying on the entry-name fallback, given that other tools (and OSG) depend on this attribute?
- Is the fallback logic actually using the glidein element name instead of the entry name, as Marco Mascheroni suspects, and does his fix resolve it?
- When will the 6.2.0D release be published?

## Related

[[glideinWMS]] · [[Factory]] · [[Factory Operations]] · [[Factory Configuration]] · [[HTCondor]] · [[CMS]] · [[OSG]] · [[Pilot Jobs]]

## Source

meeting_saved_closed_caption.txt (from `2026-07-29 17.09.41 GlideinWMS Meeting`)
