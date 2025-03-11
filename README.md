# eoap-taskfile

## Configuring Taskfile 

Enable the remote files experimental feature:

```
export TASK_X_REMOTE_TASKFILES=1
```

## Requirements

- yq
- tomlq
- skaffold
- task 

## Flow

### Build the CWL command-line tools container images

Build the containers using `kaniko` with:

```
task build-ttl
```

This will build the containers for all command-line tools defined in the `project.toml` file and push them to the `ttl.sh` container registry.

The expected output is:

```
The task you are attempting to run depends on the remote Taskfile at "https://raw.githubusercontent.com/eoap/task-files/refs/heads/feature-2/build-test/Taskfile.yaml".
--- Make sure you trust the source of this Taskfile before continuing ---
Continue? [y/N]: y
❌ Build engine is set to "cluster", skipping
🚀 Preparing skaffold build configuration
🔧 Adding build configuration for CommandLineTool crop
🔧 Adding build configuration for CommandLineTool norm_diff
🔧 Adding build configuration for CommandLineTool otsu
🔧 Adding build configuration for CommandLineTool stac
✅ Skaffold configuration generated in skaffold-auto.yaml
🚀 Building images with Skaffold...
✅ Images built successfully
🚀 Updating CWL files with the new images...
🔧 Updating cwl-workflow/app-water-bodies-cloud-native.cwl
🔧 Updating CommandLineTool crop hints with image ttl.sh/crop:2h@sha256:83d8cae01195dabd5f8b32b491ff64c55907a657c64802cb5b432cdf849e6cb8
🔧 Updating CommandLineTool norm_diff hints with image ttl.sh/norm_diff:2h@sha256:60cb227281f9778f8b9683794d1d9c35137f7ed5ce3e554fd5d979313e25a2cf
🔧 Updating CommandLineTool otsu hints with image ttl.sh/otsu:2h@sha256:e550e1a6c5aff3f1701c628ff9c2dd1ae06000b67b9d6cf1bfd1b886724a312f
🔧 Updating CommandLineTool stac hints with image ttl.sh/stac:2h@sha256:df5635b41c29268a264a909aa62c52d4ffe6c00e178001b2f6314a70cfd1f076
✅ CWL workflow cwl-workflow/app-water-bodies-cloud-native.cwl updated successfully
🔧 Updating cwl-workflow/app-water-body-cloud-native.cwl
🔧 Updating CommandLineTool crop hints with image ttl.sh/crop:2h@sha256:83d8cae01195dabd5f8b32b491ff64c55907a657c64802cb5b432cdf849e6cb8
🔧 Updating CommandLineTool norm_diff hints with image ttl.sh/norm_diff:2h@sha256:60cb227281f9778f8b9683794d1d9c35137f7ed5ce3e554fd5d979313e25a2cf
🔧 Updating CommandLineTool otsu hints with image ttl.sh/otsu:2h@sha256:e550e1a6c5aff3f1701c628ff9c2dd1ae06000b67b9d6cf1bfd1b886724a312f
🔧 Updating CommandLineTool stac hints with image ttl.sh/stac:2h@sha256:df5635b41c29268a264a909aa62c52d4ffe6c00e178001b2f6314a70cfd1f076
✅ CWL workflow cwl-workflow/app-water-body-cloud-native.cwl updated successfully
✅ CWL workflows updated successfully
```

### Test the command-line tools 

#### Test the `crop` CWL command-line tool with: 

```
task test-crop
```

This runs the configuration items found in the `project.toml` file:

```toml
[[tools.crop.tests]]
name = "crop-test-green"
description = "Test case 1 for crop tool - green band."
```

and

```toml
[[tools.crop.tests]]
name = "crop-test-nir"
description = "Test case 2 for crop tool - nir band."
```

The expected output is:

