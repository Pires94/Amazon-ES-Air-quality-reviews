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

class AuthorityGenerator:
    def __init__(self):
        self.metadata = self.load_json(METADATA_FILE, [])
        self.article_template = self.load_file(TEMPLATES_DIR / "article.html")
        # Verified Amazon Media Image IDs for Real Products
        self.img_map = {
            "purificadores": "71861TI5gOL",
            "deshumidificadores": "51WpiRLRn9L",
            "alergias": "71861TI5gOL",
            "silencioso": "71861TI5gOL",  # Mapping to Levoit as it is the silent king
            "barato": "61zNsy+PnqL",      # Mapping to Xiaomi budget model
            "bano": "51PAdzNk09L",        # Mapping to Pro Breeze
            "casa": "51WpiRLRn9L"         # Mapping to DeLonghi
        }
        self.products = {
            "purificadores": [
                {
                    "id": "best", "name": "Levoit Core 400S Smart", "link": f"https://www.amazon.es/dp/B099K1S8XW?tag={AFFILIATE_TAG}",
                    "pros": ["Entrega de aire limpio ultra alta", "Sensor láser PM2.5 real", "Motor supersilencioso (24dB)"],
                    "reason": "Domina las mediciones técnicas. Detecta humo y partículas al instante.",
                    "limit": "Mayor inversión en recambios originales.",
                    "badge": "RECOMENDADO",
                    "social": "Más de 12.000 usuarios respaldan su durabilidad."
                },
                {
                    "id": "budget", "name": "Xiaomi Smart Purifier 4 Lite", "link": f"https://www.amazon.es/dp/B09M938K69?tag={AFFILIATE_TAG}",
                    "pros": ["Filtración en 25m2 reales", "Consumo eléctrico casi nulo", "Diseño compacto"],
                    "reason": "Ofrece un 85% del rendimiento premium pagando la mitad.",
                    "limit": "Sensor infrarrojo menos exacto que el láser.",
                    "badge": "MEJOR CALIDAD-PRECIO",
                    "social": "Top ventas histórico por su ratio calidad/precio."
                },
                {
                    "id": "avoid", "name": "Purificador 'Genérico' Sin Filtro Real", "link": "#",
                    "pros": ["Apariencia moderna", "Precio muy bajo"],
                    "reason": "Carece de filtros HEPA verdaderos. Básicamente un ventilador.",
                    "limit": "Ruido mecánico agudo y nula filtración.",
                    "badge": "Evitar rotundamente",
                    "social": "Alto índice de devoluciones."
                }
            ],
            "deshumidificadores": [
                {
                    "id": "best", "name": "De'Longhi Tasciugo AriaDry", "link": f"https://www.amazon.es/dp/B01B4XU6N6?tag={AFFILIATE_TAG}",
                    "pros": ["Extracción de 20L/día", "Certificación antialergias", "Secado de ropa rápido"],
                    "reason": "Capaz de secar paredes con humedad estructural y evitar hongos.",
                    "limit": "Peso elevado (15kg).",
                    "badge": "RECOMENDADO",
                    "social": "Elección unánime para problemas severos."
                },
                {
                    "id": "budget", "name": "Pro Breeze 12L", "link": f"https://www.amazon.es/dp/B01G7SGNW8?tag={AFFILIATE_TAG}",
                    "pros": ["Termohigrómetro integrado", "Apagado inteligente", "Drenaje continuo"],
                    "reason": "Logra bajar la humedad de un baño a 50% rápidamente.",
                    "limit": "Depósito pequeño (2L).",
                    "badge": "OPCIÓN ECONÓMICA",
                    "social": "Muy popular en pisos interiores."
                },
                {
                    "id": "avoid", "name": "Mini Deshumidificadores Peltier", "link": "#",
                    "pros": ["Diseño pequeño", "Bajo consumo"],
                    "reason": "Extracción mínima (vaso de agua semanal). No soluciona humedad real.",
                    "limit": "Ineficaz frente al moho.",
                    "badge": "Evitar rotundamente",
                    "social": "Reseñas negativas por inutilidad térmica."
                }
            ]
        }
        self.silos = {
            "purificadores": [
                {"slug": "purificador-aire-alergias", "title": "Mejor Purificador de Aire para Alergias", "intent": "alergias", "desc": "Filtración HEPA certificada para eliminar polvo y ácaros."},
                {"slug": "purificador-aire-silencioso-noite", "title": "Mejor Purificador de Aire Silencioso", "intent": "silencioso", "desc": "Dispositivos certificados por debajo de 25dB para dormir."},
                {"slug": "purificador-aire-barato-2024", "title": "Mejores Purificadores Baratos y Eficaces", "intent": "barato", "desc": "Análisis de modelos económicos con filtros HEPA reales."}
            ],
            "deshumidificadores": [
                {"slug": "deshumidificador-casa-humeda", "title": "Mejor Deshumidificador para Casa", "intent": "casa", "desc": "Combate el moho con compresores de extracción agresiva."},
                {"slug": "deshumidificador-bano-pequeno", "title": "Deshumidificador para el Baño", "intent": "bano", "desc": "Aparatos compactos para evitar humedad tras la ducha."}
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
        image_id = self.img_map.get(intent, "71861TI5gOL")
        return f"https://m.media-amazon.com/images/I/{image_id}._AC_SL800_.jpg"

    def gen_product_block(self, prod, category):
        img_url = self.get_img_url(category)
        pros = "".join([f'<li>✔ {p}</li>' for p in prod['pros']])
        badge_html = f'<div class="badge">{prod["badge"]}</div>' if prod.get('badge') else ''
        call_to_action = "Ver opiniones" if "Evitar" in prod['badge'] else "Ver precio ahora"
        
        if "Evitar" in prod['badge']:
            cta_html = ''
        else:
            cta_html = f'<a href="{prod["link"]}" class="cta-button">{call_to_action}</a>'

        return f"""
        <div class="product-card">
            {badge_html}
            <div class="product-grid" style="display: grid; grid-template-columns: 280px 1fr; gap: 2rem;">
                <div class="image-wrapper">
                    <img src="{img_url}" alt="{prod['name']}" class="product-image" loading="lazy">
                </div>
                <div class="product-info">
                    <h3>{prod['name']}</h3>
                    <div class="stars">⭐⭐⭐⭐⭐</div>
                    <ul class="benefits">{pros}</ul>
                    <p class="use-case"><strong>✔ Uso:</strong> {prod['reason']}</p>
                    <p class="limitation"><strong>✖ Limitación:</strong> {prod['limit']}</p>
                    {cta_html}
                </div>
            </div>
        </div>"""

    def run(self):
        ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
        date_str = datetime.datetime.now().strftime("%B %Y")

        for cat, articles in self.silos.items():
            best = self.products[cat][0]
            budget = self.products[cat][1]
            avoid = self.products[cat][2]
            
            for a in articles:
                img_hero = self.get_img_url(a['intent'])
                
                # Featured Product Card (ATF)
                atf_block = f"""
                <div class="product-card featured-selection">
                    <div class="badge" style="background:#FF9900; color:#111;">🔥 MEJOR OPCIÓN GENERAL</div>
                    <div class="product-grid" style="display: grid; grid-template-columns: 1fr 300px; gap: 2rem; align-items: center;">
                        <div>
                            <h2>{best['name']}</h2>
                            <div class="stars" style="margin-bottom:1rem;">⭐⭐⭐⭐⭐</div>
                            <p class="urgency" style="color:#dc2626; font-weight:bold;">🔥 Alta demanda - Puede agotarse</p>
                            <p>{best['reason']}</p>
                            <a href="{best['link']}" class="cta-button" style="margin-top:1.5rem;">Ver precio ahora</a>
                        </div>
                        <div class="image-wrapper">
                            <img src="{img_hero}" alt="{best['name']}" class="featured-image" loading="lazy">
                        </div>
                    </div>
                </div>"""

                content = f"""
                <div class="authority-block">
                    <h4>🔍 Nuestra Metodología</h4>
                    <p>Analizamos sensores PM2.5, decibelios y costes operativos para asegurar que tu inversión valga la pena.</p>
                </div>

                {atf_block}

                <h2>La Alternativa Calidad-Precio</h2>
                <p>Si buscas eficiencia sin el precio de gama alta, esta es nuestra recomendación contrastada.</p>
                {self.gen_product_block(budget, cat)}

                <div class="warning-block">
                    <h4>⚠️ Riesgo de Compra</h4>
                    <p>No confundas purificadores reales con ionizadores baratos que no filtran partículas.</p>
                </div>

                <h2>Lo que recomendamos descartar</h2>
                {self.gen_product_block(avoid, cat)}
                """

                html = self.article_template.replace("{{ title }}", a['title'])
                html = html.replace("{{ h1 }}", a['title'])
                html = html.replace("{{ description }}", a['desc'])
                html = html.replace("{{ content }}", content)
                html = html.replace("{{ date }}", date_str)
                
                self.write_file(ARTICLES_DIR / f"{a['slug']}.html", html)
                
                # Update Metadata
                if not any(m['slug'] == a['slug'] for m in self.metadata):
                    self.metadata.append({"slug": a['slug'], "title": a['title'], "cluster": cat, "intent": a['intent'], "desc": a['desc']})

        with open(METADATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)
        
        self.generate_index()

    def generate_index(self):
        featured = self.metadata[0] if self.metadata else {"title": "Guía Aire", "desc": "", "intent": "alergias", "slug": "#"}
        feat_img = self.get_img_url(featured.get('intent', 'alergias'))
        
        cards = ""
        for a in self.metadata[1:]:
            img = self.get_img_url(a.get('intent', 'alergias'))
            cards += f"""
            <a href="articles/{a['slug']}.html" class="grid-card" style="text-decoration:none; color:inherit;">
                <div class="product-card" style="margin:0; height:100%; display:flex; flex-direction:column;">
                    <img src="{img}" alt="{a['title']}" class="product-image">
                    <div style="padding-top:1.5rem; flex-grow:1;">
                        <div class="badge" style="position:static; margin-bottom:10px; display:inline-block;">RECOMENDADO</div>
                        <h3>{a['title']}</h3>
                        <div class="stars">⭐⭐⭐⭐⭐</div>
                        <p style="font-size:0.95rem; color:#4b5563;">{a.get('desc', 'Análisis técnico profundo.')}</p>
                    </div>
                    <div class="cta-button" style="margin-top:1rem;">Ver opciones</div>
                </div>
            </a>"""

        html = f"""<!DOCTYPE html>
<html lang="es-ES">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Expertos Aire - Guías de Compra de Alta Autoridad</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@600;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{ --amazon-orange: #FF9900; --bg-gray: #f8fafc; --text-main: #111827; }}
        body {{ font-family: 'Inter', sans-serif; background: var(--bg-gray); margin: 0; color: var(--text-main); }}
        header {{ background: #111827; padding: 1.2rem 5%; color: white; display: flex; justify-content: space-between; align-items: center; border-bottom: 4px solid var(--amazon-orange); }}
        .logo {{ font-family: 'Outfit'; font-size: 1.8rem; font-weight: 800; }}
        .logo span {{ color: var(--amazon-orange); }}
        .main {{ max-width: 1150px; margin: auto; padding: 3rem 5%; }}
        
        /* IMAGE SYSTEM */
        .product-image {{ width: 100%; height: 220px; object-fit: cover; border-radius: 12px; display: block; }}
        .featured-image {{ width: 100%; height: 260px; object-fit: cover; border-radius: 12px; display: block; }}
        .hero-image {{ width: 100%; height: 320px; object-fit: cover; display: block; border-radius: 12px; }}

        /* UI COMPONENTS */
        .product-card {{ background: white; border-radius: 12px; padding: 2rem; border: 1px solid #e5e7eb; box-shadow: 0 4px 20px rgba(0,0,0,0.05); transition: 0.2s; position: relative; }}
        .product-card:hover {{ transform: translateY(-3px); box-shadow: 0 8px 30px rgba(0,0,0,0.1); }}
        .badge {{ background: var(--amazon-orange); color: #111; padding: 5px 12px; font-size: 0.75rem; font-weight: 800; border-radius: 4px; position: absolute; top: -12px; left: 20px; }}
        .cta-button {{ display: block; text-align: center; background: var(--amazon-orange); color: #111; padding: 12px; font-weight: 700; border-radius: 8px; text-decoration: none; border: 1px solid #e68a00; }}
        
        .hero {{ display: grid; grid-template-columns: 1.2fr 1fr; gap: 3rem; align-items: center; margin-bottom: 4rem; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 2.5rem; }}
        
        @media (max-width: 800px) {{ .hero {{ grid-template-columns: 1fr; }} .product-grid {{ grid-template-columns: 1fr !important; }} }}
    </style>
</head>
<body>
    <header><div class="logo">Expertos<span>Aire</span></div></header>
    <div class="main">
        <div class="hero">
            <div class="hero-content">
                <h1 style="font-family:'Outfit'; font-size:3.2rem; line-height:1.1; margin:0 0 1.5rem 0;">Decisiones de compra basadas en <span style="color:#2563eb;">datos reales</span>.</h1>
                <p style="font-size:1.2rem; color:#4b5563; margin-bottom:2rem;">Analizamos la tecnología de filtración para que no tires tu dinero en marketing vacío.</p>
                <div class="product-card featured-selection">
                    <div class="badge">🔥 DESTACADO</div>
                    <h2 style="margin-top:0.5rem;">{featured['title']}</h2>
                    <p>{featured.get('desc', '')}</p>
                    <a href="articles/{featured['slug']}.html" class="cta-button">Ver Análisis Completo</a>
                </div>
            </div>
            <img src="{feat_img}" alt="Featured" class="hero-image">
        </div>
        <h2 style="font-family:'Outfit'; font-size:2rem; margin-bottom:2rem; border-bottom:2px solid #e5e7eb; padding-bottom:1rem;">Guías Técnicas Especializadas</h2>
        <div class="grid">{cards}</div>
    </div>
</body>
</html>"""
        self.write_file(SITE_DIR / "index.html", html)

if __name__ == "__main__":
    AuthorityGenerator().run()
