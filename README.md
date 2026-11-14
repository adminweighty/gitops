# RightProperty365 GitOps

Argo CD source for RightProperty365 staging and production. The application repositories publish images to GHCR and update `environments/<environment>/kustomization.yaml` using `scripts/set-image.py`.

- `dev` application branches map to staging; `production` application branches map to production.
- The GitOps repository branch is `main`.
- Staging is initialized to the published frontend and API dev images. Production image mappings remain placeholders until production builds are available; do not sync the production Application until those images and runtime settings have been reviewed.
- The API requires a Kubernetes Secret named `api-database` in each namespace containing `DATABASE_URL`, and requires migrations before use. Do not put credentials in this repository.
- Traefik provides ingress. Host Nginx terminates TLS and forwards to the ingress controller.
- The Kubernetes control plane must be able to pull the images. The currently published dev images were accessible anonymously at initialization.
- Both application `dev` workflows reference `adminweighty/gitops`. Configure a `GITOPS_TOKEN` with write access in each application repository before automated updates can work.
- Staging PostgreSQL runs only inside the staging namespace and persists data on this VM at `/var/lib/rightproperty/staging-postgres`. Its `postgres-credentials` Secret and the API `api-database` Secret must be provisioned separately; protect and back up the volume and secrets. This single-node hostPath is not highly available.
- Staging Elasticsearch (listing search) runs only inside the staging namespace as a single node, with data on this VM at `/var/lib/rightproperty/staging-elasticsearch` (owned by uid 1000). It has no Ingress. Its Secret `elasticsearch-credentials` holds `ELASTIC_PASSWORD` (the `elastic` superuser) and `ELASTICSEARCH_API_KEY` (the scoped key the API uses) and must be provisioned separately. PostgreSQL stays the source of truth: rebuild the index with the backend `reindex` command after a mapping change or data loss. Not set up: snapshots, TLS inside the cluster, monitoring.

Validate with `kubectl kustomize environments/staging` and `kubectl kustomize environments/production`. The GitOps manifests do not include database passwords or automated migrations. Run and verify backend migrations before starting a newly initialized API database.
