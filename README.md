# Python command to interact with Terraform Cloud

## Prequesites
```
pip install -r requirements.txt
```

## How to use
-  Show all commands
```
python main.py --help
```

- To create a workspace
```
python create-workspace ----working_dir=projects/klen/clouds/inmotion --branch develop --name "testing-on-inmotion"
```

- To create a varset
  - Edit the clouds.config.yaml
  - Then run below command
    ```
    python main.py create-varsets --cloud inmotion
    ```

- To update varset's shared workspaces
  - Edit the clouds_config.yaml
  - Then run below command
    ```
    python main.py update-varset-workspaces --cloud inmotion
    ```
