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
@click.option("--org", help="Organization name", required=True)
@click.option("--token", help="Terraform cloud token, can be specified by TF_CLOUD_TOKEN", default=None)
@click.pass_context
def root(ctx, org, token):
    if token:
        tf_token=token
    elif os.environ.get('TF_CLOUD_TOKEN'):
        tf_token=os.environ['TF_CLOUD_TOKEN']

    if not tf_token:
        click.echo("Terraform cloud token is not found")

    ctx.ensure_object(dict)
    ctx.obj['TF_CLASS'] = tf(org=org, tf_cloud_token=token)

@root.command()
@click.pass_context
def list_varsets(ctx):
    tf = ctx.obj['TF_CLASS']
    result = tf.list_varsets()
    click.echo(result)

@root.command()
@click.pass_context
def create_varsets(ctx):
    tf = ctx.obj['TF_CLASS']
    result = tf.list_varsets()
    click.echo(result)

@root.command()
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

@root.command()
@click.option("--org", help="Organization name", required=True)
@click.option("--cloud", help="Cloud in clouds_config.yaml to create varsets", required=True)
def create_varsets(org, cloud):
    variable_sets = yaml.load(open("clouds_config.yaml"), Loader=yaml.FullLoader)
    k=tf.create_variable_sets(
            org=org,
            tf_cloud_token=os.environ['TF_CLOUD_TOKEN'],
            vars_set=variable_sets["clouds"][cloud]
        )

@root.command()
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
    root()
