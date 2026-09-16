---
type: meeting
date: 2026-09-08
participants:
  - Marco Mascheroni
  - Pablo Izquierdo Gonzalez
topics:
  - glideinWMS terminology clarification: glidein pilot vs. execution point vs. Condor startd
  - Recap of front end / factory division of responsibilities
  - Factory mission (leasing grid resources, minimizing waste)
  - Infrastructure walkthrough: node list, pools, central manager, access points
  - Front-end process, logging, and monitoring table walkthrough via SSH
  - Puppet-managed front-end configuration (frontend.xml) and GitLab config repository
  - Travel arrangements for HTCondor Week
  - Operator handover / training overlap (Florian, Pablo, Luis)
---

# GlideinWMS Frontend Training: Terminology Clarification and Infrastructure Walkthrough

## Summary

This was a continuation of the one-on-one onboarding/training sessions between Marco Mascheroni and Pablo Izquierdo Gonzalez on [[glideinWMS]], following on from the previous day's session. Pablo had been updating his own architecture diagram and reviewing older [[glideinWMS]] training presentations, and brought several terminology questions to clarify his understanding before the pair moved into a hands-on walkthrough of the actual production infrastructure.

Pablo's main point of confusion was around conflicting depictions he had seen in older presentations: some showed the "glidein pilot" as containing the execution point, while others showed it the other way around (execution point containing the pilot). Marco clarified that this is mostly a terminology issue: a glidein pilot (also called a glidein startup) is essentially a startup script/job that configures and starts an [[HTCondor]] `condor_startd` on a worker node. The glidein startup and the "glidein pilot" refer to the same thing. A single worker node (execution point) can run multiple glidein startups concurrently, each creating its own distinct HTCondor execute machine (visible as separate entries in `condor_status`), even though they run on the same physical node. Glidein sizing (e.g., number of cores) is statically defined in the factory configuration, not derived from the requirements of the job that will eventually run inside it.

Marco and Pablo also recapped and reinforced concepts from the previous session: factories are VO-agnostic and shared across virtual organizations (saving significant operational effort), while matchmaking against a user's/VO's access permissions happens in the front end, not the factory — the factory simply advertises entries to the front end. Marco read through and briefly explained the factory's stated mission from a training slide: the factory is responsible for obtaining leases on grid resources on demand, ensuring the system delivers those resources to users, and minimizing waste in the process. Pablo related this to the front end instructing the factory to increase the number of glidein instances (e.g., "give me 7 glideins at IFCA") and the factory obtaining resource leases at the site on the front end's behalf.

The pair then moved to a hands-on walkthrough, mapping the architecture diagrams Pablo had drawn to the actual list of machines the team operates. Marco introduced the concept of "pools" (e.g., the global pool, the Tier-0 pool, and the ITB — integration testbed — pool used for testing new updates), explaining that each pool has its own central manager and one or more access points, and that CMS, unlike most VOs, runs multiple front ends rather than a single one. They SSH'd into the production front end of the global pool, inspected running processes (the front end is implemented in Python), and looked at the front-end log files under `/var/log/gwms` (e.g., `main.info`, `main.debug`, `main.warning`, `main.error`), noting these correspond to standard logging levels. They then looked at the front end's monitoring output, walking through an iteration cycle and the resulting per-site table: job counts pulled from the Condor `SchedD` queues, slot counts, and the "Glidein request idle/max run" columns, which represent how many idle glideins the front end wants kept ready at a site and the maximum number of running glideins allowed there. Marco explained the purpose of keeping some glideins idle (pre-warmed capacity) is that spinning up new glideins takes time, so keeping a buffer avoids jobs waiting on cold-start latency; Pablo related this correctly to the concept as "hot" pre-provisioned capacity for high-throughput computing, and Marco confirmed there is no binding between a specific job and a specific pilot at the idle-request stage — it is a resource-provisioning signal, not a direct job assignment.

