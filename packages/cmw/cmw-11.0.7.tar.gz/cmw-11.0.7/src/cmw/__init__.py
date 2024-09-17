from mistletoe import markdown
from cmw.loader import load_yaml_with_dot_access
from pathlib import Path
from sys import argv
from shutil import copy
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from re import sub, match, DOTALL
from textwrap import dedent
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

PORT = 8000

KNOWN_CLASSES = ["center", "box"]
WATCH_SUFFIXES = [".md", "template.html", "config.yaml"]

class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if any(event.src_path.endswith(suffix) for suffix in WATCH_SUFFIXES):
            render()

    def on_created(self, event):
        if any(event.src_path.endswith(suffix) for suffix in WATCH_SUFFIXES):
            render()

def server():
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=True)
    observer.start()
    try:
        with TCPServer(("", PORT), SimpleHTTPRequestHandler) as httpd:
            print()
            print("Development server is running at:")
            print()
            print(f"    http://127.0.0.1:{PORT}")
            print()
            print("Exit with CTRL+C")
            print()
            httpd.serve_forever()
    except OSError:
        print()
        print("Port is taken by another process")
        print("or you're going too fast.")
        print()
        print("Sometimes the operating system won't")
        print("let you respawn a server that quickly.")
        print()
        print("Take, your, time.")
        print()
        print("30 seconds ~ 5 minutes")
        print()
        exit(0)
    finally:
        observer.stop()
    observer.join()

def replace_imgs(content):
    IMG_REGEX = r'([!a-zA-Z0-9_/\-\.]+)\.(jpg|png|webp)'
    def replace(match):
        filename = f"{match.group(1)}.{match.group(2)}"
        if filename.startswith("!"):
            return filename[1:]
        return f"<img src='{filename}' />"
    content = sub(IMG_REGEX, replace, content)
    return content

def my_markdown(content):
    content = wrap_blocks_with_div(content)
    content = wrap_sections_with_section_tags(content)
    content = replace_imgs(content)
    return markdown(content)

def kebab_case(text):
    # Convert the text to lowercase, keep only alphanumeric characters and spaces
    text = sub(r'[^a-zA-Z0-9\s]', '', text.lower())
    # Replace spaces with dashes
    return text.replace(' ', '-')

def wrap_sections_with_section_tags(markdown_text):
    # Define a pattern to match ## Heading 2 and its following content
    pattern = r"(## .+?)(?=(\n## |\Z))"

    # Function to wrap each matched section in <section> tags with an id
    def wrap_with_section(match):
        heading = match.group(1).split("\n", maxsplit=1)[0].strip()
        section_name = heading.replace('## ', '')  # Remove '## ' from the heading
        section_id = kebab_case(section_name) # Convert heading text to kebab-case for the id
        return f'<section id="{section_id}">\n\n{match.group(1)}\n\n</section>'

    # Substitute all sections with the wrapped version
    wrapped_markdown = sub(pattern, wrap_with_section, markdown_text, flags=DOTALL)

    return wrapped_markdown

def wrap_blocks_with_div(markdown_text):
    markdown_text += "\n"
    lines = []
    in_div = False
    in_boxes = False
    indent = 0
    for line in markdown_text.split("\n"):
        if in_div:
            if indent == 0:
                indent = len(line) - len(line.lstrip(" "))
            if indent and (line.strip() == "" or line.startswith(" " * indent)):
                lines.append(line[indent:])
                continue
            in_div = False
            indent = 0
            lines.append("")
            lines.append("</div>")
            lines.append("")
        m = match(r"([a-zA-Z0-9_-]+): ?(.*)", line)
        if (not m) or (m.group(1) not in KNOWN_CLASSES):
            if in_boxes:
                in_boxes = False
                lines.append("")
                lines.append("</div>")
                lines.append("")
            lines.append(line)
        else:
            if m.group(1) != "box" and in_boxes:
                in_boxes = False
                lines.append("")
                lines.append("</div>")
                lines.append("")
            if m.group(1) == "box" and not in_boxes:
                in_boxes = True
                lines.append("")
                lines.append("<div class='boxes'>")
                lines.append("")
            lines.append("")
            lines.append(f"<div class='{m.group(1)}'>")
            lines.append("")
            lines.append(m.group(2))
            in_div = True

    if in_div:
        lines.append("")
        lines.append("</div>")
        lines.append("")

    if in_boxes:
        lines.append("")
        lines.append("</div>")
        lines.append("")

    return "\n".join(lines)

def main():
    this_file_directory = Path(__file__).parent
    config_path = this_file_directory / "config.yaml"
    index_path = this_file_directory / "index.md"

    if len(argv) == 2 and argv[1] == "init":
        path = Path(".")
        copy(config_path, path / "config.yaml")
        copy(index_path, path / "index.md")
        print()
        print(f"Initialized a new project")
        print()
        print("To get started:")
        print()
        print(" 1. Run: cmw server")
        print(" 2. Customize config.yaml")
        print(" 3. Customize index.md")
        print()
        print("Happy coding!")
        print()
        return 0

    server_mode = (len(argv) == 2 and argv[1] == "server")
    build_mode = (len(argv) == 1)

    if not (server_mode or build_mode):
        print("Error: Unknown arguments.")
        return 1

    render()

    if server_mode:
        server()

    return 0

def render():
    this_file_directory = Path(__file__).parent
    template_path = this_file_directory / "template.html"
    config_path = this_file_directory / "config.yaml"

    # Set the template and config paths
    if Path("template.html").exists():
        template_path = Path("template.html")
    if Path("config.yaml").exists():
        config_path = Path("config.yaml")

    # Load up template
    with template_path.open("r") as file:
        template = file.read()

    # Load up config.yaml
    config = load_yaml_with_dot_access(config_path)

    # Construct navigation
    if config.Navigation:
        links = ""
        for item in config.Navigation:
            links += f" <a href='{item.URL}'>{item.Text}</a> "
        navigation = f"<nav>{links}</nav>" 
    else:
        navigation = None

    # Replace the variables that are consistent on every page
    template = template.replace("TITLE", config.Title)
    template = template.replace("HEADING", replace_imgs(config.Heading))
    template = template.replace("TAGLINE", config.Tagline if config.Tagline else "")
    template = template.replace("NAVIGATION", navigation if navigation else "")
    template = template.replace("FOOTER", replace_imgs(config.Footer) if config.Footer else "")

    for input_path in Path(".").rglob("*.md"):
        with input_path.open("r") as input_file:
            # Load up the Markdown and render it
            content = my_markdown(input_file.read())

            # Generate the output
            html = template.replace("CONTENT", content)

            # Get the output path
            output_path = Path(str(input_path)[:-2] + "html")

            # Write to disk
            with output_path.open("w") as output_file:
                output_file.write(html)

            # Print status
            print()
            print(f" - Converted {input_path} to {output_path}")
    print()
