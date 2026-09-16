---
type: meeting
date: 2026-03-05
participants:
  - Antonio Perez-Calero Yzquierdo
  - Marco Mascheroni
  - Florian Von Cube
  - Vaiva Zokaite
  - Luís Simas
topics:
  - CHEP 2026 conference contributions
  - SoCal front-end group
  - Fermilab CERN-pool front end renewal
  - volunteer pool recovery
  - HTCondor versioning
  - glideinWMS versioning
  - Mahti/Finland HPC pilot utilization
  - ARC-CE grid-resource-down errors
  - RAL GPU entry
  - CPU overloading rollout to Tier-2
  - Bari 8-to-16-core change
  - ITB front end issues
  - front-end/overloading monitoring
  - Luis onboarding
  - Puppet host groups
---

# Submission Infrastructure Weekly Meeting

## Summary

The group covered CHEP 2026 conference contribution results, infrastructure status (Fermilab CERN-pool front end renewal, the still-broken volunteer pool, and HTCondor/glideinWMS version status), and factory operations. A large part of the meeting was spent investigating a report that pilots at a Finnish HPC site (heard as "MATI"/"Matty" HPC, exact name unclear) were only using 1 of 8 requested CPU cores; live inspection of Condor queues and CMS job monitoring convinced the group the pilots and jobs are actually running and completing successfully, and that the discrepancy is most likely a reporting/accounting issue on the site's side rather than a submission-infrastructure problem. The meeting also covered the rollout of CPU overloading to some Tier-2 entries, ongoing ITB front-end problems blocking glideinWMS testing, an unresolved RAL GPU entry issue, a monitoring hotfix (SSL verification disabled), a still-open overloading Boolean/string tag bug, and the onboarding status of the new team member, Luis. It was the first meeting Luis attended as a team member.

## Decisions / Conclusions

- Four submissions were made from CMS Submission Infrastructure / related areas to the CHEP conference in May; the group was assigned 2 talks and 2 posters. Antonio, who was part of the selection committee, noted the split reflects balancing factors such as speaker diversity and overlap with similar contributions from other experiments (e.g. ALICE has a similar pilot-model talk), not just interest in the topic itself.
- The SoCal front-end group remains disabled; Diego (its owner) is on vacation and has not replied, so the group agreed to keep it disabled unless someone complains.
- Only the Fermilab CERN-pool front end (not other components) was upgraded, to a new AlmaLinux 9 machine, by Hyunwoo about two weeks prior. A subsequent failover test ran for about 5 days before switching back to the production front end; it appears to be working correctly.
- Central HTCondor machines are running the 24.6 LTS series; the ITB is on a 25.x version. Marco explained HTCondor's versioning: each year has a stable ("LTS") series (e.g. 24.0.x, 25.0.x, only patched) and a feature/development series that increments a minor version (e.g. 25.1, 25.2...) for new features; a new year's series (26) is typically released later in the year, so the group is expected to remain on 25 for now. HTCondor is described as usually strongly backward compatible; the last breaking change was the deprecation and removal of GSI (proxy-based) authentication in favor of tokens, done with significant advance warning. By contrast, Marco noted glideinWMS does not have the same backward-compatibility track record, attributed to its smaller development team and community.
- The GitLab CI access token used to generate the automatically-updated list of central HTCondor machine versions had expired; Florian renewed it a few days prior, restoring the list.
- Regarding the Finnish HPC ("MATI"/"Matty") pilot-utilization complaint: live inspection (Condor queue query showing 128 running jobs consistent with the plotted pilot count, and CMS job monitoring showing completed jobs with only a few failures) led Antonio and Marco to conclude that pilots and payload jobs are running and completing successfully from the submission-infrastructure side. The group concluded the discrepancy reported by the site contact is most likely a reporting/accounting issue on the site's side (which tracks jobs via Slurm) or in how CPU efficiency is calculated/reported for that site, rather than a pilot-scheduling or submission-infrastructure problem — though this remains a working interpretation rather than a confirmed root cause.
- The entry for this HPC site was kept enabled/in the global pool; a proposal to remove it (raised by Antonio and Vaiva as a way to test more safely, given testing is currently hampered by ITB issues) was not adopted, since the evidence reviewed live showed the entry was not causing problems (jobs completing, no "black hole" pattern).
- CPU overloading at 66% has now been enabled on some Tier-2 entries this week, extending from Tier-1-only at the start of testing; rollout follows the same partial pattern used during initial testing (a subset of entries/sites, not applied flat across every site). Marco clarified that enabling the 66% "knob" in the front end has no effect unless the corresponding factory-side glidein CPU and memory multipliers (1.25) are also set per entry; overloading is therefore effectively being enabled entry-by-entry in the factory.
- The Bari 8-to-16-core change is now in production. The site admins never replied about moving to a full-node configuration, so the current (partial) configuration was kept.
- The front-end monitoring issue from the prior week was fixed with a hotfix: monitoring scripts on VOCMS0850 (the monitoring machine) had started failing SSL certificate verification because packages in its Python virtual environment were outdated; Florian disabled SSL verification in the monitoring scripts as a temporary fix so monitoring data would keep flowing. A proper fix (recreating the virtual environment and updating packages) is still needed.
- The overloading-status monitoring dashboard issue (values shown incorrectly, previously flagged as a Boolean-vs-string mismatch) is still not fixed. The group clarified this is a type-casting/visualization issue between the value submitted by the pilot (via the factory configuration) and how it is queried/displayed in Grafana from OpenSearch — the data itself is present in OpenSearch. Two possible fixes were discussed: a quick fix in Grafana treating both string "false" and Boolean false as equivalent (which would also correctly show historical data), or a proper fix at the source. Since no historical data is being retained anyway, Antonio said fixing it going forward is sufficient; there was no clear agreement on which approach to take or who owns the fix.

