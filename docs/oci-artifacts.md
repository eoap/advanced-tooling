# 📦 OCI Artifact Publishing for CWL Workflows with Embedded SBOMs

## Overview

The CI step, `publish-oci-artifact`, publishes a **Common Workflow Language (CWL)** document as an **OCI artifact** to GitHub Container Registry (`ghcr.io`) and **attaches Software Bill of Materials (SBOMs)** for each container image referenced in the workflow.

This makes the CWL workflow self-describing, portable, and security-aware—without requiring direct access to the containers it uses at runtime.

## Why OCI Artifacts for CWL?

OCI artifacts are a standardized way to publish non-container objects like Helm charts, WASM modules, or in this case, CWL documents. This lets you:

- **Version and tag workflows** just like Docker images
- **Push to and pull from OCI-compatible registries**
- **Attach related metadata**, such as SBOMs, licenses, or provenance attestations
- **Distribute CWL workflows securely and reproducibly**

## Why Attach SBOMs?

Most CWL workflows depend on container images declared via:

```yaml
hints:
  DockerRequirement:
    dockerPull: ghcr.io/your-org/tool:1.2.3
```

However, CWL alone doesn’t embed what is inside those containers. By generating and attaching SBOMs (via syft), we enrich the CWL artifact with security and supply chain transparency:

* Security Scanning: SBOMs allow for vulnerability scans of container contents without downloading or executing the containers.

* Compliance Auditing: Includes details on licenses, libraries, and binaries used.

* Reproducibility: Makes the full dependency stack explicit.

*  Offline Analysis: Consumers can retrieve and inspect the SBOM from the CWL OCI artifact.

## What Does the CI Step Do?

Install oras and syft for pushing OCI artifacts and generating SBOMs.

* Login to ghcr.io using the GITHUB_TOKEN.

* For each CWL file:

  * Publish the CWL as an OCI artifact:

```bash
oras push ghcr.io/your-org/your-repo/your-workflow:1.2.3 \
  --artifact-type application/cwl \
  app-workflow.cwl:application/cwl
```

* Extract all container image references (dockerPull) from the CWL.

* For each image:

  * Generate an SBOM using syft.

  * Attach the SBOM to the CWL artifact:

```bash
oras attach ghcr.io/.../workflow:1.2.3 \
  --artifact-type application/spdx+json \
  sbom.spdx.json
```

## Benefits at a Glance

| **Feature**                 | **Benefit**                                                         |
|----------------------------|----------------------------------------------------------------------|
| **OCI artifact**            | CWL workflows are versioned, taggable, and registrable              |
| **SBOM attachment**         | Transparent container dependencies                                  |
| **No need for image access**| SBOMs are stored externally, no image pull required                 |
| **Reproducibility & auditing** | Enables end-to-end provenance and security introspection         |
| **CWL+OCI integration**     | Treats workflows as first-class, shareable build artifacts          |


Example Artifact Tree:

```bash
ghcr.io/org/repo/app-water-bodies-cloud-native:1.1.0
├── manifest: application/cwl
├── layer: app-water-bodies-cloud-native.cwl
├── attached:
│   ├── type: application/spdx+json
│   ├── name: ghcr.io/org/tool-a@sha256:...sbom.spdx.json
│   └── ...
```

## Related Tools

oras – OCI Registry As Storage CLI

syft – SBOM generation CLI

OCI Artifact Spec – open standard for publishing non-container objects