```
🚀 Running tests using engine cluster
tool path: cwl-workflow/app-water-bodies-cloud-native.cwl#crop
Test Name: crop-test-green
Description: Test case 1 for crop tool - green band.
---------------------------
calrissian --stdout /calrissian/crop-green/results.json --stderr /calrissian/crop-green/app.log --max-ram 1G --max-cores "1" --tmp-outdir-prefix /calrissian/crop-green/tmp/ --outdir /calrissian/crop-green/results --usage-report /calrissian/crop-green/usage.json --tool-logs-basepath /calrissian/crop-green/logs --pod-serviceaccount calrissian-sa cwl-workflow/app-water-bodies-cloud-native.cwl#crop params.yaml
INFO calrissian 0.18.1 (cwltool 3.1.20240708091337)
INFO Resolved 'cwl-workflow/app-water-bodies-cloud-native.cwl#crop' to 'file:///workspace/advanced-tooling/cwl-workflow/app-water-bodies-cloud-native.cwl#crop'
{
    "cropped": {
        "location": "file:///calrissian/crop-green/results/crop_green.tif",
        "basename": "crop_green.tif",
        "class": "File",
        "checksum": "sha1$69255dfb77442b710fb7caf4fe2c555a8a8ca404",
        "size": 87481912,
        "path": "/calrissian/crop-green/results/crop_green.tif"
    }
}INFO Final process status is success
Test Name: crop-test-nir
Description: Test case 2 for crop tool - nir band.
---------------------------
calrissian --stdout /calrissian/crop-nir/results.json --stderr /calrissian/crop-nir/app.log --max-ram 1G --max-cores "1" --tmp-outdir-prefix /calrissian/crop-nir/tmp/ --outdir /calrissian/crop-nir/results --usage-report /calrissian/crop-nir/usage.json --tool-logs-basepath /calrissian/crop-nir/logs --pod-serviceaccount calrissian-sa cwl-workflow/app-water-bodies-cloud-native.cwl#crop params.yaml
INFO calrissian 0.18.1 (cwltool 3.1.20240708091337)
INFO Resolved 'cwl-workflow/app-water-bodies-cloud-native.cwl#crop' to 'file:///workspace/advanced-tooling/cwl-workflow/app-water-bodies-cloud-native.cwl#crop'
{
    "cropped": {
        "location": "file:///calrissian/crop-nir/results/crop_nir.tif",
        "basename": "crop_nir.tif",
        "class": "File",
        "checksum": "sha1$2d6eb0dc351bd77d3f5b06672ed012ef5dec508f",
        "size": 100150064,
        "path": "/calrissian/crop-nir/results/crop_nir.tif"
    }
}INFO Final process status is success
✅ Tests passed
```

#### Test the `norm_diff` CWL command-line tool with: 

```
task test-norm-diff
```

The expected output is:

```
🚀 Running tests using engine cluster
tool path: cwl-workflow/app-water-bodies-cloud-native.cwl#norm_diff
Test Name: norm-diff-test
Description: Test case for norm_diff tool.
---------------------------
calrissian --stdout /calrissian/norm-diff/results.json --stderr /calrissian/norm-diff/app.log --max-ram 1G --max-cores "1" --tmp-outdir-prefix /calrissian/norm-diff/tmp/ --outdir /calrissian/norm-diff/results --usage-report /calrissian/norm-diff/usage.json --tool-logs-basepath /calrissian/norm-diff/logs --pod-serviceaccount calrissian-sa cwl-workflow/app-water-bodies-cloud-native.cwl#norm_diff params.yaml
INFO calrissian 0.18.1 (cwltool 3.1.20240708091337)
INFO Resolved 'cwl-workflow/app-water-bodies-cloud-native.cwl#norm_diff' to 'file:///workspace/advanced-tooling/cwl-workflow/app-water-bodies-cloud-native.cwl#norm_diff'
{
    "ndwi": {
        "location": "file:///calrissian/norm-diff/results/norm_diff.tif",
        "basename": "norm_diff.tif",
        "class": "File",
        "checksum": "sha1$ea91fcdd6f24b5105718011ca77810e4b6763c09",
        "size": 224808043,
        "path": "/calrissian/norm-diff/results/norm_diff.tif"
    }
}INFO Final process status is success
✅ Tests passed
```

