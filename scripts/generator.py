import json
import os
import datetime
import hashlib
from pathlib import Path

# Configuration
BASE_URL = "https://pires94.github.io/Amazon-ES-Air-quality-reviews/"
CONTENT_DIR = Path("content")
SITE_DIR = Path("docs")
ARTICLES_DIR = SITE_DIR / "articles"
TEMPLATES_DIR = Path("templates")
METADATA_FILE = CONTENT_DIR / "metadata.json"
KEYWORDS_FILE = CONTENT_DIR / "keywords.json"

class Generator:
    def __init__(self):
        self.metadata = self.load_json(METADATA_FILE, [])
        self.keywords = self.load_json(KEYWORDS_FILE, {})
        self.article_template = self.load_file(TEMPLATES_DIR / "article.html")
        
        # Curated pools of verified high-quality Unsplash IDs
        self.silos = {
            "purificadores": {
                "name": "Purificadores de Aire",
                "index": "#purificadores",
                "fallback": "purificadores.jpg",
                "image_ids": [
                    "photo-1584622650111-993a426fbf0a", "photo-1599423300746-b62533397364", 
                    "photo-1614035030394-b6e5b01e0737", "photo-1532003885409-ed84d334f6ee",
                    "photo-1585202900225-6d3ac20a6962", "photo-1558231013-17631379f835"
                ],
                "articles": [
                    {"slug": "purificador-aire-habitacion-pequena", "title": "Mejor Purificador de Aire para Habitación Pequeña", "h1": "¿Buscas el mejor purificador para una habitación pequeña?"},
                    {"slug": "purificador-aire-100-euros", "title": "Purificadores de Aire por menos de 100 Euros", "h1": "Los Mejores Purificadores de Aire Económicos (Menos de 100€)"},
                    {"slug": "purificador-aire-alergias", "title": "Purificadores de Aire para Alergias: Guía Definitiva", "h1": "Dile adiós a las alergias con estos purificadores"},
                    {"slug": "purificador-aire-silencioso-noite", "title": "Purificadores de Aire Silenciosos para la Noche", "h1": "Duerme tranquilo: Los purificadores más silenciosos del mercado"}
                ]
            },
            "deshumidificadores": {
                "name": "Deshumidificadores",
                "index": "#deshumidificadores",
                "fallback": "deshumidificadores.jpg",
                "image_ids": [
                    "photo-1582738411706-bfc8e691d1c2", "photo-1595191630225-03bcb07378ac",
                    "photo-1560185127-6ed189bf02f4", "photo-1520004434532-668416a08753",
                    "photo-1556911220-e15b29be8c8f", "photo-1512918728675-ed5a9ecdebfd"
                ],
                "articles": [
                    {"slug": "deshumidificador-casa-humeda", "title": "Soluciones para una Casa Húmeda", "h1": "Cómo eliminar la humedad excesiva en tu hogar"},
                    {"slug": "deshumidificador-habitacion-pequena", "title": "Deshumidificador para Habitación Pequeña", "h1": "El deshumidificador ideal para espacios compactos"},
                    {"slug": "deshumidificador-150-euros", "title": "Mejores Deshumidificadores por 150 Euros", "h1": "Eficiencia y ahorro: Deshumidificadores por menos de 150€"},
                    {"slug": "deshumidificador-consumo-energia", "title": "Deshumidificadores de Bajo Consumo", "h1": "Ahorra en tu factura de luz con estos deshumidificadores"},
                    {"slug": "deshumidificador-portatil-opiniones", "title": "Opiniones sobre Deshumidificadores Portátiles", "h1": "Guía de compra: Deshumidificadores portátiles analizados"}
                ]
            },
            "humidificadores": {
                "name": "Humidificadores",
                "index": "#humidificadores",
                "fallback": "humidificadores.jpg",
                "image_ids": [
                    "photo-1511974035430-5de47d3b95da", "photo-1526947425960-945c6e7393fe",
                    "photo-1510218830377-1e93b3846665", "photo-1490818387583-1baba5e638af",
                    "photo-1563298723-dcfebaa392e3", "photo-1449247709967-d4461a6a6103"
                ],
                "articles": [
                    {"slug": "humidificador-habitacion-seca", "title": "Humidificador para Habitación Seca", "h1": "Combate el aire seco con estos humidificadores"},
                    {"slug": "humidificador-bebes-seguro", "title": "Humidificadores Seguros para Bebés", "h1": "La seguridad de tu bebé es lo primero: Humidificadores recomendados"},
                    {"slug": "humidificador-silencioso", "title": "El Humidificador más Silencioso de 2024", "h1": "Humidificadores ultrasónicos silenciosos para tu dormitorio"},
                    {"slug": "humidificador-invierno-vale-la-pena", "title": "¿Vale la pena un humidificador en invierno?", "h1": "Humidificadores en invierno: Todo lo que necesitas saber"}
                ]
            },
            "comparativas": {
                "name": "Comparativas",
                "index": "#comparativas",
                "fallback": "comparativas.jpg",
                "image_ids": [
                    "photo-1460925895917-afdab827c52f", "photo-1451187580459-43490279c0fa",
                    "photo-1421757295538-9c80958e7520", "photo-1519389950473-47ba0277781c",
                    "photo-1504384308090-c894fdcc538d", "photo-1484417894907-623942c8ee29"
                ],
                "articles": [
                    {"slug": "purificador-vs-deshumidificador", "title": "Purificador vs Deshumidificador: ¿Cuál necesitas?", "h1": "Diferencias clave: Purificador vs Deshumidificador"},
                    {"slug": "humidificador-vs-deshumidificador", "title": "Humidificador vs Deshumidificador: Guía Comparativa", "h1": "Humidificador o Deshumidificador: Resolvemos tus dudas"},
                    {"slug": "mejor-aparato-humedad-casa", "title": "Mejor Aparato para la Humedad en Casa", "h1": "Análisis definitivo: El mejor aparato para controlar la humedad"}
                ]
            }
        }

    def load_json(self, path, default):
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return default

    def load_file(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    def save_json(self, path, data):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def write_file(self, path, content):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

    def get_image_url(self, slug, silo_key):
        silo = self.silos[silo_key]
        ids = silo['image_ids']
        idx = int(hashlib.md5(slug.encode()).hexdigest(), 16) % len(ids)
        photo_id = ids[idx]
        return f"https://images.unsplash.com/{photo_id}?auto=format&fit=crop&q=80&w=800"

    def generate_article_content(self, article, cluster_key):
        tag = "pires940f-21"
        content = f"""
        <p>Encontrar el producto adecuado para mejorar la calidad del aire en tu hogar puede ser un desafío. Especialmente cuando buscas <strong>{article['title'].lower()}</strong> en España, donde las condiciones climáticas varían tanto de una región a otra.</p>
        
        <h2>Por qué es importante elegir bien</h2>
        <p>La mala calidad del aire puede afectar seriamente a tu salud y bienestar. Ya sea que sufras de alergias, tengas una casa con demasiada humedad o el aire esté excesivamente seco en invierno, la elección correcta marcará la diferencia.</p>
        
        <table class="product-table">
            <thead>
                <tr>
                    <th>Modelo Destacado</th>
                    <th>Ventaja Principal</th>
                    <th>Precio Est.</th>
                    <th>Acción</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Premium Air Pro H13</strong></td>
                    <td>Filtrado Médico HEPA</td>
                    <td>⭐⭐⭐⭐⭐</td>
                    <td><a href="https://www.amazon.es/?tag={tag}" class="cta-button">Ver en Amazon</a></td>
                </tr>
                <tr>
                    <td><strong>Compact Silent Mode</strong></td>
                    <td>Ultra Silencioso</td>
                    <td>⭐⭐⭐⭐</td>
                    <td><a href="https://www.amazon.es/?tag={tag}" class="cta-button">Ver en Amazon</a></td>
                </tr>
            </tbody>
        </table>

        <h2>Análisis en Profundidad</h2>
        <div class="pros-cons">
            <div class="p-block pros">
                <h4>Lo que nos gusta</h4>
                <ul>
                    <li>Excelente relación calidad-precio</li>
                    <li>Consumo energético muy bajo</li>
                    <li>Soporte técnico directo de Amazon.es</li>
                </ul>
            </div>
            <div class="p-block cons">
                <h4>A mejorar</h4>
                <ul>
                    <li>Filtros algo costosos</li>
                    <li>Cable algo corto (1.5m)</li>
                </ul>
            </div>
        </div>

        <p>Al comprar un aparato para el aire, fíjate siempre en el CADR (Clean Air Delivery Rate), el nivel de ruido en decibelios y el coste de mantenimiento. No olvides revisar las opiniones en Amazon de otros usuarios.</p>
        """
        return content

    def run(self):
        ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
        existing_slugs = [a['slug'] for a in self.metadata]
        
        for silo_key, silo_data in self.silos.items():
            for article in silo_data['articles']:
                article_meta = {
                    "slug": article['slug'], "title": article['title'], "h1": article['h1'],
                    "cluster": silo_key, "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                    "description": f"Guía experta sobre {article['title']}."
                }

                content = self.generate_article_content(article, silo_key)
                related = [ {"url": f"{a['slug']}.html", "text": a['title']} for a in silo_data['articles'] if a['slug'] != article['slug']]
                
                img_url = self.get_image_url(article['slug'], silo_key)
                # CSS Layered Fallback: Unsplash -> Local Silo Fallback -> Hero
                fallback_chain = f"url('{img_url}'), url('../assets/{silo_data['fallback']}'), url('../assets/hero.jpg')"
                
                html = self.article_template.replace("{{ title }}", article_meta['title']).replace("{{ h1 }}", article_meta['h1']).replace("{{ date }}", article_meta['date']).replace("{{ description }}", article_meta['description']).replace("{{ content }}", content).replace("{{ slug }}", article_meta['slug']).replace("{{ cluster_name }}", silo_data['name']).replace("{{ cluster_index }}", "index.html" + silo_data['index']).replace("url('../assets/hero.jpg')", fallback_chain)
                
                links_html = "".join([f'<a href="{r["url"]}" class="related-card"><h4>{r["text"]}</h4></a>' for r in related[:3]])
                if '{% for link in related_links %}' in html:
                    parts = html.split('{% for link in related_links %}')
                    after_loop = parts[1].split('{% endfor %}')
                    html = parts[0] + links_html + after_loop[1]

                self.write_file(ARTICLES_DIR / f"{article['slug']}.html", html)
                if article['slug'] not in existing_slugs:
                    self.metadata.append(article_meta)
                    existing_slugs.append(article['slug'])
                
        self.save_json(METADATA_FILE, self.metadata)
        self.generate_index()
        self.generate_sitemap(); self.generate_robots()

    def generate_index(self):
        pur_cards = self.render_silo_section("purificadores", "🌬️ Recomendados: Purificadores")
        des_cards = self.render_silo_section("deshumidificadores", "💧 Soluciones de Humedad")
        hum_cards = self.render_silo_section("humidificadores", "🌫️ Confort: Humidificadores")
        com_cards = self.render_silo_section("comparativas", "⚖️ Comparativas")

        html = f"""<!DOCTYPE html>
<html lang="es-ES">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Melhor Ar Casa - Blog de Calidad de Aire</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Outfit:wght@500;700&display=swap" rel="stylesheet">
    <style>
        :root {{ --navy: #232f3e; --orange: #FF9900; --bg: #f7fafa; }}
        body {{ font-family: 'Inter', sans-serif; background: var(--bg); margin:0; color: #111827; }}
        header {{ background: white; padding: 1.5rem 5%; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        .logo {{ font-family: 'Outfit'; font-weight:700; font-size:1.5rem; color:var(--navy); text-decoration:none; }}
        .hero {{ background: linear-gradient(rgba(35, 47, 62, 0.7), rgba(35, 47, 62, 0.7)), url('assets/hero.jpg'); background-size: cover; background-position: center; padding: 8rem 5%; text-align: center; color: white; }}
        .hero h1 {{ font-family: 'Outfit', sans-serif; font-size: 3.5rem; margin:0; }}
        .hero p {{ font-size: 1.2rem; opacity: 0.9; max-width: 600px; margin: 1rem auto; }}
        main {{ max-width: 1200px; margin: 4rem auto; padding: 0 1.5rem; }}
        .section-title {{ font-family: 'Outfit', sans-serif; font-size: 2rem; margin-bottom: 2rem; border-bottom: 3px solid var(--orange); display: inline-block; }}
        .card-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 2.5rem; margin-bottom: 5rem; }}
        .card {{ background: white; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); transition: transform 0.2s, box-shadow 0.2s; text-decoration: none; color: inherit; display: flex; flex-direction: column; }}
        .card:hover {{ transform: translateY(-5px); box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1); }}
        .card-img {{ height: 200px; background: #e5e7eb; }}
        .card-body {{ padding: 1.5rem; flex-grow: 1; }}
        .card-tag {{ display: inline-block; background: #eef2ff; color: #4f46e5; padding: 0.2rem 0.6rem; border-radius: 9999px; font-size: 0.7rem; font-weight: 700; margin-bottom: 0.5rem; }}
        .card h3 {{ margin: 0.5rem 0; font-family: 'Outfit', sans-serif; font-size: 1.4rem; color: var(--navy); line-height: 1.2; }}
        .card p {{ font-size: 0.9rem; color: #6b7280; margin: 0.5rem 0 1rem 0; }}
        .card-footer {{ padding: 1rem 1.5rem; border-top: 1px solid #f3f4f6; font-size: 0.8rem; font-weight: 600; color: var(--orange); text-transform: uppercase; }}
    </style>
</head>
<body>
    <header><a href="index.html" class="logo">Melhor<span style="color:var(--orange);">Ar</span>Casa</a></header>
    <section class="hero"><h1>Tu Casa, Aire Puro</h1><p>Análisis y comparativas de los mejores aparatos de aire.</p></section>
    <main>
        {pur_cards}
        {des_cards}
        {hum_cards}
        {com_cards}
    </main>
    <footer style="background:var(--navy); color:white; padding: 4rem 5%; text-align:center;"><p>© 2024 Melhor Ar Casa.</p></footer>
</body>
</html>"""
        self.write_file(SITE_DIR / "index.html", html)

    def render_silo_section(self, cluster_key, title):
        articles = [a for a in self.metadata if a["cluster"] == cluster_key]
        if not articles: return ""
        cards = ""
        for a in articles:
            img_url = self.get_image_url(a['slug'], cluster_key)
            # CSS Layered Fallback: Unsplash -> Local Silo Fallback -> Hero
            fallback_chain = f"url('{img_url}'), url('assets/{self.silos[cluster_key]['fallback']}'), url('assets/hero.jpg')"
            cards += f"""
            <a href="articles/{a['slug']}.html" class="card">
                <div class="card-img" style="background: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), {fallback_chain}; background-size: cover; background-position: center;"></div>
                <div class="card-body">
                    <span class="card-tag">{self.silos[cluster_key]['name']}</span>
                    <h3>{a['title']}</h3>
                    <p>Guía completa y análisis detallado de los mejores modelos en Amazon.es...</p>
                </div>
                <div class="card-footer">Leer Artículo &rarr;</div>
            </a>"""
        return f'<h2 class="section-title" id="{cluster_key}">{title}</h2><div class="card-grid">{cards}</div>'

    def generate_sitemap(self):
        xml = '<?xml version="1.0" encoding="UTF-8"?>\\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\\n'
        xml += f'  <url><loc>{{BASE_URL}}</loc></url>\\n'
        for a in self.metadata: xml += f'  <url><loc>{{BASE_URL}}articles/{{a["slug"]}}.html</loc></url>\\n'
        self.write_file(SITE_DIR / "sitemap.xml", xml + '</urlset>')

    def generate_robots(self):
        self.write_file(SITE_DIR / "robots.txt", f"User-agent: *\\nAllow: /\\nSitemap: {{BASE_URL}}sitemap.xml")

if __name__ == "__main__":
    Generator().run()
