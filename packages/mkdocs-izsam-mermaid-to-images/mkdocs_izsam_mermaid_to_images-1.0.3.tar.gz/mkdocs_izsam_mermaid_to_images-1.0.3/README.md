# MkDocs IZSAM Mermaid to images

This plugin processes each page's Markdown content, finds Mermaid code blocks, converts them to images using `mermaid.cli`, and replaces the code blocks with image references. The image format can be specified in the `mkdocs.yml` configuration file.

## Installation

Install dependencies:

```bash
npm install -g @mermaid-js/mermaid-cli
```

Install the package with pip:

```bash
pip install mkdocs-izsam-mermaid-to-images
```

Enable the plugin in the `mkdocs.yml` file:

```yaml
plugins:
  - search
  - mkdocs-izsam-mermaid-to-images:
      output_dir: 'mermaid_images'
      image_format: 'svg'  # or 'png'
```

> See how to use [MkDocs Plugins](https://www.mkdocs.org/dev-guide/plugins/#using-plugins)