# eoap-taskfile
Experiments for a lean process


## TODOs

- check if the role get secrets is needed or only a service account that mounts the image pull secret



tomlq -r '.tools | keys[]' project.toml


# pipe a config 
cat skaffold.yaml | skaffold build -f -


See remote tasks in https://taskfile.dev/experiments/remote-taskfiles/