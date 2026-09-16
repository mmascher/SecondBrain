---
type: meeting
date: 2026-04-28
participants:
  - Jeff Dost
  - Marco Mascheroni
  - Luís Simas
  - Hyunwoo Kim
topics:
  - glideinWMS 3.11.4 release-candidate status
  - ARM (aarch64) resource support in glideinWMS/HTCondor
  - Condor CE auth method migration to site token
  - ARC CE submission troubleshooting
  - Fermilab power outage impact on factory operations
  - Factory-ops poster planning
  - Pilot-efficiency monitoring script / timezone handling
---

# OSG Factory Ops Meeting

## Summary

Jeff Dost reported that glideinWMS 3.11.4 testing is still blocked on a further release candidate beyond RC2, which he believes is waiting on Marco Mascheroni's autoconf/ARM-related fixes; Marco agreed to follow up with Marco Mambelli. Marco separately described work validating CMS jobs on ARM resources, including a factory-side fix for singularity image mapping and a discovered glideinWMS/HTCondor bug where an automatically-added architecture requirement keeps pilots idle at CERN's ARM resources. Luís Simas gave a status update on testing Condor CE entries for site-token authentication and raised a separate ARC CE troubleshooting question, for which Jeff and Marco suggested using low-level ARC submission tools to gather more diagnostic information. Hyunwoo Kim reported a power outage affecting the Fermilab Tier-1 cluster; the group agreed no factory-level action was needed given the short expected downtime. The group also briefly discussed pilot-efficiency monitoring timezone handling and confirmed a planned CERN-side log sync/monitoring setup remains deprioritized until after CHEP. The meeting closed with plans to hold a dedicated session on the factory-ops poster on Thursday.

## Decisions / Conclusions

