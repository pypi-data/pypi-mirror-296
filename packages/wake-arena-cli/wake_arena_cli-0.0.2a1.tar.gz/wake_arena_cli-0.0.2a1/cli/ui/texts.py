import rich_click as click

def title(msg: str):
    return click.style(msg, fg='blue', bold=True)

def help(msg: str): 
    return click.style(msg, italic=True)

def success(msg: str):
    return click.style(msg, fg='green', bold=True)

def command(msg: str):
    return click.style(msg, fg='cyan', bold=True)

def error(msg: str):
    return click.style(msg, fg='red', bold=True)