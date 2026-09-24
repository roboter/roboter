import json
import urllib.parse
import os

TECH_OVERRIDES = {
    'beehive-sensors': ('ESP32 / C++', '00599C', 'cplusplus', 'white'),
    'Drill_To_Gcode': ('CNC / G-Code', '6E7681', '', 'white'),
    'gsGCode': ('C#', '239120', 'c-sharp', 'white'),
    'LilyGO_T5_V24': ('Arduino / C++', '00979D', 'arduino', 'white'),
    'MightyBoardFirmware': ('C / C++', '00599C', 'cplusplus', 'white'),
    'ReplicatorG': ('Java / Python', '3776AB', 'python', 'white'),
    'UTFT-1': ('C++ / Arduino', '00979D', 'arduino', 'white'),
}

def get_lang_badge(name, lang):
    if name in TECH_OVERRIDES:
        tname, color, logo, logo_col = TECH_OVERRIDES[name]
        tname_clean = urllib.parse.quote(tname)
        logo_part = f"&logo={logo}&logoColor={logo_col}" if logo else ""
        return f"![{tname}](https://img.shields.io/badge/{tname_clean}-{color}?style=flat-square{logo_part})"
    if not lang or lang == 'None':
        return ''
    lang_clean = urllib.parse.quote(lang)
    color_map = {
        'C#': ('239120', 'c-sharp', 'white'),
        'C++': ('00599C', 'cplusplus', 'white'),
        'C': ('A8B9CC', 'c', 'black'),
        'TypeScript': ('3178C6', 'typescript', 'white'),
        'JavaScript': ('F7DF1E', 'javascript', 'black'),
        'Arduino': ('00979D', 'arduino', 'white'),
        'Astro': ('BC52EE', 'astro', 'white'),
        'HTML': ('E34F26', 'html5', 'white'),
        'G-code': ('6E7681', '', 'white'),
    }
    color, logo, logo_col = color_map.get(lang, ('6E7681', '', 'white'))
    logo_part = f"&logo={logo}&logoColor={logo_col}" if logo else ""
    return f"![{lang}](https://img.shields.io/badge/{lang_clean}-{color}?style=flat-square{logo_part})"

def get_fork_badge(r):
    f_info = r['fork_info']
    if not f_info['is_fork']:
        return "![Original](https://img.shields.io/badge/Original-2ea44f?style=flat-square&logo=github)"
    else:
        parent_name = f_info.get('parent_name') or 'upstream'
        parent_url = f_info.get('parent_url') or '#'
        return f"[![Fork](https://img.shields.io/badge/Fork-0969da?style=flat-square&logo=git-fork)]({parent_url})<br/>↳&nbsp;[`{parent_name}`]({parent_url})"

def get_sync_badge(r):
    f_info = r['fork_info']
    if not f_info['is_fork']:
        return "![Source](https://img.shields.io/badge/Sync-Source%20Repo-6f42c1?style=flat-square)"
    status = f_info.get('status', 'unknown')
    ahead = f_info.get('ahead_by', 0)
    behind = f_info.get('behind_by', 0)

    if status == 'ahead':
        return f"![Forward](https://img.shields.io/badge/Forward-%2B{ahead}%20commits-238636?style=flat-square&logo=git-pull-request)"
    elif status == 'behind':
        return f"![Behind](https://img.shields.io/badge/Behind--{behind}%20commits-d9381e?style=flat-square)"
    elif status == 'diverged':
        return f"![Diverged](https://img.shields.io/badge/Diverged-%2B{ahead}%20%7C%20--{behind}-dbab09?style=flat-square)"
    elif status == 'identical':
        return "![Up to Date](https://img.shields.io/badge/Up%20to%20Date-synced-2ea44f?style=flat-square&logo=check)"
    elif r['name'] == 'Drill_To_Gcode':
        return "![Empty Fork](https://img.shields.io/badge/Sync-Empty%20Fork-8b949e?style=flat-square)"
    else:
        return "![Fork](https://img.shields.io/badge/Sync-Fork-8b949e?style=flat-square)"

