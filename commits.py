import os
import json
from datetime import datetime, timedelta, timezone
import logging
import pprint

import dotenv
from github import Github, Auth

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

pp = pprint.PrettyPrinter(indent=4)

dotenv.load_dotenv()

access = os.getenv("GITHUB_ACCESS")
user_name = os.getenv("GITHUB_USER")


auth = Auth.Token(access)


g = Github(auth=auth)


def main():
    yesterday = datetime.now(timezone.utc) - timedelta(days=7)

    user = g.get_user(user_name)

    events = user.get_events()

    repository_data = {}

    for event in events:
        logger.info(f"event: {event.type}")

        if event.created_at < yesterday:
            continue

        if event.type == "PushEvent":
            repository_data = parse_push_event(event, repository_data)

    printing(repository_data)

    save_local(repository_data)

    finalize()


def parse_push_event(event, repository_data):
    repository_id = event.payload["repository_id"]
    logger.info(f"repository_id: {repository_id}")

    commits = get_commits(event)
    logger.info(f"commits: {commits}")

    if repository_id not in repository_data:
        repository_data[repository_id] = {
            "repo": event.repo.name,
            "commits": commits,
        }
    else:
        repository_data[repository_id]["commits"].extend(commits)

    return repository_data


def get_commits(event):
    commit_list = []

    commits = event.payload["commits"]
    for commit in commits:
        commit_list.append(commit["message"])

    return commit_list


def printing(repository_data):
    for _, data in repository_data.items():
        commits = data["commits"]

        print(f"🚀 : {data['repo']}")
        for commit in commits:
            print(f"🚀 : {commit}")
        print("\n")


def save_local(repository_data):
    with open("local/commits.json", "w") as f:
        json.dump(repository_data, f, ensure_ascii=False)


def finalize():
    g.close()


if __name__ == "__main__":
    main()
