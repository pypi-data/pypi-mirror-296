def get_user_action(event):
    action = "- "
    repo_name = event["repo"]["name"]

    match event["type"]:
        case "PushEvent":
            commit_count = len(event["payload"]["commits"])

            action += f"Pushed {commit_count} commit(s) to {repo_name}"

        case "WatchEvent":
            action += f"Started watching repository {repo_name}"

        case "PullRequestEvent":
            action += f"The user created a pull request in repository {repo_name}"

        case "PullRequestReviewCommentEvent":
            pr_title = event["payload"]["pull_request"]["title"]

            action += (
                f"Commented on the pull request '{pr_title}' in repository {repo_name}"
            )

        case "ForkEvent":
            repo_forked = event["payload"]["forkee"]["full_name"]

            action += f"Forked repository {repo_name} to {repo_forked}"

        case "IssueCommentEvent":
            action += f"Commented an issue in repo {repo_name}"

        case "IssuesEvent":
            action += f"Opened an issue in {repo_name}"

        case "CreateEvent":
            ref_type = event["payload"]["ref_type"]
            ref_name = event["payload"]["ref"]
            target_description = (
                f"'{repo_name}'"
                if ref_type == "repository"
                else f"'{ref_name}' in {repo_name}"
            )

            action += f"Created a new {ref_type} {target_description}"
        case "DeleteEvent":
            ref_type = event["payload"]["ref_type"]
            ref_name = event["payload"]["ref"]
            target_description = (
                f"'{repo_name}'"
                if ref_type == "repository"
                else f"'{ref_name}' in {repo_name}"
            )

            action += f"Deleted the {target_description}"

        case "ReleaseEvent":
            release_name = event["payload"]["release"]["tag_name"]

            action += f"Published a release {release_name} in {repo_name}"
        case "GollumEvent":
            pages = event["payload"]["pages"]

            action += f"Updated the wiki page {pages} in {repo_name}"

        case "PullRequestReviewEvent":
            pr_action = str.capitalize((event["payload"]["action"]))
            pr_title = event["payload"]["pull_request"]["title"]

            action += f"{pr_action} the pull request {pr_title} in {repo_name}"

        case _:
            action += "Unknown action"

    return action
