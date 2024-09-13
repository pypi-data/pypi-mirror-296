import rich_click as click
import api 
import sys

sys.path.append('../cli')

import api.project_api
import cli.ui as ui
from cli.config import Config
from cli.logger import Logger

DEMO_CLIENT_ID = 17
DEMO_CLIENT_NAME = 'demo'
DEMO_CLIENT_USER = 'demo@ackee.xyz'

@click.command("init")
@click.pass_context
def init(ctx):
    logger: Logger = ctx.obj['logger']
    config: Config = ctx.obj['config']

    click.echo(ui.title('Wake Arena API key'))
    click.echo(ui.help('The API key is needed to authorize the demo version of the CLI for the Wake Arena'))
    api_key = click.prompt('Enter the api key', type=str)

    config.add_client(
        name=DEMO_CLIENT_NAME, 
        user=DEMO_CLIENT_USER, 
        client_id=DEMO_CLIENT_ID, 
        token=api_key
    )
    
    config.set_active_client(DEMO_CLIENT_NAME)

    click.echo(ui.title('Project Name'))
    click.echo(ui.help('Give your project a name so you can recognize it better later'))
    project_name = click.prompt('Enter the project name', type=str, default='test-demo')

    project_api = api.ProjectApi(logger, client_id=DEMO_CLIENT_ID, token=api_key)
    res = project_api.create_project(project_name)

    config.set_active_project(res['id']).write()

    click.echo(ui.success('###'))
    click.echo(ui.success('# Successfully initialized!'))
    click.echo(ui.success('###'))
    click.echo('Current project set to ' + ui.command(res['name']) + f' ({res['id']})')
    click.echo('Now you can go to your code folder and use ' + ui.command('check') + ' command')