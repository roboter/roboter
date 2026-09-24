# 🚀 Repository Profile README Generator Scripts

This folder contains the complete automated pipeline for fetching public GitHub repository data for `@roboter`, analyzing fork sync statuses, discovering screenshots/previews, enriching metadata, and rendering the dynamic summary table in the root [`README.md`](../README.md).

---

## 📋 Execution Order & Script Summary

| Order | Script | Description | Primary Inputs & Outputs |
| :---: | :--- | :--- | :--- |
| **0** | [`update_all.py`](./update_all.py) | **Master Orchestrator**: Executes steps 1 through 5 in sequence. | Triggers all scripts in sequence. |
| **1** | [`1_fetch_repos.py`](./1_fetch_repos.py) | Queries the GitHub REST API (`/users/roboter/repos`) to retrieve all public repository records. | Output: `repos.json` |
| **2** | [`2_process_forks.py`](./2_process_forks.py) | Analyzes every repository to check if it is a fork. For forks, queries upstream parent info and compares commit diffs (`ahead_by`, `behind_by`, `diverged`, `identical`). Uses local caching. | Input: `repos.json`<br/>Outputs: `forks_cache.json`, `repos_data.json` |
| **3** | [`3_find_screenshots.py`](./3_find_screenshots.py) | Inspects repository `README.md` files and repository root file trees for custom screenshots/GIFs/SVGs. Falls back to GitHub OpenGraph preview cards (`opengraph.githubassets.com`). | Input: `repos_data.json`<br/>Output: Updated `repos_data.json` |
| **4** | [`4_fill_descriptions.py`](./4_fill_descriptions.py) | Ensures all repositories have clean, accurate descriptions and fallback metadata for empty descriptions. | Input: `repos_data.json`<br/>Output: Updated `repos_data.json` |
| **5** | [`5_build_readme.py`](./5_build_readme.py) | Renders the final colorful Markdown table, Shields.io badges, status indicators, and summary metrics into the root `README.md`. | Input: `repos_data.json`<br/>Output: `../README.md` |

---

## 🛠️ Usage Instructions

### Running the Entire Pipeline (Recommended)

To update the profile table in one command, run:

```bash
python scripts/update_all.py
```

### Running Individual Steps

You can also run any step independently:

```bash
python scripts/1_fetch_repos.py
python scripts/2_process_forks.py
python scripts/3_find_screenshots.py
python scripts/4_fill_descriptions.py
python scripts/5_build_readme.py
```
