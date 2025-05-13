[![][black-shield]][black]

[black]: https://roadmap.sh/projects/task-tracker
[black-shield]: https://img.shields.io/badge/Roadmap.sh-task%20tracker-black.svg?style=for-the-badge&labelColor=gray

# Task Tracker
A simple CLI-based tool for managing TODOs.

## Installing
`pip install -e .`

## Usage
* The program accepts only positional arguments like this: `task-cli <command> <arg1> <arg2> [argn]`
* Use `task-cli -h` to show available commands.

### Examples
```
task-cli add "Buy groceries"
task-cli update 1 "Buy groceries and cook dinner"
task-cli delete 1
task-cli mark-in-progress 1
task-cli mark-done 1
task-cli list
task-cli list done
task-cli list todo
task-cli list in-progress
```

### Development
Run tests and create HTML coverage report:
```
python -m coverage run -m unittest && python -m coverage html
```