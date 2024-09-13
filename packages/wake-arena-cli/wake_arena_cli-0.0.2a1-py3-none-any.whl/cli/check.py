import rich_click as click
import api 
import cli.ui as ui
from cli.config import Config
from cli.logger import Logger

DEMO_CLIENT_ID = 17
DEMO_CLIENT_NAME = 'demo'
DEMO_CLIENT_USER = 'demo@ackee.xyz'

@click.command("check")
@click.pass_context
def check(ctx):
    config: Config = ctx.obj['config']
    project_api: api.ProjectApi = ctx.obj['project_api']

    active_project = config.get_active_project()

    if not project_api:
        click.echo(ui.texts.error('Please use ') + ui.texts.command('init') + ui.texts.error(' command first'))
        return
    if not active_project:
        click.echo(ui.texts.error('Please use ') + ui.texts.command('init') + ui.texts.error(' command first'))
        return

    ## todo wake export
    ## todo zip folder

    res = project_api.get_upload_link(active_project)

    ## todo upload zip
    ## todo check for results in firestore

    click.echo(res)