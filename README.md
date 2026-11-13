# RightProperty365 GitOps

Argo CD source for RightProperty365 staging and production. The application repositories publish images to GHCR and update `environments/<environment>/kustomization.yaml` using `scripts/set-image.py`.

- `dev` application branches map to staging; `production` application branches map to production.
- The GitOps repository branch is `main`.
- Staging is initialized to the published frontend and API dev images. Production image mappings remain placeholders until production builds are available; do not sync the production Application until those images and runtime settings have been reviewed.
- The API requires a Kubernetes Secret named `api-database` in each namespace containing `DATABASE_URL`, and requires migrations before use. Do not put credentials in this repository.
- Traefik provides ingress. Host Nginx terminates TLS and forwards to the ingress controller.
- The Kubernetes control plane must be able to pull the images. The currently published dev images were accessible anonymously at initialization.
- Both application workflows currently reference the former `adminweighty/weightygitops` repository. Update them to `adminweighty/gitops` and configure a `GITOPS_TOKEN` with write access before automated updates can work.

Validate with `kubectl kustomize environments/staging` and `kubectl kustomize environments/production`. The default GitOps manifests deliberately do not include database passwords, database provisioning, or migration automation.
