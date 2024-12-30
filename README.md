[![][black-shield]][black]

[black]: https://roadmap.sh/projects/task-tracker
[black-shield]: https://img.shields.io/badge/Roadmap.sh-task%20tracker-black.svg?style=for-the-badge&labelColor=gray

# Task Tracker
A simple CLI-based tool for managing TODOs.

## Building
1. `py -m pip install --upgrade build`
2. `py -m build`

## Installing
`pip install .`

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
