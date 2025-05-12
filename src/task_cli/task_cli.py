from task_cli.cli import create_parser, process_command
from task_cli.database import init_db


def main():
    init_db()
    parser = create_parser()
    args = parser.parse_args()
    process_command(args)


if __name__ == "__main__":
    main()
