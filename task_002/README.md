# Github user activity

## Version 1 (cli)

The application should run from the command line, accept the GitHub username as an argument, fetch the user's recent activity using the GitHub API, and display it in the terminal. The user should be able to:
- [ ] Provide the GitHub username as an argument when running the CLI.
    ```sh
    ./github-activity <username>
    ```
- [x] Fetch the recent activity of the specified GitHub user using the GitHub API. You can use the following endpoint to fetch the user's activity: (https://api.github.com/users/<username>/events)
- [ ] Display the fetched activity in the terminal.
    ```sh
    Output:
    - Pushed 3 commits to kamranahmedse/developer-roadmap
    - Opened a new issue in kamranahmedse/developer-roadmap
    - Starred kamranahmedse/developer-roadmap
    - ...
    ```
- [ ] Handle errors gracefully, such as invalid usernames or API failures.
- [x] Do not use any external libraries or frameworks to fetch the GitHub activity.

If you are looking to build a more advanced version of this project, you can consider adding features like filtering the activity by event type, displaying the activity in a more structured format, or caching the fetched data to improve performance. You can also explore other endpoints of the GitHub API to fetch additional information about the user or their repositories.

Source of the project idea https://roadmap.sh/projects/github-user-activity