#### Test the `ostu` CWL command-line tool with: 

```
task test-otsu
```

The expected output is:

```
🚀 Running tests using engine cluster
tool path: cwl-workflow/app-water-bodies-cloud-native.cwl#otsu
Test Name: otsu-test
Description: Test case for otsu tool.
---------------------------
calrissian --stdout /calrissian/otsu/results.json --stderr /calrissian/otsu/app.log --max-ram 1G --max-cores "1" --tmp-outdir-prefix /calrissian/otsu/tmp/ --outdir /calrissian/otsu/results --usage-report /calrissian/otsu/usage.json --tool-logs-basepath /calrissian/otsu/logs --pod-serviceaccount calrissian-sa cwl-workflow/app-water-bodies-cloud-native.cwl#otsu params.yaml
INFO calrissian 0.18.1 (cwltool 3.1.20240708091337)
INFO Resolved 'cwl-workflow/app-water-bodies-cloud-native.cwl#otsu' to 'file:///workspace/advanced-tooling/cwl-workflow/app-water-bodies-cloud-native.cwl#otsu'
{
    "binary_mask_item": {
        "location": "file:///calrissian/otsu/results/otsu.tif",
        "basename": "otsu.tif",
        "class": "File",
        "checksum": "sha1$8cb131413518c30be6ba485ea61764491444cde5",
        "size": 290099,
        "path": "/calrissian/otsu/results/otsu.tif"
    }
}INFO Final process status is success
✅ Tests passed
```

#### Test the `stac` CWL command-line tool with: 

```
task test-stac
```

The expected output is:

```
🚀 Running tests using engine cluster
tool path: cwl-workflow/app-water-bodies-cloud-native.cwl#stac
Test Name: stac-test
Description: Test case for stac tool.
---------------------------
calrissian --stdout /calrissian/stac/results.json --stderr /calrissian/stac/app.log --max-ram 1G --max-cores "1" --tmp-outdir-prefix /calrissian/stac/tmp/ --outdir /calrissian/stac/results --usage-report /calrissian/stac/usage.json --tool-logs-basepath /calrissian/stac/logs --pod-serviceaccount calrissian-sa cwl-workflow/app-water-bodies-cloud-native.cwl#stac params.yaml
INFO calrissian 0.18.1 (cwltool 3.1.20240708091337)
INFO Resolved 'cwl-workflow/app-water-bodies-cloud-native.cwl#stac' to 'file:///workspace/advanced-tooling/cwl-workflow/app-water-bodies-cloud-native.cwl#stac'
{
    "stac_catalog": {
        "location": "file:///calrissian/stac/results/jepvrswr",
        "basename": "jepvrswr",
        "class": "Directory",
        "listing": [
            {
                "class": "File",
                "location": "file:///calrissian/stac/results/jepvrswr/catalog.json",
                "basename": "catalog.json",
                "size": 363,
                "checksum": "sha1$70e96cddbb205363b4ee9cb763e438a29fd29cdc",
                "path": "/calrissian/stac/results/jepvrswr/catalog.json"
            },
            {
                "class": "Directory",
                "location": "file:///calrissian/stac/results/jepvrswr/S2B_10TFK_20210713_0_L2A",
                "basename": "S2B_10TFK_20210713_0_L2A",
                "listing": [
                    {
                        "class": "File",
                        "location": "file:///calrissian/stac/results/jepvrswr/S2B_10TFK_20210713_0_L2A/S2B_10TFK_20210713_0_L2A.json",
                        "basename": "S2B_10TFK_20210713_0_L2A.json",
                        "size": 2766,
                        "checksum": "sha1$8aa28203970407bf716b0f12fdfa43606c3557d5",
                        "path": "/calrissian/stac/results/jepvrswr/S2B_10TFK_20210713_0_L2A/S2B_10TFK_20210713_0_L2A.json"
                    },
                    {
                        "class": "File",
                        "location": "file:///calrissian/stac/results/jepvrswr/S2B_10TFK_20210713_0_L2A/otsu.tif",
                        "basename": "otsu.tif",
                        "size": 290099,
                        "checksum": "sha1$8cb131413518c30be6ba485ea61764491444cde5",
                        "path": "/calrissian/stac/results/jepvrswr/S2B_10TFK_20210713_0_L2A/otsu.tif"
                    }
                ],
                "path": "/calrissian/stac/results/jepvrswr/S2B_10TFK_20210713_0_L2A"
            }
        ],
        "path": "/calrissian/stac/results/jepvrswr"
    }
}INFO Final process status is success
✅ Tests passed
```

