---
type: meeting
date: 2026-05-26
participants:
  - Todor
  - Alan Malta Rodrigues
  - Marco Mascheroni
  - Valentin Y Kuznetsov
  - Vijay
topics:
  - DiracX/DIRAC development environment (client-side vs. central-services setup)
  - Comparison of DIRAC's site-operations model with CMS Submission Infrastructure's site-support separation
  - WM Dev requirements/blueprint document status
  - Physics requirements discussion meeting (scheduled for the next day)
  - Sharing of individual DiracX exploration work (gists/repos)
  - Token protection feature / X509 token disabling follow-up
---

# WM Dev Team Weekly Meeting

*Note: the available transcript begins mid-discussion (16:27) and cuts off mid-sentence (16:58); the start and end of the meeting are not captured.*

## Summary

Most of the discussion concerned preparing for a DiracX hackathon and the difficulty of setting up a usable DiracX/DIRAC development environment. Todor distinguished two very different things people might mean by "development environment": (1) the client/user-side setup (the DiracOS conda-like package), which he described as easy to stand up in about two afternoons and sufficient for developing Python-based agent modules and workflow configuration; and (2) a full central-services development setup, which is heavily Kubernetes-based, involves many microservices, and is a much harder problem. Todor said he had already hit this limitation himself (as presented at the OSC week): he could develop and simulate workflow modules locally but could not deploy newly developed modules into the central services, so he was limited to simulating workflows rather than actually running them end to end.

Marco drew an analogy to CMS/WMCore to clarify: DiracOS-based development is comparable to developing WMCore code with unit tests, while what Valentin was describing — needing a full running system with databases, authentication, and all central services — is comparable to installing the full ReqMgr, database, Global Workqueue, and agent stack locally. Valentin confirmed this and described his own experience trying both the Kubernetes-based approach and DIRAC's "demo" script approach: the demo script brings up a local Kubernetes cluster with dozens of services and databases (MySQL, OpenSearch), but he then hit a wall trying to configure the authentication service (VO setup, required metadata) with no documentation or prior system knowledge, and could not get far enough to test his code against a running system. He noted that DIRAC bundles everything together, so there is no way to isolate and develop against a single subsystem in isolation — in his testing, "everything is bundled together." He also mentioned raising questions in the DIRAC/Mattermost channel and encountering pushback (being told not to "spam" the channel), leaving him feeling the team is largely on its own in figuring this out. Valentin will not attend the upcoming hackathon himself but hopes the team can use it as an opportunity to get a working infrastructure set up, since without that (or help from the DIRAC side) he expects development to remain very difficult.

Marco raised whether the team really needs the full DIRAC ecosystem or only the transformation system, since the team plans to keep using glideinWMS and HTCondor rather than DIRAC's own workload-management system. Alan pushed back, noting DIRAC has roughly ten or more subsystems and that WMCore/WMAgent is "just one piece of the puzzle" (data management, an SI layer, etc. are separate concerns for CMS but are embedded within DIRAC's workload management), and that the team will likely end up adopting other DIRAC systems beyond transformation. Valentin agreed with Alan's framing from his own experience, saying he found no way to extract and work on a single DIRAC system independently of the rest.

Alan proposed that someone in addition to Valentin go through the documentation Federico (Fermilab) provided, to assess what it does and does not cover and whether it is sufficient at least for the hackathon (Alan was skeptical it would fully prepare the team for the broader CMS/DiracX effort). Vijay volunteered to review the documentation. Alan suggested taking ~20 minutes in a future meeting (tentatively the following week, since Alan expects to be away that week) to discuss findings and blockers before escalating specific gaps to the DIRAC development team.

Separately, Todor mentioned attending a DIRAC operations meeting the previous week and observed that, unlike CMS (where Factory Operations/WMS work is separated from direct site support, with a dedicated team handling site-facing issues), DIRAC sites report status directly into the central operations meeting, with no equivalent separation, and DIRAC works more directly with underlying grid middleware. He was not asserting this is better or worse, just flagging the difference. Alan suggested this difference stems from DIRAC integrating more functionality (data management, a resource catalog, and an SI-like layer) directly into its workload-management system, whereas WMCore is only one piece of a larger CMS toolset that also relies on separate data-management and SI components; the team expects to learn and adapt to DIRAC's model over time.

Marco asked Valentin and Todor whether they saw value in showing the team what they had done so far. Valentin said he had documented his work in a gist and could show his "current struggle," but had not yet seen Federico's documentation; he confirmed he will not be able to attend the hackathon at CERN in person or via Zoom due to other plans, but is in discussion with Federico about a subsequent DiracX event in Prague (Valentin described it as also being positioned as a hackathon, while Alan characterized the Prague event as a workshop rather than a hackathon). Todor said his own DiracX exploration work is in a Git repository (name transcribed as "Diracle," uncertain), which he offered to point Marco to directly rather than prepare a formal presentation.

Alan also gave a status update on the requirements/blueprint document: under each stakeholder section, Andrea went through earlier discussion notes and turned them into concrete requirement lists (explicitly not meant to be read as "desiderata," but as candidate requirements for the blueprint document), plus an open-points section for items needing further discussion or with dependencies on other stakeholders. The previously separate Tier-0 requirements document and the user-workflows requirements document have both now been merged into this shared document. Alan asked the team to read through it and leave comments. He also flagged a physics-requirements discussion meeting scheduled for the next day (2026-05-27) at 5pm with physics coordination and others, noting the team's own meeting-tracking list looked stale (from roughly two weeks prior) and that he was not aware of other meetings planned for the current week, partly because some team members are at CHEP.

