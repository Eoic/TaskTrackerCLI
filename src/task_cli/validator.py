def is_valid_description(value: str):
    return type(value) is str and len(value) <= 255


def is_valid_status(value: str):
    from task_cli.model import Status

    return value in Status.__members__