### Test the CWL Workflow

```
task scenario-1
```

The expected output is:

```
🚀 Running tests using engine cluster
Workflow Path: cwl-workflow/app-water-bodies-cloud-native.cwl#water-bodies
Test Name: water-detection-test-1
Description: Test case 1 for water bodies detection.
---------------------------
calrissian --stdout /calrissian/water-bodies/results.json --stderr /calrissian/water-bodies/app.log --max-ram 4G --max-cores "8" --tmp-outdir-prefix /calrissian/water-bodies/tmp/ --outdir /calrissian/water-bodies/results --usage-report /calrissian/water-bodies/usage.json --tool-logs-basepath /calrissian/water-bodies/logs --pod-serviceaccount calrissian-sa cwl-workflow/app-water-bodies-cloud-native.cwl#water-bodies params.yaml
INFO calrissian 0.18.1 (cwltool 3.1.20240708091337)
INFO Resolved 'cwl-workflow/app-water-bodies-cloud-native.cwl#water-bodies' to 'file:///workspace/advanced-tooling/cwl-workflow/app-water-bodies-cloud-native.cwl#water-bodies'
INFO [workflow ] starting step node_water_bodies
INFO [step node_water_bodies] start
...
INFO [step node_stac] completed success
INFO [workflow ] completed success
{
    "stac_catalog": {
        "location": "file:///calrissian/water-bodies/results/2htowb6_",
        "basename": "2htowb6_",
        "class": "Directory",
        "listing": [
            {
                "class": "File",
                "location": "file:///calrissian/water-bodies/results/2htowb6_/catalog.json",
                "basename": "catalog.json",
                "size": 508,
                "checksum": "sha1$2496d410f1f58684d81b32f780bbb27536d2c13f",
                "path": "/calrissian/water-bodies/results/2htowb6_/catalog.json"
            },
            {
                "class": "Directory",
                "location": "file:///calrissian/water-bodies/results/2htowb6_/S2B_10TFK_20210713_0_L2A",
                "basename": "S2B_10TFK_20210713_0_L2A",
                "listing": [
                    {
                        "class": "File",
                        "location": "file:///calrissian/water-bodies/results/2htowb6_/S2B_10TFK_20210713_0_L2A/S2B_10TFK_20210713_0_L2A.json",
                        "basename": "S2B_10TFK_20210713_0_L2A.json",
                        "size": 2766,
                        "checksum": "sha1$8aa28203970407bf716b0f12fdfa43606c3557d5",
                        "path": "/calrissian/water-bodies/results/2htowb6_/S2B_10TFK_20210713_0_L2A/S2B_10TFK_20210713_0_L2A.json"
                    },
                    {
                        "class": "File",
                        "location": "file:///calrissian/water-bodies/results/2htowb6_/S2B_10TFK_20210713_0_L2A/otsu.tif",
                        "basename": "otsu.tif",
                        "size": 290099,
                        "checksum": "sha1$8cb131413518c30be6ba485ea61764491444cde5",
                        "path": "/calrissian/water-bodies/results/2htowb6_/S2B_10TFK_20210713_0_L2A/otsu.tif"
                    }
                ],
                "path": "/calrissian/water-bodies/results/2htowb6_/S2B_10TFK_20210713_0_L2A"
            },
            {
                "class": "Directory",
                "location": "file:///calrissian/water-bodies/results/2htowb6_/S2A_10TFK_20220524_0_L2A",
                "basename": "S2A_10TFK_20220524_0_L2A",
                "listing": [
                    {
                        "class": "File",
                        "location": "file:///calrissian/water-bodies/results/2htowb6_/S2A_10TFK_20220524_0_L2A/S2A_10TFK_20220524_0_L2A.json",
                        "basename": "S2A_10TFK_20220524_0_L2A.json",
                        "size": 2766,
                        "checksum": "sha1$e75de787df90f3d1fe026e2164567eb92432e10d",
                        "path": "/calrissian/water-bodies/results/2htowb6_/S2A_10TFK_20220524_0_L2A/S2A_10TFK_20220524_0_L2A.json"
                    },
                    {
                        "class": "File",
                        "location": "file:///calrissian/water-bodies/results/2htowb6_/S2A_10TFK_20220524_0_L2A/otsu.tif",
                        "basename": "otsu.tif",
                        "size": 371699,
                        "checksum": "sha1$8a97a5260b1039d7f867c2f9ab8ee36a5cb5fbd4",
                        "path": "/calrissian/water-bodies/results/2htowb6_/S2A_10TFK_20220524_0_L2A/otsu.tif"
                    }
                ],
                "path": "/calrissian/water-bodies/results/2htowb6_/S2A_10TFK_20220524_0_L2A"
            }
        ],
        "path": "/calrissian/water-bodies/results/2htowb6_"
    }
}INFO Final process status is success
✅ Tests passed
```


