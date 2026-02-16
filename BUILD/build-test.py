#!/usr/bin/env python3
import json
import argparse
from pathlib import Path
from pybars import Compiler

ROOT = Path(__file__).resolve().parent.parent
compiler = Compiler()


def include_helper(this, file_path, options=None):
    """
    Handlebars helper to include a file's content.
    - If file ends with .md, it will be compiled and rendered as a template.
    - Otherwise, content is returned as fs-safe block.

    Usage in template:
    {{include "SCHEMA/TEST-DEFINITION.json"}}
    """
    full_path = ROOT + "/" + file_path

    if not full_path.exists():
        raise FileNotFoundError(f"Include file not found: {full_path}")

    content = full_path.read_text()

    # If it's a Markdown file, compile & render it
    if full_path.suffix.lower() == ".md":
        template = compiler.compile(content)
        # Render with the current context (`this`) and all helpers
        return template(this, helpers=helpers)
    else:
        # For other file types, wrap as fs-safe block
        return fs_safe_block(content)


def eq_helper(this, a, b, options=None):
    """
    Handlebars helper to check equality between two values.
    Usage in template:

    {{#eq a b}}
        ... content if equal ...
    {{else}}
        ... content if not equal ...
    {{/eq}}
    """
    # Pybars passes `options` for block helpers (like #if/#each)
    if options is None:
        # Called as inline helper: {{eq a b}}
        return a == b
    else:
        # Block helper usage
        if a == b:
            return options['fn'](this)  # Render "then" block
        else:
            return options['inverse'](this)  # Render "else" block


helpers = {
    "eq": eq_helper,
    "include": include_helper
}



def load(path):
    return Path(path).read_text()


def load_json(path):
    return json.loads(Path(path).read_text())

def fs_safe_block(content):
    return f"````fs-safe\n{content}\n````"

def render_template(template_str, context):
    template = compiler.compile(template_str)
    return template(context, helpers=helpers)

def build_test(version):
    # Handlebars helper: {{#if (eq a b)}} ... {{/if}}
    # Paths
    test_json_path = ROOT / "TESTS" / f"{version}.json"
    instructions_path = ROOT / "TEMPLATES/INSTRUCTIONS.md"
    schema_run_path = ROOT / "SCHEMA/TEST-DEFINITION.json"
    template_test_path = ROOT / "TEMPLATES/TEST.md"

    # Load components
    test_json = load_json(test_json_path)
    instructions = load(instructions_path)
    schema_run = load(schema_run_path)


    # Inject schema into instructions
    with open(ROOT / "TEMPLATES/TEST/CATEGORY.md") as f:
        category_template = compiler.compile(f.read())
    with open(ROOT / "TEMPLATES/TEST/QUESTION.md") as f:
        question_template = compiler.compile(f.read())
    # Register partials
    partials = {
        "question": question_template,
        "category": category_template,
    }
    with open(ROOT / "TEMPLATES/TEST.md") as f:
        full_template = compiler.compile(f.read())


    # Render
    rendered_test = full_template(test_json, partials=partials, helpers=helpers)


    # Final bundle
    bundle = (
        "# Garden Benchmark Test Bundle\n\n"
        f"## Test Version: {version}\n\n"
        "### Instructions\n\n"
        f"{instructions}\n\n"
        "### Rendered Test\n\n"
        f"{rendered_test}\n"
    )

    out_path = ROOT  / f"GARDEN_BENCHMARK_{version}.md"
    out_path.write_text(bundle)
    print(f"Built test bundle: {out_path}")



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=False, default="V1", help="Test version (e.g., V1)")
    args = parser.parse_args()
    build_test(args.version)

if __name__ == "__main__":
    main()
