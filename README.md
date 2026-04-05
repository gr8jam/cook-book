# Cook Book

A vegan recipe cookbook published as a static site using [MkDocs Material](https://squidfundry.github.io/mkdocs-material/), hosted on GitHub Pages.

**Live site:** https://gr8jam.github.io/cook-book/

## Prerequisites

- Python 3.12
- [uv](https://docs.astral.sh/uv/) (Python package manager)

## Getting Started

```bash
# Clone the repo
git clone https://github.com/gr8jam/cook-book.git
cd cook-book

# Install dependencies
uv sync

# Start local preview
mkdocs serve
```

The site will be available at `http://127.0.0.1:8000/`.

## Adding a Recipe

1. Create a new directory under `docs/recipes/`:
   ```bash
   mkdir docs/recipes/my_new_recipe
   ```

2. Copy the template and fill in your recipe:
   ```bash
   cp .template/index.md docs/recipes/my_new_recipe/index.md
   ```

3. Edit `docs/recipes/my_new_recipe/index.md` — set the title, tags, ingredients, and instructions. Tags control which category the recipe appears under (e.g. `pasta`, `italian`, `asian`, `cake`).

4. Process a photo for the recipe (creates a standardized `image.jpg` and `thumbnail.jpg`):
   ```bash
   python -m preprocces_image <photo> --out docs/recipes/my_new_recipe/
   ```
   Use `--roi` to interactively crop a region of interest.

5. Add a thumbnail entry to the appropriate category section in `docs/index.md`.

## Project Structure

```
docs/
  index.md                        # Gallery page with thumbnail grid
  recipes/<name>/index.md         # Individual recipe pages
  recipes/<name>/image.jpg        # Hero image (800x600)
  recipes/<name>/thumbnail.jpg    # Gallery thumbnail (180x180)
.template/index.md                # Template for new recipes
preprocces_image.py               # CLI tool to crop/resize recipe photos
mkdocs.yml                        # MkDocs site configuration
```

## Deploying

```bash
mkdocs gh-deploy
```

This builds the site and pushes it to the `gh-pages` branch.
