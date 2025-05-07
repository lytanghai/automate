import requests
import json
from requests.auth import HTTPBasicAuth

from util.config import save_cache


def get_default_reviewer(username, password, write_log):
    default_reviewers = []
    url = f"https://api.bitbucket.org/2.0/repositories/wingdev/resilience-sample/default-reviewers"
    response = requests.get(url, auth=HTTPBasicAuth(username, password))
    write_log("calling to fetch default reviewers...")

    if response.status_code == 200:
        response_data = response.json()
        
        for value in response_data.get('values', []):
            display_name = value.get("display_name", "No Display Name")
            default_reviewers.append(display_name)

    save_cache("default_reviewers", default_reviewers)
    write_log("save cache for default reviewer")
    return default_reviewers

def get_repository(workspace, username, password):
    url = f"https://api.bitbucket.org/2.0/repositories/{workspace}"
    print(f"calling to fetch repository under workspace: {url}")
    response = requests.get(url, auth=HTTPBasicAuth(username, password))
    
    if response.status_code == 200:
        data = response.json()
        repository_names = [repo['name'].lower().replace(" ", "-") for repo in data['values']]
        save_cache("repository_name", repository_names)
        return repository_names
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return []

def get_pr_detail(workspace, repo_slug, status, size, username, password, write_log):
    url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_slug}/pullrequests?pagelen={size}&state={status}"
    response = requests.get(url, auth=HTTPBasicAuth(username, password))
    write_log("fetch pull request detail...")
    if response.status_code == 200:
        return response.json()
    else:
        write_log(f"Failed to retrieve data. Status code: {response.status_code}")
        return []

def check_enforce_rule(id, default_reviewers, report_slug, username, password, write_log, total_approvals, total_default_reviewer_approvals):
    result = False
    default_approvals = 0
    total_approvals = 0

    url = f"https://api.bitbucket.org/2.0/repositories/wingdev/{report_slug}/pullrequests/{id}"
    response = requests.get(url, auth=HTTPBasicAuth(username, password))
    write_log(f"📡 Calling to fetch pull request detail by ID: {url}")

    if response.status_code == 200:
        data = response.json()
        participants = data.get("participants", [])

        for participant in participants:
            reviewer_name = participant["user"]["display_name"]
            is_approve = participant.get("approved", False)

            if is_approve:
                total_approvals += 1
                if reviewer_name in default_reviewers:
                    default_approvals += 1
                    write_log(f"✅ Default reviewer '{reviewer_name}' approved the PR.")
                else:
                    write_log(f"✅ Non-default reviewer '{reviewer_name}' approved the PR.")

        if total_approvals >= total_approvals and default_approvals >= total_default_reviewer_approvals:
            result = True
        else:
            write_log(f"⚠️ Enforcement rule not met: {total_approvals} approvals "
                      f"({default_approvals} from default reviewers).")
    else:
        write_log(f"❌ Failed to retrieve PR data. Status code: {response.status_code}")

    return result, total_approvals, default_approvals
