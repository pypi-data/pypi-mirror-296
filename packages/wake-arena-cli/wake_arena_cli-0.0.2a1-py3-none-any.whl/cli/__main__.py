import rich_click as click
from click.core import Context

from api.project_api import ProjectApi
from cli.config import Config
from cli.init import init as init_command
from cli.check import check as check_command
from cli.logger import Logger

@click.group()
@click.pass_context
def main(ctx):
    ctx.ensure_object(dict)
    logger=Logger()
    config = Config()
    client = config.get_active_client()

    ctx.obj['logger'] = logger
    ctx.obj['config'] = config
    if client:
        ctx.obj['project_api'] = ProjectApi(logger=logger, client_id=client['client_id'], token=client['token']) 
    else:
        ctx.obj['project_api'] = None
    pass

main.add_command(init_command)
main.add_command(check_command)

if __name__ == '__main__':
    main()