#!/bin/bash
# Minify CSS
css-minify -f assets/styles/justify.css -o assets/styles/

# Build site
mkdocs build --clean

# Optimize HTML (optional)
# npm install -g html-minifier
# html-minifier --input-dir site --output-dir site --file-ext html --remove-comments --collapse-whitespace