Finally, Marco showed Pablo where the front end's live configuration lives: `/etc/gwms-frontend/frontend.xml` on the front-end machine, which is a symlink managed by [[Puppet]] and should not be edited directly — the authoritative source is a config repository in GitLab, updated through a templating mechanism that Marco said they would go through in a future session. He also mentioned the Puppet host group used for the front end and pointed Pablo toward two Puppet module/host-group repository links (sent in chat) as well as CERN IT documentation on Puppet, though he was unable to locate the latter link during the call. A component called the CCB (central collection broker) was mentioned as appearing in some documentation but not yet covered or mapped into the pair's architecture picture, and was deferred to a later session.

Outside of the technical walkthrough, Pablo mentioned he had started the travel paperwork (hotel and train bookings) for HTCondor Week, prompting Marco to note he still needs to do the same for UCSD. Marco and Pablo also briefly discussed the training/operator handover: Pablo is being trained as the front-end operator while Luis is the factory operator; Florian, who had previously covered the front-end role, left earlier than his planned October end date, so the usual ~1-month operator overlap/training period has been compressed, with Marco covering some of the gap. Pablo noted he still needs help understanding how the various Puppet repositories relate to one another, and plans to ask Luis (who is about to go on vacation) and/or Viva. The session ended with Marco and Pablo agreeing to continue the walkthrough the next day, tentatively between 2 and 3 PM (Spanish/CERN time), picking up from the front-end XML configuration and templating mechanism.

## Decisions / Conclusions

- A glidein pilot and a glidein startup refer to the same thing: a startup job/script that validates the worker node, downloads Condor binaries, configures and starts a Condor `condor_startd` on that node.
- A single worker node (execution point) can run multiple glidein startups concurrently; each one creates a distinct HTCondor execute machine visible separately via `condor_status`, even though they share the same physical node.
- Glidein size (e.g., core count) is statically defined in the factory configuration and does not depend on the requirements of the job(s) that will eventually run inside it.
- Recap/confirmation from the prior session: entries are owned by the factory; matchmaking against user/VO access permissions happens in the front end, not the factory. This is why factories can be shared/VO-agnostic across experiments while CMS still runs multiple front ends.
- The factory's mission (per training material) is to obtain leases on grid resources on demand, ensure resources are reliably delivered to users, and minimize waste in that process.
- Each operational pool (e.g., global pool, Tier-0 pool, ITB test pool) has its own central manager and one or more access points; the ITB pool is used specifically for testing new updates before production rollout.
- The front end's live configuration file, `/etc/gwms-frontend/frontend.xml`, is a Puppet-managed symlink and must not be edited directly; the authoritative source is a GitLab config repository, applied through a templating mechanism (to be covered in a future session).
- Idle glidein requests (e.g., "100 idle, 600 max run" at a site) represent pre-provisioned capacity to absorb incoming job pressure without waiting for new glideins to start; there is no binding between a specific job and a specific pilot at that stage.

## Action Items

- [ ] Create the travel request for HTCondor Week — Marco Mascheroni
- [ ] Continue reviewing/updating the glideinWMS architecture diagram and training material using today's clarifications — Pablo Izquierdo Gonzalez
- [ ] Talk to Luis Simas and/or Viva about how the Puppet repositories relate to one another — Pablo Izquierdo Gonzalez
- [ ] Continue the training session tomorrow, tentatively 2–3 PM, starting from the front-end `frontend.xml` configuration and templating mechanism — Marco Mascheroni, Pablo Izquierdo Gonzalez

## Discussion

### Glidein pilot vs. execution point terminology
Pablo raised confusion from older presentations that depicted the relationship between "glidein pilot" and "execution point" inconsistently (one containing the other, or vice versa). Marco clarified this is largely a terminology artifact: the glidein pilot/glidein startup is a job that configures and starts a Condor `condor_startd` on a worker node (execution point); a worker node can host multiple glidein startups at once (e.g., sized at 16 cores for Tier-2 or larger multiples for Tier-1), each producing its own separate Condor execute machine. Marco noted worker nodes may simultaneously run pilots from multiple experiments (e.g., CMS and ATLAS glideins side-by-side on the same physical node, unless it is a "whole node" allocation), and that ATLAS uses its own terminology ("pilots") rather than "glideins."

