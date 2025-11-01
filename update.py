import requests


def fetch_language_colors():
    url = "https://raw.githubusercontent.com/ozh/github-colors/master/colors.json"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch language colors: {response.status_code}")
    return response.json()


LANG_COLORS = fetch_language_colors()


def fetch_latest_repos(max_projects=5):
    url = f"https://api.github.com/users/0x1bd/repos?sort=updated&per_page={max_projects}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch repos: {response.status_code}")
    return response.json()


def badge(message, color="8A2BE2"):
    msg_enc = message.replace(" ", "%20")
    return f"![{message}](https://img.shields.io/badge/{msg_enc}-{color})"


def get_language_color(language):
    if not language or language not in LANG_COLORS:
        return "8A2BE2"
    return LANG_COLORS[language]["color"].lstrip("#")


def generate_projects_section(repos):
    section = "| Project | Description | Stars | Language |\n"
    section += "|--------|-------------|-------|---------|\n"
    for repo in repos:
        name = repo["name"]
        url = repo["html_url"]
        desc = repo["description"] or "No idea what this does"
        stars = repo["stargazers_count"]

        if name == "0x1bd":
            continue

        language = repo["language"] or "Unknown"
        lang_color = get_language_color(language)
        lang_badge = badge(language, lang_color)

        section += f"| [{name}]({url}) | {desc} | ⭐ {stars} | {lang_badge} |\n"
    return section


def update_readme(readme_path, new_content):
    with open(readme_path, "r", encoding="utf-8") as f:
        readme = f.read()

    start_tag = "<!--START_LATEST_PROJECTS-->"
    end_tag = "<!--END_LATEST_PROJECTS-->"

    start_idx = readme.find(start_tag) + len(start_tag)
    end_idx = readme.find(end_tag)

    updated_readme = readme[:start_idx] + "\n" + new_content + readme[end_idx:]

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(updated_readme)


if __name__ == "__main__":
    repos = fetch_latest_repos(6)  # repos+1
    new_section = generate_projects_section(repos)
    update_readme("README.md", new_section)
