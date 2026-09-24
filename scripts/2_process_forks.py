import urllib.request
import urllib.error
import json
import os
import time

def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "roboter-profile-builder"})
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f"  Error fetching {url}: {e}")
        return None

def process_forks():
    script_dir = os.path.dirname(__file__)
    repos_file = os.path.join(script_dir, 'repos.json')
    cache_file = os.path.join(script_dir, 'forks_cache.json')

    if not os.path.exists(repos_file):
        print(f"Error: {repos_file} not found. Run 1_fetch_repos.py first.")
        return

    with open(repos_file, 'r', encoding='utf-8') as f:
        repos = json.load(f)

    forks_cache = {}
    if os.path.exists(cache_file):
        with open(cache_file, 'r', encoding='utf-8') as f:
            forks_cache = json.load(f)

    print("Analyzing repository upstream & commit sync status...")
    for idx, r in enumerate(repos):
        name = r['name']
        is_fork = r['fork']
        default_branch = r.get('default_branch', 'master')

        fork_info = {
            'is_fork': is_fork,
            'parent_name': None,
            'parent_url': None,
            'status': 'source',
            'ahead_by': 0,
            'behind_by': 0,
            'parent_branch': None
        }

        if is_fork:
            if name in forks_cache:
                fork_info = forks_cache[name]
            else:
                print(f"  Checking upstream for fork: {name}")
                repo_detail = fetch_json(f"https://api.github.com/repos/roboter/{name}")
                if repo_detail and 'parent' in repo_detail:
                    parent = repo_detail['parent']
                    parent_full_name = parent['full_name']
                    parent_url = parent['html_url']
                    parent_default_branch = parent.get('default_branch', 'master')

                    fork_info['parent_name'] = parent_full_name
                    fork_info['parent_url'] = parent_url
                    fork_info['parent_branch'] = parent_default_branch

                    compare_url = f"https://api.github.com/repos/{parent_full_name}/compare/{parent_default_branch}...roboter:{default_branch}"
                    cmp_data = fetch_json(compare_url)
                    if cmp_data:
                        fork_info['status'] = cmp_data.get('status', 'unknown')
                        fork_info['ahead_by'] = cmp_data.get('ahead_by', 0)
                        fork_info['behind_by'] = cmp_data.get('behind_by', 0)
                    else:
                        fork_info['status'] = 'unknown'
                else:
                    fork_info['status'] = 'fork'

                forks_cache[name] = fork_info
                with open(cache_file, 'w', encoding='utf-8') as f:
                    json.dump(forks_cache, f, indent=2)
                time.sleep(0.3)

        r['fork_info'] = fork_info

    output_path = os.path.join(script_dir, 'repos_data.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(repos, f, indent=2)
    print(f"Fork analysis complete. Saved to {output_path}")

if __name__ == '__main__':
    process_forks()
