# In-Cluster Container Image Build using Kaniko

This guide describes the in-cluster container image build process using Kaniko and Skaffold, configured through a custom project.toml and Taskfile.yaml. It supports building container images for CWL CommandLineTools defined in a modular CWL workflow.

## Project Structure

The root project contains:

* `project.toml`: Declarative metadata about tools, workflows, build engine, test parameters.

* `command-line-tools/`: One subdirectory per tool, each with a Dockerfile and tool-specific code.

* `cwl-workflow/`: CWL workflows referencing tools via path anchors.

## Build Configuration

`project.toml` key sections

```toml
[build]
engine = "cluster"

[build.cluster]
namespace = "eoap-advanced-tooling"
serviceAccount = "kaniko-sa"
registry = "ghcr.io/eoap"
secret = "kaniko-secret"
```

The above sets the build engine to cluster, targeting in-cluster Kaniko builds in namespace `eoap-advanced-tooling` using the given service account and secret for pushing to the container registry.

Each tool under [tools.<name>] defines:

* `context`: Path to Docker build context.

* `path`: CWL document reference to update post-build.

## Build Process Overview

1. Prepare Skaffold Config (Task: prepare-kaniko)

This generates a dynamic skaffold-auto.yaml by:

- Extracting all tool context directories and image names.

- Inserting them into .build.artifacts using yq.

- Mounting the kaniko-secret to authenticate with ghcr.io.

This enables Skaffold to understand how to build each tool's container image with Kaniko.

2. Execute In-Cluster Build (Task: build-kaniko)

Runs:

bash
`skaffold build -f skaffold-auto.yaml -v=error -q > build.json`

Result:

- Kaniko builds each image from the provided context.

- Images are pushed to the configured registry.

- `build.json` captures the image digests (e.g., sha256: tags).

3. CWL DockerRequirement Update (Task: update)

This task reads `build.json`, extracts each built image tag, and updates the CWL files defined in `project.toml`:

If a tool has `hints.DockerRequirement`, it is updated.

Otherwise, `requirements.DockerRequirement` is injected or updated.

Effectively, this replaces all `dockerPull: hints` in CWL CommandLineTools with the freshly built and pushed image references.

## Full Build Chain

To run the entire build:

```bash
task build
```

This executes:

- prepare-kaniko
- build-kaniko
- update

You can also build locally for debugging (build-local) or generate TTL-based images (`build-ttl`).

##  Running Tests in Cluster

The test task uses Calrissian to run tests defined under:

```toml
[tools.<tool>.tests]

[[workflows.tests]]
```

Each test defines inputs, execution config (RAM, CPU, service account), and output locations. The engine is automatically detected from `project.toml`.

Example command executed:

```bash
calrissian \
  --stdout /calrissian/crop-green/results.json \
  --stderr /calrissian/crop-green/app.log \
  --max-ram 1G \
  --max-cores 1 \
  --outdir /calrissian/crop-green/results \
  --tool-logs-basepath logs \
  --pod-serviceaccount calrissian-sa \
  cwl-workflow/app-water-bodies-cloud-native.cwl#crop params.yaml
```

To run all tests:

`task test-all`

## Summary

| Step               | Tool Used         | Description                                                                 |
|--------------------|------------------|-----------------------------------------------------------------------------|
| Config generation  | `prepare-kaniko` | Builds `skaffold-auto.yaml` dynamically from `project.toml`.               |
| Image build        | `skaffold` + Kaniko | Executes in-cluster container builds and pushes to the container registry. |
| CWL update         | `update`         | Rewrites `DockerRequirement` with SHA-based image tags in CWL documents.   |
| Execution          | `calrissian`     | Runs CWL `CommandLineTool` and `Workflow` tests inside the Kubernetes cluster. |

## Notes

- Works with multi-tool CWL workflows.
- Enables SHA-pinned reproducibility via update step.
- TTL build support targets ephemeral build systems (e.g., ttl.sh).