## For developers

You can debug the tasks with e.g.:

```
task -t task-files/Taskfile.yaml -d . prepare build update
```

```
task -t task-files/Taskfile.yaml -d . test-tool VAR=crop
```

## Documentation

| Feature           | How It Works                                   |
|------------------|-----------------------------------------------|
| Execution Tool   | Uses `calrissian` inside Kubernetes            |
| Where It Runs    | Inside a Kubernetes pod                      |
| Storage Access   | Uses Kubernetes PVC (`/calrissian`)            |
| Resource Limits  | Uses `max_ram` and `max_cores`                   |
| Service Account  | Uses `calrissian-sa` for authentication        |
| Logging         | Uses kubectl logs or calrissian log paths     |
| Use Case        | Large-scale execution, parallelized workloads |


| Step | Description |
|------|--------------------------------------------------------------|
| 1️⃣ | Selects calrissian as the engine - The test runs inside a Kubernetes pod. |
| 2️⃣ | Uses Kubernetes PVC for Storage - Workflow runs in /calrissian, outputs are stored there. |
| 3️⃣ | Uses Resource Limits (max_ram, max_cores) - Ensures proper resource allocation in the cluster. |
| 4️⃣ | Runs Workflows Inside a Pod - Uses a Pod with a ServiceAccount for execution. |
| 5️⃣ | Extracts Logs from Kubernetes - kubectl logs or Calrissian's tool_logs_basepath provides logs. |


## Explanation of project.toml and Its Usage in Taskfile


The `project.toml` defines configurations for **building, testing, and executing CWL tools and workflows**, supporting both **local and in-cluster** execution. The **Taskfile** automates build and test execution based on the `project.toml` configuration.

###  Understanding project.toml Structure

This TOML file is divided into sections:

* Project Metadata (`[project]`)
* Build Configuration (`[build]`)
* Tool Definitions (`[tools]`)
* Workflow Definitions (`[[workflows]]`)

