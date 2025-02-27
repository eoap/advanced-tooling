# eoap-taskfile

Experiments for a lean process

## Task 

Enable the remote files experimental feature:

```
export TASK_X_REMOTE_TASKFILES=1
```

## Requirements

- yq
- tomlq
- skaffold
- task 

## For developers

You can debug the tasks with e.g.:

```
task -t task-files/Taskfile.yaml -d . prepare build update
```

```
task -t task-files/Taskfile.yaml -d . test-tool VAR=crop
```

## TODOs

- add cwl workflow update of requirements - DONE
- add [[workflows]] in toml - DONE
- check if the role get secrets is needed or only a service account that mounts the image pull secret
- check service account role for pod/exec

## Executing the Application Package

Run the updated CWL description
```
calrissian \
    --stdout /calrissian/results.json \
    --stderr /calrissian/app.log \
    --max-ram 4G \
    --max-cores "8" \
    --tmp-outdir-prefix /calrissian/tmp \
    --outdir /calrissian/results \
    --usage-report /calrissian/usage.json \
    --tool-logs-basepath /calrissian/logs \
    --pod-serviceaccount calrissian-sa \
    cwl-workflow/app-water-bodies-cloud-native.cwl#water-bodies \
    params.yml
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
registry = "cr.terradue.com/earthquake-monitoring"
```

* Specifies container runtime (`docker` or `podman`).
* Uses registry for storing images when pushing.

#### [build.cluster] - In-Cluster Build Settings

```toml
[build.cluster]
namespace = "eoap-advanced-tooling"
serviceAccount = "kaniko-sa"
registry = "cr.terradue.com/earthquake-monitoring"
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