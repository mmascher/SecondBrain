---
type: meeting
date: 2026-09-04
participants:
  - Marco Mascheroni
  - James Letts
topics:
  - Marco Mascheroni's potential move to the Workload Management (WM) Level 2 position
  - draft response email to Tulika
  - Submission Infrastructure (SI) priorities for 2026-27
  - CMS offline & computing organizational structure and Project Office history
  - Factory migration to Kubernetes (re-evaluation)
---

# Marco's Transition to WM Level 2 and SI Priorities Discussion (with James Letts)

## Summary

Marco Mascheroni and James Letts discussed a draft response Marco was preparing to an email from Tulika concerning Marco's potential move into the Workload Management (WM) Level 2 position, and Tulika's question about whether this move would slow down Submission Infrastructure (SI) activities. James had reviewed Scarlett and Duong's recent budget-review slides, which he confirmed included SI content (largely drawn from material Marco had previously provided to them), including 2026 highlights (large-scale validation of the global pool, stable operations, factory migration to Kubernetes, improved resource efficiency including high I/O slots, CPU efficiency monitoring) and 2027 priorities (attention to the DiracX transition to ensure operations are included, and scalability tests of submission infrastructure in connection with the new workflow management system). The two also discussed CMS's offline & computing organizational structure (coordination area vs. project, and the history of the "Project Office") for context on Tulika's and Liz's roles, and briefly discussed upcoming conference travel.

## Decisions / Conclusions

- Marco's planned response to Tulika will reframe the question "is SI slowing down" — the conclusion reached in the conversation is that SI is not slowing down but rather speeding up toward the new WM, since supporting the CMS transition to DiracX is itself a top SI priority; Marco's move to WM Level 2 is consistent with, not a distraction from, SI's own direction.
- Marco will retain his GlideinWMS operations and development responsibilities (reported as ~75% of his time) regardless of the WM Level 2 move, and will remain involved in and retain a voice in SI as a senior/experienced developer.
- SI priorities for 2026-27, as previously communicated by Marco to Duong and Scarlett for the budget review: supporting the CMS transition to DiracX (described as the highest priority, tied to ONC's main critical activities) and scale testing of CRAB, WMAgent, and the new DIRAC-based scheduler processes (monitoring, remote job reporting, etc.), plus improved efficiency.

## Action Items

- [ ] Draft and send the (hopefully final) response email to Tulika — Marco Mascheroni, planned for that evening.
- [ ] Review Marco's draft email before it is sent — James Letts.
- [ ] Submit a travel request for the DIRAC workshop in Prague (starting 28 September) — Marco Mascheroni.

## Discussion

- Marco reported he is in contact with Liz, who was already aware of the email to Tulika and reacted positively, including floating the idea of collaborating on planning charts she is expected to deliver.
- James suggested Marco emphasize in the email: his recent hands-on Kubernetes/DiracX proof-of-concept development work (with Valentin, and integration work with the WN group), and his established, productive working relationship with that group, as evidence of management/coordination readiness alongside his technical experience across both submission infrastructure and workflow management.
- Re-evaluating the Factory-to-Kubernetes migration: a prior milestone considered evaluating moving the Factory to CMS/OSG's Kubernetes infrastructure; at the time it was judged not worth it because Kubernetes infrastructures differ enough between sites that configurations can't simply be copied across. Marco proposed revisiting this now, since his recent hands-on Kubernetes experience (via DiracX deployment/testing work) has grown significantly since that earlier evaluation. Luis was noted as also interested in this.
- CMS organizational structure: James explained that offline & computing is a "coordination area" (like physics, trigger, PPD, ONC, and run coordination), not a "project" (e.g., HGCal, detector, tracker); coordination areas have very small centrally-funded budgets (roughly $1–1.5M, versus $10–20M+ for projects such as HGCal) covering little beyond Cat-A/fellows and minor travel/equipment, and cannot directly direct people's work the way projects can.
- The "Project Office" was created (during James's time as coordinator) as a workaround to give offline & computing some project-like coordination structure without formal budget or authority; it originated from the CDR editors. James described its current composition as mostly Fermilab or Fermilab-adjacent people, with Daniel described as the one actively driving organizational/software work and Tulika involved but very busy.
- James described his own past experience working under Liz (in a Ken Bloom/Tulika-analogous reporting structure) as positive, and suggested Tulika's question about "impact on SI activities" likely reflects a wish to confirm Marco understands the scale of responsibility involved, rather than a specific concern tied to Liz.
- Level 2 position demographics: Marco noted Liz had also applied earlier for the WM Level 2 position but was reportedly told a non-US person was wanted for it; James explained CMS aims to keep the proportion of non-US Level 2 positions below roughly half, to avoid raising questions from funding agencies, but did not see it as necessarily a problem if the SI-specific Level 2 slot were absorbed into a role held by a non-US person, given the US's strong existing base in HTCondor/GlideinWMS. It was also noted that the current SI Level 2, Andrea Piccinelli, is moving to a Level 2 position in physics (outside offline & computing), which will reduce the count of SI-affiliated Level 2 positions further regardless.
- James characterized the WM Level 2 role, especially through the DiracX transition, as high-visibility and high-pressure, needing to succeed before CSA28 (roughly a year and a half away), and as a genuine growth opportunity for Marco given his combined SI/workflow-management technical and management experience.

## Open Questions

- Whether it would be a problem, organizationally, if the CMS org chart no longer shows a dedicated SI Level 2 position (were that slot to effectively move to an EU/non-US person) — James's initial view was that this is not necessarily a problem, but the point was raised informally and not conclusively resolved.

## Related

[[CMS]] · [[DiracX]] · [[GlideinWMS]] · [[Workload Management]] · [[Submission Infrastructure]] · [[CRAB]] · [[WMAgent]] · [[Kubernetes]] · [[Factory]] · [[WLCG]]

## Source

meeting_saved_closed_caption.txt (from `2026-09-04 17.53.47 Marco Mascheroni's Personal Meeting Room`)