Each tool and workflow includes test cases with parameters and execution settings.

#### [project] - Project Metadata

```toml
[project]
name = "my-cwl-project"
version = "1.0.0"
```

Defines the project’s name and version for identification.

#### [build] - Build Configuration

```toml
[build]
engine = "cluster"
```

Determines where the build runs:

* `"local"` → Uses Docker/Podman
* `"cluster"` → Uses Skaffold + Kaniko in Kubernetes

#### [build.local] - Local Build Settings

```toml
[build.local]
runtime = "docker"
registry = "ghcr.io/eoap"
```

* Specifies container runtime (`docker` or `podman`).
* Uses registry for storing images when pushing.

#### [build.cluster] - In-Cluster Build Settings

```toml
[build.cluster]
namespace = "eoap-advanced-tooling"
serviceAccount = "kaniko-sa"
registry = "ghcr.io/eoap"
secret = "kaniko-secret"
```

* Defines the Kubernetes namespace and service account for kaniko builds.
* Uses a registry and secret for authentication.

#### CWL CommandLineTools: [tools] Section

Each CWL tool has:

* A directory containing the tool code (`context`)
* A CWL workflow file with the tool's entry point (`path`)
* Test cases (tests)

Example: Crop Tool

```toml
[tools.crop]
context = "command-line-tools/crop"
path = "cwl-workflow/app-water-bodies-cloud-native.cwl#crop"
```

* Defines the CWL tool
* Specifies its directory (`context`) and CWL workflow path (`path`)


#### Tool Test Cases: [[tools.<tool>.tests]]

Each tool has one or more test cases, specifying:

* Test input parameters
* Execution settings
* Storage paths

Example: Crop Tool (Green Band Test)

```toml
[[tools.crop.tests]]
name = "crop-test-green"
description = "Test case 1 for crop tool - green band."
```

Defines a test case for the tool.

#### [tools.<tool>.tests.params] - Test Parameters

```toml
[tools.crop.tests.params]
item = "https://earth-search.aws.element84.com/.../S2B_10TFK_20210713_0_L2A"
aoi = "-121.399,39.834,-120.74,40.472"
epsg = "EPSG:4326"
band = "green"
```

Defines input parameters for the test.

#### [tools.<tool>.tests.execution.cluster] - In-Cluster Execution Settings

```toml
[tools.crop.tests.execution.cluster]
max_ram = "1G"
max_cores = 1
pod_serviceaccount = "calrissian-sa"
usage_report = "usage.json"
tool_logs_basepath = "logs"
```

* Specifies CPU & memory limits for Kubernetes.
* Uses a Kubernetes service account (`calrissian-sa`) for execution.

#### [tools.<tool>.tests.execution.paths] - File Storage Paths

```toml
[tools.crop.tests.execution.paths]
stdout = "results.json"
stderr = "app.log"
tmp_outdir_prefix = "tmp"
outdir = "results"
volume = "/calrissian/crop-green"
```

Defines where outputs and logs are stored.


#### Workflows: [[workflows]] Section

Workflows combine multiple tools into a complete processing pipeline.

Example: Water Bodies Detection Workflow

```toml
[[workflows]]
path = "cwl-workflow/app-water-bodies-cloud-native.cwl#water-bodies"
```

Defines the CWL workflow and entry point.

#### Workflow Test Cases: [[workflows.tests]]

Each workflow has test cases similar to tools.

```toml
[[workflows.tests]]
name = "water-detection-test-1"
description = "Test case 1 for water bodies detection."
```

Defines a test case for the workflow.

#### [workflows.tests.params] - Test Inputs

```toml
[workflows.tests.params]
stac_items = ["https://earth-search.aws.element84.com/..."]
aoi = "-121.399,39.834,-120.74,40.472"
epsg = "EPSG:4326"
```

Defines input STAC items for processing.

