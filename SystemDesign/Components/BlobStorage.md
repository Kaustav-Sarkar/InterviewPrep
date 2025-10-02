# BlobStorage

## Quick Refresh
- Object storage (S3, GCS, Azure Blob) holds unstructured data with virtually unlimited capacity and high durability.
- Objects are retrieved by key; there is no hierarchical update—uploads replace entire objects or add versions.
- Presigned URLs let clients upload/download directly without routing large payloads through your servers.

## When to Reach For It
- Storing images, videos, machine learning datasets, logs, and backups cheaply at scale.
- Large file ingestion pipelines needing multipart uploads and lifecycle policies.
- Serving static assets via CDN, or sharing data across analytics/batch jobs.

## Example Scenario
Photo-sharing application:
- Mobile clients request presigned upload URLs from the backend, then upload photos straight to object storage.
- Backend stores metadata (user, album, key) in a relational database referencing the blob URL.
- Lifecycle rules move older media to Glacier/Archive tiers after 90 days to reduce costs.

## Visualizations
```mermaid
sequenceDiagram
    autonumber
    participant Client
    participant Backend as App Server
    participant ObjectStore as S3 Bucket
    participant MetadataDB as Metadata DB

    Client->>Backend: Request upload URL
    Backend->>ObjectStore: Generate presigned URL
    ObjectStore-->>Backend: URL + expiry
    Backend-->>Client: Presigned URL
    Client->>ObjectStore: Multipart upload (parts 1..N)
    Client->>Backend: Notify completion + key
    Backend->>MetadataDB: Persist metadata
    MetadataDB-->>Backend: Ack
    Backend-->>Client: Upload confirmed
```

```mermaid
flowchart LR
    subgraph HotPath
        CDN[(CDN Edge)]
        ImgProxy[Image Resizing Service]
        Cache[(Redis Metadata Cache)]
    end

    subgraph Storage
        PrimaryBucket[(S3 Primary)]
        Archive[(Glacier Archive)]
        DR[(DR Region Bucket)]
    end

    Users[[Users]] --> CDN
    CDN --> ImgProxy
    ImgProxy --> PrimaryBucket
    ImgProxy --> Cache
    PrimaryBucket --> Archive
    PrimaryBucket --> DR
```

```mermaid
stateDiagram-v2
    [*] --> Upload
    Upload --> Lifecycle : 30 days
    Lifecycle --> IA[Infrequent Access]
    IA --> Archive : 90 days
    Archive --> Delete : Retention met
    Delete --> [*]
```

## Operational Guidance
- Avoid storing large binaries directly in relational databases; offload to object storage for cost and performance.
- Use versioning and replication for durability; enable server-side encryption and IAM policies for security.
- Monitor bandwidth and set up multipart uploads for objects beyond gateway limits (e.g., 5MB chunking in S3).
- Design signed downloader URLs for clients to stream content without hitting your backend.

## Deepen Your Understanding
- Hello Interview – Storage Building Blocks: https://www.hellointerview.com/learn/system-design/in-a-hurry/storage
- AWS re:Invent – Deep Dive on Amazon S3 (2024): https://youtu.be/vVj2wURQqV8
- Gaurav Sen – Object Storage Explained: https://youtu.be/OZDGEmTsA1M