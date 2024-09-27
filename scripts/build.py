import fnmatch
import os
from pathlib import Path
import shutil
from jinja2 import Environment, FileSystemLoader
import frontmatter
import mistune

markdown = mistune.create_markdown(plugins=["math"])

SRC_PATH = Path("src/")
DST_PATH = Path("site/")

SOLUTIONS_FOLDER = SRC_PATH / "solutions"
STATIC_FOLDER = SRC_PATH / "assets"
TEMPLATES_FOLDER = SRC_PATH / "templates"

SOLUTION_TEMPLATE = "solution.html"

ALLOWED = ["*.html", "favicon.ico", "static/*"]

environment = Environment(loader=FileSystemLoader(TEMPLATES_FOLDER))

def render_html(content: str):
    """Render."""
    template = environment.get_template(SOLUTION_TEMPLATE)
    metadata, content = frontmatter.parse(content)
    rendered_html = template.render(metadata, content=content)
    return rendered_html

def build_file(file: Path):
    """Build file."""
    if file.is_dir():
        for root, _, files in os.walk(file):
            for _file in files:
                build_file(Path(root) / _file)
        return

    if not file.is_relative_to(SRC_PATH):
        return

    if file.is_relative_to(TEMPLATES_FOLDER):
        return

    dst_file = DST_PATH / file.relative_to(SRC_PATH)
    os.makedirs(dst_file.parent, exist_ok=True)

    if file.is_relative_to(STATIC_FOLDER):
        shutil.copyfile(file, dst_file)
        return
    
    if file.is_relative_to(SOLUTIONS_FOLDER):
        with open(file) as f:
            file_content = f.read()
        dst_content = render_html(file_content)
        with open(dst_file.with_suffix(".html"), "w") as f:
            f.write(dst_content)
        return

    if any(fnmatch.fnmatch(str(file), allowed) for allowed in ALLOWED):
        shutil.copyfile(file, dst_file)
        return

def build():
    """Build."""
    os.makedirs(DST_PATH, exist_ok=True)


    for root, _, files in os.walk(SRC_PATH):
        for file in files:
            build_file(Path(root) / file)

if __name__ == "__main__":
    build()
