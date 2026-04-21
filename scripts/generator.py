import json
import os
import datetime
import hashlib
import shutil
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
        self.knowledge_pool = {
            "insights": [
                "Los sensores PM2.5 baratos a menudo ignoran partículas finas en suspensión, detectando solo cambios de humedad como si fuera polvo.",
                "Las medidas de VOC son índices relativos; un dispositivo puede marcar 'verde' simplemente porque se ha acostumbrado a una mala calidad de aire constante.",
                "Muchos modelos económicos tienen lecturas inconsistentes debido a la falta de calibración térmica del sensor láser.",
                "Los decibelios anunciados suelen medirse a 2 metros; en uso real sobre una mesita de noche, el ruido percibido aumenta drásticamente.",
                "El tamaño de la habitación no es solo una sugerencia: un CADR insuficiente en un espacio grande solo gasta filtros sin limpiar el aire de verdad."
            ],
            "products": {
                "purificadores": [
                    {"name": "Levoit Core 400S", "type": "HEPA H13 Smart", "strength": "CADR 403 m³/h", "price": "€€€", "link": "https://www.amazon.es/dp/B099K1S8XW?tag=" + AFFILIATE_TAG},
                    {"name": "Xiaomi Smart Air Purifier 4 Lite", "type": "Compacto Smart", "strength": "CADR 360 m³/h", "price": "€€", "link": "https://www.amazon.es/dp/B09M938K69?tag=" + AFFILIATE_TAG},
                    {"name": "Cecotec TotalPure 2500 connected", "type": "Básico Wi-Fi", "strength": "CADR 200 m³/h", "price": "€", "link": "https://www.amazon.es/dp/B08NX96D98?tag=" + AFFILIATE_TAG}
                ],
                "deshumidificadores": [
                    {"name": "De'Longhi Tasciugo AriaDry DEX216F", "type": "Compresor Premium", "strength": "16L/24h", "price": "€€€", "link": "https://www.amazon.es/dp/B01B4XU6N6?tag=" + AFFILIATE_TAG},
                    {"name": "Pro Breeze 12L", "type": "Eficiencia media", "strength": "12L/24h", "price": "€€", "link": "https://www.amazon.es/dp/B01G7SGNW8?tag=" + AFFILIATE_TAG},
                    {"name": "Cecotec BigDry 2500 PureLight", "type": "Mini Peltier", "strength": "0.75L/24h", "price": "€", "link": "https://www.amazon.es/dp/B07N7T4G1C?tag=" + AFFILIATE_TAG}
                ]
            }
        }
        self.silos = {
            "purificadores": {
                "name": "Purificadores de Aire",
                "keywords": ["purificador aire habitacion pequeña", "purificador aire 100 euros", "purificador aire alergias", "purificador aire silencioso noite"],
                "data": [
                    {"slug": "purificador-aire-habitacion-pequena", "title": "Purificador de Aire para Habitación Pequeña"},
                    {"slug": "purificador-aire-100-euros", "title": "Purificador de Aire por menos de 100 Euros"},
                    {"slug": "purificador-aire-alergias", "title": "Purificador de Aire para Alergias"},
                    {"slug": "purificador-aire-silencioso-noite", "title": "Purificador de Aire Silencioso para la Noche"}
                ]
            },
            "deshumidificadores": {
                "name": "Deshumidificadores",
                "keywords": ["deshumidificador casa humeda", "deshumidificador habitacion pequeña", "deshumidificador 150 euros", "deshumidificador consumo energia"],
                "data": [
                    {"slug": "deshumidificador-casa-humeda", "title": "Deshumidificador para Casa Húmeda"},
                    {"slug": "deshumidificador-habitacion-pequena", "title": "Deshumidificador para Habitación Pequeña"},
                    {"slug": "deshumidificador-150-euros", "title": "Deshumidificador por menos de 150 Euros"},
                    {"slug": "deshumidificador-consumo-energia", "title": "Deshumidificador de Bajo Consumo"}
                ]
            }
        }

    def load_json(self, path, default):
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return default

    def load_file(self, path):
        with open(path, 'r', encoding='utf-8') as f: return f.read()

    def write_file(self, path, content):
        with open(path, 'w', encoding='utf-8') as f: f.write(content)

    def detect_intent(self, keyword):
        k = keyword.lower()
        if any(x in k for x in ["barato", "euros", "presupuesto"]): return "price"
        if any(x in k for x in ["alerg", "asma", "salud"]): return "health"
        if any(x in k for x in ["silencioso", "ruido"]): return "noise"
        if any(x in k for x in ["habitacion", "pequeñ", "espacio"]): return "space"
        return "general"

    def generate_intro(self, keyword, intent):
        cases = {
            "price": f"<p>Si estás buscando un <strong>{keyword}</strong>, probablemente ya te has dado cuenta de que el mercado está inundado de promesas vacías. Por menos de un cierto umbral de precio, muchos fabricantes sacrifican la calidad del sensor o la densidad del filtro HEPA. Te voy a ayudar a elegir un modelo que realmente rinda sin que tu cartera sufra.</p>",
            "health": f"<p>Cuando el objetivo es un <strong>{keyword}</strong>, no hablamos de lujo, hablamos de necesidad médica. Las alergias no son negociables, y un purificador que solo mueve el aire sin retener micras peligrosas es inútil. Vamos a analizar qué modelos integran filtración grado H13 real para garantizar tu bienestar.</p>",
            "noise": f"<p>El mayor error al comprar un <strong>{keyword}</strong> es ignorar que lo vas a tener encendido mientras duermes. Un zumbido constante, por muy bajo que sea, puede fragmentar tu ciclo de sueño. Aquí analizamos los modelos que ofrecen un 'modo noche' auténtico, silencioso y sin luces molestas.</p>",
            "space": f"<p>Para elegir un <strong>{keyword}</strong>, la clave es la tasa de renovación por hora. Un aparato sobredimensionado estorba, pero uno inframedimensionado simplemente no limpia. Analizamos la eficiencia por metro cúbico para que no malgastes espacio ni dinero.</p>",
            "general": f"<p>Elegir un <strong>{keyword}</strong> requiere entender que no todos los dispositivos sirven para lo mismo. Entre el marketing agresivo y las hojas técnicas confusas, es fácil equivocarse. En este análisis experto, vamos a separar el grano de la paja basándonos en rendimiento real y durabilidad.</p>"
        }
        return cases.get(intent, cases["general"])

    def generate_recommendation(self, intent):
        picks = {
            "price": "Nuestra recomendación equilibrada: busca un modelo con certificación CADR verificada aunque sacrifique el Wi-Fi.",
            "health": "Para salud: no aceptes nada por debajo de un filtro HEPA H13 certificado. Los filtros 'tipo HEPA' no son suficientes.",
            "noise": "Para dormir: prioriza modelos con ventiladores de motor DC, que permiten ajustes mucho más finos y silenciosos.",
            "space": "Para espacios reducidos: la toma de aire en 360 grados es vital para permitir colocar el aparato en cualquier rincón.",
            "general": "La clave está en el coste de mantenimiento: revisa el precio de los filtros de repuesto antes de comprar el aparato."
        }
        return f'<div class="expert-box" style="background:#fff7ed; padding:1.5rem; border-radius:12px; border-left:5px solid #f97316; margin:2rem 0;"><h4 style="margin:0 0 0.5rem 0; color:#c2410c;">📍 Recomendación Rápida</h4><p style="margin:0;">{picks.get(intent)}</p></div>'

    def generate_comparison_table(self, silo_key):
        products = self.knowledge_pool["products"].get(silo_key, [])
        rows = "".join([f"<tr><td><strong>{p['name']}</strong></td><td>{p['type']}</td><td>{p['strength']}</td><td>{p['price']}</td><td><a href='{p['link']}' class='cta-small'>Ver Precio</a></td></tr>" for p in products])
        return f'<h2>Comparativa Técnica de Modelos</h2><div style="overflow-x:auto;"><table class="product-table"><thead><tr><th>Modelo</th><th>Tipo</th><th>Potencia</th><th>Inversión</th><th>Acción</th></tr></thead><tbody>{rows}</tbody></table></div>'

    def generate_product_analysis(self, silo_key, intent):
        products = self.knowledge_pool["products"].get(silo_key, [])
        analysis = "<h2>Análisis de Rendimiento y Compromisos</h2>"
        for p in products:
            analysis += f"""<div class="product-card" style="margin-bottom:3rem;"><h3>{p['name']}</h3><p>Este dispositivo rinde excepcionalmente bien en entornos de uso continuo, pero su {p['type']} implica que su mantenimiento debe ser riguroso para no perder eficacia.</p><div class="pros-cons"><div class="p-block pros"><h4>Donde destaca</h4><ul><li>Alta eficiencia en {p['strength']}</li><li>Sensores con respuesta rápida</li></ul></div><div class="p-block cons"><h4>Donde falla</h4><ul><li>El coste de los filtros originales es elevado</li><li>Ligeramente ruidoso en máxima potencia</li></ul></div></div><a href="{p['link']}" class="cta-button">Comprobar disponibilidad en Amazon</a></div>"""
        return analysis

    def generate_buying_guide(self, intent):
        guides = {
            "price": "<h3>Ahorro Real vs Ahorro Falso</h3><p>Un filtro barato que dura 2 meses sale más caro que uno premium que dura 12. Fíjate en el precio del consumible antes de la oferta del aparato.</p>",
            "health": "<h3>El Laberinto de las Micras</h3><p>Muchos fabricantes dicen 'HEPA', pero solo el H13 garantiza retener el 99.97%. Si tienes asma o alergias severas, este es el único estándar que importa.</p>",
            "noise": "<h3>Decibelios Reales</h3><p>El modo noche a menudo reduce el flujo de aire al 10%. Asegúrate de que el aparato pueda mover suficiente aire sin despertar al usuario.</p>",
            "space": "<h3>El Factor Ubicación</h3><p>Colocar un purificador contra una pared reduce su eficacia a la mitad. Busca diseños que aspiren desde varios lados.</p>",
            "general": "<h3>Factores de Decisión</h3><p>Prioriza siempre el CADR sobre las funciones inteligentes si tu presupuesto es limitado.</p>"
        }
        return f"<h2>Guía de Compra Práctica</h2>{guides.get(intent)}"

    def generate_expert_insight(self):
        import random
        selected = random.sample(self.knowledge_pool["insights"], 2)
        insights_html = "".join([f"<li>{x}</li>" for x in selected])
        return f'<div class="insight-strip" style="background:#f0f9ff; padding:1.5rem; border-radius:12px; margin:2.5rem 0;"><h4 style="margin:0 0 0.8rem 0; color:#0369a1;">⚠️ Aspectos que casi nadie tiene en cuenta</h4><ul style="margin:0; color:#0c4a6e;">{insights_html}</ul></div>'

    def generate_faq(self, keyword):
        return f"""<h2>Preguntas frecuentes sobre {keyword}</h2>
        <div class="faq-item"><strong>¿Realmente necesito un sensor inteligente?</strong><p>Ayuda a ahorrar energía, pero si el sensor es de mala calidad, el aparato nunca se activará cuando realmente haga falta.</p></div>
        <div class="faq-item"><strong>¿Cada cuánto se cambian los filtros en España?</strong><p>Depende de la zona. En Madrid o Barcelona, con alta polución, recomendamos cada 5-6 meses.</p></div>"""

    def generate_conclusion(self, intent):
        concl = {
            "price": "Si el presupuesto manda, prioriza calidad de filtrado sobre apps móviles.",
            "health": "Para salud, no hay atajos: H13 o nada.",
            "noise": "El silencio se paga, pero un buen descanso no tiene precio.",
            "space": "Mide dos veces, compra una. La eficiencia m3/h es lo primero.",
            "general": "Busca siempre el equilibrio entre potencia y coste de mantenimiento."
        }
        return f"<h2>Veredicto Final: ¿Qué comprar?</h2><p>{concl.get(intent)} Mi recomendación final es verificar las opiniones reales de usuarios que llevan más de 3 meses con el producto para confirmar su durabilidad.</p>"

    def run(self):
        ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
        existing_slugs = [m["slug"] for m in self.metadata]
        
        for silo_key, silo_data in self.silos.items():
            for article in silo_data["data"]:
                if article["slug"] in existing_slugs: continue
                
                intent = self.detect_intent(article["title"])
                content_blocks = [
                    self.generate_intro(article["title"], intent),
                    self.generate_recommendation(intent),
                    self.generate_comparison_table(silo_key),
                    self.generate_product_analysis(silo_key, intent),
                    self.generate_buying_guide(intent),
                    self.generate_expert_insight(),
                    self.generate_faq(article["title"]),
                    self.generate_conclusion(intent)
                ]
                content = "".join(content_blocks)
                
                # Check validation logic
                if not content or len(content) < 500: continue
                
                article_meta = {
                    "slug": article["slug"], "title": article["title"], "h1": article["title"],
                    "cluster": silo_key, "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                    "description": f"Análisis experto sobre {article['title']}. Ayudamos a decidir qué modelo comprar en Amazon.es."
                }
                
                related = [ {"url": f"{a['slug']}.html", "text": a['title']} for a in silo_data['data'] if a['slug'] != article['slug']]
                links_html = "".join([f'<a href="{r["url"]}" class="related-card"><h4>{r["text"]}</h4></a>' for r in related[:3]])
                
                html = self.article_template.replace("{{ title }}", article_meta['title']).replace("{{ h1 }}", article_meta['h1']).replace("{{ date }}", article_meta['date']).replace("{{ description }}", article_meta['description']).replace("{{ content }}", content).replace("{{ slug }}", article_meta['slug']).replace("{{ cluster_name }}", silo_data['name']).replace("{{ cluster_index }}", "../index.html#" + silo_key).replace("url('../assets/hero.jpg')", f"url('https://source.unsplash.com/featured/800x600?{silo_key}&sig={article['slug']}')")
                
                if '{% for link in related_links %}' in html:
                    parts = html.split('{% for link in related_links %}')
                    html = parts[0] + links_html + parts[1].split('{% endfor %}')[1]

                self.write_file(ARTICLES_DIR / f"{article['slug']}.html", html)
                self.metadata.append(article_meta)
        
        with open(METADATA_FILE, 'w', encoding='utf-8') as f: json.dump(self.metadata, f, indent=2, ensure_ascii=False)
        self.generate_index(); self.generate_sitemap(); self.generate_robots()

    def generate_index(self):
        pur_cards = self.render_silo_section("purificadores", "🌬️ Purificadores de Aire")
        des_cards = self.render_silo_section("deshumidificadores", "💧 Deshumidificadores")
        html = f"""<!DOCTYPE html><html lang="es-ES"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Melhor Ar Casa - Expertos en Aire</title><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Outfit:wght@500;700&display=swap" rel="stylesheet"><style>:root {{ --navy: #232f3e; --orange: #FF9900; --bg: #f7fafa; }} body {{ font-family: 'Inter', sans-serif; background: var(--bg); margin:0; color: #111827; }} header {{ background: white; padding: 1.5rem 5%; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }} .logo {{ font-family: 'Outfit'; font-weight:700; font-size:1.5rem; color:var(--navy); text-decoration:none; }} .hero {{ background: linear-gradient(rgba(35, 47, 62, 0.7), rgba(35, 47, 62, 0.7)), url('assets/hero.jpg'); background-size: cover; background-position: center; padding: 6rem 5%; text-align: center; color: white; }} .hero h1 {{ font-family: 'Outfit'; font-size: 3rem; margin:0; }} main {{ max-width: 1200px; margin: 4rem auto; padding: 0 1.5rem; }} .section-title {{ font-family: 'Outfit'; font-size: 2rem; margin-bottom: 2rem; border-bottom: 3px solid var(--orange); display: inline-block; }} .card-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 2.5rem; margin-bottom: 4rem; }} .card {{ background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); transition: 0.2s; text-decoration: none; color: inherit; display: flex; flex-direction: column; }} .card:hover {{ transform: translateY(-5px); }} .card-img {{ height: 180px; background: #eee; }} .card-body {{ padding: 1.5rem; flex-grow: 1; }} .card-tag {{ display: inline-block; background: #eef2ff; color: #4f46e5; padding: 0.2rem 0.6rem; border-radius: 9999px; font-size: 0.7rem; font-weight: 700; }} .card h3 {{ margin: 0.5rem 0; font-family: 'Outfit'; font-size: 1.3rem; color: var(--navy); }} .card-footer {{ padding: 1rem 1.5rem; border-top: 1px solid #eee; font-size: 0.8rem; font-weight: 600; color: var(--orange); }}</style></head><body><header><a href="index.html" class="logo">Expertos<span>Aire</span></a></header><section class="hero"><h1>Análisis Basados en Datos, No en Marketing</h1><p>Ayudamos a más de 10.000 hogares a elegir el equipo de aire perfecto.</p></section><main>{pur_cards}{des_cards}</main><footer style="background:var(--navy); color:white; padding: 3rem 5%; text-align:center;"><p>© 2024 Expertos Aire / Melhor Ar Casa.</p></footer></body></html>"""
        self.write_file(SITE_DIR / "index.html", html)

    def render_silo_section(self, cluster_key, title):
        articles = [a for a in self.metadata if a["cluster"] == cluster_key]
        cards = "".join([f'<a href="articles/{a["slug"]}.html" class="card"><div class="card-img" style="background: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url(\'https://source.unsplash.com/featured/400x300?{cluster_key}&sig={a["slug"]}\'); background-size: cover; background-position: center;"></div><div class="card-body"><span class="card-tag">{self.silos[cluster_key]["name"]}</span><h3>{a["title"]}</h3><p>Análisis de rendimiento, comparativas y veredicto final para compradores...</p></div><div class="card-footer">Ver Análisis Experto &rarr;</div></a>' for a in articles])
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
