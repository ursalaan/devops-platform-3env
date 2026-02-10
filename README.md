# DevOps 3-Environment Deployment Platform

A small but complete DevOps platform showing how a modern engineering team builds, packages, deploys, and promotes an application across dev → staging → prod.

The application itself is deliberately minimal. This repository is a portfolio and reference implementation focused on delivery mechanics rather than product features. It exists to demonstrate how software should move from a commit to a running service in a predictable, auditable way: built once, versioned immutably, deployed safely, and promoted without rebuilding. The design choices prioritise clarity, traceability, and control over scale or feature depth.

This project was built to practise and demonstrate core DevOps delivery patterns in a setup that is small enough to understand end-to-end, yet realistic enough to reflect how real teams work. It is intended to be inspected, questioned, and extended rather than treated as a finished product.

## What this repository demonstrates

### Build once, deploy many
Each commit produces a single Docker image. That exact image is promoted through dev, staging, and prod without rebuilding, ensuring the artifact tested earlier is the same artifact released later.

### Three environments in one cluster
dev, staging, and prod run in separate Kubernetes namespaces. This keeps environments isolated while sharing the same cluster, reflecting how teams often balance separation with operational simplicity.

### Continuous Integration (CI)
Every push triggers automated tests, a Docker build, and publication to GitHub Container Registry (GHCR). Images are tagged with the commit SHA to support clear release identification and auditing.

### Continuous Deployment (CD – dev)
When CI succeeds, the pipeline automatically deploys to the dev environment. This keeps feedback fast and reduces manual steps, while leaving staging and production as controlled promotion targets.

### Release traceability
The service exposes the exact Git commit SHA via `/version`. At any point, it is possible to confirm precisely what code is running in each environment without relying on external dashboards or guesswork.

## Architecture overview

### Core components
- FastAPI — minimal API used for health checks, environment reporting, and version visibility  
- Docker — produces an immutable container image per commit  
- Kubernetes — runs the service with replicas, health probes, and rolling updates  
- GitHub Actions — automates CI and deployment workflows  
- GitHub Container Registry (GHCR) — stores versioned container images  

### Environments
- dev — automatically updated after successful CI  
- staging — reserved for controlled, manual promotion  
- prod — reserved for controlled, manual promotion  

Promotion is image-only. No environment rebuilds artifacts.

## API endpoints

| Endpoint  | Purpose |
|----------|---------|
| /health  | Liveness and readiness checks for Kubernetes |
| /env     | Returns the environment the service is running in |
| /version | Returns the deployed release version (commit SHA) |

Example response:

{"version":"4d322b9e324c8b208bea8c15aa47b039cea89a43"}

## CI/CD flow

### Continuous Integration (on push to master)
- Run application tests  
- Build a Docker image  
- Publish the image to GHCR with two tags:  
  - ghcr.io/ursalaan/devops-platform-3env:<commit-sha>  
  - ghcr.io/ursalaan/devops-platform-3env:latest  

The commit-SHA tag is treated as the release identifier. Deployments reference this tag directly so changes can be reproduced, traced, and audited cleanly.

### Continuous Deployment (dev)
- Update the dev Deployment to reference the commit-SHA image  
- Set VERSION=<commit-sha> as an environment variable  
- Perform a rolling update and wait for readiness  

No rebuilds occur between environments. Promotion to staging and prod is intentionally gated to mirror real release control.

## Running locally

### Python
cd app  
python -m venv .venv  
source .venv/bin/activate  
pip install -r requirements.txt  
uvicorn main:app --reload  

### Docker
docker build -f docker/Dockerfile -t devops-platform-api .  
docker run --rm -p 8000:8000 devops-platform-api  

## Running on Kubernetes (kind)

### Create a local cluster
kind create cluster --name devops-3env  

### Deploy to dev
kubectl apply -f k8s/dev.yaml  

### Access the service
kubectl port-forward -n dev svc/api 8000:80  

## Repository structure

app/ FastAPI application and tests  
docker/ Dockerfile  
k8s/ Kubernetes manifests (dev / staging / prod)  
.github/workflows/ CI/CD pipelines  
terraform/ Infrastructure (placeholder for future cloud provisioning)  

## Notes

This project is intentionally small but complete. It is designed as a reference implementation of core delivery practices: immutable artifacts, environment isolation, automated deployment to dev, controlled promotion to staging and production, and clear release traceability.

In a full production environment, promotion would typically be driven by explicit release workflows, quality gates, approvals, or policy checks. Those concerns are deliberately simplified here so the core delivery mechanics remain clear and inspectable.

The goal is not complexity or scale, but predictable delivery and a workflow that could be lifted into a larger system with minimal change.
