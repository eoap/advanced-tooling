# eoap-taskfile


Experiments for a lean process

Enable the remote files experimental feature:

```
export TASK_X_REMOTE_TASKFILES=1
```

## TODOs

- add cwl workflow update of requirements
- add [[workflows]] in toml
- check if the role get secrets is needed or only a service account that mounts the image pull secret
- check service account role for pod/exec


tomlq -r '.tools | keys[]' project.toml


# pipe a config 

cat skaffold.yaml | skaffold build -f -
See remote tasks in https://taskfile.dev/experiments/remote-taskfiles/



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