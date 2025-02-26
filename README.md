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