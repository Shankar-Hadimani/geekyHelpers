import requests
import argparse
import os

def update_repo_visibility(github_token, username, visibility):
    # GitHub API URL for user's repositories
    github_api_url = f"https://api.github.com/users/{username}/repos"
    # Headers for authentication
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Convert visibility to boolean (private=True, public=False)
    is_private = visibility.lower() == "private"

    # Get all repositories for the user
    response = requests.get(github_api_url, headers=headers)
    if response.status_code == 200:
        repos = response.json()
        for repo in repos:
            repo_name = repo["name"]
            current_visibility = "private" if repo["private"] else "public"
            if repo["private"] != is_private:  # Only update if visibility is different
                repo_url = repo["url"]
                print(f"Changing repository '{repo_name}' from {current_visibility} to {visibility}...")
                # Update repository visibility
                update_response = requests.patch(repo_url, headers=headers, json={"private": is_private})
                
                if update_response.status_code == 200:
                    print(f"'{repo_name}' is now {visibility}.")
                else:
                    print(f"Failed to change '{repo_name}' to {visibility}: {update_response.json()}")
            else:
                print(f"'{repo_name}' is already {current_visibility}. No changes needed.")
    else:
        print(f"Failed to fetch repositories: {response.status_code} {response.text}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update GitHub repository visibility.")
    parser.add_argument("--github_token", help="Your GitHub personal access token.")
    parser.add_argument("--username", help="Your GitHub username.")
    parser.add_argument("--visibility", required=True, choices=["private", "public"],
                        help="Set the visibility of the repositories (private or public).")
    args = parser.parse_args()

    # Fallback to environment variables if arguments are not provided
    github_token = args.github_token or os.getenv("GITHUB_TOKEN")
    username = args.username or os.getenv("GITHUB_USERNAME")

    if not github_token or not username:
        raise ValueError("GITHUB_TOKEN and USERNAME must be provided either as arguments or environment variables.")

    update_repo_visibility(github_token, username, args.visibility)
