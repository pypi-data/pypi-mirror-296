import click
from athenaeum.render import Render

render = Render()


@click.command()
@click.argument('project_name')
def render_project(project_name: str) -> None:
    """
    使用命令：
    <poetry run> render_project example

    :param project_name:
    :return:
    """
    try:
        click.echo(f'渲染开始')
        render.render_project(project_name=project_name)
    except Exception as exception:
        click.echo(f'渲染出错了，exception：`{exception}`！')
    finally:
        click.echo(f'渲染结束')
