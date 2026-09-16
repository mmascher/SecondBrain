---
type: meeting
date: 2026-09-15
participants:
  - Jeff Dost
  - Marco Mascheroni
  - Pablo Izquierdo Gonzalez
topics:
  - "Immortal pilots" concept (long-lived, non-retiring glideins)
  - Nebraska NRP Kubernetes cluster data center migration
  - TACC Vista ARM-based site fix (LD library path issue on Alma 9)
  - Team introduction (Pablo Izquierdo Gonzalez)
---

# OSG Factory Ops Meeting

## Summary

This was a short, quiet-week meeting. Pablo Izquierdo Gonzalez, new to the Factory Ops team, introduced himself (Tier-2 site admin at IFCA/Cantabria, Spain, ~1.5 years on the grid, background with ARC CE, currently learning HTCondor and glideinWMS). Marco Mascheroni reported on an idea discussed the previous week with Hyunwoo Kim: "immortal pilots" — glideins configured to run indefinitely (no retirement/draining) in order to eliminate draining-time inefficiencies. The proposal, its motivation, and several unresolved technical concerns were discussed but no decision to proceed was made. Jeff Dost also gave two brief operational updates: Nebraska's NRP Kubernetes cluster is undergoing a physical data-center migration (unrelated to CMS but reducing OSG to a single active factory, Tiger at Wisconsin, for most of the week), and Jamie (HTCondor developer) has identified the root cause of the TACC Vista (ARM-based site) issue, related to unexpected `LD` library path behavior on Alma 9, with a fix in progress. Jeff and Marco also briefly discussed status of their in-progress paper draft.

## Decisions / Conclusions

- No decision was made to implement immortal pilots; it remains an idea Marco considers worth experimenting with, despite three identified concerns (see Discussion).
- No decision was made on glidein sizing/shape for a potential immortal-pilot experiment (single-core vs. whole-node); this was raised as an open trade-off, not resolved.

## Action Items

None identified.

## Discussion

### "Immortal pilots" concept

Marco Mascheroni reported that he and Hyunwoo Kim had discussed, the previous week, an idea nicknamed "immortal pilots": glideins configured to keep running indefinitely rather than retiring, to avoid the draining time and associated inefficiencies that occur when pilots retire and are replaced. The proposal was to try this at Fermilab by adding a new compute-element queue entry with a limit of 1, so a single pilot could be tested with this characteristic.

Jeff Dost raised several practical questions and concerns:
- What happens if the underlying machine restarts — does a replacement pilot simply take over, or is there any state-saving/self-restart mechanism? Marco confirmed there is currently no such mechanism.
- In practice, getting started would likely mean giving the pilot a very long (or effectively unset) wall time; Jeff noted that some assumed values in the glidein (e.g., end time / retire time) would still need *some* very large value set, since fields that assume an eventual end time can't simply be left unset.
- Whether the glidein should be single-core (to minimize fragmentation risk) or a whole node (with a fragmentation risk over time, mitigated by periodically killing and replacing the pilot). Marco didn't think there were currently enough single-core jobs targeting Fermilab to create significant fragmentation, but wanted to observe this in practice. He noted HTCondor's defrag daemon as an existing mitigation tool (allows setting a threshold, e.g., dedicating half of pilots to single-core, with rules to defragment the rest).
- Jeff referenced a past experience working with Hosted CE at a site called Hypatia (via Iglin) that intentionally used fixed 64-core glideins matching only exactly-64-core user jobs, for 100% efficiency when in use, at the cost of long idle periods when there was no matching demand. He raised this as an example of how the size/shape trade-off could be approached, though not as a recommendation to replicate this specific pattern.

Marco summarized three technical concerns ("downsides," which he described as possibly "showstoppers") identified in the earlier discussion with Hyunwoo:
1. **Fragmentation** — long-lived pilots occupying node fragments over time.
2. **Credential expiration** — credentials sent to pilots are normally renewed periodically (e.g., a credential valid for one week), and a pilot that outlives the credential's validity would be affected; this is "not that simple" to resolve. Marco mentioned he had discussed this with Jamie (an HTCondor developer), speculating that a possible needed HTCondor feature would be for a long-running pilot to periodically report/simulate completion state.
3. **Accounting** — accounting data is currently collected when a pilot finishes; a pilot that never finishes would not generate this accounting data.

Marco said he was "not so sure now" given these concerns but still felt the idea was worth trying as an experiment. Jeff agreed it was an interesting experiment to consider. No further steps were assigned.

### Team introduction

Pablo Izquierdo Gonzalez introduced himself: based in northern Spain, working for about 1.5 years at the IFCA Tier-2 site (Cantabria) for CMS, with experience managing/administering site machines. IFCA currently uses ARC as its compute element, and Pablo is now learning HTCondor and glideinWMS. Marco and Jeff welcomed him to the team.

### Nebraska NRP Kubernetes cluster migration

Jeff Dost noted that although it doesn't directly affect CMS, Nebraska (UNL) is undergoing a major migration of its NRP Kubernetes cluster: their existing data center, located under the campus football stadium for 10+ years, must be vacated for other campus use, requiring a physical move of all hardware to another data center. The migration is expected to keep Nebraska's systems down for most of the week; things were reportedly going smoothly at the time of the meeting. As a consequence, OSG has only one active factory (Tiger, at Wisconsin) for the duration.

### TACC Vista (ARM) site fix

Jeff Dost reported an update from Jamie (HTCondor developer): the root cause of an issue affecting TACC Vista, the ARM-based site, has been identified — related to unexpected behavior of variables affecting the `LD` library path on Alma 9. A fix is in progress but not yet complete.

### Paper draft status

Jeff Dost said he is still catching up and has early, unshared notes/ideas mapped out for a joint paper, hoping to have something presentable within the week. Marco asked whether he should independently draft content (e.g., an AI-assisted draft, or content from an existing poster) to merge with Jeff's version, or wait for Jeff's revision. Jeff said he has a fairly clear idea of what he wants to say and left the choice to Marco, noting he'd prefer to share his own "brain dump" iteration first; Marco agreed to wait and, if useful, create a placeholder Overleaf document in the meantime.

## Open Questions

- Whether HTCondor could support a feature allowing a long-running pilot to periodically report or simulate completion state, addressing the accounting gap for non-finishing pilots — raised as a possible need, not yet pursued with HTCondor developers as a concrete request.
- Whether/how credential expiration would be handled for pilots that outlive a renewed credential's validity window.
- What glidein size/shape (single-core vs. whole-node, and whether to periodically recycle pilots) would work best for an immortal-pilot experiment at Fermilab.
- Whether fragmentation from single-core immortal pilots targeting Fermilab would actually become a practical problem, absent real-world testing.

## Related

[[Factory]] · [[Factory Operations]] · [[Pilot Jobs]] · [[HTCondor]] · [[glideinWMS]] · [[OSG]] · [[Kubernetes]] · [[Resource Provisioning]]

## Source

OSG Factory Ops Meeting transcript_2026-09-15_17.18.18.txt (from `2026-09-15 17.05.09 OSG Factory Ops Meeting`)
