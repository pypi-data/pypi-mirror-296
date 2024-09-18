import click
import subprocess
from cli.utils.helm import Helm
from cli.utils.cli_utils import CliUtils
import sys
# Helper function to run Helm commands

def run_helm_command(args):
    result = subprocess.run(['helm'] + args, capture_output=True, text=True)
    if result.returncode != 0:
        click.echo(result.stderr.strip(),err=True)
        sys.exit(1)
    click.echo(result.stdout.strip())
    sys.exit(result.returncode)

@click.command(context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True,
))
@click.option('--help','-h', is_flag=True, help="Show this message and exit.")
@click.argument('helm_args', nargs=-1, type=click.UNPROCESSED)
def cli(help, helm_args):
    """Delegate commands to Helm"""
    cli_utils=CliUtils()
    namespace= None
    context=None
    for idx,value in enumerate(helm_args):
        if "--namespace" in value or "-n" in value:
            if "--namespace=" in value:
                namespace=helm_args[idx].split("=")[1]
            elif "-n" == value:
                namespace=helm_args[idx+1]
            elif "--namespace" in value:
                namespace=helm_args[idx+1]
        if "--kube-context" in value:
            if "--kube-context=" in value:
                context=helm_args[idx].split("=")[1]
            elif "--kube-context" in value:
                context=helm_args[idx+1]
    helm=Helm(context=context,namespace=namespace)



    no_validation= "--no-validation" in helm_args
    force = "--force" in helm_args
    if "diff" in helm_args:
        release_name,chart_path=cli_utils.get_release_name_and_chart(helm_args)
        values=cli_utils.extract_files(helm_args)
        if help:
            if cli_utils.return_help(helm_args): 
                return click.echo(cli_utils.return_help(helm_args))
            return run_helm_command(args=list(helm_args)+["--help"])
        elif "upgrade" in helm_args:
            no_validation and click.echo("Skipping validation for test helm branch")
            no_validation or click.echo("Validating charts...")
            validation=no_validation or helm.validate_chart(chart_path)
            if validation is not True:
                return click.echo(validation)
            output,status_code=helm.diff(release_name,chart_path,values)
            if status_code!=0:
                return click.echo(output.strip(),err=True)
            click.echo(output)
        elif "revision" in helm_args:
            old_revision=helm_args[3] if len(helm_args)>3 else ""
            new_revision=helm_args[4] if len(helm_args)>4 else ""
            output=helm.diff_revison(release_name=release_name,old_revision=old_revision,new_revision=new_revision)
            click.echo(output)

        else:
            run_helm_command(list(helm_args))
    elif "upgrade" in helm_args:
        release_name,chart_path=cli_utils.get_release_name_and_chart(helm_args)
        if help:
            return click.echo(cli_utils.help_upgrade())
        else:
            values=cli_utils.extract_files(helm_args)
            no_validation or force or click.echo("Validating Chart...")
            validation=no_validation or force or helm.validate_chart(chart_path)
            no_validation and click.echo("Skipping validation for test helm branch")
            if no_validation and force==False: proceed=input("You are about to upgrade a release with no validations. Do you want to proceed? (yes/no): ")
            if no_validation and proceed.lower() != "yes":
                return click.echo("Aborting")
            if  validation is not True:
                return click.echo(validation)
            output=helm.diff(release_name,chart_path,values)
            click.echo(output)
            prompt= force or input("enter Yes to perform the upgrade: ")
            if force or prompt.lower() == "yes":
                return run_helm_command(args=list(helm_args))
    elif help:
        return run_helm_command(list(helm_args)+['--help'])

    else:
        return run_helm_command(list(helm_args))

if __name__ == '__main__':
    cli()