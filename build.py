#!/usr/bin/env python3
"""Static release-notes site (en, es, pt-BR). No dependencies.   python3 build.py  ->  ./site

content/site.json              product name, docs and product links, host (per language where text)
content/releases.json          [{version, date, status}] newest first (status: stable | superseded)
content/<version>/<lang>.json  {title, summary, items:[{tag: new|improved|changed|fixed, title, body, bullets?}]}
"""
import json, os, shutil
from html import escape as esc

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'site')
LANGS = [('en', 'English'), ('es', 'Español'), ('pt-BR', 'Português (Brasil)')]
LOGO = ('<svg class="logo-mark" viewBox="0 0 64 64" aria-hidden="true" width="36" height="36"><defs>'
        '<linearGradient id="nx-mark" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="hsl(213,94%,62%)"/>'
        '<stop offset="1" stop-color="hsl(220,100%,52%)"/></linearGradient></defs>'
        '<rect width="64" height="64" rx="14" fill="#0b1730" stroke="rgba(59,130,246,.35)" stroke-width="1.5"/>'
        '<path d="M18 46V18h8l12 17.5V18h8v28h-8L26 28.5V46z" fill="url(#nx-mark)"/></svg>'
        '<span class="logo-word">NE<span>X</span>WALL</span>')
GLOBE = ('<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" '
         'stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/></svg>')
MONTHS = {
    'en': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
    'es': ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'],
    'pt-BR': ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'],
}
UI = {
    'en': dict(skip='Skip to content', all='All releases', latest='Latest release', date='Released', docs='Documentation', support='Support',
               language='Language', theme='Theme', stable='Current', superseded='Superseded', main='Nexwall website',
               new='New', improved='Improved', changed='Changed', fixed='Fixed', back='All releases', eyebrow='Release notes',
               footer='Release notes are published for each version.', lead_suffix='What is new in each version.'),
    'es': dict(skip='Saltar al contenido', all='Todas las versiones', latest='Última versión', date='Publicada', docs='Documentación', support='Soporte',
               language='Idioma', theme='Tema', stable='Actual', superseded='Anterior', main='Sitio de Nexwall',
               new='Nuevo', improved='Mejorado', changed='Cambiado', fixed='Corregido', back='Todas las versiones', eyebrow='Notas de versión',
               footer='Las notas de versión se publican para cada versión.', lead_suffix='Qué hay de nuevo en cada versión.'),
    'pt-BR': dict(skip='Ir para o conteúdo', all='Todas as versões', latest='Última versão', date='Publicada', docs='Documentação', support='Suporte',
                  language='Idioma', theme='Tema', stable='Atual', superseded='Anterior', main='Site da Nexwall',
                  new='Novo', improved='Melhorado', changed='Alterado', fixed='Corrigido', back='Todas as versões', eyebrow='Notas de versão',
                  footer='As notas de versão são publicadas para cada versão.', lead_suffix='O que há de novo em cada versão.'),
}


def load(*p):
    with open(os.path.join(ROOT, *p), encoding='utf-8') as f:
        return json.load(f)


def write(path, text):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)


def nice(lang, iso):
    y, m, d = (int(x) for x in iso.split('-'))
    n = MONTHS[lang][m - 1]
    return '%s %d, %d' % (n, d, y) if lang == 'en' else '%d de %s de %d' % (d, n, y)


def shell(lang, site, title, desc, body, depth, here):
    ui = UI[lang]
    base = '../' * depth if depth else './'
    langs = ''.join('<a href="%s%s/%s" hreflang="%s"%s>%s</a>' % (base, c, here, c, ' aria-current="true"' if c == lang else '', esc(n)) for c, n in LANGS)
    return '''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="{base}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{base}assets/style.css">
<script>try{{var t=localStorage.getItem('nx-theme');if(t)document.documentElement.setAttribute('data-theme',t)}}catch(e){{}}</script>
</head>
<body>
<a class="skip" href="#main">{skip}</a>
<header class="top"><div class="top-in">
  <a class="brand" href="https://nexwall.com.br" aria-label="Nexwall">{logo}</a>
  <nav class="top-nav"><a href="{base}{lang}/">{all}</a><a href="{docs_url}" rel="noopener">{docs}</a><a href="https://support.nexwall.com.br/{lang}/" rel="noopener">{support}</a></nav>
  <div class="top-tools"><details class="lang"><summary aria-label="{language}" title="{language}">{globe}</summary><div class="menu">{langs}</div></details>
  <button class="icon-btn" id="theme" type="button" aria-label="{theme}" title="{theme}">&#9680;</button></div>
</div></header>
{body}
<footer class="foot"><div class="foot-in"><span>{footer}</span><span class="foot-links"><a href="https://nexwall.com.br" rel="noopener">{main}</a> &middot; &copy; Nexwall</span></div></footer>
<script src="{base}assets/site.js"></script>
</body></html>
'''.format(lang=lang, title=esc(title), desc=esc(desc), base=base, skip=esc(ui['skip']), logo=LOGO, all=esc(ui['all']),
           docs_url=esc(site['docs_url']), docs=esc(ui['docs']), support=esc(ui['support']), language=esc(ui['language']),
           globe=GLOBE, langs=langs, theme=esc(ui['theme']), body=body, footer=esc(ui['footer']), main=esc(ui['main']))


