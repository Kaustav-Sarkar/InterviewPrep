# CDNs

## Quick Refresh
- Content Delivery Networks cache assets at edge locations to serve users from nearby points-of-presence (PoPs).
- Reduce origin load, improve latency, and offer protection against DDoS by absorbing traffic globally.
- Work best with static or cacheable content; dynamic acceleration adds TCP/TLS optimizations.

## When to Reach For It
- Delivering static assets (images, videos, JS/CSS) to global audiences.
- Offloading API reads where responses can be cached safely.
- Protecting origins from traffic spikes, bot attacks, or DDoS.

## Example Scenario
Video streaming platform:
- Users request video segments; CDN edge checks cache, falls back to origin if needed.
- Origin signs URLs with limited lifetime to prevent hotlinking; CDN enforces token-based access.
- Analytics track edge cache hit ratios per region to decide where to warm caches.

## Visualization
```mermaid
graph LR
    User[Viewer]
    DNS[DNS]
    CDNPoP[CDN Edge PoP]
    Origin[Origin Servers]

    User --> DNS
    DNS --> CDNPoP
    CDNPoP --> User
    CDNPoP -- Cache Miss --> Origin
    Origin --> CDNPoP
```

## Operational Guidance
- Set cache-control headers (TTL, `stale-while-revalidate`) and version assets with fingerprints.
- Pre-warm critical assets during deployments to avoid cold-start penalties.
- Integrate CDN logs with observability stack to monitor latency and error rates.
- Plan invalidation strategies: purge on deploy, soft TTL plus background refresh, or cache busting query params.

## Deepen Your Understanding
- Hello Interview – CDNs & Edge: https://www.hellointerview.com/learn/system-design/cdn
- Gaurav Sen – CDN Deep Dive: https://youtu.be/5vV0H0mp1gI
- Akamai Engineering – How CDNs Work: https://youtu.be/7_L58h4xXfM
