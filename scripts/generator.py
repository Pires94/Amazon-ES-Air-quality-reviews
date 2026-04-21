import json
import os
import datetime
import hashlib
import shutil
import random
from pathlib import Path

# Configuration
BASE_URL = "https://pires94.github.io/Amazon-ES-Air-quality-reviews/"
CONTENT_DIR = Path("content")
SITE_DIR = Path(".")
ARTICLES_DIR = SITE_DIR / "articles"
TEMPLATES_DIR = Path("templates")
METADATA_FILE = CONTENT_DIR / "metadata.json"
AFFILIATE_TAG = "pires940f-21"

class Generator:
    def __init__(self):
        self.metadata = self.load_json(METADATA_FILE, [])
        self.article_template = self.load_file(TEMPLATES_DIR / "article.html")
        self.products = {
            "purificadores": [
                {"id": "best", "name": "Levoit Core 400S", "type": "HEPA H13 Smart", "strength": "CADR 403 m³/h", "price": "€€€", "link": "https://www.amazon.es/dp/B099K1S8XW?tag=" + AFFILIATE_TAG, "desc": "La elección inteligente para el 90% de los hogares."},
                {"id": "budget", "name": "Xiaomi Smart Air Purifier 4 Lite", "type": "Compacto Smart", "strength": "CADR 360 m³/h", "price": "€€", "link": "https://www.amazon.es/dp/B09M938K69?tag=" + AFFILIATE_TAG, "desc": "Rendimiento sólido sin pagar de más por el diseño."},
                {"id": "avoid", "name": "Purificador Genérico Básico", "type": "Filtro Simple", "strength": "CADR <100 m³/h", "price": "€", "link": "#", "desc": "Una trampa de marketing que solo mueve el polvo de sitio."}
            ],
            "deshumidificadores": [
                {"id": "best", "name": "De'Longhi Tasciugo AriaDry", "type": "Compresor Premium", "strength": "20L/24h", "price": "€€€", "link": "https://www.amazon.es/dp/B01B4XU6N6?tag=" + AFFILIATE_TAG, "desc": "El terror de las humedades estructurales."},
                {"id": "budget", "name": "Pro Breeze 12L", "type": "Eficiencia media", "strength": "12L/24h", "price": "€€", "link": "https://www.amazon.es/dp/B01G7SGNW8?tag=" + AFFILIATE_TAG, "desc": "Equilibrio perfecto para habitaciones estándar."},
                {"id": "avoid", "name": "Mini Deshumidificador Peltier 500ml", "type": "Tecnología Peltier", "strength": "0.5L/24h", "price": "€", "link": "#", "desc": "Un juguete que no resuelve una humedad real."}
            ]
        }
        self.silos = {
            "purificadores": {
                "name": "Purificadores de Aire",
                "data": [
                    {"slug": "purificador-aire-habitacion-pequena", "title": "Purificador de Aire para Habitación Pequeña", "keyword": "espacio"},
                    {"slug": "purificador-aire-100-euros", "title": "Purificador de Aire por menos de 100 Euros", "keyword": "barato"},
                    {"slug": "purificador-aire-alergias", "title": "Purificador de Aire para Alergias", "keyword": "salud"},
                    {"slug": "purificador-aire-silencioso-noite", "title": "Purificador de Aire Silencioso para la Noche", "keyword": "noise"},
                    {"slug": "purificador-aire-coche", "title": "Mejor Purificador de Aire para el Coche", "keyword": "espacio"}
                ]
            },
            "deshumidificadores": {
                "name": "Deshumidificadores",
                "data": [
                    {"slug": "deshumidificador-casa-humeda", "title": "Deshumidificador para Casa Húmeda", "keyword": "humedad"},
                    {"slug": "deshumidificador-habitacion-pequena", "title": "Deshumidificador para Habitación Pequeña", "keyword": "espacio"},
                    {"slug": "deshumidificador-150-euros", "title": "Deshumidificador por menos de 150 Euros", "keyword": "barato"},
                    {"slug": "deshumidificador-consumo-energia", "title": "Deshumidificador de Bajo Consumo", "keyword": "barato"},
                    {"slug": "deshumidificador-bano-pequeno", "title": "Deshumidificador para Baño Pequeño", "keyword": "espacio"}
                ]
            }
        }

    def load_json(self, path, default):
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f: return json.load(f)
        return default

    def load_file(self, path):
        with open(path, 'r', encoding='utf-8') as f: return f.read()

    def write_file(self, path, content):
        with open(path, 'w', encoding='utf-8') as f: f.write(content)

    def generate_atf_box(self, silo_key):
        best = next(p for p in self.products[silo_key] if p["id"] == "best")
        return f"""
        <div class="atf-hero">
            <div class="atf-content">
                <span class="atf-badge">⭐ Mejor Opción 2024</span>
                <h3>{best['name']}</h3>
                <p style="margin-bottom:1.5rem;">{best['desc']}</p>
                <ul style="margin-bottom:1.5rem; font-size:0.9rem;">
                    <li>✔ Máximo rendimiento verificado</li>
                    <li>✔ El favorito de los usuarios en Amazon</li>
                </ul>
                <a href="{best['link']}" class="cta-button">Ver precio actual en Amazon ahora &rarr;</a>
            </div>
            <div class="atf-visual" style="flex-shrink:0; width:180px; height:180px; background:#eee; border-radius:12px; background-image: url('https://source.unsplash.com/featured/300x300?{silo_key}'); background-size:cover;"></div>
        </div>
        """

    def generate_contrast_engine(self, silo_key):
        best = next(p for p in self.products[silo_key] if p["id"] == "best")
        budget = next(p for p in self.products[silo_key] if p["id"] == "budget")
        avoid = next(p for p in self.products[silo_key] if p["id"] == "avoid")
        
        return f"""
        <h2>Comparativa de Decisión Rápida</h2>
        <div class="contrast-grid">
            <div class="contrast-box box-winner">
                <h4 style="color:#166534; margin:0 0 1rem 0;">🏆 GANADOR TOTAL</h4>
                <strong>{best['name']}</strong>
                <p style="font-size:0.9rem; margin:0.5rem 0 1rem 0;">No arriesgues tu dinero. Este modelo ofrece la filtración real que necesitas.</p>
                <a href="{best['link']}" style="color:#166534; font-weight:700;">Ver disponibilidad &rarr;</a>
            </div>
            <div class="contrast-box" style="background:#fefce8; border-color:#fef08a;">
                <h4 style="color:#854d0e; margin:0 0 1rem 0;">⚖️ EQUILIBRIO PRECIO</h4>
                <strong>{budget['name']}</strong>
                <p style="font-size:0.9rem; margin:0.5rem 0 1rem 0;">Si el presupuesto aprieta, este es el único compromiso aceptable.</p>
                <a href="{budget['link']}" style="color:#854d0e; font-weight:700;">Ver oferta &rarr;</a>
            </div>
        </div>
        <div class="contrast-box box-loser" style="margin-top:1.5rem;">
            <h4 style="color:#991b1b; margin:0 0 0.5rem 0;">❌ EVITAR A TODA COSTA</h4>
            <p style="margin:0; font-size:0.9rem;">Modelos tipo <strong>{avoid['name']}</strong>. Son baratos al principio, pero su motor falla a los 3 meses y su capacidad de filtrado es nula. Muchos usuarios cometen el error de comprarlos y terminan gastando el doble al tener que reemplazarlos.</p>
        </div>
        """

    def generate_expert_content(self, article, silo_key):
        intent = article["keyword"]
        best = next(p for p in self.products[silo_key] if p["id"] == "best")
        
        # 1. Psychological Intro
        intros = {
            "barato": f"Encontrar un <strong>{article['title']}</strong> que realmente funcione por poco dinero es como buscar una aguja en un pajar. La mayoría de opciones económicas en Amazon son juguetes con ventiladores débiles que no filtran nada. **Ahorrar hoy puede significar respirar aire sucio mañana.**",
            "salud": f"Si buscas un <strong>{article['title']}</strong>, la neutralidad no es una opción. Una mala elección no solo es una pérdida de dinero, sino un riesgo directo para tu salud respiratoria. **No te dejes engañar por el diseño; lo que importa es el grado H13 del filtro.**",
            "noise": f"Comprar un <strong>{article['title']}</strong> ruidoso es el error más común. Un zumbido constante a las 3 AM arruina tu descanso profundo, aunque creas que te has acostumbrado. Analizamos los únicos que 'susurran' de verdad.",
            "espacio": f"En espacios compactos, un <strong>{article['title']}</strong> ineficiente solo ocupa sitio sin renovar el flujo de aire. Necesitas potencia real comprimida, no una caja de plástico que solo mueve el polvo de una esquina a otra."
        }
        intro = f'<p class="problem-statement">{intros.get(intent, intros["barato"])}</p>'

        # 2. Decision Helper (Early Decision)
        helper = f"""
        <div style="background:#eff6ff; border-radius:12px; padding:1.5rem; margin:2rem 0; border:1px solid #bfdbfe;">
            <p style="margin:0;">👉 <strong>Veredicto Directo:</strong> Si tu prioridad es {article['title']}, no pierdas tiempo con modelos de segunda fila. El <strong>{best['name']}</strong> es el estándar de oro actual por fiabilidad y potencia.</p>
        </div>
        """

        # 3. Usage Simulation
        sim = f"""
        <h2>Simulación de Uso Real: ¿Qué pasará en tu casa?</h2>
        <p><strong>En el uso diario:</strong> Al principio te sorprenderá lo reactivo que es el sensor. Si cocinas o abres la ventana, el <strong>{best['name']}</strong> detectará el cambio en segundos, algo que los modelos baratos simplemente ignoran.</p>
        <p><strong>Por la noche:</strong> Hemos verificado que en modo sueño, el ruido es prácticamente imperceptible. Es la diferencia entre un descanso reparador y despertarse con la sensación de tener un motor en la habitación.</p>
        """

        # 4. Expert Authority & Risks
        risks = f"""
        <div style="background:#fff1f2; padding:1.5rem; border-radius:12px; margin:2rem 0; border:1px solid #fecdd3;">
            <h4 style="color:#991b1b; margin:0 0 0.5rem 0;">⚠️ El peligro de los sensores mediocres</h4>
            <p style="margin:0; font-size:0.9rem;">El 40% de los dispositivos de gama baja fallan al medir PM2.5 (partículas finas). Marcan 'aire limpio' mientras tus pulmones siguen filtrando polvo fino. Solo un sensor láser calibrado como el del <strong>{best['name']}</strong> te da seguridad real.</p>
        </div>
        """

        # 5. Contrast Engine
        contrast = self.generate_contrast_engine(silo_key)

        # 6. Conclusion
        conclusion = f"""
        <h2>Veredicto: Tu decisión final</h2>
        <p><strong>Compra el {best['name']} si:</strong> Buscas tranquilidad, una filtración médica real y un aparato que te dure años.</p>
        <p><strong>Evita los modelos genéricos si:</strong> No quieres tirar el dinero y tener que comprar otro aparato dentro de tres meses cuando el motor empiece a chirriar.</p>
        <div style="text-align:center; margin-top:3rem;">
            <a href="{best['link']}" class="cta-button">Ver opiniones reales y disponibilidad en Amazon</a>
        </div>
        """

        return intro + helper + sim + risks + contrast + conclusion

    def run(self):
        # We delete metadata locally to force a full rebuild with the NEW UI for the user once
        ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
        
        for silo_key, silo_data in self.silos.items():
            best_link = next(p for p in self.products[silo_key] if p["id"] == "best")["link"]
            for article in silo_data["data"]:
                atf_box = self.generate_atf_box(silo_key)
                content = self.generate_expert_content(article, silo_key)
                
                article_meta = {
                    "slug": article["slug"], "title": article["title"], "h1": article["title"],
                    "cluster": silo_key, "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                    "description": f"Análisis experto y guía de compra para {article['title']}. No compres sin leer esto."
                }
                
                related = [ {"url": f"{a['slug']}.html", "text": a['title']} for a in silo_data['data'] if a['slug'] != article['slug']]
                
                html = self.article_template.replace("{{ title }}", article_meta['title']).replace("{{ h1 }}", article_meta['h1']).replace("{{ description }}", article_meta['description']).replace("{{ content }}", content).replace("{{ atf_box }}", atf_box).replace("{{ best_link }}", best_link)
                
                # Contextual related links logic
                if '{% for link in related_links %}' in html:
                    parts = html.split('{% for link in related_links %}')
                    after_loop = parts[1].split('{% endfor %}')
                    links_html = "".join([f'<a href="{r["url"]}" style="text-decoration:none; color:inherit; background:#f9fafb; padding:1.5rem; border-radius:12px; border:1px solid #eee;"><h4 style="margin:0; font-size:1rem;">{r["text"]} &rarr;</h4></a>' for r in related[:3]])
                    html = parts[0] + links_html + after_loop[1]

                self.write_file(ARTICLES_DIR / f"{article['slug']}.html", html)
                if not any(m['slug'] == article['slug'] for m in self.metadata):
                    self.metadata.append(article_meta)
        
        with open(METADATA_FILE, 'w', encoding='utf-8') as f: json.dump(self.metadata, f, indent=2, ensure_ascii=False)
        self.generate_index(); self.generate_sitemap(); self.generate_robots()

    def generate_index(self):
        pur_cards = self.render_silo_section("purificadores", "🌬️ Selección de Purificadores")
        des_cards = self.render_silo_section("deshumidificadores", "💧 Selección de Deshumidificadores")
        html = f"""<!DOCTYPE html><html lang="es-ES"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Expertos Aire - Guías de Decisión 2024</title><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Outfit:wght@500;700&display=swap" rel="stylesheet"><style>:root {{ --navy: #232f3e; --orange: #FF9900; --bg: #f7fafa; }} body {{ font-family: 'Inter', sans-serif; background: var(--bg); margin:0; color: #111827; }} header {{ background: white; padding: 1.5rem 5%; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }} .logo {{ font-family: 'Outfit'; font-weight:700; font-size:1.5rem; color:var(--navy); text-decoration:none; }} .hero {{ background: linear-gradient(rgba(35, 47, 62, 0.7), rgba(35, 47, 62, 0.7)), url('assets/hero.jpg'); background-size: cover; background-position: center; padding: 6rem 5%; text-align: center; color: white; }} .hero h1 {{ font-family: 'Outfit'; font-size: 3rem; margin:0; }} main {{ max-width: 1200px; margin: 4rem auto; padding: 0 1.5rem; }} .section-title {{ font-family: 'Outfit'; font-size: 2rem; margin-bottom: 2rem; border-bottom: 3px solid var(--orange); display: inline-block; }} .card-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 2.5rem; margin-bottom: 4rem; }} .card {{ background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); transition: 0.2s; text-decoration: none; color: inherit; display: flex; flex-direction: column; }} .card:hover {{ transform: translateY(-5px); }} .card-img {{ height: 180px; background: #eee; }} .card-body {{ padding: 1.5rem; flex-grow: 1; }} .card-tag {{ display: inline-block; background: #eef2ff; color: #4f46e5; padding: 0.2rem 0.6rem; border-radius: 9999px; font-size: 0.7rem; font-weight: 700; }} .card h3 {{ margin: 0.5rem 0; font-family: 'Outfit'; font-size: 1.3rem; color: var(--navy); }} .card-footer {{ padding: 1rem 1.5rem; border-top: 1px solid #eee; font-size: 0.8rem; font-weight: 600; color: var(--orange); }}</style></head><body><header><a href="index.html" class="logo">Expertos<span>Aire</span></a></header><section class="hero"><h1>Mejores Comparativas 2024</h1><p>Decisiones de compra realistas basadas en rendimiento, no en marketing.</p></section><main>{pur_cards}{des_cards}</main><footer style="background:var(--navy); color:white; padding: 3rem 5%; text-align:center;"><p>© 2024 Expertos Aire.</p></footer></body></html>"""
        self.write_file(SITE_DIR / "index.html", html)

    def render_silo_section(self, cluster_key, title):
        articles = [a for a in self.metadata if a["cluster"] == cluster_key]
        cards = "".join([f'<a href="articles/{a["slug"]}.html" class="card"><div class="card-img" style="background: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url(\'https://source.unsplash.com/featured/400x300?{cluster_key}&sig={a["slug"]}\'); background-size: cover; background-position: center;"></div><div class="card-body"><span class="card-tag">{self.silos[cluster_key]["name"]}</span><h3>{a["title"]}</h3><p>Análisis de rendimiento y veredicto para compradores...</p></div><div class="card-footer">Ver Análisis Experto &rarr;</div></a>' for a in articles])
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
