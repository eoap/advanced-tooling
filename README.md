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
