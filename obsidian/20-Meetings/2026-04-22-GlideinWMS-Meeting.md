---
type: meeting
date: 2026-04-22
participants:
  - Marco Mascheroni
  - Marco Mambelli
  - Shreyas Bhat
  - Namratha Urs
  - Jeff Dost
  - Nick Peregonow
  - Steve White
topics:
  - GPU partitioning / logical GPUs (Condor `-divide`, resource slot config)
  - ID tokens for GLAD variables (issue #281)
  - analyze_entries RRD statistics discrepancies
  - Lancaster glidein working-directory issue
  - HTCondor 3.11 upgrade (front end / OSG pool)
  - HTCondor CE GSI vs. token flag
  - front-end proxy / ID token authentication troubleshooting
  - InCommon webinar
---

# GlideinWMS Meeting

## Summary

This was a GlideinWMS development/status meeting covering several parallel threads. The bulk of the early discussion was a technical exchange between Marco Mascheroni and Marco Mambelli about how to configure logical/partitioned GPUs for an upcoming CHEP contribution on heterogeneous computing, concluding that this can currently be done via matching, consistent configuration in two places (factory Condor attributes and the resource slot configuration) without code changes. Shreyas Bhat gave a brief update on ID-token-related work (issue #281) and asked to schedule time to review testing with Marco Mambelli or Namratha Urs. Namratha Urs reported ongoing investigation into discrepancies between `analyze_entries` glidein/job statistics and actual values, tracing the issue toward how RRD tool fetch consolidates (averages) data points; Jeff Dost noted the factory-ops team generally distrusts those numbers already and mainly relies on the report for validation/startup errors. Vito (Quarium) reported a Lancaster site issue where glideins were running in the wrong working directory. Nick Peregonow reported the HTCondor 3.11 upgrade on GP Grid went smoothly, but surfaced an issue with HTCondor CEs still reporting GSI-only support, which Jeff explained is a known flag CMS is now clear to flip; a related, unresolved bug prevents upgrading the OSG pool to 3.11 for front ends using project ID. Nick and Marco Mambelli then debugged why disabling the front-end GSI proxy breaks communication to the factory in Nick's setup, without reaching a resolution; they agreed to continue offline once Nick shares his configuration. Vito mentioned an InCommon webinar on future services happening that day.

## Decisions / Conclusions

- For the GPU partitioning experiment (targeting a CHEP contribution on heterogeneous computing), Marco Mambelli concluded the current approach requires two consistent configuration changes: (1) Condor attributes added to the factory configuration (glidein resource slot) to make Condor split/advertise the GPU, and (2) the corresponding number set in the resource slot configuration (which defaults to `auto` but can take an explicit number). The same number must be used in both places; this is described as "a little bit hacky" since it is not a single unified parameter, but should work without code changes for now. A more robust mechanism would require future code changes.
- Marco Mascheroni confirmed the GPU-splitting settings for Condor would go in the submit attributes (Condor attributes placed in the submit file), separate from the resource-slot GPU count setting.
- The Lancaster glidein working-directory issue was attributed by Vito to something on the site's end; the site asked for a factory ticket/change, and roughly 11 of 16 states were reported working with 2 others tried and failed (exact meaning of "16 states" was not further clarified in the transcript).
- HTCondor 3.11 upgrade of GP Grid (front end) went smoothly for Nick Peregonow, largely reusing prior work done with Bruno for an earlier RC candidate upgrade.
- CMS has given the go-ahead to flip the flag so HTCondor CEs stop reporting GSI-only support; Jeff Dost and Marco Mascheroni agreed to test this in ITB first, then flip it across entries, expected within about a week.
- A known, unresolved bug tied to front ends using project ID is currently blocking the upgrade of the OSG pool to 3.11; per Vito, essentially no entries currently use project ID except one legacy case (a Nova group and an "Ohio Supercomputing Center"-type entry), which have reportedly not been used in a long time.
- Marco Mambelli confirmed that disabling the front-end GSI proxy is possible ("you can do it") in principle, and that some installations already run with only an ID token to the factory and a site token to the CE — but this did not resolve Nick's specific issue, where jobs/communication to the factory stopped working when Nick tried removing the front-end proxy (setting the security class ad's front-end-proxy setting to the host cert), even though his SCHEDDs already authenticate purely via tokens.

## Action Items

- [ ] Schedule time on Friday with Marco Mambelli or Namratha Urs to walk through testing changes for issue #281 (ID tokens / GLAD variables) — Shreyas Bhat
- [ ] Try configuring matching GPU-split values in the factory Condor attributes and the resource slot configuration (no code change) — Marco Mascheroni
- [ ] Continue investigating whether `analyze_entries`' glidein/job counts reflect actual or RRD-consolidated (averaged) values — Namratha Urs
- [ ] Test the HTCondor-CE GSI-flag change in ITB before flipping it across entries — Jeff Dost / Marco Mascheroni
- [ ] Share front-end/group configuration with Marco Mambelli so he can look into why removing the front-end GSI proxy breaks factory communication — Nick Peregonow
- [ ] Follow up with Nick Peregonow next week on the front-end proxy configuration issue — Marco Mambelli
- [ ] Follow up with Namratha Urs about a release review Marco Mambelli has started going through — Marco Mambelli

## Discussion

### GPU partitioning / logical GPUs
The discussion opened with a follow-up on a mailing-list thread (raised by Vito) about "logical GPUs": once a logical GPU is created via MIG-style splitting on a GPU node, its size is fixed for the lifetime of the glidein's `startd` and cannot be resized later (e.g., a 4-GPU node split 1/3 cannot later be repartitioned 2/2). Marco Mambelli confirmed this is defined at `startd` startup in Condor and stays fixed for the pilot's duration, regardless of how many jobs run within it — this is a static, not dynamic, partition.

Marco Mascheroni explained the goal is to advertise multiple logical GPUs from what is physically one GPU (relying on Condor's own GPU scheduling), sharing GPU memory rather than doing true hardware partitioning (MIG). The risk is running out of memory if usage isn't well-behaved, but the assumption is that jobs will request and respect a memory limit. This is described as an experiment intended to produce results for a CHEP talk on heterogeneous computing, with potential future reuse in production if promising.

Marco Mambelli confirmed this would be configured per-site in the factory configuration by adding Condor attributes there. He then walked through the concrete mechanism: Condor attributes (to make Condor split the GPU) go in the glidein/factory configuration's submit attributes (i.e., attributes placed in the Condor submit file), while the GPU count itself is set via the resource slot configuration, which defaults to `auto` but can be set to an explicit number (as CMS/OSG typically already does). Both numbers must match and be kept consistent manually, since there is currently no single parameter controlling both. Marco Mascheroni raised a follow-up question about what happens if a job requests more GPUs (`request_gpus`) than are actually available on a node (risk of jobs idling forever); Marco Mambelli suggested using the same number in both places should avoid this, and the two agreed to test and touch base again. Marco Mambelli noted this configuration-only approach should work for now, with a more robust mechanism to follow later via code changes.

### ID tokens for GLAD variables (issue #281)
Shreyas Bhat reported he has identified likely code locations for the change needed for issue #281 (ID tokens file / GLAD variables) but is still unfamiliar with the codebase and wants to confirm whether the change actually works. He asked to schedule time with Marco Mambelli or Namratha Urs on Friday to go over testing; Marco Mambelli agreed.

### analyze_entries statistics discrepancies (Namratha Urs)
Namratha Urs is not currently working on the decision engine and instead has been investigating a discrepancy (raised earlier by Jeff Dost) between the number of glideins and jobs reported by `analyze_entries` and the actual numbers. She has narrowed the investigation to how RRDs are created/updated and read, and believes an RRD tool fetch may return a consolidated (averaged) value over the configured step interval (30 seconds by default) rather than the actual raw data point. She asked Jeff whether he had previously observed the reported glidein/job numbers being roughly accurate or noticeably too high.

Jeff Dost responded that the factory-ops team generally does not trust many of the numbers in those reports; in practice they mainly rely on the first few columns — glidein validation and startup errors — which are usually accurate. He noted Tim Cartwright has had longstanding complaints about the report, and that James Letts had at one point asked to stop being sent the report for CMS Connect because he didn't trust it. Namratha said she checked both a 24-hour window (showing larger discrepancies) and a 2-hour window (more reasonable), and is continuing to narrow down whether the RRD fetch returns consolidated vs. raw values.

### Factory operations round-robin
- Vito (Quarium): checked Jenkins; a decision-engine model test/unit-test failure has been present "for a while" and is not new. Otherwise looked okay.
- Steve White: reported a strange issue at Lancaster where all glideins were running in the wrong directory; believed to be something on the site's end, though the site asked for a factory-side ticket/change. He described "11 of 16 states" working with 2 others tried and failed, and said they were going to continue working on it (details of "16 states" unclear from the transcript).

### HTCondor 3.11 upgrade and CE GSI flag
Nick Peregonow reported upgrading GP Grid to the 3.11 RC candidate went smoothly, largely reusing earlier work done with Bruno roughly a year prior. The one issue found: some sites' HTCondor CEs still report GSI-only support. Nick said he would likely file a ticket with Jeff to get an entry/CE setting adjusted. Jeff confirmed this was discussed at yesterday's factory-ops call — the flag has been changed everywhere possible, and the team was waiting on CMS approval, which has now been given; per Marco Mascheroni, the plan is to test in ITB first and then flip the flag across entries, expected within about a week.

Jeff then asked whether Nick's front end uses project ID for any resources. Nick confirmed it does. Jeff explained there is a known, unrelated bug affecting front ends using project ID that is currently blocking upgrading the OSG pool to 3.11 (Marco Mambelli clarified this is a front-end-side issue, not factory-side). Vito noted essentially nothing has used that project-ID entry in 3–4 years (one Nova group and an Ohio-related supercomputing center entry), though it is technically still configured.

### Front-end proxy / token authentication troubleshooting
Marco Mambelli asked whether Nick's front end and factory are on 3.11 consistently — confirmed yes, since Nick's front ends connect to CMS factories already on 3.11.

Nick then raised a general question: whether the front-end GSI proxy can be turned off given SCHEDDs are already fully token-based. Vito noted there is no good documentation on which front-end fields still require a DN, and that although the front-end proxy is theoretically no longer needed to communicate with the factory (ID token should suffice), it is still generated as before "because we don't know" — and Vito said sites shouldn't rely on the front-end proxy for factory communication going forward, though it is still being produced by default.

Nick reported that when he changed the front-end security-class-ad setting from the proxy to the host cert (per documentation), nothing worked: the glidein/front-end process appeared to run and requests went out, but jobs did not run on the resulting glideins, suggesting factory communication was broken. Marco Mambelli asked clarifying questions (whether the SCHEDD is on the same host as the front end — no, they're separate; whether the proxy authenticates the SCHEDD — no, SCHEDDs are all token-based) but could not immediately explain the failure and suggested looking at logs. Nick had reverted to using the proxy to get things working again and said he would retest once the factory-side entry/token issues are resolved, at which point he plans to try disabling the GSI proxy for all his groups. Marco Mambelli noted CMS does have installations running with only an ID token to the factory and a site token to the CE, so this should be possible in principle. Nick asked whether having proxies still configured in his front-end groups could itself be the obstacle to disabling the top-level front-end proxy; Vito indicated the proxy still needs to be kept for some purposes even if otherwise unused. Marco Mambelli offered to look at Nick's configuration directly if shared, and Nick agreed to send it.

### InCommon webinar
Vito mentioned an InCommon webinar today on their future services, at 2:30 Eastern / 1:30 Central, saying he would post details in the Zoom chat; he noted he could only attend the first half hour.

### Meeting close
Marco Mambelli closed the meeting, noting he would follow up with Nick about the front-end proxy configuration next week, and with Namratha about a release review he had started going through. Steve White asked Marco Mambelli to stay on briefly after the meeting for a separate conversation; the content of that conversation is not part of this transcript.

## Open Questions

- Does `analyze_entries` report actual glidein/job counts, or RRD-consolidated (averaged) values — and if the latter, does that explain the observed discrepancies between 24-hour and 2-hour windows?
- What exactly is causing all glideins at Lancaster to run in the wrong working directory, and is a factory-side change actually required, or is it purely site-side?
- Why does disabling the front-end GSI proxy (switching the security-class-ad setting to the host cert) break factory communication in Nick Peregonow's setup, given his SCHEDDs already use tokens exclusively?
- What is the nature of the known bug preventing front ends using project ID from upgrading the OSG pool to HTCondor 3.11?

## Related

[[glideinWMS]] · [[HTCondor]] · [[Pilot Jobs]] · [[Factory Operations]] · [[Factory Configuration]] · [[GPU]] · [[Heterogeneous Computing]] · [[CMS]] · [[Monitoring]]

## Source

meeting_saved_closed_caption.txt (from `2026-04-22 17.18.19 GlideinWMS Meeting`)
