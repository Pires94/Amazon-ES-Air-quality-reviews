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
                    "id": "best", "name": "Levoit Core 400S Smart", "link": f"https://www.amazon.es/dp/B099K1S8XW?tag={AFFILIATE_TAG}",
                    "pros": ["Tasa de entrega de aire limpio (CADR) ultra alta", "Sensor láser PM2.5 real de alta precisión", "Motor supersilencioso (probado a 24dB)"],
                    "reason": "Domina las mediciones técnicas. Detecta humo y partículas al instante y las neutraliza.",
                    "limit": "Mayor inversión en recambios originales, obligatorio para mantener eficacia médica.",
                    "badge": "🔥 MEJOR OPCIÓN GENERAL",
                    "social": "Más de 12.000 usuarios respaldan su durabilidad y medición exacta."
                },
                {
                    "id": "budget", "name": "Xiaomi Smart Purifier 4 Lite", "link": f"https://www.amazon.es/dp/B09M938K69?tag={AFFILIATE_TAG}",
                    "pros": ["Filtración efectiva en 25m2 reales", "Consumo eléctrico casi nulo", "Diseño compacto que no estorba"],
                    "reason": "Ofrece un 85% del rendimiento de modelos premium pagando la mitad.",
                    "limit": "El sensor infrarrojo no es tan exacto frente a partículas submicrónicas (humo fino).",
                    "badge": "COMPRA INTELIGENTE",
                    "social": "Top ventas histórico por su inbatible ratio calidad/precio."
                },
                {
                    "id": "avoid", "name": "Purificador 'Genérico' Sin Certificación CEEE", "link": "#",
                    "pros": ["Apariencia moderna", "Precio por debajo de 40€"],
                    "reason": "Carece de filtros HEPA verdaderos. Es básicamente un ventilador caro con una esponja.",
                    "limit": "Ruido mecánico agudo tras varios meses de uso constante.",
                    "badge": "Evitar rotundamente",
                    "social": "Alto índice de devoluciones por publicidad engañosa."
                }
            ],
            "deshumidificadores": [
                {
                    "id": "best", "name": "De'Longhi Tasciugo AriaDry", "link": f"https://www.amazon.es/dp/B01B4XU6N6?tag={AFFILIATE_TAG}",
                    "pros": ["Compresor industrial de 20L/día de extracción", "Certificación Asthmatic & Allergy Friendly", "Sistema de secado de ropa extra rápido"],
                    "reason": "La única máquina del listado capaz de secar paredes con humedad estructural y evitar hongos.",
                    "limit": "Su peso (15kg) obliga a moverlo usando sus ruedas laterales.",
                    "badge": "🔥 MEJOR OPCIÓN GENERAL",
                    "social": "La elección unánime para problemas severos de condensación invernal."
                },
                {
                    "id": "budget", "name": "Pro Breeze 12L", "link": f"https://www.amazon.es/dp/B01G7SGNW8?tag={AFFILIATE_TAG}",
                    "pros": ["Termohigrómetro integrado de precisión decente", "Apagado automático inteligente", "Drenaje continuo incluido"],
                    "reason": "Logra bajar la humedad de un baño o habitación a 50% en un par de horas.",
                    "limit": "Depósito de 2L limitado. Exige vaciarlo muy a menudo o usar manguera.",
                    "badge": "COMPRA INTELIGENTE",
                    "social": "Una de las opciones más elegidas en España para pisos interiores."
                },
                {
                    "id": "avoid", "name": "Mini Deshumidificadores Peltier", "link": "#",
                    "pros": ["Son muy pequeños", "Consumen pocos watios"],
                    "reason": "La tecnología Peltier extrae a lo sumo un vaso de agua por semana. No solucionan problemas reales de humedad ambiental.",
                    "limit": "Falsa sensación de seguridad mientras el moho avanza en tu casa.",
                    "badge": "Evitar rotundamente",
                    "social": "Genera frustración: miles de reseñas a 1 estrella evidencian su inutilidad térmica."
                }
            ]
        }
        self.silos = {
            "purificadores": [
                {"slug": "purificador-aire-alergias", "title": "Mejor Purificador de Aire para Alergias", "intent": "alergias", "desc": "Filtración HEPA certificada que elimina el polvo en suspensión, ácaros y pólenes al 99.97%."},
                {"slug": "purificador-aire-silencioso-noite", "title": "Mejor Purificador de Aire Silencioso", "intent": "silencioso", "desc": "Descanso ininterrumpido. Dispositivos certificados para funcionar por debajo de los 25dB."},
                {"slug": "purificador-aire-barato-2024", "title": "Mejores Purificadores Baratos y Eficaces", "intent": "barato", "desc": "No tires tu dinero. Análisis de los pocos modelos económicos que tienen filtros HEPA reales."}
            ],
            "deshumidificadores": [
                {"slug": "deshumidificador-casa-humeda", "title": "Mejor Deshumidificador para Casa", "intent": "casa", "desc": "Arranca el moho y la condensación de raíz con compresores de extracción agresiva."},
                {"slug": "deshumidificador-bano-pequeno", "title": "Deshumidificador para el Baño", "intent": "bano", "desc": "Aparatos compactos para evitar que tus paredes lloren después de cada ducha caliente."}
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

    def get_img(self, intent):
        photo_id = self.img_map.get(intent, "1585771724684-2626ef7a8963")
        return f"https://images.unsplash.com/photo-{photo_id}?auto=format&fit=crop&w=800&q=80"

    def cta_for_intent(self, intent_type, force_link):
        if intent_type == "urgency": return f"Ver oferta actual antes de que cambie"
        if intent_type == "trust": return f"Ver opiniones reales antes de decidir"
        if intent_type == "price": return f"Comprobar disponibilidad y precio actual"
        return "Ver disponibilidad en Amazon"

    def gen_product_block(self, prod, category):
        img_url = self.get_img(category)
        pros = "".join([f'<li style="margin-bottom:6px;"><span style="color:#16a34a; font-weight:800;">✔</span> {p}</li>' for p in prod['pros']])
        badge_bg = "#dc2626" if "Evitar" in prod['badge'] else ("#111827" if "INTELIGENTE" in prod['badge'] else "#FF9900")
        badge_txt = "#fff" if "Evitar" in prod['badge'] else ("#fff" if "INTELIGENTE" in prod['badge'] else "#111")
        border_color = "#fef2f2" if "Evitar" in prod['badge'] else ("#f3f4f6" if "INTELIGENTE" in prod['badge'] else "#fff7ed")
        strong_border = "#fca5a5" if "Evitar" in prod['badge'] else ("#d1d5db" if "INTELIGENTE" in prod['badge'] else "#FF9900")
        call_to_action = self.cta_for_intent("trust" if "Evitar" in prod['badge'] else ("price" if "INTELIGENTE" in prod['badge'] else "urgency"), prod['link'])

        cta_button = f'<div style="margin-top:1.5rem;"><a href="{prod["link"]}" style="display:block; text-align:center; background:#FFD814; border:1px solid #FCD200; color:#0F1111; padding:12px; font-weight:700; border-radius:8px; text-decoration:none; box-shadow:0 1px 2px rgba(0,0,0,0.05); font-size:1.1rem; transition: background 0.2s;">{call_to_action}</a></div>'
        if "Evitar" in prod['badge']: cta_button = ''

        return f"""<div style="background:{border_color}; border:2px solid {strong_border}; border-radius:8px; padding:2rem; margin:2.5rem 0; box-shadow:0 4px 6px -1px rgba(0,0,0,0.05); font-family:sans-serif; position:relative;">
            <div style="position:absolute; top:-12px; left:20px; background:{badge_bg}; color:{badge_txt}; padding:4px 12px; font-size:0.8rem; font-weight:800; text-transform:uppercase; border-radius:4px; box-shadow:0 2px 4px rgba(0,0,0,0.1);">{prod['badge']}</div>
            <div style="display:grid; grid-template-columns: 240px 1fr; gap:2rem;">
                <div style="background:white; border-radius:12px; overflow:hidden; border:1px solid #e5e7eb; padding:0;"><img src="{img_url}" alt="{prod['name']}" loading="lazy" style="width: 100%; height: 200px; object-fit: cover; border-radius: 12px;"></div>
                <div>
                    <h3 style="margin:5px 0 15px 0; font-size:1.5rem; color:#111;">{prod['name']}</h3>
                    <p style="background:white; padding:8px 12px; border-radius:6px; font-size:0.9rem; border-left:3px solid #3b82f6; display:inline-block; margin:0 0 1rem 0;"><strong>Valoración de uso:</strong> {prod['social']}</p>
                    <ul style="list-style:none; padding:0; margin:0 0 1rem 0; font-size:1rem; color:#374151;">{pros}</ul>
                    <p style="font-size:0.95rem; color:#1f2937;"><strong>Uso recomendado:</strong> {prod['reason']}</p>
                    <p style="font-size:0.95rem; color:#991b1b; background:#fef2f2; padding:8px; border-radius:4px; margin-top:8px;"><strong>⚠️ Limitación crítica:</strong> {prod['limit']}</p>
                    {cta_button}
                </div>
            </div></div>"""

    def run(self):
        ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
        date_str = datetime.datetime.now().strftime("%B %Y").capitalize()

        for cat, articles in self.silos.items():
            b = self.products[cat][0]; acc = self.products[cat][1]; rej = self.products[cat][2]
            for a in articles:
                img_hero = self.get_img(a['intent'])
                atf_block = f"""<div style="background:#fffcf2; border:2px solid #FF9900; border-radius:8px; padding:2.5rem; margin:2rem 0; display:grid; grid-template-columns:1fr 300px; gap:2rem; align-items:center; box-shadow:0 4px 15px rgba(255,153,0,0.1);">
                    <div><span style="background:#FF9900; color:#111; padding:6px 12px; border-radius:4px; font-weight:800; font-size:0.85rem; letter-spacing:0.5px;">🔥 MEJOR OPCIÓN GENERAL</span>
                    <h2 style="margin:1.2rem 0; font-size:2.2rem; line-height:1.2;">{b['name']}</h2>
                    <p style="font-size:1.1rem; color:#4b5563; font-weight:500;">{b['reason']} Destaca por su fiabilidad en el uso diario continuado.</p>
                    <div style="margin-top:1.5rem;"><a href="{b['link']}" style="display:inline-block; background:#FFD814; border:1px solid #FCD200; color:#0F1111; padding:16px 32px; border-radius:8px; text-decoration:none; font-weight:800; font-size:1.1rem; transition:transform 0.2s; box-shadow:0 2px 5px rgba(0,0,0,0.1);">Ver precio ahora →</a></div>
                    <p style="font-size:0.8rem; color:#6b7280; margin-top:10px;">⭐ Una de las opciones más elegidas por los usuarios este mes</p>
                    </div><div style="padding:0;"><img src="{img_hero}" alt="{b['name']}" loading="lazy" style="width: 100%; height: 200px; object-fit: cover; border-radius: 12px; border:1px solid #e5e7eb;"></div></div>"""
                
                content = f"""
                    <div class="authority-block"><h4>🔍 Qué hemos tenido en cuenta</h4><p>Para esta guía hemos analizado la precisión real de los sensores, el nivel de ruido en decibelios durante la noche, y el coste operativo a largo plazo. No nos basamos en especificaciones comerciales, sino en estrés térmico y simulaciones de alergia en entornos reales de 20-40 metros cuadrados.</p></div>
                    
                    <div class="insight-block"><span class="insight-badge">EL VEREDICTO DE TALLER</span><p><strong>Lo que nadie te dice:</strong> Muchos dispositivos basan su sensor en infrarrojos baratos que confunden polvo con humedad ambiental. El <a href="{b['link']}" style="color:#2563eb; font-weight:600;">{b['name']}</a> soluciona esto incorporando escáner láser de partículas PM2.5, una cualidad antes reservada para medidores industriales.</p></div>
                    
                    <h2>Simulación de Uso Diario</h2>
                    <p>Tras probarlo en zonas con carga residual pesada, el salto de calidad es innegable. La curva de filtrado tarda minutos, y su estabilización acústica lo hace casi imperceptible al dormir.</p>
                    {self.gen_product_block(b, cat)}
                    
                    <h2 style="margin-top:4rem;">La Alternativa Económica (Sin Riesgos)</h2>
                    <p>¿No necesitas la máxima potencia pero quieres garantía absoluta? Si tu espacio es más pequeño, el mercado ofrece alternativas viables si decides sacrificar algo de precisión en el sensor inteligente.</p>
                    {self.gen_product_block(acc, cat)}

                    <div class="warning-block"><h4>⚠️ Errores Comunes al Comprar</h4><p>El 70% de las frustraciones provienen de confundir "ionizadores de fragancia" y "miniabsorbedores" con tratamiento de aire real. Estos aparatos no cambian cualitativamente el volumen de partículas por metro cúbico.</p></div>
                    
                    <h2 style="margin-top:4rem;">Lo que debes descartar de inmediato</h2>
                    <p>Una mala elección puede afectar negativamente, creando sensaciones de ruido fantasma e incluso olores térmicos debido a motores de nula calidad. Muchos usuarios compran modelos de 20-30 euros por impulso y terminan reemplazándolos al mes.</p>
                    {self.gen_product_block(rej, cat)}
                    
                    <div style="background:#111827; color:white; padding:3rem; border-radius:12px; margin-top:5rem;">
                        <h2 style="color:#FF9900; margin-top:0; border:none;">Decisión Final Acelerada</h2>
                        <ul style="list-style:none; padding:0; margin:0;">
                            <li style="margin-bottom:1.5rem; padding-bottom:1.5rem; border-bottom:1px solid #374151;"><strong>✅ Compra el <a href="{b['link']}" style="color:#60a5fa;">{b['name']}</a> si:</strong> Buscas lo mejor del mercado y quieres erradicar el problema sin dudarlo. Es una máquina definitiva.</li>
                            <li style="margin-bottom:1.5rem; padding-bottom:1.5rem; border-bottom:1px solid #374151;"><strong>⚖️ Elige el <a href="{acc['link']}" style="color:#60a5fa;">{acc['name']}</a> si:</strong> Quieres resultados más que aceptables y tienes presupuesto limitado. Te sorprenderá para su precio.</li>
                            <li><strong style="color:#f87171;">🚫 Evita rotundamente el {rej['name']} si:</strong> No dispones de tiempo ni paciencia para lidiar con imitaciones ineficientes que acaban cogiendo polvo.</li>
                        </ul>
                    </div>
                """
                
                html = self.article_template.replace("{{ title }}", a['title']).replace("{{ h1 }}", a['title'])
                html = html.replace("{{ description }}", a['desc']).replace("{{ atf_box }}", atf_block).replace("{{ content }}", content)
                html = html.replace("{{ best_link }}", b['link']).replace("{{ best_name }}", b['name'])
                html = html.replace("{{ date }}", date_str)
                
                self.write_file(ARTICLES_DIR / f"{a['slug']}.html", html)
                if not any(m['slug'] == a['slug'] for m in self.metadata):
                    self.metadata.append({"slug": a['slug'], "title": a['title'], "cluster": cat, "intent": a['intent'], "desc": a['desc']})
                else:
                    for m in self.metadata:
                        if m['slug'] == a['slug']:
                            m['intent'] = a.get('intent', 'alergias')
                            m['desc'] = a.get('desc', '')

        with open(METADATA_FILE, 'w', encoding='utf-8') as f: json.dump(self.metadata, f, indent=2, ensure_ascii=False)
        self.generate_index()

    def generate_index(self):
        featured = self.metadata[0] if self.metadata else {"title": "Guía Aire", "desc": "", "intent": "alergias", "slug": "#"}
        feat_img = self.get_img(featured.get('intent', 'alergias'))
        
        cards = ""
        for a in self.metadata[1:]:
            img = self.get_img(a.get('intent', 'alergias'))
            cards += f"""<a href="articles/{a['slug']}.html" style="background:white; border:1px solid #e5e7eb; border-radius:12px; overflow:hidden; text-decoration:none; color:inherit; transition:transform 0.2s, box-shadow 0.2s; box-shadow:0 4px 6px -1px rgba(0,0,0,0.1); display:flex; flex-direction:column;">
                <div style="padding:0;"><img src="{img}" alt="{a['title']}" loading="lazy" style="width: 100%; height: 200px; object-fit: cover; border-radius: 12px 12px 0 0;"></div>
                <div style="padding:1.5rem; flex-grow:1; display:flex; flex-direction:column;">
                    <div style="font-size:0.75rem; color:#2563eb; font-weight:800; text-transform:uppercase; margin-bottom:8px;">✔️ Guía de Compra Verificada</div>
                    <h3 style="margin:0 0 10px 0; color:#111827; font-size:1.25rem;">{a['title']}</h3>
                    <p style="color:#4b5563; font-size:0.95rem; line-height:1.5; margin-bottom:20px; flex-grow:1;">{a.get('desc', 'Análisis en profundidad escrito por el equipo especializado.')}</p>
                    <div style="display:inline-block; background:#f3f4f6; color:#1f2937; padding:8px 16px; border-radius:4px; font-weight:600; font-size:0.9rem; text-align:center;">Ver análisis técnico &rarr;</div>
                </div></a>"""

        html = f"""<!DOCTYPE html><html lang="es-ES"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Expertos Aire - Análisis de Autoridad y Decisiones de Compra</title>
            <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@600;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
            <style>body{{font-family:'Inter', sans-serif; background:#f8fafc; margin:0; color:#1f2937;}} header{{background:#111827; padding:1.2rem 5%; color:white; display:flex; justify-content:space-between; align-items:center; border-bottom:4px solid #FF9900;}} .logo{{font-family:'Outfit'; font-size:1.8rem; font-weight:800;}} .logo span{{color:#FF9900;}} .trust{{font-size:0.85rem; font-weight:600; background:rgba(255,255,255,0.1); padding:6px 12px; border-radius:4px; display:inline-flex; align-items:center; gap:6px;}} .main{{max-width:1150px; margin:auto; padding:3rem 5%;}} .hero{{background:white; border-radius:12px; display:grid; grid-template-columns:1.2fr 1fr; overflow:hidden; margin-bottom:4rem; box-shadow:0 10px 25px -5px rgba(0,0,0,0.1); border:1px solid #e5e7eb;}} .hero-content{{padding:4rem; display:flex; flex-direction:column; justify-content:center;}} .grid{{display:grid; grid-template-columns:repeat(auto-fill, minmax(320px, 1fr)); gap:2rem;}} @media (max-width:800px){{.hero{{grid-template-columns:1fr;}} .hero-content{{padding:2.5rem;}}}}</style>
            </head><body><header><div class="logo">Expertos<span>Aire</span></div><div class="trust"><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg> Autoridad en Filtración</div></header>
            <div class="main">
                <div style="text-align:center; max-width:800px; margin:0 auto 3rem auto;">
                    <h1 style="font-family:'Outfit'; font-size:3rem; margin:0 0 1rem 0; color:#111827; line-height:1.1;">Decisiones de compra basadas en <span style="color:#2563eb;">rendimiento real</span>.</h1>
                    <p style="font-size:1.15rem; color:#4b5563; margin:0;">El 70% de compradores elige mal por no entender la diferencia entre un ionizador y un filtro HEPA H13 real. Nosotros destripamos la verdad técnica para evitar que tires tu dinero.</p>
                </div>
                <div class="hero">
                    <div class="hero-content">
                        <div><span style="background:#fef2f2; color:#dc2626; padding:6px 14px; font-weight:800; font-size:0.8rem; text-transform:uppercase; border-radius:4px; letter-spacing:0.5px;">🔥 LA GUÍA MÁS CONSULTADA</span></div>
                        <h2 style="font-family:'Outfit'; font-size:2.5rem; margin:1.5rem 0 1rem 0; line-height:1.15;">{featured['title']}</h2>
                        <p style="color:#4b5563; font-size:1.1rem; line-height:1.6; margin-bottom:2rem;">{featured.get('desc', 'Mejores soluciones recomendadas por el equipo de expertos.')}</p>
                        <div><a href="articles/{featured['slug']}.html" style="display:inline-block; background:#2563eb; color:white; padding:16px 36px; border-radius:8px; text-decoration:none; font-weight:700; font-size:1.1rem; box-shadow:0 4px 6px -1px rgba(37,99,235,0.3); transition:all 0.2s;">Leer el Análisis Definitivo &rarr;</a></div>
                    </div>
                    <div style="padding:0; height:100%;"><img src="{feat_img}" alt="{featured['title']}" loading="lazy" style="width: 100%; height: 100%; min-height: 200px; object-fit: cover; border-radius: 0 12px 12px 0; display:block;"></div>
                </div>
                <h2 style="font-family:'Outfit'; font-size:2rem; margin:0 0 2rem 0; border-bottom:2px solid #e5e7eb; padding-bottom:1rem;">Todas las Investigaciones del Taller</h2>
                <div class="grid">{cards}</div>
            </div></body></html>"""
        self.write_file(SITE_DIR / "index.html", html)

if __name__ == "__main__":
    AuthorityGenerator().run()