### Front end / factory responsibilities recap
Building on the prior session, Marco and Pablo reaffirmed that factories are VO-agnostic and shared across experiments to reduce operational effort, while the front end performs matchmaking of jobs to entries based on VO/user credentials and access. Marco read through the factory's stated mission from training material: obtaining leases on grid resources on demand, ensuring reliable delivery of those resources to users, and minimizing waste. Pablo connected this to the front end instructing the factory to request a specific number of glideins at a site (e.g., "7 glideins at IFCA"), with the factory then obtaining the resource lease at that site.

### Infrastructure and pool walkthrough
Using the team's node list, Marco introduced "pools" as roughly corresponding to individual front ends (CMS runs multiple, unlike most VOs which run one). They identified the global pool (production), the Tier-0 pool, and the ITB (integration testbed) pool used for testing new software/updates. Each pool has its own central manager (single machine) and one or more access points (multiple machines). The Condor collector/negotiator run on the central manager machine.

### Front-end process, logs, and monitoring
Pablo and Marco SSH'd into the production front end of the global pool. `ps` showed the front end's Python processes, including sub-processes used for per-schedd/site queries. Log files live under `/var/log/gwms/<group>/`, split by log level (info, debug, warning, error); Marco said he typically checks `main.info` first, then `debug`/`error` if more detail is needed. They then reviewed the front-end monitoring output for an iteration cycle, in particular a per-site table showing: job counts pulled from Condor `SchedD` queues (e.g., idle jobs matching a given site such as KIT, noting jobs can match multiple sites and are counted once wherever they land), slot counts, and "Glidein request idle/max run" — the number of idle glideins the front end wants kept ready at a site and the maximum allowed running there. Marco noted most sites were requesting the maximum idle count (100) except a few identified as likely large sites (e.g., Fermilab, Caltech) which may be running whole-node allocations.

### Puppet-managed configuration
Marco showed that the front end's configuration file (`/etc/gwms-frontend/frontend.xml`) is a Puppet-managed symlink, not to be edited directly; the source of truth is a config repository in GitLab, deployed via a templating mechanism to be covered in a future session. They also looked briefly at the corresponding Puppet host group and module repositories (branches such as QA and master/production), though Marco noted he does not work with Puppet often and suggested Pablo follow up with Luis or Viva. A related component, the CCB (central collection broker), was noted as appearing in some documentation but was not yet mapped into their architecture picture and was deferred.

### Travel and staffing
Pablo mentioned he had already started travel paperwork (hotel/train bookings) for HTCondor Week; Marco noted he still needs to submit his own for UCSD. Separately, Marco and Pablo discussed the operator handover: Pablo is training as the front-end operator, with Luis as the factory operator. Florian, who previously covered part of this training, left earlier than his planned October departure, compressing the usual ~1-month operator overlap period; Marco is covering part of the gap. Pablo said understanding how the numerous Puppet repositories relate to each other remains a gap, which he plans to address with Luis (soon going on vacation) and/or Viva.

## Open Questions

- The role and architecture placement of the CCB (central collection broker) has not yet been discussed or mapped into Pablo's diagram.
- Marco was unable to locate the CERN IT Puppet documentation link during the call and said he would send it later if found.
- It is unclear from the transcript who "Bob" refers to (mentioned once regarding full-saturation resource-usage mode).
- How the various Puppet repositories/host groups relate to one another was left as an open item for Pablo to resolve with Luis and/or Viva.

## Related

[[glideinWMS]] · [[Frontend]] · [[Factory]] · [[HTCondor]] · [[Pilot Jobs]] · [[CMS]] · [[OSG]] · [[Submission Infrastructure]] · [[Puppet]] · [[Factory Operations]]

## Source

meeting_saved_closed_caption.txt (from `2026-09-08 15.28.03 Submission Infrastructure Weekly Meeting`)
