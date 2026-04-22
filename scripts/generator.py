import json
import os
import datetime
from pathlib import Path

# Configuration
CONTENT_DIR = Path("content")
SITE_DIR = Path(".")
ARTICLES_DIR = SITE_DIR / "articles"
TEMPLATES_DIR = Path("templates")
METADATA_FILE = CONTENT_DIR / "metadata.json"
AFFILIATE_TAG = "pires940f-21"

class HighConversionGenerator:
    def __init__(self):
        self.metadata = self.load_json(METADATA_FILE, [])
        self.article_template = self.load_file(TEMPLATES_DIR / "article.html")
        # Stable Curated Imagery Mapping
        self.img_map = {
            "purificadores": "1585771724684-2626ef7a8963",
            "deshumidificadores": "1591147055011-8cc5c478a06e",
            "alergias": "1585771724684-2626ef7a8963",
            "silencioso": "1632928274371-878938e4d825",
            "barato": "1632733152643-41bbd011f06f",
            "bano": "1585642875141-8f5539498263",
            "casa": "1621230182745-f0e2270c2941"
        }
        self.products = {
            "purificadores": [
                {
                    "id": "best", "name": "Levoit Core 400S", "link": f"https://www.amazon.es/dp/B099K1S8XW?tag={AFFILIATE_TAG}",
                    "pros": ["Filtración HEPA H13 certificada", "Modo noche ultrasilencioso (24dB)", "App VeSync con control PM2.5 real"],
                    "reason": "La única opción que garantiza aire puro en salones grandes sin ruido mecánico intrusivo.",
                    "limit": "Los filtros oficiales son caros, pero necesarios para mantener la garantía.",
                    "badge": "MEJOR OPCIÓN GENERAL"
                },
                {
                    "id": "budget", "name": "Xiaomi Smart Air Purifier 4 Lite", "link": f"https://www.amazon.es/dp/B09M938K69?tag={AFFILIATE_TAG}",
                    "pros": ["Diseño minimalista compacto", "Perfecto para habitaciones de hasta 25m2", "Bajo consumo eléctrico"],
                    "reason": "Rendimiento sólido para presupuestos ajustados. Cumple su función sin adornos.",
                    "limit": "Filtro más básico que la competencia de alta gama.",
                    "badge": "OPCIÓN ECONÓMICA"
                },
                {
                    "id": "avoid", "name": "Modelos 'Tipo HEPA' sin Filtro Real", "link": "#",
                    "pros": ["Precio de ganga", "Pequeño y ligero"],
                    "reason": "Aunque parecen baratos, su capacidad de filtrado es casi nula contra PM2.5.",
                    "limit": "No recomendado para alérgicos o salud respiratoria.",
                    "badge": "NO RECOMENDADO"
                }
            ],
            "deshumidificadores": [
                {
                    "id": "best", "name": "De'Longhi Tasciugo AriaDry", "link": f"https://www.amazon.es/dp/B01B4XU6N6?tag={AFFILIATE_TAG}",
                    "pros": ["20L de extracción real por día", "Drenaje continuo para sótanos", "Marca líder en fiabilidad"],
                    "reason": "La solución definitiva si tienes problemas de condensación o humedad estructural.",
                    "limit": "Inversión inicial alta, pero ahorra en reparaciones de pintura.",
                    "badge": "ALTO RENDIMIENTO"
                },
                {
                    "id": "budget", "name": "Pro Breeze 12L", "link": f"https://www.amazon.es/dp/B01G7SGNW8?tag={AFFILIATE_TAG}",
                    "pros": ["Ligero y fácil de mover", "Sensor de humedad digital", "Ideal para baños y lavanderías"],
                    "reason": "Excelente equilibrio entre precio y capacidad de extracción diaria.",
                    "limit": "Depósito de 2L que requiere vaciado frecuente en zonas muy húmedas.",
                    "badge": "CALIDAD-PRECIO"
                },
                {
                    "id": "avoid", "name": "Mini Absorbedores Peltier", "link": "#",
                    "pros": ["Silencio total", "Bajo consumo"],
                    "reason": "Su capacidad es tan baja que no sirve para habitaciones, solo para armarios muy pequeños.",
                    "limit": "No sirve para problemas reales de humedad.",
                    "badge": "EVITAR"
                }
            ]
        }
        self.silos = {
            "purificadores": [
                {"slug": "purificador-aire-alergias", "title": "Mejor Purificador de Aire para Alergias", "intent": "alergias", "desc": "Filtración HEPA H13 real para eliminar polen y polvo."},
                {"slug": "purificador-aire-silencioso-noite", "title": "Purificador Silencioso para Dormir", "intent": "silencioso", "desc": "Descansa mejor con tecnología de bajo ruido certificado."},
                {"slug": "purificador-aire-barato-2024", "title": "Purificadores Baratos que SÍ Funcionan", "intent": "barato", "desc": "Opciones económicas sin sacrificar la salud de tu aire."}
            ],
            "deshumidificadores": [
                {"slug": "deshumidificador-casa-humeda", "title": "Soluciones para Humedad en Casa", "intent": "casa", "desc": "Elimina la condensación y el olor a humedad de raíz."},
                {"slug": "deshumidificador-bano-pequeno", "title": "Mejor Deshumidificador para Baño", "intent": "bano", "desc": "Potencia compacta para evitar el moho en el cuarto de baño."}
            ]
        }

    def load_json(self, path, default):
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f: return json.load(f)
        return default

    def load_file(self, path):
        with open(path, 'r', encoding='utf-8') as f: return f.read()

    def write_file(self, path, content):
        with open(path, 'w', encoding='utf-8') as f: f.write(content)

    def get_img_url(self, intent):
        photo_id = self.img_map.get(intent, "1585771724684-2626ef7a8963")
        return f"https://images.unsplash.com/photo-{photo_id}?auto=format&fit=crop&w=800&q=80"

    def gen_product_block(self, prod, category):
        img_id = self.img_map.get(category, "1585771724684-2626ef7a8963")
        img_url = f"https://images.unsplash.com/photo-{img_id}?auto=format&fit=crop&w=600&q=80"
        pros = "".join([f'<li><span style="color:green; font-weight:bold;">✔</span> {p}</li>' for p in prod['pros']])
        return f"""<div style="background:white; border:1px solid #e2e8f0; border-radius:12px; padding:2rem; margin:2rem 0; box-shadow:0 10px 15px -3px rgba(0,0,0,0.1);">
            <div style="display:grid; grid-template-columns: 240px 1fr; gap:2rem;">
                <div style="overflow:hidden; border-radius:8px;"><img src="{img_url}" alt="{prod['name']}" style="width:100%; height:200px; object-fit:cover;"></div>
                <div>
                    <span style="background:#FF9900; color:white; padding:4px 10px; border-radius:4px; font-weight:800; font-size:0.75rem;">{prod['badge']}</span>
                    <h3 style="margin:10px 0; font-size:1.5rem;">{prod['name']}</h3>
                    <ul style="list-style:none; padding:0; margin:0 0 1rem 0; font-size:0.95rem;">{pros}</ul>
                    <p style="font-size:0.9rem; color:#4a5568;"><strong>Limitación:</strong> {prod['limit']}</p>
                    <a href="{prod['link']}" style="display:inline-block; background:#FF9900; color:white; padding:12px 24px; border-radius:6px; text-decoration:none; font-weight:bold; width:100%; text-align:center;">Ver precio en Amazon</a>
                </div>
            </div></div>"""

    def run(self):
        ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
        for cat, articles in self.silos.items():
            best = self.products[cat][0]; budget = self.products[cat][1]; avoid = self.products[cat][2]
            for a in articles:
                img_hero = self.get_img_url(a['intent'])
                atf_block = f"""<div style="background:#fffcf2; border:2px solid #FF9900; border-radius:12px; padding:2rem; margin:2rem 0; display:grid; grid-template-columns:1fr 300px; gap:2rem; align-items:center;">
                    <div><span style="background:#FF9900; color:white; padding:4px 10px; border-radius:4px; font-weight:bold; font-size:0.8rem;">MEJOR OPCIÓN ANALIZADA</span>
                    <h2 style="margin:1rem 0;">{best['name']}</h2><p>{best['reason']}</p>
                    <a href="{best['link']}" style="display:inline-block; background:#FF9900; color:white; padding:15px 30px; border-radius:8px; text-decoration:none; font-weight:800; margin-top:1rem;">Asegurar disponibilidad en Amazon</a></div>
                    <div><img src="{img_hero}" style="width:100%; border-radius:8px; box-shadow:0 4px 6px rgba(0,0,0,0.1);"></div></div>"""
                
                content = f"""<h2>Análisis de Decisión</h2><p>Elegir un {cat[:-2]} no debería ser una cuestión de suerte. Hemos analizado el rendimiento real, el ruido y la fiabilidad para que no tires tu dinero.</p>
                    {self.gen_product_block(best, cat)}
                    <div style="background:#f7fafc; padding:1.5rem; border-left:4px solid #cbd5e0; margin:2rem 0; font-style:italic;">Si tu presupuesto es más ajustado, la siguiente opción ofrece un rendimiento digno por debajo de los 100€.</div>
                    {self.gen_product_block(budget, cat)}
                    <h2 style="color:#e53e3e;">Por qué deberías evitar modelos ultra-baratos</h2>
                    <p>Mucha gente comete el error de comprar dispositivos de 30-40 euros esperando milagros. La realidad es que estos aparatos suelen ser juguetes ruidosos sin capacidad real.</p>
                    {self.gen_product_block(avoid, cat)}
                """
                
                html = self.article_template.replace("{{ title }}", a['title']).replace("{{ h1 }}", a['title'])
                html = html.replace("{{ description }}", a['desc']).replace("{{ atf_box }}", atf_block).replace("{{ content }}", content)
                html = html.replace("{{ best_link }}", best['link']).replace("{{ best_name }}", best['name'])
                
                self.write_file(ARTICLES_DIR / f"{a['slug']}.html", html)
                if not any(m['slug'] == a['slug'] for m in self.metadata):
                    self.metadata.append({"slug": a['slug'], "title": a['title'], "cluster": cat, "intent": a['intent'], "desc": a['desc']})

        with open(METADATA_FILE, 'w', encoding='utf-8') as f: json.dump(self.metadata, f, indent=2, ensure_ascii=False)
        self.generate_index()

    def generate_index(self):
        featured = self.metadata[0] if self.metadata else None
        feat_img = self.get_img_url(featured['intent'] if featured else "alergias")
        
        cards_html = ""
        for a in self.metadata[1:]:
            img = self.get_img_url(a['intent'])
            cards_html += f"""<a href="articles/{a['slug']}.html" style="background:white; border-radius:12px; overflow:hidden; text-decoration:none; color:inherit; box-shadow:0 4px 6px -1px rgba(0,0,0,0.1); transition:transform 0.2s;">
                <img src="{img}" style="width:100%; height:180px; object-fit:cover;">
                <div style="padding:1.5rem;"><h3>{a['title']}</h3><p style="font-size:0.9rem; color:#4a5568;">{a['desc']}</p><span style="color:#FF9900; font-weight:bold;">Ver análisis &rarr;</span></div>
            </a>"""

        html = f"""<!DOCTYPE html><html lang="es-ES"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Expertos Aire - Guías de Compra</title>
            <style>body{{font-family:sans-serif; background:#f7fafc; margin:0;}} .main{{max-width:1100px; margin:auto; padding:2rem;}} .hero{{background:#2d3748; color:white; padding:4rem 2rem; text-align:center;}} .grid{{display:grid; grid-template-columns:repeat(auto-fill, minmax(300px, 1fr)); gap:2rem; margin-top:3rem;}}</style></head>
            <body><div class="hero"><h1>Mejores soluciones para mejorar el aire en casa</h1><p>Análisis expertos y decisiones directas para tu salud.</p></div>
            <div class="main">
                <div style="background:white; border-radius:16px; display:grid; grid-template-columns:1fr 1fr; overflow:hidden; box-shadow:0 20px 25px -5px rgba(0,0,0,0.1); margin-bottom:4rem;">
                    <div style="padding:3rem;">
                        <span style="background:#fed7d7; color:#c53030; padding:4px 12px; border-radius:20px; font-weight:bold; font-size:0.8rem;">🔥 MÁS RECOMENDADO</span>
                        <h2 style="font-size:2rem; margin:1rem 0;">{featured['title']}</h2><p>{featured['desc']}</p>
                        <a href="articles/{featured['slug']}.html" style="display:inline-block; background:#FF9900; color:white; padding:15px 40px; border-radius:8px; text-decoration:none; font-weight:800; font-size:1.1rem;">Ver análisis completo</a>
                    </div>
                    <div style="background:url('{feat_img}') center/cover;"></div>
                </div>
                <div class="grid">{cards_html}</div>
            </div></body></html>"""
        self.write_file(SITE_DIR / "index.html", html)

if __name__ == "__main__":
    HighConversionGenerator().run()
