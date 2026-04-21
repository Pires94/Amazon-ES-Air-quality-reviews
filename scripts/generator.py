import json
import os
import datetime
import hashlib
from pathlib import Path

# Configuration
BASE_URL = "https://pires94.github.io/Amazon-ES-Air-quality-reviews/"
CONTENT_DIR = Path("content")
SITE_DIR = Path(".")
ARTICLES_DIR = SITE_DIR / "articles"
TEMPLATES_DIR = Path("templates")
METADATA_FILE = CONTENT_DIR / "metadata.json"
KEYWORDS_FILE = CONTENT_DIR / "keywords.json"

class Generator:
    def __init__(self):
        self.metadata = self.load_json(METADATA_FILE, [])
        self.keywords = self.load_json(KEYWORDS_FILE, {})
        self.article_template = self.load_file(TEMPLATES_DIR / "article.html")
        
        # Expert Insights Pool
        self.insights = {
            "air_quality": "Muchos modelos económicos fallan al detectar PM2.5 (partículas finas). Un sensor de precisión láser es clave para automatizar el filtrado de forma real y no solo por tiempo.",
            "humidity": "Una humedad por encima del 60% no solo es incómoda; es el caldo de cultivo perfecto para el moho negro, que puede causar problemas respiratorios crónicos en niños.",
            "sleep": "Cualquier dispositivo por encima de los 25dB en modo noche puede fragmentar el sueño profundo, aunque no te despiertes del todo. El ruido blanco estable es preferible al intermitente.",
            "filters": "El marketing del 'Filtro HEPA' a veces oculta que no son filtros H13 grado médico. Solo un H13 garantiza retener el 99.97% de partículas de 0.3 micras."
        }

        self.silos = {
            "purificadores": {
                "name": "Purificadores de Aire",
                "index": "#purificadores",
                "fallback": "purificadores.jpg",
                "image_ids": ["photo-1584622650111-993a426fbf0a", "photo-1599423300746-b62533397364", "photo-1614035030394-b6e5b01e0737", "photo-1532003885409-ed84d334f6ee"],
                "articles": [
                    {"slug": "purificador-aire-habitacion-pequena", "title": "Mejor Purificador de Aire para Habitación Pequeña", "h1": "¿Buscas el mejor purificador para una habitación pequeña?", "angle": "efficiency"},
                    {"slug": "purificador-aire-100-euros", "title": "Purificadores de Aire por menos de 100 Euros", "h1": "Los Mejores Purificadores de Aire Económicos (Menos de 100€)", "angle": "price"},
                    {"slug": "purificador-aire-alergias", "title": "Purificadores de Aire para Alergias: Guía Definitiva", "h1": "Dile adiós a las alergias con estos purificadores", "angle": "health"},
                    {"slug": "purificador-aire-silencioso-noite", "title": "Purificadores de Aire Silenciosos para la Noche", "h1": "Duerme tranquilo: Los purificadores más silenciosos del mercado", "angle": "stealth"}
                ],
                "recommended_products": [
                    {"name": "Levoit Core 300S", "type": "HEPA H13", "strength": "CADR 240 m³/h", "price": "€€", "link": "https://www.amazon.es/dp/B087V7N59N?tag=pires940f-21"},
                    {"name": "Xiaomi Smart Air Purifier 4", "type": "Smart Filter", "strength": "CADR 400 m³/h", "price": "€€€", "link": "https://www.amazon.es/dp/B09M92CDY4?tag=pires940f-21"},
                    {"name": "Cecotec TotalPure 2500", "type": "Básico", "strength": "CADR 200 m³/h", "price": "€", "link": "https://www.amazon.es/dp/B08NX96D98?tag=pires940f-21"}
                ]
            },
            "deshumidificadores": {
                "name": "Deshumidificadores",
                "index": "#deshumidificadores",
                "fallback": "deshumidificadores.jpg",
                "image_ids": ["photo-1582738411706-bfc8e691d1c2", "photo-1595191630225-03bcb07378ac", "photo-1560185127-6ed189bf02f4"],
                "articles": [
                    {"slug": "deshumidificador-casa-humeda", "title": "Soluciones para una Casa Húmeda", "h1": "Cómo eliminar la humedad excesiva en tu hogar", "angle": "efficiency"},
                    {"slug": "deshumidificador-habitacion-pequena", "title": "Deshumidificador para Habitación Pequeña", "h1": "El deshumidificador ideal para espacios compactos", "angle": "efficiency"},
                    {"slug": "deshumidificador-150-euros", "title": "Mejores Deshumidificadores por 150 Euros", "h1": "Eficiencia y ahorro: Deshumidificadores por menos de 150€", "angle": "price"},
                    {"slug": "deshumidificador-consumo-energia", "title": "Deshumidificadores de Bajo Consumo", "h1": "Ahorra en tu factura de luz con estos deshumidificadores", "angle": "price"},
                    {"slug": "deshumidificador-portatil-opiniones", "title": "Opiniones sobre Deshumidificadores Portátiles", "h1": "Guía de compra: Deshumidificadores portátiles analizados", "angle": "comparison"}
                ],
                "recommended_products": [
                    {"name": "De'Longhi Tasciugo AriaDry", "type": "Compresor", "strength": "20L / 24h", "price": "€€€", "link": "https://www.amazon.es/dp/B01B4XU6N6?tag=pires940f-21"},
                    {"name": "Pro Breeze 12L", "type": "Compacto", "strength": "12L / 24h", "price": "€€", "link": "https://www.amazon.es/dp/B01G7SGNW8?tag=pires940f-21"},
                    {"name": "Cecotec BigDry 2000", "type": "Peltier", "strength": "0.3L / 24h", "price": "€", "link": "https://www.amazon.es/dp/B07N7T4G1C?tag=pires940f-21"}
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

    def generate_expert_content(self, article, silo_key):
        angle = article.get("angle", "efficiency")
        products = self.silos[silo_key].get("recommended_products", [])
        
        # 1. INTRODUCTION (Problem based)
        intros = {
            "price": f"<p>Si estás buscando <strong>{article['title'].lower()}</strong>, probablemente ya te has dado cuenta de que el mercado está inundado de opciones mediocres. Como analista, mi objetivo es ayudarte a filtrar el marketing y encontrar lo que realmente vale cada euro de tu presupuesto.</p>",
            "health": f"<p>Cuando hablamos de <strong>{article['title'].lower()}</strong>, no solo hablamos de confort, hablamos de salud. Las partículas PM2.5 y los alérgenos no perdonan, y elegir el equipo equivocado puede ser una pérdida de tiempo y bienestar. Te voy a ayudar a decidir con datos técnicos.</p>",
            "stealth": f"<p>¿De qué sirve mejorar el aire si el ruido no te deja dormir? En esta guía sobre <strong>{article['title'].lower()}</strong>, nos enfocamos en el equilibrio perfecto entre rendimiento y silencio absoluto. Vamos a separar los modelos que 'susurran' de los que 'rugen'.</p>",
            "efficiency": f"<p>Optimizar el espacio es clave. Para <strong>{article['title'].lower()}</strong>, buscamos modelos que ocupen poco pero rindan mucho. No te dejes engañar por el tamaño compacto: la potencia real se mide en la capacidad de procesado del aire.</p>",
            "comparison": f"<p>Navegar entre decenas de especificaciones es agotador. Para entender realmente <strong>{article['title'].lower()}</strong>, hemos comparado los modelos líderes cara a cara. Aquí no hay favoritos por marca, solo ganadores por rendimiento.</p>"
        }
        intro = intros.get(angle, intros["efficiency"])

        # 2. QUICK RECOMMENDATION
        best_product = products[0] if products else {"name": "Modelo Premium", "link": "#"}
        rec_block = f"""
        <div class="expert-box" style="background:#fff7ed; padding:1.5rem; border-radius:12px; border-left:5px solid #f97316; margin:2rem 0;">
            <h4 style="margin:0 0 0.5rem 0; color:#c2410c;">📍 Recomendación Rápida de Experto</h4>
            <p style="margin:0;">Si buscas la opción más equilibrada hoy: El <strong>{best_product['name']}</strong> es nuestra elección. Su relación entre capacidad y eficiencia energética lo sitúa por encima de la competencia en el mercado español.</p>
            <a href="{best_product['link']}" style="display:inline-block; margin-top:0.8rem; font-weight:700; color:#c2410c;">Ver precio actual en Amazon &rarr;</a>
        </div>
        """

        # 3. COMPARISON TABLE
        rows = "".join([f"<tr><td><strong>{p['name']}</strong></td><td>{p['type']}</td><td>{p['strength']}</td><td>{p['price']}</td><td><a href='{p['link']}' class='cta-small'>Comprobar</a></td></tr>" for p in products])
        table = f"""
        <h2>Comparativa de Modelos Recomendados</h2>
        <div style="overflow-x:auto;">
            <table class="product-table">
                <thead><tr><th>Modelo</th><th>Tecnología</th><th>Capacidad/Potencia</th><th>Rango Precio</th><th>Acción</th></tr></thead>
                <tbody>{rows}</tbody>
            </table>
        </div>
        """

        # 4. PRODUCT ANALYSIS
        analysis = "<h2>Análisis Detallado: ¿Cuál es para ti?</h2>"
        for p in products:
            analysis += f"""
            <div class="product-card" style="margin-bottom:3rem;">
                <h3>{p['name']} - La apuesta segura</h3>
                <p>Este modelo destaca por su {p['type']}. Es ideal para usuarios que no quieren complicaciones técnicas y buscan un rendimiento estable desde el primer minuto.</p>
                <div class="pros-cons">
                    <div class="p-block pros"><h4>Por qué elegirlo</h4><ul><li>Alto rendimiento en {p['strength']}</li><li>Construcción robusta</li><li>Fácil mantenimiento</li></ul></div>
                    <div class="p-block cons"><h4>Puntos débiles</h4><ul><li>Precio inicial superior a la media</li><li>Manual de usuario mejorable</li></ul></div>
                </div>
                <a href="{p['link']}" class="cta-button">Ver opiniones reales en Amazon</a>
            </div>
            """

        # 5. BUYING GUIDE & 6. REAL-WORLD INSIGHT
        insight_key = "air_quality" if silo_key == "purificadores" else "humidity"
        insight = self.insights.get(insight_key, "")
        guide = f"""
        <h2>Guía de Compra: Lo que el marketing no te cuenta</h2>
        <p>Al elegir tu equipo, olvida las etiquetas de colores. Lo que realmente importa es:</p>
        <ul>
            <li><strong>Capacidad Real:</strong> No midas por metros cuadrados, mide por volumen de aire/hora.</li>
            <li><strong>Sensores:</strong> Si el aparato no tiene un sensor de partículas real, solo está trabajando a ciegas.</li>
        </ul>
        <div class="insight-strip" style="background:#f0f9ff; padding:1.5rem; border-radius:12px; margin:2rem 0;">
            <h4 style="margin:0 0 0.5rem 0; color:#0369a1;">💡 Insight del Analista</h4>
            <p style="margin:0;">{insight}</p>
        </div>
        """

        # 7. FAQ
        faq = f"""
        <h2>Preguntas Frecuentes (FAQ)</h2>
        <div class="faq-item"><strong>¿Cuánto consume realmente al mes?</strong><p>En España, con los precios actuales de la luz, un modelo de bajo consumo apenas suma 3-5 euros a tu factura mensual si lo usas de forma inteligente.</p></div>
        <div class="faq-item"><strong>¿Cada cuánto debo limpiar los filtros?</strong><p>Para mantener el rendimiento, te recomendamos una revisión visual cada 15 días y un cambio profundo según las horas de uso (normalmente 6 meses).</p></div>
        """

        # 8. CONCLUSION
        conclusion = f"""
        <h2>Conclusión: Nuestra Decisión Final</h2>
        <p>Si sufres de problemas respiratorios severos, no escatimes: ve por el <strong>{best_product['name']}</strong>. Sin embargo, para una habitación secundaria o uso ocasional, las opciones más económicas de nuestra tabla cumplirán con creces.</p>
        <p><strong>¿Nuestra sugerencia?</strong> Comprueba ahora la disponibilidad, ya que el stock de estos modelos suele ser volátil durante las estaciones de alta demanda en Amazon.es.</p>
        """

        return intro + rec_block + table + analysis + guide + faq + conclusion

    def run(self):
        ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
        existing_slugs = [a['slug'] for a in self.metadata]
        
        for silo_key, silo_data in self.silos.items():
            for article in silo_data['articles']:
                article_meta = {
                    "slug": article['slug'], "title": article['title'], "h1": article['h1'],
                    "cluster": silo_key, "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                    "description": f"Análisis experto sobre {article['title']}. Ayudamos a decidir qué modelo comprar en Amazon.es."
                }

                content = self.generate_expert_content(article, silo_key)
                related = [ {"url": f"{a['slug']}.html", "text": a['title']} for a in silo_data['articles'] if a['slug'] != article['slug']]
                
                img_url = self.get_image_url(article['slug'], silo_key)
                # CSS Layered Fallback: Unsplash -> Local Silo Fallback -> Hero
                fallback_chain = f"url('{img_url}'), url('../assets/{silo_data['fallback']}'), url('../assets/hero.jpg')"
                
                html = self.article_template.replace("{{ title }}", article_meta['title']).replace("{{ h1 }}", article_meta['h1']).replace("{{ date }}", article_meta['date']).replace("{{ description }}", article_meta['description']).replace("{{ content }}", content).replace("{{ slug }}", article_meta['slug']).replace("{{ cluster_name }}", silo_data['name']).replace("{{ cluster_index }}", "../index.html#" + silo_key).replace("url('../assets/hero.jpg')", fallback_chain)
                
                # Contextual related links
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
    <main>{pur_cards}{des_cards}</main>
    <footer style="background:var(--navy); color:white; padding: 4rem 5%; text-align:center;"><p>© 2024 Melhor Ar Casa.</p></footer>
</body>
</html>"""
        self.write_file(SITE_DIR / "index.html", html)

    def render_silo_section(self, cluster_key, title):
        articles = [a for a in self.metadata if a.get("cluster") == cluster_key]
        if not articles: return ""
        cards = ""
        for a in articles:
            img_url = self.get_image_url(a['slug'], cluster_key)
            fallback_chain = f"url('{img_url}'), url('assets/{self.silos[cluster_key]['fallback']}'), url('assets/hero.jpg')"
            cards += f"""<a href="articles/{a['slug']}.html" class="card"><div class="card-img" style="background: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), {fallback_chain}; background-size: cover; background-position: center;"></div><div class="card-body"><span class="card-tag">{self.silos[cluster_key]['name']}</span><h3>{a['title']}</h3><p>Análisis técnico y comparativa para ayudarte a elegir tu equipo ideal...</p></div><div class="card-footer">Ver Análisis &rarr;</div></a>"""
        return f'<h2 class="section-title" id="{cluster_key}">{title}</h2><div class="card-grid">{cards}</div>'

    def generate_sitemap(self):
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        xml += f'  <url><loc>{BASE_URL}</loc></url>\n'
        for a in self.metadata: xml += f'  <url><loc>{BASE_URL}articles/{a["slug"]}.html</loc></url>\n'
        self.write_file(SITE_DIR / "sitemap.xml", xml + '</urlset>')

    def generate_robots(self):
        self.write_file(SITE_DIR / "robots.txt", f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}sitemap.xml")

if __name__ == "__main__":
    Generator().run()