def build_readme():
    script_dir = os.path.dirname(__file__)
    data_file = os.path.join(script_dir, 'repos_data.json')
    readme_file = os.path.abspath(os.path.join(script_dir, '..', 'README.md'))

    if not os.path.exists(data_file):
        print(f"Error: {data_file} not found. Run previous pipeline steps first.")
        return

    with open(data_file, 'r', encoding='utf-8') as f:
        repos = json.load(f)

    def sort_key(r):
        is_fork = 1 if r['fork_info']['is_fork'] else 0
        stars = r.get('stars', 0)
        ahead = r['fork_info'].get('ahead_by', 0)
        return (is_fork, -stars, -ahead, r['name'].lower())

    sorted_repos = sorted(repos, key=sort_key)

    total_count = len(repos)
    fork_count = sum(1 for r in repos if r['fork_info']['is_fork'])
    orig_count = total_count - fork_count
    ahead_count = sum(1 for r in repos if r['fork_info'].get('status') == 'ahead')
    diverged_count = sum(1 for r in repos if r['fork_info'].get('status') == 'diverged')
    identical_count = sum(1 for r in repos if r['fork_info'].get('status') == 'identical')

    lines = []
    lines.append("### Hi there 👋")
    lines.append("")
    lines.append("![Visitors since 11 Nov 2020](http://estruyf-github.azurewebsites.net/api/VisitorHit?user=roboter&repo=roboter&countColor=%237B1E7A)")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 📦 Public Repositories Overview")
    lines.append("")
    lines.append(f"[![Total Repos](https://img.shields.io/badge/Total%20Repos-{total_count}-blue?style=for-the-badge&logo=github)](https://github.com/roboter?tab=repositories) "
                 f"[![Original](https://img.shields.io/badge/Original%20Projects-{orig_count}-2ea44f?style=for-the-badge&logo=git)](https://github.com/roboter?tab=repositories&q=&type=source) "
                 f"[![Forks](https://img.shields.io/badge/Forks-{fork_count}-0969da?style=for-the-badge&logo=git-fork)](https://github.com/roboter?tab=repositories&q=&type=fork) "
                 f"[![Forward](https://img.shields.io/badge/Ahead%20of%20Upstream-{ahead_count}-238636?style=for-the-badge)](https://github.com/roboter) "
                 f"[![Diverged](https://img.shields.io/badge/Diverged-{diverged_count}-dbab09?style=for-the-badge)](https://github.com/roboter) "
                 f"[![Synced](https://img.shields.io/badge/Up%20to%20Date-{identical_count}-brightgreen?style=for-the-badge)](https://github.com/roboter)")
    lines.append("")
    lines.append("> 💡 **Legend:**")
    lines.append("> - **Original**: Source repository created and maintained by roboter.")
    lines.append("> - **Fork**: Forked from upstream repository (clickable link to upstream).")
    lines.append("> - **Forward / Ahead**: Includes original commits ahead of upstream.")
    lines.append("> - **Diverged**: Both ahead of and behind upstream branch.")
    lines.append("> - **Up to Date**: Fully synchronized with upstream.")
    lines.append("")
    lines.append("| Preview / Screenshot | Repository | Type / Fork | Sync Status (Behind / Forward) | Description |")
    lines.append("| :---: | :--- | :---: | :---: | :--- |")

    for r in sorted_repos:
        name = r['name']
        url = r['html_url']
        desc = r['description'] or ''
        clean_desc = desc.replace('|', '&#124;').replace('\n', ' ').strip()

        screenshot = r['screenshot_url']
        img_html = f'<a href="{url}"><img src="{screenshot}" width="160" alt="{name}" /></a>'

        lang_badge = get_lang_badge(name, r['language'])
        star_count = r.get('stars', 0)
        star_badge = f" [![Stars](https://img.shields.io/badge/★-{star_count}-f1e05a?style=flat-square&logo=github&logoColor=black)]({url}/stargazers)" if star_count > 0 else ""

        badges_row = ""
        if lang_badge or star_badge:
            badges_row = f"<br/>{lang_badge}{star_badge}"

        repo_cell = f"[**`{name}`**]({url}){badges_row}"
        fork_cell = get_fork_badge(r)
        sync_cell = get_sync_badge(r)

        row = f"| {img_html} | {repo_cell} | {fork_cell} | {sync_cell} | {clean_desc} |"
        lines.append(row)

    lines.append("")
    lines.append("---")
    lines.append("*Generated automatically with GitHub repository sync data.*")

    content = "\n".join(lines) + "\n"

    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Generated {readme_file} with {len(sorted_repos)} repository rows!")

if __name__ == '__main__':
    build_readme()
