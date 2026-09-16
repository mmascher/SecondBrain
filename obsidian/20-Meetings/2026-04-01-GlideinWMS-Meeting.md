---
type: meeting
date: 2026-04-01
participants:
  - Marco Mascheroni
topics:
  - proxy authentication
  - SciTokens migration
---

# GlideinWMS Meeting

## Summary

The group discussed the loss of SSL-client-certificate support in a dependency and its impact on CMS backup frontends that still submit proxy-authenticated jobs.

## Decisions / Conclusions

- CMS should identify entries still using proxy authentication and plan migration to [[SciTokens]].
- The currently renewed backup-frontend certificate provides less than a year of runway; revocation would remove that buffer.

## Action Items

- [ ] Inventory CMS entries that still use proxy authentication and plan their migration to SciTokens — Marco Mascheroni

## Discussion

The backup frontends for Tier 0 and the Global Pool can no longer create SSL client certificates after the dependency change. ARC sites are expected to support SciTokens, though some entries still use proxies because site migration is incomplete. The transcript reported six proxy-only sites in the speaker’s scope and around 40 ARC factory entries still using proxies overall; the CMS-specific subset was not established.

## Related

[[CMS]] · [[glideinWMS]] · [[SciTokens]] · [[Tier 0]] · [[Global Pool]]

## Source

meeting_saved_closed_caption.txt (from `2026-04-01 17.17.56 GlideinWMS Meeting`)
