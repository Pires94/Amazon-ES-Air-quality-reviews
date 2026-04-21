import json
import os
import datetime
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
        # Deterministic Stable Image IDs (Unsplash)
        self.img_map = {
            "levoit": "1585771724684-2626ef7a8963",
            "xiaomi": "1632733152643-41bbd011f06f",
            "cecotec_pur": "1633513222533-3d027de1e2a8",
            "delonghi": "1591147055011-8cc5c478a06e",
            "probreeze": "1591864506306-031af4c9a626",
            "cecotec_des": "1621230182745-f0e2270c2941"
        }
        self.products = {
            "purificadores": [
                {
                    "id": "best", "name": "Levoit Core 400S", "link": f"https://www.amazon.es/dp/B099K1S8XW?tag={AFFILIATE_TAG}",
                    "img": f"https://images.unsplash.com/photo-{self.img_map['levoit']}?auto=format&fit=crop&w=800&q=80",
                    "pros": ["Filtración HEPA H13 real", "Extremadamente silencioso", "App Smart muy fiable"],
                    "use": "Salones grandes y dormitorios", "limit": "Recambios originales caros"
                },
                {
                    "id": "budget", "name": "Xiaomi Air Purifier 4 Lite", "link": f"https://www.amazon.es/dp/B09M938K69?tag={AFFILIATE_TAG}",
                    "img": f"https://images.unsplash.com/photo-{self.img_map['xiaomi']}?auto=format&fit=crop&w=800&q=80",
                    "pros": ["Diseño minimalista", "Precio imbatible", "Bajo consumo"],
                    "use": "Oficinas y habitaciones medianas", "limit": "Sensor VOC algo impreciso"
                },
                {
                    "id": "avoid", "name": "Purificador 'Tipo HEPA' Genérico", "link": "#",
                    "img": f"https://images.unsplash.com/photo-{self.img_map['cecotec_pur']}?auto=format&fit=crop&w=800&q=80",
                    "pros": ["Muy barato", "Pequeño"],
                    "use": "No recomendado", "limit": "No filtra PM2.5 real"
                }
            ],
            "deshumidificadores": [
                {
                    "id": "best", "name": "De'Longhi Tasciugo AriaDry", "link": f"https://www.amazon.es/dp/B01B4XU6N6?tag={AFFILIATE_TAG}",
                    "img": f"https://images.unsplash.com/photo-{self.img_map['delonghi']}?auto=format&fit=crop&w=800&q=80",
                    "pros": ["20L de extracción real", "Drenaje continuo", "Marca líder en fiabilidad"],
                    "use": "Sótanos y casas con mucha humedad", "limit": "Inversión inicial elevada"
                },
                {
                    "id": "budget", "name": "Pro Breeze 12L", "link": f"https://www.amazon.es/dp/B01G7SGNW8?tag={AFFILIATE_TAG}",
                    "img": f"https://images.unsplash.com/photo-{self.img_map['probreeze']}?auto=format&fit=crop&w=800&q=80",
                    "pros": ["Sensor de humedad regulable", "Ligero y portátil", "Modo ropa"],
                    "use": "Baños y habitaciones estándar", "limit": "Depósito pequeño (2L)"
                },
                {
                    "id": "avoid", "name": "Mini Deshumidificador Peltier", "link": "#",
                    "img": f"https://images.unsplash.com/photo-{self.img_map['cecotec_des']}?auto=format&fit=crop&w=800&q=80",
                    "pros": ["Muy barato", "Sin ruido"],
                    "use": "Solo armarios pequeños", "limit": "Extracción casi inexistente"
                }
            ]
        }
        self.silos = {
            "purificadores": [
                {"slug": "purificador-aire-alergias", "title": "Mejor Purificador para Alergias", "intent": "health"},
                {"slug": "purificador-aire-silencioso-noite", "title": "Purificador Silencioso para Dormir", "intent": "noise"},
                {"slug": "purificador-aire-100-euros", "title": "Purificadores por menos de 100€", "intent": "price"}
            ],
            "deshumidificadores": [
                {"slug": "deshumidificador-casa-humeda", "title": "Eliminar Humedad en Casa", "intent": "power"},
                {"slug": "deshumidificador-bano-pequeno", "title": "Mejor Deshumidificador para Baño", "intent": "space"}
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

    def gen_card(self, prod, is_best=False):
        badge = '<div class="recommendation-label">RECOMENDADO</div>' if is_best else ''
        cls = 'recommended' if is_best else ''
        pros = "".join([f"<li>{p}</li>" for p in prod['pros']])
        return f"""<div class="product-card-v2 {cls}">{badge}
            <div class="product-image"><img src="{prod['img']}" alt="{prod['name']}"></div>
            <div class="product-info"><h3>{prod['name']}</h3>
                <ul class="advantage-list">{pros}</ul>
                <p><strong>Uso ideal:</strong> {prod['use']}</p>
                <div class="limitation">✖ {prod['limit']}</div>
                <a href="{prod['link']}" class="cta-button">Ver precio actual en Amazon</a>
            </div></div>"""

    def apply_intent(self, intent):
        if intent == "health": return "El peligro de las PM2.5 no se ve, pero se siente. Una filtración mediocre es un riesgo inaceptable.", "Salud y Filtrado"
        if intent == "noise": return "El ruido blanco de un motor mal equilibrado arruina el sueño profundo. Analizamos el silencio real.", "Silencio y Descanso"
        if intent == "price": return "Lo barato sale caro si tienes que comprarlo dos veces. Estos son los únicos modelos económicos que rinden.", "Precio y Valor"
        return "La humedad estructural destruye cimientos y salud. Necesitas potencia demostrable.", "Potencia y Resultados"

    def run(self):
        ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
        for cat, articles in self.silos.items():
            best = self.products[cat][0]; budget = self.products[cat][1]; avoid = self.products[cat][2]
            for a in articles:
                risk, focus = self.apply_intent(a['intent'])
                atf = f'<div class="atf-hero"><div class="atf-visual"><img src="{best["img"]}"></div><div class="atf-content"><div class="atf-badge">TOP 1 RECOMENDADO</div><h3>Mejor opción: {best["name"]}</h3><p>La decisión más segura para {focus.lower()}.</p><a href="{best["link"]}" class="cta-button">Comprobar disponibilidad ahora</a></div></div>'
                content = f"""<p style="font-weight:bold; color:#B12704;">🚨 {risk}</p>
                    <h2>Análisis de Uso Real</h2>
                    <p><strong>En uso diario:</strong> La diferencia entre el {best['name']} y un modelo genérico se nota en los sensores. Mientras los baratos ignoran las partículas finas, este modelo reacciona en segundos.</p>
                    {self.gen_card(best, True)}
                    <p><strong>Por la noche:</strong> Si buscas {focus}, el ruido es el factor decisivo. El modelo de De'Longhi o Levoit (según categoría) permite dormir sin interrupciones, algo imposible con la gama baja.</p>
                    {self.gen_card(budget)}
                    <div style="background:#fff1f2; padding:1.5rem; border-left:4px solid #B12704; margin:2rem 0;">
                        <h4 style="margin:0; color:#B12704;">❌ POR QUÉ EVITAR: {avoid['name']}</h4>
                        <p style="margin:0.5rem 0 0 0; font-size:0.9rem;">Muchos usuarios cometen el error de comprar estos modelos por su precio. La realidad es que su capacidad de {cat[:-2]} es simbólica. Comprar esto es tirar el dinero.</p>
                    </div>
                    <h2>Veredicto Final</h2>
                    <p>Si valoras tu salud y tu tiempo, el <strong>{best['name']}</strong> es la única compra lógica en 2024. Evita los riesgos de marcas blancas y apuesta por rendimiento verificado.</p>
                    <a href="{best['link']}" class="cta-button" style="margin-top:1rem; padding:1.2rem;">Ver opiniones reales en Amazon antes de comprar</a>"""
                
                html = self.article_template.replace("{{ title }}", a['title']).replace("{{ h1 }}", a['title'])
                html = html.replace("{{ description }}", f"Guía de compra experta para {a['title']}").replace("{{ atf_box }}", atf)
                html = html.replace("{{ content }}", content).replace("{{ best_link }}", best['link'])
                self.write_file(ARTICLES_DIR / f"{a['slug']}.html", html)
                if not any(m['slug'] == a['slug'] for m in self.metadata):
                    self.metadata.append({"slug": a['slug'], "title": a['title'], "cluster": cat})
        
        with open(METADATA_FILE, 'w', encoding='utf-8') as f: json.dump(self.metadata, f, indent=2, ensure_ascii=False)
        self.generate_index()

    def generate_index(self):
        html = f'<!DOCTYPE html><html lang="es-ES"><head><meta charset="UTF-8"><title>Expertos Aire</title><style>body{{font-family:sans-serif; background:#f2f2f2; margin:0; padding:2rem;}} .grid{{display:grid; grid-template-columns:repeat(auto-fill, minmax(300px, 1fr)); gap:2rem; max-width:1200px; margin:auto;}} .card{{background:white; padding:1.5rem; border-radius:8px; text-decoration:none; color:inherit; box-shadow:0 1px 3px rgba(0,0,0,0.1);}} .card h3{{margin:0; color:#007185;}}</style></head><body><h1 style="text-align:center;">Guías de Decisión 2024</h1><div class="grid">'
        for a in self.metadata: html += f'<a href="articles/{a["slug"]}.html" class="card"><h3>{a["title"]}</h3><p>Análisis experto &rarr;</p></a>'
        self.write_file(SITE_DIR / "index.html", html + '</div></body></html>')

if __name__ == "__main__":
    Generator().run()
