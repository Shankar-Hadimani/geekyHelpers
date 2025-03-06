import requests
import argparse
import os

def toggle_repo_visibility(github_token, username):
    """
    Toggle the visibility of all repositories:
    - If a repo is public, make it private.
    - If a repo is private, make it public.
    """
    # GitHub API URL for user's repositories
    github_api_url = f"https://api.github.com/user/repos"
    # Headers for authentication
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Get all repositories for the authenticated user
    response = requests.get(github_api_url, headers=headers)

    if response.status_code == 200:
        repos = response.json()
        for repo in repos:
            repo_name = repo["name"]
            repo_visibility = repo["private"]
            repo_url = repo["url"]

            new_visibility = not repo_visibility  # Toggle the visibility
            
            print(f"Changing visibility of '{repo_name}' to {'private' if new_visibility else 'public'}...")

            # Update repository visibility
            update_response = requests.patch(repo_url, headers=headers, json={"private": new_visibility})
            
            if update_response.status_code == 200:
                print(f"'{repo_name}' is now {'private' if new_visibility else 'public'}.")
            else:
                print(f"Failed to update '{repo_name}': {update_response.json()}")
    else:
        print(f"Failed to fetch repositories: {response.status_code} {response.text}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Toggle GitHub repository visibility.")
    parser.add_argument("--github_token", help="Your GitHub personal access token.")
    args = parser.parse_args()

    # Fallback to environment variable if argument is not provided
    github_token = args.github_token or os.getenv("GITHUB_TOKEN")

    if not github_token:
        raise ValueError("GITHUB_TOKEN must be provided either as an argument or environment variable.")

    # Get username from token instead of requiring it as input
    user_response = requests.get("https://api.github.com/user", headers={"Authorization": f"token {github_token}"})
    
    if user_response.status_code == 200:
        username = user_response.json()["login"]
        print(f"Authenticated as {username}. Toggling repo visibility...")
        toggle_repo_visibility(github_token, username)
    else:
        print(f"Failed to authenticate: {user_response.status_code} {user_response.text}")