### How project.toml is Used in Taskfile.yaml

The Taskfile automates:

* Building images
* Updating CWL workflows
* Running tests locally or in Kubernetes

#### Building Images: build Task

* Cluster Build (`Skaffold` + `Kaniko`)

```yaml
tasks:
  build-cluster:
    silent: true
    cmds:
    - task: prepare-kaniko
    - task: build-kaniko
```

* Runs Skaffold & Kaniko only if `build.engine = cluster`.
* Generates `skaffold-auto.yaml` dynamically from `project.toml`.

#### Local Build (Docker/Podman)

```yaml
tasks:
  build-local:
    silent: true
    cmds:
      - |
        engine=$(tomlq -r '.build.engine' project.toml)
        if [ "$engine" != "local" ]; then exit 0; fi

        runtime=$(tomlq -r '.build.local.runtime' project.toml)
        registry=$(tomlq -r '.build.local.registry' project.toml)

        for tool in $(tomlq -r '.tools | keys[]' project.toml); do
            path=$(tomlq -r ".tools.$tool.context" project.toml)
            eval $runtime build -t $registry/$tool $path
        done
```

Reads `project.toml` to build tools using Docker/Podman.

#### Running Tests: test Task

Runs Tests for Each Workflow

```yaml
tasks:
  test:
    silent: true
    cmds:
      - |
        engine=$(tomlq -r '.build.engine' project.toml)
        tomlq -c '.workflows[]' project.toml | while read -r workflow; do
          path=$(tomlq -r ".workflows[$i].path" project.toml)

          if [ "$engine" = "cluster" ]; then
            cmd="calrissian --stdout ... --stderr ... ${path} params.yaml"
          elif [ "$engine" = "local" ]; then
            cmd="cwltool --tmp-outdir-prefix ... ${path} params.yaml"
          fi

          eval $cmd
        done
```

* Uses Calrissian in Kubernetes or CWLTool locally.
* Runs each workflow test dynamically.

## Project Taskfile

The Taskfile imports a remote Taskfile from https://github.com/eoap/task-files/tree/main/build-test and simply combines remote tasks

```yaml
version: '3'

includes:
  remote: https://raw.githubusercontent.com/eoap/task-files/c750354651eed547cc310aa7a856921e77ebc058/build-test/Taskfile.yaml

tasks:
  build:
  - task: remote:build

  prepare:
  - task: remote:prepare

  test:
  - task: remote:test

  test-all:
    cmds: 
    - task: test-crop
    - task: test-norm-diff
    - task: test-otsu
    - task: test-stac

  test-crop:
    cmds:
    - task: remote:test-tool
      vars:
        VAR: "crop"

  test-norm-diff:
    cmds:
    - task: remote:test-tool
      vars:
        VAR: "norm_diff"

  test-otsu:
    cmds:
    - task: remote:test-tool
      vars:
        VAR: "otsu" 

  test-stac:
    cmds:
    - task: remote:test-tool
      vars:
        VAR: "stac"
```

## Cluster configuration

Create an image pull secret:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: kaniko-secret
data:
  .dockerconfigjson: >-
    eyJh..ViJ9fX0=
type: kubernetes.io/dockerconfigjson
```

Create a ServiceAccount and mount the image pull secret:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: kaniko-sa
imagePullSecrets:
  - name: kaniko-secret
```

Create a Role with:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: kaniko-role
rules:
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["create", "get", "list", "watch", "delete"]
  - apiGroups: [""]
    resources: ["pods/exec"]
    verbs: ["create"]
  - apiGroups: [""]
    resources: ["pods/log"]
    verbs: ["get","list"]
```

And the RoleBinding to associate the Role to the ServiceAccount:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: kaniko-rolebinding
subjects:
  - kind: ServiceAccount
    name: kaniko-sa
roleRef:
  kind: Role
  name: kaniko-role
  apiGroup: rbac.authorization.k8s.io
```