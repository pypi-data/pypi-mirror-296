import click

@click.command()
@click.option("-u", "--pms-user", default=None, type=click.STRING, help="")
@click.option("-p", "--pms-password", default=None, type=click.STRING, help="")
@click.option("-t", "--task-id", default=None, type=click.STRING, help="")
@click.option("-s", "--suite-id", default=None, type=click.STRING, help="")
@click.option("-sp", "--send2pms", default=None, type=click.STRING, help="")
def cli(
        pms_user,
        pms_password,
        task_id,
        suite_id,
        send2pms,
):
    if task_id:
        from pms_driver.task import Task
        Task(pms_user, pms_password).write_case_data(task_id)
    elif suite_id:
        from pms_driver.suite import Suite
        Suite(pms_user, pms_password).write_case_data(suite_id)
    if send2pms:
        from pms_driver.send2pms import Send2Pms
        Send2Pms(pms_user, pms_password, task_id, suite_id).send()


if __name__ == "__main__":
    cli()
