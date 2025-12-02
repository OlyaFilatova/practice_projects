# Task manager

This project is engineered to support different input/output solutions.

Currently it has two:
- cli
- PyQt6

To choose input/output solutions update following settings in the task_001/config.ini file.
```
input-type = pyqt
output-type = pyqt
```
supported values: pyqt, cli

## Running project with PyQt UI

Edit following settings in the task_001/config.ini file as here:
```
input-type = pyqt
output-type = pyqt
```

Then run
`./task_001/task-cli`

## Running project with CLI

Edit following settings in the task_001/config.ini file as here:
```
input-type = cli
output-type = cli
```

### Examples of use

```sh
# Adding a new task
./task_001/task-cli add "Buy groceries"
# Output: Task added successfully (ID: 1)
# Updating and deleting tasks
./task_001/task-cli update 1 "Buy groceries and cook dinner"
./task_001/task-cli delete 1
# Marking a task as in progress or done
./task_001/task-cli mark-in-progress 1
./task_001/task-cli mark-done 1
# Listing all tasks
./task_001/task-cli list
# Listing tasks by status
./task_001/task-cli list --status done
./task_001/task-cli list --status todo
./task_001/task-cli list --status in-progress
```

More about requirements for the first version at https://roadmap.sh/projects/task-tracker

## Ideas for future versions
- [ ] Add UI adapters (REST API, WebSockets, etc.)
- [ ] Add subtasks.
- [ ] Add task priority.
- [ ] Make categories of tasks using different files and subfolders.
- [ ] Add "archived" status of a task. "archived" tasks will not be shown in the default "list" command.
    - [ ] Add "list archived" command.
- [ ] Show user if a task is stale.
- [ ] Add deadline timestamp.
- [ ] Add status change history.
- [ ] Add adapters for different storage types. (Use docker where a local DB setup is needed)
    - [ ] CSV
    - [ ] SQLite
    - [ ] PostgreSQL
    - ...
- [ ] Add tests.
- [ ] Integrate LLM to add ability to request suggestions for the task execution.

## Version 0.4.0
- [x] Changed JSON structure to have ids based on counter.
- [ ] (in progress) Add PyQT UI adapter

## Version 0.3.0
- [x] Support asynchronous logic
- [x] Make storage file name configurable. By default store at data/uncategorized.json
    
## Version 0.2.0
- [x] Restructure code to make storage type configurable.
    - [x] Add storage adapter for json
    - [x] Add storage adapter for in-memory
- [x] Restructure code to make output type configurable.
    - [x] Add UI adapter for cli
- [x] Restructure code to make input type configurable.
    - [x] Add UI adapter for cli

## Version 0.1.2
The user should be able to:
- [x] Add, Update, and Delete tasks
- [x] Mark a task as in progress or done
- [x] List all tasks
- [x] List all tasks that are done
- [x] List all tasks that are planned
- [x] List all tasks that are in progress

Here are some constraints to guide the implementation:
- [x] Use positional arguments in command line to accept user inputs.
- [x] Use a JSON file to store the tasks in the current directory.
- [x] The JSON file should be created if it does not exist.
- [x] Use the native file system module of your programming language to interact with the JSON file.
- [x] Do not use any external libraries or frameworks to build this project.
- [x] Ensure to handle errors and edge cases gracefully.
