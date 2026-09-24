import urllib.request
import json
import os

def fetch_repos(username="roboter"):
    print(f"Fetching public repositories for '{username}'...")
    url = f"https://api.github.com/users/{username}/repos?per_page=100"
    req = urllib.request.Request(url, headers={"User-Agent": "roboter-profile-builder"})
    with urllib.request.urlopen(req) as resp:
        repos = json.loads(resp.read().decode('utf-8'))
    
    output_path = os.path.join(os.path.dirname(__file__), 'repos.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(repos, f, indent=2)
    print(f"Saved {len(repos)} repositories to {output_path}")

if __name__ == '__main__':
    fetch_repos()
