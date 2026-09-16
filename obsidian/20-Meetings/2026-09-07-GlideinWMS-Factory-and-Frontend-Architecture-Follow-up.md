---
type: meeting
date: 2026-09-07
participants:
  - Marco Mascheroni
  - Pablo Izquierdo Gonzalez
topics:
  - glideinWMS Factory vs. Frontend roles and responsibilities
  - Factory redundancy: Fermilab (Tier-1), OSG/"Tiger" (CMS + other experiments), CERN (CMS) factories
  - Frontend-per-experiment model and per-experiment credentials
  - Entry ownership (factory) vs. entry querying (frontend)
  - Virtual organizations served by the shared factory infrastructure
  - Factory operations meeting schedule
---

# GlideinWMS Factory and Frontend Architecture Follow-up (Onboarding)

## Summary

This was a short one-on-one follow-up session in which Marco Mascheroni continued onboarding Pablo Izquierdo Gonzalez on the [[glideinWMS]] architecture, building on questions Pablo had while reviewing a glideinWMS presentation and updating his own diagram of the system.

Marco first clarified the meaning of "VO" (virtual organization): the [[glideinWMS]] infrastructure is built to serve multiple virtual organizations/experiments, not just [[CMS]] — it also serves other experiments such as DUNE, IceCube, and LIGO (the gravitational-wave interferometer experiment). Marco noted some factories are CMS-only, while others ("common factories") serve all experiments.

Pablo asked whether entries (queues at sites) are defined per-experiment front end or centrally. Marco clarified that entries belong to the [[Factory]], not the [[Frontend]]: the front end does not define entries itself but queries the factory every 10 minutes to get the list of entries. The factory is what knows about the entries/queues at the sites, and can determine which sites serve which experiments (CMS, LIGO, IceCube, DUNE, etc.).

Marco then explained the current factory topology: there are four factories in total, of which CMS uses three. The three factories represent different flavors of redundancy rather than being identical replicas:
- A factory dedicated to CMS Tier-1 sites only, run at Fermilab, managed by "he" (a name the transcript does not clearly resolve) — motivated by wanting Tier-1 support to be especially reliable.
- A factory serving CMS plus other experiments, called the "Tiger" factory (named after the Tiger Kubernetes cluster it runs on), managed by Jeff, and also referred to as the OSG factory.
- A factory serving all CMS sites, run at CERN, managed by Luis Simas.

In contrast to the multiple/shared factories, there is one [[Frontend]] per experiment (CMS, DUNE, IceCube, LIGO, etc.) — this was highlighted as the key distinction between the two components. Marco asked Pablo to reason through why the factory is shared/common while the frontend is per-experiment, rather than simply explaining it. Pablo proposed it could relate to user/VO permissions, i.e., jobs needing to go to particular entries depending on the experiment's permissions. Marco confirmed this is related to credentials: each frontend holds its own set of credentials for accessing sites, and sends these credentials to the factory, which uses them to access the site on behalf of that experiment — different experiments use different credentials, and each frontend also has its own set of [[HTCondor]] access points (APs). Each frontend determines pilot pressure (how many pilots are needed) based on its own experiment's job queue at its access points; Marco noted experiment demand is "spiky," with experiments launching campaigns and then going quiet, and that CMS, being one of the biggest experiments, is organized in a similar wave-like pattern.

Pablo asked whether a single glideinWMS deployment (front end + factory, as one logical "box" in his diagram) manages one VO or could manage multiple. Marco clarified that "glideinWMS" as a system is the frontend plus the factory together, and within that pairing, the factory manages multiple VOs/experiments while the front end manages only one.

Towards the end, discussion turned briefly to scheduling: Marco mentioned a recurring page listing team meetings, including a weekly CMS/OSG factory operations meeting held Tuesdays at 5pm, which Marco suggested Pablo should attend going forward, though he noted it might be skipped the next occurrence since Jeff was still on vacation. Marco also mentioned he holds separate recurring check-ins with Luis Simas (less frequently than with Pablo, since Luis is already ramped up) and needs to check with Hyunwoo (referred to as "Hanvoo"/"Yongvu" in the transcript) about whether a similar check-in is needed. Marco and Pablo agreed to continue the onboarding/training session the next day, tentatively around 3pm, after Marco's other meetings.

## Decisions / Conclusions

