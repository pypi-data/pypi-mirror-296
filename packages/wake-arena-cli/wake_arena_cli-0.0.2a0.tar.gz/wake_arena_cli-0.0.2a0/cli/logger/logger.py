import rich_click as click

class Logger:
    def error(self, msg):
        click.echo(click.style(msg, bg='black', fg='red', bold=True), err=True)
    def log(self, msg):
        click.echo(msg)