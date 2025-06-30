import os

def run(config, **kwargs):
    site_url = config.get('site_url', '').rstrip('/')
    sitemap_path = os.path.join(config['site_dir'], 'sitemap.xml')

    urls = []
    for root, _, files in os.walk(config['site_dir']):
        for file in files:
            if file.endswith('.html') and file != '404.html':
                rel_path = os.path.relpath(os.path.join(root, file), config['site_dir'])
                url = site_url + '/' + rel_path.replace(os.path.sep, '/')
                urls.append(url)

    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        sitemap += f'  <url><loc>{url}</loc></url>\n'
    sitemap += '</urlset>'

    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(sitemap)

    print(f"[sitemap] Created sitemap.xml with {len(urls)} URLs")