- No enabled CMS entries currently declare more than one auth method.
- Entries with `enabled: false` should still be included in the Condor CE site-token migration work, since they are sometimes re-enabled later (revising Jeff's earlier guidance that disabled entries could be ignored).
- For the Fermilab power outage, no factory-level action (e.g. marking entries down, declaring an OSG/topology downtime) was needed: glideins that can't start at Fermilab will naturally match elsewhere, and other sites tend to already be saturated with pilot pressure regardless. A downtime declaration would only be reconsidered if the outage were expected to last days rather than hours.
- Setting up an rsync-based log sync (requiring Kubernetes updates) so CERN can monitor "Tiger" factory-side Condor activity logs remains deprioritized; it is not urgent for CHEP since Fermilab and CERN factory data are already sufficient for the relevant overload plots, and can wait until after CHEP.
- Factory Condor activity logs are in UTC; the web monitoring UI, by contrast, displays times adjusted to the browser's local timezone.

## Action Items

- [ ] Follow up with Marco Mambelli about the status of the ARM-related autoconf pull request (no reply seen yet) — Marco Mascheroni
- [ ] Update the glideinWMS 3.11.4 status tracking table to reflect that it is still in testing (RC2) — Jeff Dost
- [ ] Continue the glideinWMS/HTCondor fix (with Marco Mambelli) for the architecture-requirement bug blocking ARM pilots at CERN — Marco Mascheroni
- [ ] Write a script to test Condor CE authentication for each entry, first via a shipping-style test, then by flipping entries in ITB and submitting individual test pilots — Luís Simas
- [ ] Look into low-level ARC submission tooling (e.g. an ARC REST client) together, to help produce more diagnostic information for the ARC CE ticket and potentially document an example for future use — Luís Simas, Marco Mascheroni
- [ ] Try demonstrating to the site admin that a direct `arc submit` succeeds, to help push the site to look harder for server-side batch-system logs — Luís Simas
- [ ] Update the pilot-efficiency monitoring script to stop assuming the local timezone and instead treat factory Condor activity logs as UTC — Luís Simas
- [ ] Prepare/continue updates to the factory-ops poster draft and email major updates to Marco Mascheroni before Thursday — Jeff Dost
- [ ] Hold a dedicated meeting on the factory-ops poster on Thursday at 4 PM (Marco's time), one hour before the regular SI chat — Jeff Dost, Marco Mascheroni

## Discussion

### glideinWMS 3.11.4 status

Jeff Dost said he still has a few things to verify for 3.11.4 and is waiting on bug fixes, including autoconf-related fixes from Marco Mascheroni, to land in a release candidate beyond RC2 — the only one currently visible in the repo. Marco had previously told Jeff to hold off because another release candidate was coming, but Marco now believes this may be waiting on a pull request he submitted (regarding ARM) that he has not seen a reply to from Marco Mambelli. Jeff will mark 3.11.4 as still in testing in his tracking table.

### ARM (aarch64) resource validation

Marco Mascheroni described testing CMS jobs on ARM resources, prompted by renewed interest raised in the CMS offline computing general meeting (the software stack had last been validated end-to-end on ARM roughly 4–5 years ago, when CMS software was not yet ready; some things were again found broken this time). For ARM resources, the singularity image mapping normally set in the front end must be overridden so that EL7/EL8/EL9 map to ARM images instead of the default x86_64 images; Marco fixed this in the factory repository.

Separately, Marco found that glideinWMS/HTCondor automatically adds a `TARGET.Arch == x86_64` requirement to the pilot submission (since factory machines are x86_64). At CERN, the compute element enforces this requirement, so ARM pilots stay idle and never run on ARM resources there. Two other ARM sites, NAF and KIT (each contributing roughly 1,000–2,000 cores), appear to route pilots without checking this requirement, so the issue does not manifest there — Marco suggested this may depend on the batch system in use. Marco is working with Marco Mambelli to fix this in glideinWMS; this fix is believed to be one of the items Jeff is waiting on for the next 3.11.4 release candidate.

### Condor CE auth method migration (site token)

Luís Simas reported he sent an email summarizing the current state of Condor CE entries but has not yet made any changes. Jeff reiterated that entries with `enabled: false` could be considered decommissioned and ignored, but Luís noted that since such entries are sometimes re-enabled, he included them in scope anyway for consistency; Jeff agreed this was reasonable. Luís confirmed no enabled CMS entries currently declare more than one auth method, and that roughly 200 Condor CE entries declare grid-proxy authentication.

The plan, per Luís (building on an idea from Marco), is to write a script to test authentication for each entry: first testing via a shipping-style Condor CE test, then flipping entries individually in ITB and submitting a test pilot end-to-end. Jeff agreed this approach makes sense — entries that pass can be updated immediately, while others will require reaching out to the affected sites to understand why site-token authentication doesn't work. Jeff was uncertain what to expect overall but was optimistic that most Condor CEs should work. Jeff also noted this exercise is a good learning opportunity for submitting jobs and testing end-to-end.

### ARC CE submission troubleshooting

Luís Simas raised a question while troubleshooting a ticket involving an ARC CE with a site admin: the pilot submits successfully to the CE, but the subsequent submission from the CE to the underlying batch system fails, and the site admin claims no logs or failure information are available. Luís asked whether there is any way to get more information beyond the grid manager logs.

Jeff recalled that Marco has (or had) a web page with recipes for manually running ARC commands (possibly via the ARC REST interface) to debug issues end-to-end, previously used mainly for authentication issues; he was unsure whether it would help in this failure mode or whether it covers submission specifically. Marco noted the page doesn't currently have a submission example but offered to create one together with Luís — potentially using an LLM to help figure out installing an ARC REST client and submitting a pilot from an external node to an ARC CE. Marco also mentioned the ARC "gap" (grid manager) log, likely located under `/var/tmp` or a similar login-accessible path, as a possible additional source of information. Both Jeff and Luís expressed surprise that the site admin claims no server-side logs exist for a failure that appears to occur on the batch-system side. Marco suggested that demonstrating a direct `arc submit` success to the site admin might help motivate them to look more carefully for logs.

### Fermilab power outage

Hyunwoo Kim reported that an electrical tower near Fermilab collapsed around 1 PM the previous day, causing a power outage that took down the Tier-1 cluster and all worker nodes (factory and CE servers remained up but were not useful without workers). An email indicated restoration was expected later that day (afternoon or evening); this was described as better than initially feared, since an earlier estimate suggested the outage could last the entire week. The lab itself was closed and Hyunwoo did not have visibility into effects on experiments or backup power.

Hyunwoo asked whether Fermilab entries should be marked down so glideins would route elsewhere. Jeff explained this isn't necessary: if glideins can't start at Fermilab, jobs will automatically match at other sites with no action required. He said a downtime declaration in OSG/topology would only be considered if the outage were expected to last multiple days. Marco agreed, adding that other sites tend to already be saturated with pilots regardless, so not declaring a downtime doesn't create additional risk. Hyunwoo confirmed CEs were still receiving and routing glideins, which remained idle pending worker availability. Jeff noted the team could help clear out old pilots from the factories to encourage new submissions if the outage persisted beyond the estimate.

### Pilot-efficiency monitoring and timezone handling

Luís asked whether "the factory" (referred to in the discussion as the "Tiger" factory) uses local time or UTC, in the context of writing a new script to monitor pilot efficiency; old scripts had incorrectly assumed local time. Jeff confirmed factory Condor activity logs are in UTC. He noted separately that the web-based monitoring UI adjusts displayed times to the browser's local timezone, which can create confusion. Luís mentioned CERN's monitoring machine doesn't currently have logs for this factory, which they may look into in the future.

This led to a reminder that a planned rsync-based log sync to CERN (requiring Kubernetes updates) was never set up, having been repeatedly deprioritized behind higher-priority work. Marco clarified this sync is unrelated to the site-token effort — it concerns getting overload-related plots for CHEP — but is not urgent since data from Fermilab and CERN factories is already sufficient for that purpose; both Jeff and Marco agreed it could wait until after CHEP.

### Factory-ops poster

Marco confirmed he reviewed Jeff's rough first draft of the factory-ops poster and thought it was a good starting point. Jeff said he still wants to make further updates — turning it into more of a graphic illustrating the current situation, how the proposed approach improves it, an example ticket exchange with a site admin, and a table showing how the whole process works end-to-end. He had hoped to work on it the previous evening but was too tired. They agreed to have a dedicated discussion on Thursday rather than cover it in this meeting, with Jeff sending updates by email or ping beforehand so Marco could comment ahead of time. Thursday's poster discussion was set for 4 PM (Marco's time), one hour earlier than their usual slot to avoid conflicting with the SI chat; Jeff noted this is a little early for him but agreed to make it work.

## Open Questions

- When the next glideinWMS 3.11.4 release candidate (incorporating the ARM/autoconf fixes) will be available.
- Whether the glideinWMS/HTCondor architecture-requirement fix for ARM pilots at CERN will be included in 3.11.4 or a later release.
- Why the ARC CE site admin claims no server-side batch-system logs are available, and whether ARC's own grid-manager logs or REST interface can surface more diagnostic information.
- Final results of the Condor CE site-token authentication testing, and which sites will need direct follow-up.

## Related

[[OSG]] · [[CMS]] · [[CERN]] · [[HTCondor]] · [[glideinWMS]] · [[Factory Operations]] · [[Factory Configuration]] · [[Pilot Jobs]]

## Source

meeting_saved_closed_caption.txt (from `2026-04-28 17.06.49 OSG Factory Ops Meeting`)
