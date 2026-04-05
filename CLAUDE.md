# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A vegan recipe cookbook published as a static site using MkDocs Material, hosted on GitHub Pages at https://gr8jam.github.io/cook-book/.

## Commands

```bash
# Local preview
mkdocs serve

# Deploy to GitHub Pages
mkdocs gh-deploy

# Pre-process a recipe image (creates image.jpg + thumbnail.jpg)
python -m preprocces_image <source-image> --out docs/recipes/<recipe_name>/
# Add --roi to interactively select a region of interest
```

Uses `uv` for Python dependency management (Python 3.12). Pre-commit hooks enforce YAML validity, trailing whitespace, end-of-file newlines, and EXIF metadata stripping on images.

## Architecture

- **`docs/`** - MkDocs content root
  - **`index.md`** - Gallery page with thumbnail grid, organized by category (Pasta, Mains, Cakes, Other)
  - **`recipes/<name>/index.md`** - Individual recipe pages with YAML frontmatter tags
  - **`recipes/<name>/image.jpg`** + **`thumbnail.jpg`** - Processed images (800x600 and 180x180)
- **`.template/index.md`** - Template for new recipes
- **`preprocces_image.py`** - OpenCV-based CLI tool (Typer) that crops/resizes source images into standardized image.jpg and thumbnail.jpg
- **`mkdocs.yml`** - Site config with Material theme, search, and tags plugin

## Adding a New Recipe

1. Create `docs/recipes/<recipe_name>/` directory
2. Copy `.template/index.md` into it and fill in the recipe details
3. Set appropriate tags in the YAML frontmatter (e.g., `italian`, `pasta`, `asian`, `cake`)
4. Process the recipe photo: `python -m preprocces_image <photo> --out docs/recipes/<recipe_name>/`
5. Add a thumbnail entry to the appropriate category section in `docs/index.md`

## Recipe Format

Each recipe uses YAML frontmatter for tags and follows a consistent structure: title, hero image, time/servings table, ingredients list (quantities in `_italics_`), numbered instructions, and optional inspiration links. Uses Material for MkDocs emoji syntax (`:material-clock-outline:`, `:fork_and_knife:`).
