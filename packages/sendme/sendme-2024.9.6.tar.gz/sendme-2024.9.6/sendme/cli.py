import click

@click.option("--base-url", default="http://localhost:8000", type=click.STRING, help="Base URL")
@click.option("--username", default="", type=click.STRING, help="Username")
@click.option("--password", default="", type=click.STRING, help="Password")
@click.option("--custom-api", default="", type=click.STRING, help="Custom API")
@click.option("--task-id", default="", type=click.STRING, help="json报告回填所属任务id")
def cli(base_url, username, password, custom_api, task_id):
    from sendme.main import SendMe
    SendMe(base_url, username, password, custom_api).backfill(task_id)