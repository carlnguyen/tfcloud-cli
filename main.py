from terraform_cloud_api import TerraformCloudApi as tf
import os
import yaml
import click

###
# After manually connect to a VCS provider, please check in your cloud for detail
vcs_providers= {
        'example': {
                "identifier": "",
                "oauth_token_id": ""
            }
    }

@click.group()
def cli():
    pass

@cli.command()
@click.option("--org", help="Organization name", required=True)
@click.option("--working_dir", help="Working directory in the repository", required=True)
@click.option("--branch", help="Branch to watch in the repository", required=True)
@click.option("--name", help="Workspace name", required=True)
def create_workspace(org, name, branch, working_dir):
    k=tf.create_workspace(
            org=org,
            vcs_oauth_token_id=vcs_providers['devops']['oauth_token_id'],
            vcs_identifier = vcs_providers['devops']['identifier'],
            tf_cloud_token=os.environ['TF_CLOUD_TOKEN'],
            working_directory=working_dir,
            branch_to_watch=branch,
            workspace_name=name
        )

@cli.command()
@click.option("--org", help="Organization name", required=True)
@click.option("--cloud", help="Cloud in clouds_config.yaml to create varsets", required=True)
def create_varsets(org, cloud):
    variable_sets = yaml.load(open("clouds_config.yaml"), Loader=yaml.FullLoader)
    k=tf.create_variable_sets(
            org=org,
            tf_cloud_token=os.environ['TF_CLOUD_TOKEN'],
            vars_set=variable_sets["clouds"][cloud]
        )

@cli.command()
@click.option("--cloud", help="Cloud in clouds_config.yaml to create varsets", required=True)
@click.option("--org", help="Organization name", required=True)
def update_varset_workspaces(org, cloud):
    variable_sets = yaml.load(open("clouds_config.yaml"), Loader=yaml.FullLoader)
    t = tf()
    k=t.update_varset_workspaces(
            org=org,
            tf_cloud_token=os.environ['TF_CLOUD_TOKEN'],
            vars_set=variable_sets["clouds"][cloud]
        )


if __name__ == '__main__':
    cli()