def paragraphs(t):
    return ''.join('<p>%s</p>' % esc(p) for p in t.split('\n\n') if p.strip())


def item(ui, it):
    tag = it.get('tag', 'new')
    b = '<ul>%s</ul>' % ''.join('<li>%s</li>' % esc(x) for x in it['bullets']) if it.get('bullets') else ''
    return ('<article class="item" data-tag="%s"><header><span class="tag tag-%s">%s</span><h3>%s</h3></header>%s%s</article>'
            % (esc(tag), esc(tag), esc(ui[tag]), esc(it['title']), paragraphs(it.get('body', '')), b))


def main():
    shutil.rmtree(OUT, ignore_errors=True)
    site = load('content', 'site.json')
    releases = load('content', 'releases.json')
    shutil.copytree(os.path.join(ROOT, 'assets'), os.path.join(OUT, 'assets'))
    if os.path.exists(os.path.join(ROOT, 'CNAME')):
        shutil.copy(os.path.join(ROOT, 'CNAME'), os.path.join(OUT, 'CNAME'))
    write('index.html', '''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Nexwall</title>
<script>(function(){var m={en:'en/',es:'es/',pt:'pt-BR/'};var l=(navigator.language||'en').slice(0,2).toLowerCase();var s=null;try{s=localStorage.getItem('nx-lang')}catch(e){}location.replace(s||m[l]||'en/')})();</script>
</head><body><p><a href="en/">English</a> &middot; <a href="es/">Español</a> &middot; <a href="pt-BR/">Português (Brasil)</a></p></body></html>''')
    write('404.html', '<!doctype html><meta charset="utf-8"><title>404</title><p><a href="/">Nexwall release notes</a></p>')
    urls = []
    for lang, _ in LANGS:
        ui = UI[lang]
        pname = site['product'][lang]
        notes = {r['version']: load('content', r['version'], lang + '.json') for r in releases}
        latest = releases[0]
        cards = ''.join('''<a class="card release" href="{v}/"><div class="card-top"><span class="ver">{v}</span><span class="status status-{s}">{sl}</span></div>
<h3>{t}</h3><p>{sm}</p><div class="card-meta"><span>{dl}: <time datetime="{d}">{nd}</time></span></div></a>'''.format(
            v=esc(r['version']), s=esc(r['status']), sl=esc(ui[r['status']]), t=esc(notes[r['version']]['title']), sm=esc(notes[r['version']]['summary']),
            dl=esc(ui['date']), d=esc(r['date']), nd=esc(nice(lang, r['date']))) for r in releases)
        body = '''<main id="main"><section class="hero"><div class="wrap"><p class="eyebrow">{eb}</p><h1>{pn}</h1><p class="lead">{lead}</p>
<p><a class="btn" href="{lv}/">{ll}: {lv}</a> <span class="latest-date"><time datetime="{ld}">{lnd}</time></span></p></div></section>
<section class="wrap"><h2>{all}</h2><div class="grid">{cards}</div></section></main>'''.format(
            eb=esc(ui['eyebrow']), pn=esc(pname), lead=esc(site['lead'][lang] + ' ' + ui['lead_suffix']), lv=esc(latest['version']), ll=esc(ui['latest']),
            ld=esc(latest['date']), lnd=esc(nice(lang, latest['date'])), all=esc(ui['all']), cards=cards)
        write('%s/index.html' % lang, shell(lang, site, '%s | %s | Nexwall' % (ui['eyebrow'], pname), site['lead'][lang], body, 1, ''))
        urls.append('%s/' % lang)
        for r in releases:
            n = notes[r['version']]
            body = '''<main id="main"><section class="release-head"><div class="wrap"><p class="crumbs"><a href="../">{back}</a></p>
<h1>{pn} {v}</h1><p class="lead">{sm}</p><p class="meta"><span class="status status-{s}">{sl}</span><span>{dl}: <time datetime="{d}">{nd}</time></span></p></div></section>
<section class="wrap" style="padding-top:1.5rem;padding-bottom:3rem">{items}</section></main>'''.format(
                back=esc(ui['back']), pn=esc(pname), v=esc(r['version']), sm=esc(n['summary']), s=esc(r['status']), sl=esc(ui[r['status']]),
                dl=esc(ui['date']), d=esc(r['date']), nd=esc(nice(lang, r['date'])), items=''.join(item(ui, i) for i in n['items']))
            write('%s/%s/index.html' % (lang, r['version']), shell(lang, site, '%s %s | Nexwall' % (pname, r['version']), n['summary'], body, 2, r['version'] + '/'))
            urls.append('%s/%s/' % (lang, r['version']))
    host = site['host']
    write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n' % ''.join('<url><loc>https://%s/%s</loc></url>\n' % (host, u) for u in urls))
    write('robots.txt', 'User-agent: *\nAllow: /\nSitemap: https://%s/sitemap.xml\n' % host)
    print('%d pages' % (len(urls) + 3))


if __name__ == '__main__':
    main()
