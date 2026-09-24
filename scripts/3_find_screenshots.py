import urllib.request
import json
import re
import os

def fetch_raw_text(url):
    req = urllib.request.Request(url, headers={"User-Agent": "roboter-profile-builder"})
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.read().decode('utf-8', errors='ignore')
    except Exception:
        return None

def find_screenshots():
    script_dir = os.path.dirname(__file__)
    data_file = os.path.join(script_dir, 'repos_data.json')

    if not os.path.exists(data_file):
        print(f"Error: {data_file} not found. Run 2_process_forks.py first.")
        return

    with open(data_file, 'r', encoding='utf-8') as f:
        repos = json.load(f)

    print("Locating screenshots and images for repositories...")

    for r in repos:
        name = r['name']
        branch = r.get('default_branch', 'master')
        screenshot_url = None
        has_custom = False

        # Method 1: Check README.md for inline images
        readme_urls = [
            f"https://raw.githubusercontent.com/roboter/{name}/{branch}/README.md",
            f"https://raw.githubusercontent.com/roboter/{name}/master/README.md",
            f"https://raw.githubusercontent.com/roboter/{name}/main/README.md"
        ]

        readme_content = None
        for r_url in readme_urls:
            content = fetch_raw_text(r_url)
            if content:
                readme_content = content
                break

        if readme_content:
            img_matches = re.findall(r'!\[.*?\]\((.+?)\)', readme_content)
            html_img_matches = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', readme_content, re.IGNORECASE)
            all_imgs = img_matches + html_img_matches

            for img in all_imgs:
                img = img.strip().split()[0]
                img_lower = img.lower()
                if any(badge in img_lower for badge in ['shields.io', 'badgen.net', 'travis-ci', 'badge', 'visitor', 'youtube.com/vi', 'buymeacoffee']):
                    continue
                if any(img_lower.endswith(ext) or ext + '?' in img_lower for ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg']):
                    if img.startswith('http://') or img.startswith('https://'):
                        screenshot_url = img
                    else:
                        clean_path = img.lstrip('./').lstrip('/')
                        screenshot_url = f"https://raw.githubusercontent.com/roboter/{name}/{branch}/{clean_path}"
                    has_custom = True
                    break

        # Method 2: Check repo root folder HTML for image assets if none found in README
        if not screenshot_url:
            try:
                repo_url = f"https://github.com/roboter/{name}"
                html = fetch_raw_text(repo_url)
                if html:
                    img_files = re.findall(r'href="(/roboter/' + name + r'/blob/' + branch + r'/[^"]+\.(?:png|jpg|jpeg|gif|svg))"', html, re.I)
                    if img_files:
                        screenshot_url = "https://raw.githubusercontent.com" + img_files[0].replace('/blob/', '/')
                        has_custom = True
            except Exception:
                pass

        # Method 3: Fallback to OpenGraph preview card
        if not screenshot_url:
            screenshot_url = f"https://opengraph.githubassets.com/1/roboter/{name}"
            has_custom = False

        r['screenshot_url'] = screenshot_url
        r['has_custom_screenshot'] = has_custom

    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(repos, f, indent=2)

    custom_count = sum(1 for r in repos if r['has_custom_screenshot'])
    print(f"Screenshots updated ({custom_count} custom screenshots, {len(repos)-custom_count} OpenGraph cards).")

if __name__ == '__main__':
    find_screenshots()
