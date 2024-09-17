import click
import subprocess
import json
import tempfile
import os
from convisoappsec.flowcli.context import pass_flow_context
from datetime import datetime
from convisoappsec.flowcli.requirements_verifier import RequirementsVerifier
from convisoappsec.flowcli import help_option
from convisoappsec.flowcli.common import (asset_id_option, project_code_option, on_http_error)
from convisoappsec.sast.sastbox import SASTBox


@click.command()
@project_code_option(required=False)
@asset_id_option(required=False)
@click.option(
    "-s",
    "--start-commit",
    required=False,
    help="If no value is set so the empty tree hash commit is used.",
)
@click.option(
    "-e",
    "--end-commit",
    required=False,
    help="""If no value is set so the HEAD commit
    from the current branch is used""",
)
@click.option(
    "-r",
    "--repository-dir",
    default=".",
    show_default=True,
    type=click.Path(
        exists=True,
        resolve_path=True,
    ),
    required=False,
    help="The source code repository directory.",
)
@click.option(
    "--fail-on-severity-threshold",
    required=False,
    help="If the threshold of the informed severity and higher has reach, then the command will fail after send the results to AppSec Flow.\n \
    The severity levels are: UNDEFINED, INFO, LOW, MEDIUM, HIGH, CRITICAL.",
    type=click.Tuple([str, int]),
    default=(None, None),
)
@click.option(
    "--fail-on-threshold",
    required=False,
    help="If the threshold has reach then the command will fail after send the result to AppSec Flow",
    type=int,
    default=False,
)
@click.option(
    "--send-to-flow/--no-send-to-flow",
    default=True,
    show_default=True,
    required=False,
    hidden=True,
    help="""Enable or disable the ability of send analysis result
    reports to flow. When --send-to-flow option is set the --project-code
    option is required""",
)
@click.option(
    "--deploy-id",
    default=None,
    required=False,
    hidden=True,
    envvar=("CONVISO_DEPLOY_ID", "FLOW_DEPLOY_ID")
)
@click.option(
    "--sastbox-registry",
    default="",
    required=False,
    hidden=True,
    envvar=("CONVISO_SASTBOX_REGISTRY", "FLOW_SASTBOX_REGISTRY"),
)
@click.option(
    "--sastbox-repository-name",
    default="",
    required=False,
    hidden=True,
    envvar=("CONVISO_SASTBOX_REPOSITORY_NAME", "FLOW_SASTBOX_REPOSITORY_NAME"),
)
@click.option(
    "--sastbox-tag",
    default=SASTBox.DEFAULT_TAG,
    required=False,
    hidden=True,
    envvar=("CONVISO_SASTBOX_TAG", "FLOW_SASTBOX_TAG"),
)
@click.option(
    "--sastbox-skip-login/--sastbox-no-skip-login",
    default=False,
    required=False,
    hidden=True,
    envvar=("CONVISO_SASTBOX_SKIP_LOGIN", "FLOW_SASTBOX_SKIP_LOGIN"),
)
@click.option(
    '--experimental',
    default=False,
    is_flag=True,
    hidden=True,
    help="Enable experimental features.",
)
@click.option(
    "--company-id",
    required=False,
    envvar=("CONVISO_COMPANY_ID", "FLOW_COMPANY_ID"),
    help="Company ID on Conviso Platform",
)
@click.option(
    '--asset-name',
    required=False,
    envvar=("CONVISO_ASSET_NAME", "FLOW_ASSET_NAME"),
    help="Provides a asset name.",
)
@click.option(
    '--vulnerability-auto-close',
    default=False,
    is_flag=True,
    hidden=True,
    help="Enable auto fixing vulnerabilities on cp.",
)
@click.option(
    '--from-ast',
    default=False,
    is_flag=True,
    hidden=True,
    help="Internal use only.",
)
@help_option
@pass_flow_context
@click.pass_context
def generate(context, flow_context, project_code, asset_id, company_id, end_commit, start_commit, repository_dir,
             send_to_flow, deploy_id, sastbox_registry, sastbox_repository_name, sastbox_tag, sastbox_skip_login,
             fail_on_threshold, fail_on_severity_threshold, experimental, asset_name, vulnerability_auto_close,
             from_ast):
    context.params['company_id'] = context.params.get('company_id') or company_id

    if not context.params['company_id']:
        log_func("Invalid company_id: {company_id}. Exiting.".format(company_id=company_id))
        return

    if not from_ast:
        prepared_context = RequirementsVerifier.prepare_context(context)

        params_to_copy = [
            'project_code', 'asset_id', 'start_commit', 'end_commit',
            'repository_dir', 'send_to_flow', 'deploy_id', 'sastbox_registry',
            'sastbox_repository_name', 'sastbox_tag', 'sastbox_skip_login',
            'experimental', 'asset_name', 'vulnerability_auto_close', 'company_id'
        ]

        for param_name in params_to_copy:
            context.params[param_name] = (
                    locals()[param_name] or prepared_context.params[param_name]
            )

    log_func("Generating SBOM file...")
    asset_name = context.params['asset_name']
    temp_dir = tempfile.gettempdir()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_name = os.path.join(temp_dir, "sbom_{asset_name}_{timestamp}.json".format(
        asset_name=asset_name, timestamp=timestamp
    ))

    command = [
        f"syft packages {repository_dir} -o syft-json={file_name}"
    ]

    try:
        subprocess.run(command, shell=True, check=True, capture_output=True)
        log_func(f"SBOM file generated successfully!")
    except subprocess.CalledProcessError as error:
        log_func("We have a problem when try to generate the sbom file ...{error}".format(error=error), color='red')
        return

    with open(file_name, 'r') as sbom_file:
        sbom_data = json.load(sbom_file)
        # TODO: here we already have the file, so we need to send to cp


def log_func(msg, new_line=True, color='blue'):
    click.echo(click.style(msg, bold=True, fg=color), nl=new_line, err=True)
