---
type: meeting
date: 2026-03-10
participants:
  - Marco Mascheroni
  - Vaiva Zokaite
  - Hyunwoo Kim
topics:
  - HTCondor 25
  - glideinWMS testing
---

# OSG Factory Ops Meeting

## Summary

The group reviewed a gradual [[HTCondor]] 25.0.7 rollout, the unstable 3.11.3 frontend test, and repository selection for [[glideinWMS]] packages.

## Decisions / Conclusions

- HTCondor 25.0.7 was working on tested Fermilab machines, except for a Python-bindings issue to be reported upstream.
- The 3.11.3 frontend issue was not attributed to HTCondor 25; it involved frontend/factory exchange and decryption of key data.
- Development repositories should not be used without explicit release-team guidance.

## Action Items

- [ ] Open an HTCondor ticket for the Python-bindings issue — Hyunwoo Kim
- [ ] Investigate the 3.11.3 frontend key-exchange/decryption failure — Marco Mascheroni

## Discussion

The production factory used 3.11.3-2 to obtain pilot-monitoring functionality. ITB had been reconfigured and worked with the Fermilab frontend, but the new frontend version still had an unresolved bug. The group discussed moving SI machines to HTCondor 25 after testing, while retaining the older glideinWMS frontend until the 3.11.3 issue was understood.

## Related

[[OSG]] · [[Factory Operations]] · [[glideinWMS]] · [[HTCondor]]

## Source

meeting_saved_closed_caption.txt (from `2026-03-10 17.15.12 OSG Factory Ops Meeting`)