- Entries (site/queue definitions) belong to the factory, not the frontend; the frontend queries the factory periodically (every 10 minutes) to obtain the list of entries rather than defining them itself.
- CMS uses three of the four existing factories: a Fermilab factory dedicated to CMS Tier-1 sites, the "Tiger"/OSG factory (CMS plus other experiments, managed by Jeff), and a CERN factory for all CMS sites (managed by Luis Simas). These provide redundancy, but each also serves a distinct purpose rather than being pure replicas of each other.
- There is one frontend per experiment/virtual organization (CMS, DUNE, IceCube, LIGO, etc.), in contrast to the shared/common factory infrastructure; this difference is driven by each experiment/frontend needing its own site-access credentials and its own set of HTCondor access points.
- Within a glideinWMS deployment (frontend + factory), the factory manages multiple virtual organizations while the frontend manages only one.

## Action Items

- [ ] Continue the onboarding/training session the next day (tentatively around 3pm, after Marco's other meetings) — Marco Mascheroni, Pablo Izquierdo Gonzalez
- [ ] Attend the weekly CMS/OSG factory operations meeting (Tuesdays at 5pm) going forward, noting it may be skipped the next occurrence while Jeff is on vacation — Pablo Izquierdo Gonzalez

## Discussion

### Virtual organizations and shared infrastructure
Marco explained that "VO" stands for virtual organization, and that the glideinWMS infrastructure serves multiple VOs/experiments beyond CMS, including DUNE, IceCube, and LIGO. Some factories are CMS-only, while "common" factories serve all experiments.

### Entries belong to the factory, not the frontend
Pablo had understood entries to potentially be defined in the frontend; Marco clarified that entries are not defined in the frontend but belong to the factory, which knows about the queues at each site and which experiments each site supports. The frontend queries the factory every 10 minutes to obtain the current list of entries.

### Factory topology and redundancy
There are four factories in total; CMS uses three of them:
- **Fermilab factory** — serves CMS Tier-1 sites only; described by Marco as motivated by wanting extra reliability specifically for Tier-1s. Managed by a person the transcript does not clearly identify by name.
- **"Tiger" factory** (also referred to as the OSG factory, named for the Tiger Kubernetes cluster) — serves CMS plus other experiments; managed by Jeff.
- **CERN factory** — serves all CMS sites; managed by Luis Simas.

Marco described this setup as providing redundancy, but not identical/uniform redundancy — different factories exist for different reasons (e.g., extra assurance specifically for Tier-1s) rather than being pure duplicates of one another.

### Frontend-per-experiment and credentials
Unlike the shared factory model, there is one frontend per experiment (CMS, DUNE, IceCube, LIGO, etc.). Marco asked Pablo to reason about why this asymmetry exists; Pablo suggested a connection to user/VO permissions. Marco confirmed the frontend holds experiment-specific credentials for site access, which it passes to the factory for use in accessing sites on that experiment's behalf — different experiments use different credentials. Each frontend also has its own set of HTCondor access points, and determines pilot pressure/demand based on its own experiment's job queue. Marco noted that experiment demand tends to be "spiky" (campaigns launched, then quiet periods), including for CMS as one of the largest experiments.

### glideinWMS as frontend + factory
In response to Pablo's question about whether one deployment manages one or multiple VOs, Marco clarified that "glideinWMS" refers to the frontend-plus-factory pairing; within this pairing, the factory manages multiple VOs/experiments while the frontend manages only one.

### Meeting schedule
Marco pointed Pablo to a shared page listing team meetings, including a weekly CMS/OSG factory operations meeting on Tuesdays at 5pm, which Marco suggested Pablo attend, while noting the next occurrence might be skipped since Jeff was still on vacation. Marco also mentioned separate periodic check-ins with Luis Simas (less frequent than with Pablo) and a need to check with Hyunwoo about whether a similar check-in is warranted.

## Open Questions

- Who specifically manages the Fermilab Tier-1 factory (the transcript does not clearly resolve the name given)?
- Whether the weekly CMS/OSG factory operations meeting would take place the following week, given Jeff's vacation, was left unresolved ("probably skipping it").

## Related

[[glideinWMS]] · [[Factory]] · [[Frontend]] · [[HTCondor]] · [[Submission Infrastructure]] · [[Pilot Jobs]] · [[CMS]] · [[Factory Operations]] · [[Workload Management]]

## Source

meeting_saved_closed_caption.txt (from `2026-09-07 15.41.13 Submission Infrastructure Weekly Meeting`)
