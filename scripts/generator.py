import json
import os
import datetime
from pathlib import Path

# Configuration
BASE_URL = "https://pires94.github.io/Amazon-ES-Air-quality-reviews/"
CONTENT_DIR = Path("content")
SITE_DIR = Path("site")
ARTICLES_DIR = SITE_DIR / "articles"
TEMPLATES_DIR = Path("templates")
METADATA_FILE = CONTENT_DIR / "metadata.json"
KEYWORDS_FILE = CONTENT_DIR / "keywords.json"

class Generator:
    def __init__(self):
        self.metadata = self.load_json(METADATA_FILE, [])
        self.keywords = self.load_json(KEYWORDS_FILE, {})
        self.article_template = self.load_file(TEMPLATES_DIR / "article.html")
        
        # Define Silos
        self.silos = {
            "purificadores": {
                "name": "Purificadores de Aire",
                "index": "#purificadores",
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

    def generate_article_content(self, article, cluster_key):
        tag = "pires940f-21"
        # Realistic SEO-optimized content generation in Spain Spanish
        keywords = ", ".join(self.keywords.get(cluster_key, [])[:3])
        content = f"""
        <p>Encontrar el producto adecuado para mejorar la calidad del aire en tu hogar puede ser un desafío. Especialmente cuando buscas <strong>{article['title'].lower()}</strong> en España, donde las condiciones climáticas varían tanto de una región a otra.</p>
        
        <h2>Por qué es importante elegir bien</h2>
        <p>La mala calidad del aire puede afectar seriamente a tu salud y bienestar. Ya sea que sufras de alergias, tengas una casa con demasiada humedad o el aire esté excesivamente seco en invierno, la elección correcta marcará la diferencia. En esta guía analizamos los mejores modelos disponibles en <strong>Amazon.es</strong>.</p>
        
        <h2>Tabla Comparativa de Productos Recomendados</h2>
        <table class="product-table">
            <thead>
                <tr>
                    <th>Modelo</th>
                    <th>Característica Principal</th>
                    <th>Ideal para</th>
                    <th>Precio</th>
                    <th>Acción</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Modelo Premium Pro</td>
                    <td>Filtro HEPA H13</td>
                    <td>Salones grandes</td>
                    <td>⭐⭐⭐⭐⭐</td>
                    <td><a href="https://www.amazon.es/?tag={tag}" class="cta-button">Ver en Amazon</a></td>
                </tr>
                <tr>
                    <td>Compact Eco-Friendly</td>
                    <td>Bajo Consumo</td>
                    <td>Dormitorios</td>
                    <td>⭐⭐⭐⭐</td>
                    <td><a href="https://www.amazon.es/?tag={tag}" class="cta-button">Ver en Amazon</a></td>
                </tr>
                <tr>
                    <td>Advanced Silent Mod</td>
                    <td>Ultra Silencioso</td>
                    <td>Bebés / Noche</td>
                    <td>⭐⭐⭐⭐⭐</td>
                    <td><a href="https://www.amazon.es/?tag={tag}" class="cta-button">Ver en Amazon</a></td>
                </tr>
            </tbody>
        </table>

        <h2>Análisis de los Mejores Modelos</h2>
        <h3>1. Modelo Premium Pro</h3>
        <p>Este modelo destaca por su eficiencia energética y su capacidad para filtrar partículas de hasta 0.3 micras. Es perfecto para quienes buscan la máxima calidad sin compromisos.</p>
        <div class="pros-cons">
            <div class="pros"><strong>Pros:</strong> <ul><li>Filtro de alta eficiencia</li><li>Control inteligente</li><li>Diseño elegante</li></ul></div>
            <div class="cons"><strong>Contras:</strong> <ul><li>Precio algo elevado</li><li>Filtros de repuesto costosos</li></ul></div>
        </div>

        <h3>2. Compact Eco-Friendly</h3>
        <p>Si el espacio es un problema, este modelo compacto es la solución ideal. Ofrece un rendimiento sorprendente para su tamaño.</p>
        <div class="pros-cons">
            <div class="pros"><strong>Pros:</strong> <ul><li>Muy ligero</li><li>Silencioso</li><li>Precio competitivo</li></ul></div>
            <div class="cons"><strong>Contras:</strong> <ul><li>No recomendado para salas de más de 20m2</li></ul></div>
        </div>

        <h2>Guía de Compra: Qué tener en cuenta</h2>
        <p>Al comprar un aparato para el aire, fíjate siempre en el CADR (Clean Air Delivery Rate), el nivel de ruido en decibelios y el coste de mantenimiento de los filtros. No olvides revisar las opiniones en Amazon.es de otros usuarios en España.</p>

        <div class="faq">
            <h3>Preguntas Frecuentes (FAQ)</h3>
            <dl>
                <dt>¿Consume mucha electricidad?</dt>
                <dd>La mayoría de los modelos modernos están diseñados para ser eficientes, consumiendo menos que una bombilla tradicional.</dd>
                <dt>¿Cada cuánto hay que cambiar los filtros?</dt>
                <dd>Dependerá del uso, pero generalmente se recomienda cada 6-12 meses.</dd>
            </dl>
        </div>
        """
        return content

    def run(self):
        ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
        existing_slugs = [a['slug'] for a in self.metadata]
        new_articles_count = 0

        for silo_key, silo_data in self.silos.items():
            for article in silo_data['articles']:
                if article['slug'] in existing_slugs:
                    continue

                # Prepare metadata
                article_meta = {
                    "slug": article['slug'],
                    "title": article['title'],
                    "h1": article['h1'],
                    "cluster": silo_key,
                    "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                    "description": f"Análisis y guía de compra sobre {article['title']}. Encuentra el mejor producto en Amazon.es para mejorar la calidad de aire en tu casa."
                }

                # Generate Content
                content = self.generate_article_content(article, silo_key)
                
                # Internal links (within same cluster)
                related = [
                    {"url": f"{a['slug']}.html", "text": a['title']} 
                    for a in silo_data['articles'] if a['slug'] != article['slug']
                ]

                # Render Template
                html = self.article_template
                html = html.replace("{{ title }}", article_meta['title'])
                html = html.replace("{{ h1 }}", article_meta['h1'])
                html = html.replace("{{ description }}", article_meta['description'])
                html = html.replace("{{ content }}", content)
                html = html.replace("{{ slug }}", article_meta['slug'])
                html = html.replace("{{ cluster_name }}", silo_data['name'])
                html = html.replace("{{ cluster_index }}", "index.html" + silo_data['index'])
                
                # Simple loop replacement for related links
                links_html = "".join([f'<li><a href="{r["url"]}">{r["text"]}</a></li>' for r in related[:2]])
                html = html.replace("{% for link in related_links %}", "").replace("{% endfor %}", "")
                html = html.replace('<li><a href="{{ link.url }}">{{ link.text }}</a></li>', links_html)

                # Save file
                self.write_file(ARTICLES_DIR / f"{article['slug']}.html", html)
                
                # Update metadata
                self.metadata.append(article_meta)
                existing_slugs.append(article['slug'])
                new_articles_count += 1
                
        self.save_json(METADATA_FILE, self.metadata)
        self.generate_index()
        self.generate_sitemap()
        self.generate_robots()
        print(f"Generación completada. {new_articles_count} artículos nuevos creados.")

    def generate_index(self):
        index_html = f"""<!DOCTYPE html>
<html lang="es-ES">
<head>
    <meta charset="UTF-8">
    <title>Melhor Ar Casa - Guía de Calidad de Aire y Amazon.es</title>
    <meta name="description" content="Guía especializada en Purificadores, Deshumidificadores y Humidificadores. Encuentra el mejor equipo para tu hogar.">
    <style>
        body {{ font-family: sans-serif; line-height: 1.6; max-width: 1000px; margin: 0 auto; padding: 20px; background: #f4f7f6; color: #333; }}
        header {{ background: #2563eb; color: white; padding: 40px; text-align: center; border-radius: 10px; margin-bottom: 30px; }}
        .cluster {{ background: white; padding: 25px; margin-bottom: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        h2 {{ color: #2563eb; border-bottom: 2px solid #eef2f3; padding-bottom: 10px; }}
        ul {{ list-style: none; padding: 0; }}
        li {{ margin-bottom: 12px; }}
        a {{ text-decoration: none; color: #1e40af; font-weight: 500; }}
        a:hover {{ text-decoration: underline; }}
        .silo-link {{ display: block; background: #eef2f3; padding: 10px; border-radius: 5px; }}
    </style>
</head>
<body>
    <header>
        <h1>Melhor Ar Casa</h1>
        <p>Tu guía experta para el mejor aire en el hogar (Amazon.es)</p>
    </header>
    <main>
        <section class="cluster" id="purificadores">
            <h2>🌬️ Purificadores de Aire</h2>
            <ul>
                {"".join([f'<li><a href="articles/{a["slug"]}.html">{a["title"]}</a></li>' for a in self.metadata if a["cluster"] == "purificadores"])}
            </ul>
        </section>
        <section class="cluster" id="deshumidificadores">
            <h2>💧 Deshumidificadores</h2>
            <ul>
                {"".join([f'<li><a href="articles/{a["slug"]}.html">{a["title"]}</a></li>' for a in self.metadata if a["cluster"] == "deshumidificadores"])}
            </ul>
        </section>
        <section class="cluster" id="humidificadores">
            <h2>🌫️ Humidificadores</h2>
            <ul>
                {"".join([f'<li><a href="articles/{a["slug"]}.html">{a["title"]}</a></li>' for a in self.metadata if a["cluster"] == "humidificadores"])}
            </ul>
        </section>
        <section class="cluster" id="comparativas">
            <h2>⚖️ Comparativas</h2>
            <ul>
                {"".join([f'<li><a href="articles/{a["slug"]}.html">{a["title"]}</a></li>' for a in self.metadata if a["cluster"] == "comparativas"])}
            </ul>
        </section>
    </main>
    <footer style="text-align: center; margin-top: 50px; color: #777;">
        <p>© 2024 Melhor Ar Casa. Participamos en el Programa de Afiliados de Amazon.es.</p>
    </footer>
</body>
</html>"""
        self.write_file(SITE_DIR / "index.html", index_html)

    def generate_sitemap(self):
        sitemap = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        sitemap += f'  <url><loc>{BASE_URL}</loc><priority>1.0</priority></url>\n'
        for article in self.metadata:
            sitemap += f'  <url><loc>{BASE_URL}articles/{article["slug"]}.html</loc><lastmod>{article["date"]}</lastmod><priority>0.8</priority></url>\n'
        sitemap += '</urlset>'
        self.write_file(SITE_DIR / "sitemap.xml", sitemap)

    def generate_robots(self):
        robots = f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}sitemap.xml"
        self.write_file(SITE_DIR / "robots.txt", robots)

if __name__ == "__main__":
    Generator().run()
