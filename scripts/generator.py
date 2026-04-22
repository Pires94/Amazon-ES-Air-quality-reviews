import json
import os
import datetime
import random
from pathlib import Path

# Configuration
CONTENT_DIR = Path("content")
SITE_DIR = Path(".")
ARTICLES_DIR = SITE_DIR / "articles"
TEMPLATES_DIR = Path("templates")
METADATA_FILE = CONTENT_DIR / "metadata.json"
AFFILIATE_TAG = "pires940f-21"

class ProfitGenerator:
    def __init__(self):
        self.metadata = self.load_json(METADATA_FILE, [])
        self.article_template = self.load_file(TEMPLATES_DIR / "article.html")
        # Stable Curated Imagery
        self.images = {
            "purificadores": {
                "health": "1585771724684-2626ef7a8963",
                "noise": "1632928274371-878938e4d825",
                "price": "1632733152643-41bbd011f06f"
            },
            "deshumidificadores": {
                "power": "1591147055011-8cc5c478a06e",
                "space": "1591864506306-031af4c9a626",
                "extreme": "1621230182745-f0e2270c2941"
            }
        }
        self.products = {
            "purificadores": [
                {
                    "id": "best", "name": "Levoit Core 400S", "link": f"https://www.amazon.es/dp/B099K1S8XW?tag={AFFILIATE_TAG}",
                    "pros": ["Filtración HEPA H13 certificada", "Modo noche ultrasilencioso (24dB)", "App VeSync con control PM2.5 real"],
                    "reason": "Es el único que realmente detecta y elimina partículas finas en segundos sin ruidos molestos.",
                    "negative": "Los filtros de marca blanca no rinden igual, lo que obliga a comprar originales."
                },
                {
                    "id": "budget", "name": "Xiaomi Smart Air Purifier 4 Lite", "link": f"https://www.amazon.es/dp/B09M938K69?tag={AFFILIATE_TAG}",
                    "pros": ["Diseño compacto efectivo", "Consumo energético mínimo", "Ideal para oficinas"],
                    "reason": "Funciona bien para espacios pequeños, pero el sensor no es de grado médico.",
                    "negative": "En velocidad máxima el ruido es excesivo para dormir cerca de él."
                },
                {
                    "id": "avoid", "name": "Purificador 'Ionizador' Genérico", "link": "#",
                    "pros": ["Precio ridículo", "Portátil USB"],
                    "reason": "No tiene filtro HEPA real; solo mueve el aire sucio usando electricidad.",
                    "negative": "Produce ozono residual que puede ser irritante para personas sensibles."
                }
            ],
            "deshumidificadores": [
                {
                    "id": "best", "name": "De'Longhi Tasciugo AriaDry", "link": f"https://www.amazon.es/dp/B01B4XU6N6?tag={AFFILIATE_TAG}",
                    "pros": ["Capacidad de 20L verificada", "Filtro anti-polvo lavable", "Drenaje continuo para sótanos"],
                    "reason": "La única solución definitiva para humedades estructurales y condensación severa.",
                    "negative": "Pesa bastante y las ruedas no son las mejores en alfombras."
                },
                {
                    "id": "budget", "name": "Pro Breeze 12L", "link": f"https://www.amazon.es/dp/B01G7SGNW8?tag={AFFILIATE_TAG}",
                    "pros": ["Automático por porcentaje", "Pantalla LED de humedad", "Muy ligero"],
                    "reason": "Perfecto para baños o habitaciones con humedad leve por falta de ventilación.",
                    "negative": "El depósito de 2 litros se llena en una tarde si hay mucha humedad."
                },
                {
                    "id": "avoid", "name": "Absorbedor de Humedad Químico", "link": "#",
                    "pros": ["No gasta luz", "Sin ruido"],
                    "reason": "Es incapaz de reducir la humedad ambiental; solo sirve para cajones cerrados.",
                    "negative": "El líquido residual es tóxico y requiere recambios constantes que salen caros."
                }
            ]
        }
        self.silos = {
            "purificadores": [
                {"slug": "purificador-aire-alergias", "title": "Purificador de Aire para Alergias", "intent": "health"},
                {"slug": "purificador-aire-silencioso-noite", "title": "Purificador de Aire Silencioso para Dormir", "intent": "noise"},
                {"slug": "purificador-aire-habitacion-pequena", "title": "Purificador de Aire para Espacios Pequeños", "intent": "price"}
            ],
            "deshumidificadores": [
                {"slug": "deshumidificador-casa-humeda", "title": "Eliminar Humedad en Casa Húmeda", "intent": "power"},
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

    def get_img(self, cat, intent):
        photo_id = self.images[cat].get(intent, self.images[cat].get("health", "default"))
        return f"https://images.unsplash.com/photo-{photo_id}?auto=format&fit=crop&w=800&q=80"

    def cta(self, intent):
        opts = {
            "price": "Ver precio actual en Amazon",
            "urgency": "Comprobar disponibilidad ahora",
            "trust": "Ver opiniones reales antes de comprar"
        }
        return f'<a href="#" class="cta-btn">{opts.get(intent, opts["urgency"])}</a>'

    def gen_product_card(self, prod, status="best"):
        cat = "purificadores" # simplified
        img = self.get_img("purificadores", "health") # simplified
        badge = '<div class="winner-badge">🔥 MEJOR OPCIÓN GENERAL</div>' if status == "best" else ""
        cls = "winner" if status == "best" else ("loser" if status == "avoid" else "")
        pros = "".join([f'<li class="pro">{p}</li>' for p in prod['pros']])
        con = f'<li class="con">{prod["negative"]}</li>'
        return f"""<div class="product-card {cls}">{badge}
            <div class="card-layout">
                <div class="card-img"><img src="{img}" alt="{prod['name']}"></div>
                <div class="card-content">
                    <h3>{prod['name']}</h3>
                    <ul class="feature-list">{pros}{con}</ul>
                    <p><strong>Por qué es clave:</strong> {prod['reason']}</p>
                    <a href="{prod['link']}" class="cta-btn">{self.cta_text(status)}</a>
                </div>
            </div></div>"""

    def cta_text(self, status):
        if status == "best": return "Comprobar disponibilidad ahora"
        if status == "budget": return "Ver precio actual en Amazon"
        return "Ver opiniones reales (decepción garantizada)"

    def run(self):
        ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
        for cat, articles in self.silos.items():
            b = self.products[cat][0]; acc = self.products[cat][1]; rej = self.products[cat][2]
            for a in articles:
                img_hero = self.get_img(cat, a['intent'])
                anchor = f"""<div class="atf-anchor"><div class="atf-text"><span class="atf-badge">RECOMENDACIÓN DIRECTA</span>
                    <h3>Mejor opción: {b['name']}</h3><p>{b['reason']}</p>
                    <a href="{b['link']}" class="cta-btn">Ver precio actual en Amazon</a></div>
                    <div class="atf-visual"><img src="{img_hero}"></div></div>"""
                
                content = f"""<p class="micro-decision">Si buscas {a['title'].lower()} → ya has encontrado la respuesta. No pierdas tiempo con modelos de bajo rendimiento que tendrás que reemplazar en 6 meses.</p>
                    <h2>Simulación de Uso Real</h2>
                    <p><strong>En el uso diario:</strong> La diferencia se nota en los primeros 15 minutos. Mientras los modelos baratos solo mueven el polvo, el <strong>{b['name']}</strong> purifica el flujo de aire de forma masiva. Después de varias horas, el sensor láser confirma la bajada real de PM2.5.</p>
                    <p><strong>Por la noche:</strong> En modo sueño, el silencio es real. No hay vibraciones mecánicas ni pitidos molestos. Es la diferencia entre levantarse descansado o con dolor de cabeza por el zumbido constante.</p>
                    {self.gen_product_card(b, "best")}
                    <div class="micro-decision">Si tienes un presupuesto más ajustado → la siguiente opción es aceptable, pero tiene límites claros.</div>
                    {self.gen_product_card(acc, "budget")}
                    <h2>El peligro de elegir mal</h2>
                    <p>Comprar un dispositivo sin certificación HEPA real o con un compresor ineficiente no es ahorrar; es tirar el dinero. Muchos usuarios caen en la trampa del diseño bonito y terminan con un aparato ruidoso que no resuelve el problema.</p>
                    {self.gen_product_card(rej, "avoid")}
                """
                
                final = f"""<div class="final-push"><h3>Veredicto Final: Haz tu elección hoy</h3>
                    <div class="push-item"><h4>Compra el {b['name']} si:</h4><p>Buscas la solución definitiva, potencia verificada y tranquilidad total para tu salud.</p></div>
                    <div class="push-item"><h4>Elige el {acc['name']} si:</h4><p>Tienes menos presupuesto y el ruido no es tu prioridad principal.</p></div>
                    <div class="push-item"><h4 style="color:#ef4444">Evita el {rej['name']} si:</h4><p>No quieres perder el tiempo con un aparato que no cumple lo que promete.</p></div>
                    <a href="{b['link']}" class="cta-btn" style="box-shadow:none; background:#FFF; color:#111;">Ver opiniones reales de compradores en Amazon</a></div>"""
                
                html = self.article_template.replace("{{ title }}", a['title']).replace("{{ h1 }}", a['title'])
                html = html.replace("{{ description }}", f"Guía decisiva para {a['title']}. Análisis honesto del rendimiento real.").replace("{{ anchor_block }}", anchor)
                html = html.replace("{{ content }}", content).replace("{{ final_decision }}", final).replace("{{ best_link }}", b['link']).replace("{{ best_name }}", b['name'])
                
                self.write_file(ARTICLES_DIR / f"{a['slug']}.html", html)
                if not any(m['slug'] == a['slug'] for m in self.metadata):
                    self.metadata.append({"slug": a['slug'], "title": a['title'], "cluster": cat})

        with open(METADATA_FILE, 'w', encoding='utf-8') as f: json.dump(self.metadata, f, indent=2, ensure_ascii=False)
        self.gen_index()

    def gen_index(self):
        html = f'<!DOCTYPE html><html lang="es-ES"><head><meta charset="UTF-8"><title>Expertos Aire</title><style>body{{font-family:sans-serif; background:#f8f9fa; margin:0; padding:2rem;}} .grid{{display:grid; grid-template-columns:repeat(auto-fill, minmax(300px, 1fr)); gap:2rem; max-width:1200px; margin:auto;}} .card{{background:white; padding:1.5rem; border-radius:12px; text-decoration:none; color:inherit; box-shadow:0 1px 3px rgba(0,0,0,0.1);}}</style></head><body><h1 style="text-align:center;">Guías de Decisión 2024</h1><div class="grid">'
        for a in self.metadata: html += f'<a href="articles/{a["slug"]}.html" class="card"><h3>{a["title"]}</h3><p>Ver análisis y veredicto &rarr;</p></a>'
        self.write_file(SITE_DIR / "index.html", html + '</div></body></html>')

if __name__ == "__main__":
    ProfitGenerator().run()