## Action Items

- [ ] Look into why the volunteer pool front end is not obtaining resources after the machine redeploy — Florian Von Cube, with Marco Mascheroni (planned to look at it together outside the meeting)
- [ ] Reset up the Python virtual environment on the monitoring machine (VOCMS0850) and update outdated packages to properly fix SSL certificate verification (currently disabled as a hotfix) — Florian Von Cube
- [ ] Reply regarding the RAL GPU entry ticket/email about whether `--pid` can be dropped from the container command, as suggested by the RAL site admin — Marco Mascheroni (acknowledged he should have replied already; Vaiva Zokaite had emailed the relevant contact directly, cc'ing Marco, since the ticket reply had not come through)
- [ ] Try to catch the periodic "grid resource down" / curl error seen in the Condor/ARC-CE entry logs in real time to help establish a pattern — Vaiva Zokaite

## Discussion

### CHEP 2026 conference contributions
Antonio reported CHEP results are now visible per-contribution on the conference website (individual authors were not notified directly because CMS submitted the abstracts as a single group through one committee member). Out of 4 infrastructure-related CMS submissions, 2 were accepted as talks and 2 as posters. Antonio, having been on the selection committee, explained the balance reflects factors beyond topic interest, including number of distinct speakers and overlap with similar contributions from other experiments (ALICE was mentioned as having a similar pilot-model talk). Whether anyone will travel to the conference (in Thailand) given current world conditions was raised as an open question.

### SoCal front-end group
No update from Diego, who is on vacation; the group remains disabled, consistent with the prior week's decision.

### Fermilab CERN-pool front end renewal
Florian confirmed only the front end (not other components) was upgraded to a new AlmaLinux 9 machine by Hyunwoo roughly two weeks prior. A failover test then ran for about 5 days before switching back to the production front end around Monday/Tuesday of that week; it appears to be working.

### Volunteer front-end status
Following the previous redeploy (after the Puppet certificate expiry), Florian confirmed he copied over tokens/certificates and redeployed transparently under the same hostname, IP, and pool password (all managed by Puppet). Marco had verified this. However, the machine is still not obtaining resources, and Florian has not yet identified the cause after looking at the front-end logs. Ivan and Federica are asking about the machine's status. Florian and Marco planned to look into it together, possibly the next day.

### HTCondor and glideinWMS version status
Florian showed a CI-generated, weekly-updated list of HTCondor versions running on central Submission Infrastructure machines: mostly 24.6 (the LTS series), with the ITB on a 25.x version. The GitLab access token that the CI job uses to generate this list had expired and was renewed by Florian a few days earlier. Antonio asked whether the 24 series was too old, prompted by a question from a CERN colleague (Antonio's colleague, also named Antonio) about the HTCondor support mailing list, which suggested 24 might be near the end of its ~2-year support window. Marco clarified the versioning scheme (see Decisions) and confirmed the group is not behind — 26 is not expected until later in the year. Florian noted he could push the ITB front end and factory to the newest available version (still 25, since 26 is not yet released) once the current ITB token-generation issue is fixed, and run it for a couple of weeks before considering it for the global and Tier-1 pools. Luís asked about breaking changes between major HTCondor versions; Marco and Florian described HTCondor as generally very backward compatible and safe to run with mixed versions in a pool if not too far apart, citing the GSI-to-token authentication migration as the last major breaking change (removed after a long deprecation/warning period). Marco contrasted this with glideinWMS, which he said cannot claim the same track record, attributing it to its smaller team and community size.

### Finnish HPC ("MATI"/"Matty") pilot utilization investigation
Antonio raised an ongoing email thread about a claim from a site contact that only 1 of 8 CPUs requested per pilot was actually being used. Looking at a job-monitoring plot, Antonio instead saw roughly 20 out of a maximum ~160 (28 8-core) pilots running, not full utilization but not "1 out of 8" either, and suggested the contact might be describing actual payload CPU efficiency rather than scheduling/slot utilization — payload inefficiency being common. Antonio hypothesized the underlying issue could be pilots allocating dynamic slots for jobs that then fail to start (e.g. due to a nested-container configuration issue), producing an apparent idle CPU despite the slot being allocated — drawing a parallel to a similar problem seen at BSC (Barcelona).

Vaiva noted she had separately observed a periodic "grid resource down" issue in the Condor/entry logs, related to `curl_easy_perform` failures, similar to (but not identical to) a past recurring issue with ARC entries; it is intermittent and hard to pin down a pattern, and she planned to investigate further and try to catch it in real time. She also noted an additional "fat container" (apptainer/similar) layer at this site that had caused issues during initial ARC-CE entry testing, and that validation checks executed by the pilot can pass (e.g. Singularity setup checks) while the actual job still fails at a deeper level not visible to validation — a problem the group agreed is likely beyond the submission-infrastructure domain and belongs with sites/facilities.

The entry had been temporarily disabled in the past due to earlier issues and was re-enabled a few weeks before this meeting; Vaiva believes facilities people are included in the relevant ticket. Antonio suggested redirecting the ticket/discussion toward Stefan or Andres Haba (Barcelona facility contact, name as heard) given the issue may be beyond the team's debugging expertise.

Live investigation during the meeting (Condor queue query for entry-matching running jobs, and the CMS job-monitoring dashboard filtered to the site) showed 128 running jobs consistent with the plotted pilot count and successfully completing jobs with only a few failures. Marco and Antonio concluded there is no real submission-infrastructure-side problem, and that the discrepancy is likely a reporting issue on the site's side (which uses Slurm-based job tracking) or in how CPU efficiency is being reported/aggregated — noting the CPU efficiency field for this site appeared broken/empty in the monitoring dashboard when checked. Vaiva raised whether it might be worth temporarily disabling the entry again given testing is hampered by ongoing ITB issues, but Marco argued against removing it since it is not causing problems; the group agreed to keep investigating without removing the entry from the global pool.

### RAL GPU entry
No progress to report. Vaiva added glideinWMS developers/support contacts to the ticket but is unsure whether they have seen it, so she emailed directly (cc'ing Marco) that day. She believes the issue may be the same one previously seen with other entries (referenced as "beer entries", exact term unclear) and an issue LHCb reportedly hit as well (per Ben Jones): when a site runs its job environment inside Docker, it cannot enable namespaces. The suggested fix from the RAL site admin was to drop `--pid` from the container/apptainer command, but the team does not yet know how to implement that; Marco is expected to advise, and acknowledged he had not yet replied to the relevant ticket/email.

### CPU overloading rollout
Overloading at 66% has been enabled on some Tier-2 entries this week (previously Tier-1 only), following the same partial-rollout pattern used during earlier testing (a subset of entries, not applied uniformly). Marco reiterated that the front-end 66% setting alone has no effect unless the factory-side glidein CPU and memory multipliers (1.25) are also configured for each entry, so overloading is effectively being turned on entry-by-entry at the factory level.

### ITB front end / glideinWMS testing
The ITB front end remains down due to an unresolved token-generation issue Florian has been investigating without success so far. This is blocking Vaiva's testing of the entry configuration changes (she had upgraded Condor and the ITB factory to 25 hoping it would help the ITB front end at CERN reconnect, without success). As a workaround, Vaiva proposed downgrading the ITB front-end glideinWMS version to the last known-working version (glideinWMS 3.10.17 or similar, exact version unclear). Marco pointed out the factory should already be usable via the working Fermilab backup front end, and argued against downgrading the ITB front end since the team also wants to keep debugging the underlying issue. Vaiva also proposed resuming work on setting up a dedicated ITB-dev environment (raised previously, about 5 months earlier per Vaiva) so pilots can be properly tested without affecting other testing; Antonio agreed this would be useful, noting that using the ITB for its intended purpose (testing new components against sites, via test/HammerCloud jobs) is preferable to routing production-adjacent traffic through it.

### Bari 8-to-16-core change
Now in production. Site admins never responded regarding moving to a full whole-node configuration, so the current partial configuration was kept as-is.

### Dynamic resources / HPCs (BSC)
No update this week; Antonio had planned to test new tools shared by Marco with BSC but had nothing to report.

### Front-end and overloading monitoring
Florian described the front-end monitoring hotfix: outdated packages in the Python virtual environment on VOCMS0850 (the monitoring machine) broke SSL certificate verification; as a quick fix he disabled certificate verification in the monitoring scripts so monitoring data keeps flowing, but the proper fix (recreating the virtual environment and updating packages) is still pending.

Antonio separately raised that the overloading-status dashboard is still showing a declining/fluctuating trend, asking whether the previously-identified Boolean-vs-string casting bug in the overloading tag has been fixed. Neither Florian nor Marco had worked on it. The group clarified the issue is likely a Grafana/visualization-level casting mismatch (string vs. Boolean representation of the overload flag), not a data-loss issue in OpenSearch, and that pilots are correctly carrying the tag (used by Marco for related reports). No owner was assigned; the group agreed the fix only needs to apply going forward, since historical data is not retained, and further debugging will happen in real time outside the meeting.

### Luis onboarding
Luis still lacks full CMS registration/access (e.g. e-groups), which is blocking several things; this has been followed up with the CERN Secretariat and with "Luca" (the person responsible for CMS registration approval), and the group is hopeful it will be resolved by the following week. Florian raised including the CMS Level 1s (computing coordinators) in the escalation if delays continue, arguing that CMS management should push people to process access requests faster — noting it was already Thursday of Luis's first week with accesses still missing. Vaiva/Luis noted CMS registration is a process independent of Level 1 involvement. Antonio agreed that escalating to computing coordinators would be reasonable if there is continued, unexplained delay, but not before giving the normal process a reasonable chance. Florian sent an email during the meeting to what he believes is the CMS offline computing coordinator address, raising the delay.

Separately, Luis received a laptop, allowing him to start working alongside Vaiva at the same desk. In the meantime he has been doing administrative tasks (e.g. setting up a bank account) and starting Puppet and OpenStack training to learn CERN's tooling, working without a CMS registration so far.

### Puppet host groups
In the context of Luis's OpenStack/Puppet training, Marco and Vaiva noted CMS offline/computing is not particularly proud of how Puppet is managed; some host groups are cleaner than others, with the shared VOCMS host group (used broadly across computing) described as being in a particularly messy state. Marco expressed the opinion that the team should move toward using containers with a minimal, generic machine base to reduce Puppet dependency going forward; he noted the factory's own host group is comparatively better maintained.

## Open Questions

- Why is the volunteer pool front end still not obtaining resources after the machine redeploy?
- What exactly is causing the periodic "grid resource down"/curl errors seen in the Condor/entry logs, and is there a discernible pattern?
- Is the Finnish HPC ("MATI"/"Matty") utilization discrepancy actually a site-side reporting/accounting issue, or is there an underlying submission-infrastructure or payload-execution problem still to be found?
- What is causing the ITB front-end token-generation issue, and when will it be resolved?
- How should the RAL GPU entry's namespace/Docker-in-Docker issue be fixed (i.e. how to safely drop `--pid` from the container command)?
- Who will own and how will the overloading Boolean/string tag casting issue in the monitoring dashboard be fixed (dirty Grafana-level fix vs. proper source-level fix)?
- Will Luis's CMS registration/access be resolved by the following week, and will escalation to Level 1s/computing coordinators be needed?

## Related

[[Submission Infrastructure]] · [[HTCondor]] · [[glideinWMS]] · [[Monitoring]] · [[CMS]] · [[WLCG]] · [[CERN]] · [[GPU]] · [[Factory Operations]] · [[Pilot Jobs]] · [[Dynamic Resource Provisioning]]

## Source

meeting_saved_closed_caption.txt (from `2026-03-05 17.25.19 Submission Infrastructure Weekly Meeting`)
