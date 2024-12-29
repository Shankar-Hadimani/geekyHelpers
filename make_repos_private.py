import requests
import argparse
import os

def make_repos_private(github_token, username):
    # GitHub API URL for user's repositories
    github_api_url = f"https://api.github.com/users/{username}/repos"
    # Headers for authentication
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Get all repositories for the user
    response = requests.get(github_api_url, headers=headers)
    if response.status_code == 200:
        repos = response.json()
        for repo in repos:
            repo_name = repo["name"]
            if not repo["private"]:  # Check if the repo is already public
                repo_url = repo["url"]
                print(f"Making repository '{repo_name}' private...")
                # Update repository visibility
                update_response = requests.patch(repo_url, headers=headers, json={"private": True})
                
                if update_response.status_code == 200:
                    print(f"'{repo_name}' is now private.")
                else:
                    print(f"Failed to make '{repo_name}' private: {update_response.json()}")
            else:
                print(f"'{repo_name}' is already private.")
    else:
        print(f"Failed to fetch repositories: {response.status_code} {response.text}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Make all GitHub repositories private.")
    parser.add_argument("--github_token", help="Your GitHub personal access token.")
    parser.add_argument("--username", help="Your GitHub username.")
    args = parser.parse_args()

    # Fallback to environment variables if arguments are not provided
    github_token = args.github_token or os.getenv("GITHUB_TOKEN")
    username = args.username or os.getenv("GITHUB_USERNAME")

    if not github_token or not username:
        raise ValueError("GITHUB_TOKEN and USERNAME must be provided either as arguments or environment variables.")

    make_repos_private(github_token, username)
