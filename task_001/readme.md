# Task manager

## Ideas for future versions
- [ ] Add tests. Further continue through TDD.
- [ ] Make storage file name configurable. By default store at data/uncategorized.json
    - [ ] Make categories of tasks using different files and subfolders.
- [ ] Add subtasks.
- [ ] Add "archived" status of a task. "archived" tasks will not be shown in the default "list" command.
    - [ ] Add "list archived" command.
- [ ] Add creation timestamp.
    - [ ] Show user if a task is stale.
- [ ] Add deadline timestamp.
- [ ] Add status change history.
- [ ] Add task priority.
- [ ] Add adapters for different storage types. (Use docker where a local DB setup is needed)
    - [ ] CSV
    - [ ] SQLite
    - [ ] PostgreSQL
    - ...

## Version 0.1.1
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