Toward the end, Alan followed up with Todor on the token-protection feature. Todor said he had only skimmed the relevant material and did not see development work needed on the WM Dev side; his impression was that the open issue concerns when the token server needs to be deployed, which is not something on their side. Alan clarified the team does not yet have the full token infrastructure, and that the current known problem is on the agent/HTCondor side: when trying to keep X509 tokens disabled, job ClassAds are still getting X509 attributes populated, and disabling this fully through the ClassAds isn't working. Kenji had suggested testing to confirm whether this is actually an HTCondor issue. Todor identified the relevant GitHub issue as #1288 (a second number, transcribed as "12228," was also mentioned in the same exchange but is unclear/likely a transcription artifact) and agreed to look again at the comments and sync with Alan.

## Decisions / Conclusions

- No development-environment strategy was decided; the discussion remained exploratory. The working understanding reached was that DiracOS (client-side) is adequate for developing Python-based agent/workflow-configuration code, but a much harder, largely Kubernetes-based effort is needed to develop and integrate against DIRAC's central services.
- Based on his own hands-on testing, Valentin concluded there is currently no way to isolate and develop against a single DIRAC subsystem — the ecosystem is tightly bundled together.
- Whether the team needs to integrate with most/all of the DIRAC ecosystem, or can scope down primarily to the transformation system while continuing to rely on glideinWMS/HTCondor for workload management, was not resolved — Marco and Alan expressed differing views, with Alan and Valentin leaning toward broader ecosystem involvement being likely necessary.
- The requirements/blueprint document now incorporates the previously separate Tier-0 and user-workflows requirements documents, plus stakeholder-specific requirement lists derived by Andrea from earlier discussion notes, alongside an open-points section.

## Action Items

- [ ] Go through the DiracX documentation Federico provided and assess coverage/gaps ahead of the hackathon — Vijay
- [ ] Share pointers to DiracX exploration work (Git repository, name transcribed as "Diracle") directly with Marco — Todor
- [ ] Review the requirements/blueprint document and leave comments/clarifications — team
- [ ] Post the physics-requirements meeting details (2026-05-27, 5pm) in the Mattermost channel — Alan Malta Rodrigues
- [ ] Re-review the comments on GitHub issue #1288 (X509 token / job ClassAds) and sync with Alan — Todor

## Discussion

### DiracX/DIRAC development environment
See Summary. Key technical distinction raised by Todor: DiracOS (client-side, conda-like package) vs. central-services development (Kubernetes-based, multiple microservices). Valentin's practical experience with both the Kubernetes approach and DIRAC's "demo" script surfaced blockers around authentication/VO configuration that he could not resolve without documentation or prior system knowledge.

### Scope of DIRAC ecosystem integration
Unresolved disagreement between Marco (team may only need the transformation system, since glideinWMS/HTCondor will remain the workload-management layer) and Alan (DIRAC has ~10+ subsystems and WMCore covers only part of the equivalent CMS functionality, so broader adoption is likely). Valentin's testing supports the view that subsystems cannot be cleanly separated.

### DIRAC operations model vs. CMS site support
Todor observed, from attending a DIRAC operations meeting, that DIRAC sites report status directly into central operations meetings, unlike CMS's separated Factory Operations/WMS and site-support structure. Alan attributed part of the difference to DIRAC embedding data management and an SI-like layer directly into its workload-management system, functionality that in CMS is handled by separate components alongside WMCore.

### Requirements/blueprint document
Alan walked through the current state of the shared requirements document: per-stakeholder requirement lists (derived by Andrea from earlier discussion notes, not to be read as "desiderata"), an open-points section, and the now-merged Tier-0 and user-workflows requirement sets. The team was asked to review and comment.

### Token protection / X509 disabling follow-up
The team does not yet have full token infrastructure. The currently understood blocker is that job ClassAds still populate X509 attributes even when X509 is meant to be disabled, which may be an HTCondor-side issue (per Kenji's suggestion) rather than something requiring WM Dev-side development. Reference: GitHub issue #1288.

## Open Questions

- Will Federico's documentation be sufficient to prepare the team for the DiracX hackathon, even if it does not cover full central-services development?
- Does the team need to integrate with most of the DIRAC ecosystem, or can it scope down to a subset of subsystems (e.g., transformation) while keeping glideinWMS/HTCondor for workload management?
- Is the X509-in-ClassAds issue actually caused by HTCondor, as Kenji suggested, and does resolving it require any action on the WM Dev side beyond confirming the token server deployment timeline?
- What exactly is needed from the DIRAC development team to unblock central-services development, once the team has gone through Federico's documentation?

## Related

[[DIRAC]] · [[DIRACX]] · [[WMCore]] · [[HTCondor]] · [[glideinWMS]] · [[Kubernetes]] · [[Submission Infrastructure]] · [[CMS]] · [[CHEP]]

## Source

meeting_saved_closed_caption.txt (from `2026-05-26 16.37.02 New WM Dev team weekly meeting`)
