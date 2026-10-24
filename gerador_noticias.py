import requests
import json
import random
from datetime import datetime

# ==============================================================================
# CONFIGURAÇÃO DE MÚLTIPLAS APIs E MONETIZAÇÃO ADSTERRA
# ==============================================================================
NEWS_API_KEY = "4e42db8a8a6645fbad1039ba84a6ea4f"
# ==============================================================================

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechNews PRO - Inovação, Ciência & Negócios</title>
    <style>
        :root {
            --bg-color: #f4f6f9;
            --card-bg: #ffffff;
            --text-main: #111827;
            --text-muted: #6b7280;
            --primary: #ef4444; 
            --accent: #2563eb;
            --dark: #0f172a;
            --ad-bg: #e2e8f0;
            --border: #e5e7eb;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
        body { background-color: var(--bg-color); color: var(--text-main); line-height: 1.6; }

        #progress-bar { position: fixed; top: 0; left: 0; height: 4px; background: var(--primary); width: 0%; z-index: 9999; transition: width 0.2s; }

        .breaking-ticker { background: var(--primary); color: #fff; padding: 0.4rem 5%; font-size: 0.85rem; font-weight: 600; display: flex; align-items: center; gap: 1rem; overflow: hidden; white-space: nowrap; }
        .breaking-badge { background: #000; color: #fff; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; animation: pulse 1.5s infinite; }
        @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.6; } 100% { opacity: 1; } }

        header { background: var(--dark); color: #fff; padding: 1.2rem 5%; position: sticky; top: 0; z-index: 1000; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
        .nav-container { max-width: 1400px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; }
        .logo { font-size: 2rem; font-weight: 900; letter-spacing: -1px; color: #fff; text-decoration: none; display: flex; align-items: center; gap: 5px; }
        .logo span { color: var(--primary); }
        .nav-links { display: flex; gap: 1.5rem; list-style: none; }
        .nav-links a { color: #cbd5e1; text-decoration: none; font-weight: 600; font-size: 0.95rem; transition: color 0.2s; }
        .nav-links a:hover { color: #fff; }
        .cta-btn { background: var(--primary); color: #fff; border: none; padding: 0.6rem 1.4rem; border-radius: 6px; font-weight: 700; cursor: pointer; transition: 0.3s; text-decoration: none; font-size: 0.9rem; }
        .cta-btn:hover { background: #dc2626; transform: scale(1.03); }

        /* ESPAÇO PUBLICITÁRIO DO TOPO (Com o seu Banner Adsterra 728x90) */
        .ad-banner-top { max-width: 970px; min-height: 90px; margin: 1.8rem auto; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }

        .main-container { max-width: 1400px; margin: 0 auto 4rem auto; padding: 0 5%; display: grid; grid-template-columns: 7fr 3fr; gap: 2.5rem; }

        .hero-card { position: relative; border-radius: 14px; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.1); margin-bottom: 2.5rem; display: block; text-decoration: none; background: #000; }
        .hero-card img { width: 100%; height: 460px; object-fit: cover; opacity: 0.85; transition: transform 0.5s ease, opacity 0.3s; }
        .hero-card:hover img { transform: scale(1.03); opacity: 0.7; }
        .hero-overlay { position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(to top, rgba(0,0,0,0.95) 10%, rgba(0,0,0,0.5) 60%, transparent 100%); padding: 2.5rem; color: #fff; }
        .badge-source { background: var(--primary); color: #fff; padding: 4px 12px; border-radius: 4px; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; display: inline-block; margin-bottom: 0.8rem; }
        .hero-overlay h1 { font-size: 2.2rem; line-height: 1.25; margin-bottom: 0.8rem; font-weight: 800; }
        .hero-overlay p { color: #e2e8f0; font-size: 1.05rem; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }

        .section-title { font-size: 1.4rem; font-weight: 800; margin-bottom: 1.5rem; border-left: 5px solid var(--primary); padding-left: 12px; color: var(--dark); }
        .feed-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.8rem; }
        .news-card { background: var(--card-bg); border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.04); border: 1px solid var(--border); display: flex; flex-direction: column; transition: transform 0.25s ease, box-shadow 0.25s ease; }
        .news-card:hover { transform: translateY(-6px); box-shadow: 0 12px 24px rgba(0,0,0,0.1); }
        .card-img-wrapper { position: relative; width: 100%; height: 200px; overflow: hidden; background: #e5e7eb; }
        .card-img-wrapper img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.4s ease; }
        .news-card:hover .card-img-wrapper img { transform: scale(1.06); }
        .card-tag { position: absolute; top: 12px; left: 12px; background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(4px); color: #fff; padding: 4px 10px; border-radius: 6px; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; }
        .card-body { padding: 1.5rem; display: flex; flex-direction: column; flex-grow: 1; }
        .card-meta { font-size: 0.78rem; color: var(--text-muted); margin-bottom: 0.6rem; display: flex; justify-content: space-between; font-weight: 600; }
        .card-title { font-size: 1.15rem; font-weight: 700; color: var(--text-main); margin-bottom: 0.8rem; line-height: 1.35; }
        .card-desc { font-size: 0.92rem; color: var(--text-muted); margin-bottom: 1.4rem; flex-grow: 1; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
        .read-btn { display: inline-flex; align-items: center; justify-content: center; background: #f1f5f9; color: var(--dark); font-weight: 700; font-size: 0.88rem; padding: 0.75rem 1rem; border-radius: 8px; text-decoration: none; transition: 0.2s; margin-top: auto; }
        .read-btn:hover { background: var(--primary); color: #fff; }

        .native-ad-card { background: linear-gradient(145deg, #ffffff, #fff5f5); border: 2px solid #fecaca; border-radius: 12px; padding: 1.8rem; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; box-shadow: 0 4px 15px rgba(239, 68, 68, 0.08); }
        .native-ad-card .ad-badge { background: #fee2e2; color: #b91c1c; font-size: 0.7rem; font-weight: 800; padding: 3px 10px; border-radius: 20px; text-transform: uppercase; margin-bottom: 1rem; }
        .native-ad-card h3 { font-size: 1.25rem; color: var(--dark); margin-bottom: 0.8rem; }
        .native-ad-card p { font-size: 0.9rem; color: var(--text-muted); margin-bottom: 1.5rem; }

        .sidebar { display: flex; flex-direction: column; gap: 2rem; }
        .widget { background: var(--card-bg); border-radius: 12px; padding: 1.6rem; border: 1px solid var(--border); box-shadow: 0 4px 12px rgba(0,0,0,0.03); }
        .widget-title { font-size: 1.1rem; font-weight: 800; margin-bottom: 1.2rem; padding-bottom: 0.6rem; border-bottom: 2px solid var(--primary); display: flex; align-items: center; justify-content: space-between; }
        
        .trending-list { list-style: none; display: flex; flex-direction: column; gap: 1rem; }
        .trending-item { display: flex; gap: 1rem; align-items: flex-start; text-decoration: none; color: inherit; }
        .trending-num { font-size: 1.6rem; font-weight: 900; color: #cbd5e1; line-height: 1; }
        .trending-item:hover .trending-text { color: var(--primary); }
        .trending-text { font-size: 0.92rem; font-weight: 700; line-height: 1.35; transition: 0.2s; }

        .newsletter-box { background: var(--dark); color: #fff; border-radius: 12px; padding: 1.8rem; text-align: center; }
        .newsletter-box h3 { font-size: 1.25rem; margin-bottom: 0.6rem; }
        .newsletter-box p { font-size: 0.88rem; color: #94a3b8; margin-bottom: 1.2rem; }
        .newsletter-box input { width: 100%; padding: 0.8rem; border-radius: 6px; border: none; margin-bottom: 0.8rem; font-size: 0.9rem; }
        .newsletter-box button { width: 100%; padding: 0.85rem; background: var(--primary); color: #fff; border: none; border-radius: 6px; font-weight: 800; cursor: pointer; transition: 0.2s; }
        .newsletter-box button:hover { background: #dc2626; }

        .sticky-ad-container { position: sticky; top: 90px; }
        .ad-sidebar-box { width: 100%; height: 600px; background: var(--ad-bg); border: 2px dashed #cbd5e1; border-radius: 12px; display: flex; flex-direction: column; align-items: center; justify-content: center; color: var(--text-muted); text-align: center; padding: 1rem; }

        footer { background: var(--dark); color: #94a3b8; text-align: center; padding: 3rem 5%; font-size: 0.9rem; border-top: 4px solid var(--primary); }

        @media (max-width: 992px) {
            .main-container { grid-template-columns: 1fr; }
            .nav-links { display: none; }
            .hero-card img { height: 320px; }
            .hero-overlay h1 { font-size: 1.6rem; }
        }
    </style>
</head>
<body>
    <div id="progress-bar"></div>

    <div class="breaking-ticker">
        <span class="breaking-badge">Ao Vivo</span>
        <span>🚀 Portal Automatizado • Sincronizado via Multi-API • Atualizado em: {data_atualizacao}</span>
    </div>

    <header>
        <div class="nav-container">
            <a href="#" class="logo">TechNews<span>.PRO</span></a>
            <ul class="nav-links">
                <li><a href="#">Tecnologia</a></li>
                <li><a href="#">Negócios & Finanças</a></li>
                <li><a href="#">Ciência & Espaço</a></li>
                <li><a href="#">Inteligência Artificial</a></li>
            </ul>
            <a href="#newsletter" class="cta-btn">Assinar VIP</a>
        </div>
    </header>

    <!-- SEU ANÚNCIO REAL ADSTERRA (728x90) NO TOPO -->
    <div class="ad-banner-top">
        <script>
          atOptions = {
            'key' : '06959dfe796ac17610a3027d9ede544f',
            'format' : 'iframe',
            'height' : 90,
            'width' : 728,
            'params' : {}
          };
        </script>
        <script src="https://bicea.org/22/06959dfe796ac17610a3027d9ede544f"></script>
    </div>

    <main class="main-container">
        <div class="content-column">
            {hero_section}

            <h2 class="section-title">Últimas Atualizações do Ecossistema</h2>
            <div class="feed-grid">
                {feed_section}
            </div>
        </div>

        <aside class="sidebar">
            <div class="widget">
                <div class="widget-title">
                    <span>🔥 Mais Lidas Hoje</span>
                </div>
                <ul class="trending-list">
                    {trending_section}
                </ul>
            </div>

            <div class="newsletter-box" id="newsletter">
                <h3>💰 Newsletter Lucrativa</h3>
                <p>Receba análises exclusivas de tecnologia, IA e oportunidades de negócios todas as manhãs.</p>
                <input type="email" placeholder="Digite seu melhor e-mail...">
                <button onclick="alert('Inscrição simulada com sucesso!')">Quero Receber Grátis</button>
            </div>

            <div class="sticky-ad-container">
                <div class="ad-sidebar-box">
                    <span class="ad-label">Publicidade Fixa (300x600)</span>
                    <strong>[ Próximo Bloco de Anúncio ]</strong>
                    <p style="font-size: 0.8rem; margin-top: 10px;">Anúncio lateral fixo para maximizar sua receita por visualização.</p>
                </div>
            </div>
        </aside>
    </main>

    <footer>
        <p><strong>TechNews.PRO</strong> &copy; {ano_atual} — Portal Automatizado via Python Multi-API.</p>
        <p style="margin-top: 8px; font-size: 0.8rem;">Fontes Integradas: NewsAPI • IBGE Notícias • Spaceflight News • Dev.to</p>
    </footer>

    <script>
        window.onscroll = function() {
            var winScroll = document.body.scrollTop || document.documentElement.scrollTop;
            var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            var scrolled = (winScroll / height) * 100;
            document.getElementById("progress-bar").style.width = scrolled + "%";
        };
    </script>
</body>
</html>
"""

def fetch_ibge_noticias():
    noticias = []
    try:
        url = "https://servicodados.ibge.gov.br/api/v3/noticias/?qtd=6"
        r = requests.get(url, timeout=8)
        if r.status_code == 200:
            for item in r.json().get("items", []):
                img_url = "https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?auto=format&fit=crop&w=800&q=80"
                try:
                    imagens_json = json.loads(item.get("imagens", "{}"))
                    if imagens_json.get("image_intro"):
                        img_url = "https://agenciadenoticias.ibge.gov.br/" + imagens_json["image_intro"]
                except:
                    pass
                noticias.append({
                    "title": item.get("titulo"),
                    "desc": item.get("introducao", "Confira os dados completos divulgados pelo portal oficial."),
                    "img": img_url,
                    "url": item.get("link", "#"),
                    "source": "IBGE Brasil",
                    "date": item.get("data_publicacao", "Hoje")[:10]
                })
    except:
        pass
    return noticias

def fetch_devto_pt():
    noticias = []
    try:
        url = "https://dev.to/api/articles?tag=portuguese&per_page=6"
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=8)
        if r.status_code == 200:
            for item in r.json():
                noticias.append({
                    "title": item.get("title"),
                    "desc": item.get("description") or "Artigo técnico publicado na comunidade global de desenvolvedores.",
                    "img": item.get("cover_image") or item.get("social_image") or "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=800&q=80",
                    "url": item.get("url", "#"),
                    "source": "Dev.to Tech",
                    "date": item.get("readable_publish_date", "Recente")
                })
    except:
        pass
    return noticias

def fetch_spaceflight_news():
    noticias = []
    try:
        url = "https://api.spaceflightnewsapi.net/v4/articles/?limit=4"
        r = requests.get(url, timeout=8)
        if r.status_code == 200:
            for item in r.json().get("results", []):
                noticias.append({
                    "title": item.get("title"),
                    "desc": item.get("summary", ""),
                    "img": item.get("image_url") or "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=800&q=80",
                    "url": item.get("url", "#"),
                    "source": "SpaceTech Global",
                    "date": item.get("published_at", "")[:10]
                })
    except:
        pass
    return noticias

def fetch_newsapi():
    noticias = []
    if not NEWS_API_KEY:
        return noticias
    try:
        url = f"https://newsapi.org/v2/everything?q=tecnologia OR inteligencia artificial OR mercado&language=pt&sortBy=publishedAt&pageSize=6&apiKey={NEWS_API_KEY}"
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=8)
        if r.status_code == 200:
            for item in r.json().get("articles", []):
                if item.get("title") and item.get("title") != "[Removed]":
                    noticias.append({
                        "title": item.get("title"),
                        "desc": item.get("description") or "Clique para ler a matéria completa na fonte oficial.",
                        "img": item.get("urlToImage") or "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=800&q=80",
                        "url": item.get("url", "#"),
                        "source": item.get("source", {}).get("name", "NewsAPI"),
                        "date": item.get("publishedAt", "")[:10]
                    })
    except:
        pass
    return noticias

FALLBACK_NEWS = [
    {
        "title": "Inteligência Artificial Generativa redefine o mercado de tecnologia e cria novas profissões em alta",
        "desc": "Grandes corporações aceleram a adoção de agentes autônomos para otimizar processos e escalar produtos digitais.",
        "img": "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=1200&q=80",
        "url": "https://news.google.com",
        "source": "Destaque IA",
        "date": "3 min de leitura"
    },
    {
        "title": "Fintechs brasileiras batem recorde de captação e expandem soluções de pagamento instantâneo",
        "desc": "Novos relatórios apontam crescimento expressivo no setor financeiro digital com foco em crédito inteligente.",
        "img": "https://images.unsplash.com/photo-1559526324-4b87b5e36e44?auto=format&fit=crop&w=800&q=80",
        "url": "https://agenciadenoticias.ibge.gov.br",
        "source": "Finanças & Negócios",
        "date": "4 min de leitura"
    },
    {
        "title": "Computação em Nuvem e Cibersegurança lideram os investimentos de TI neste trimestre",
        "desc": "Proteção de dados críticos e infraestrutura escalável tornam-se prioridade máxima para startups e bancos.",
        "img": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=800&q=80",
        "url": "https://dev.to",
        "source": "Cibersegurança",
        "date": "5 min de leitura"
    },
    {
        "title": "Nova geração de satélites de baixa órbita promete internet de alta velocidade em áreas remotas",
        "desc": "Avanços na indústria aeroespacial reduzem o custo de lançamento e conectam regiões agrícolas.",
        "img": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=800&q=80",
        "url": "https://spaceflightnewsapi.net",
        "source": "SpaceTech",
        "date": "3 min de leitura"
    }
]

def gerar_portal():
    todas_noticias = []
    todas_noticias.extend(fetch_newsapi())
    todas_noticias.extend(fetch_ibge_noticias())
    todas_noticias.extend(fetch_devto_pt())
    todas_noticias.extend(fetch_spaceflight_news())

    if len(todas_noticias) < 4:
        todas_noticias.extend(FALLBACK_NEWS)
    else:
        random.shuffle(todas_noticias)

    hero = todas_noticias[0]
    hero_html = f"""
    <a href="{hero['url']}" target="_blank" rel="noopener noreferrer" class="hero-card">
        <img src="{hero['img']}" alt="Destaque" onerror="this.src='https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&q=80'">
        <div class="hero-overlay">
            <span class="badge-source">🔥 Destaque • {hero['source']}</span>
            <h1>{hero['title']}</h1>
            <p>{hero['desc']}</p>
        </div>
    </a>
    """

    feed_html = ""
    for idx, art in enumerate(todas_noticias[1:9]):
        feed_html += f"""
        <article class="news-card">
            <div class="card-img-wrapper">
                <span class="card-tag">{art['source']}</span>
                <img src="{art['img']}" alt="Capa" onerror="this.src='https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=800&q=80'">
            </div>
            <div class="card-body">
                <div class="card-meta">
                    <span>📅 {art['date']}</span>
                    <span>⚡ Leitura Rápida</span>
                </div>
                <h3 class="card-title">{art['title']}</h3>
                <p class="card-desc">{art['desc']}</p>
                <a href="{art['url']}" target="_blank" rel="noopener noreferrer" class="read-btn">Ler Artigo Completo &rarr;</a>
            </div>
        </article>
        """

        if idx == 1:
            feed_html += """
            <div class="native-ad-card">
                <span class="ad-badge">Conteúdo Patrocinado • Native Ad</span>
                <h3>🚀 Descubra a Ferramenta de IA que Automatiza Negócios</h3>
                <p>Espaço estratégico para link de afiliado (Hotmart, Kiwify, Amazon) ou bloco In-Feed.</p>
                <a href="#newsletter" class="cta-btn" style="width: 100%;">Conhecer Oferta Agora &rarr;</a>
            </div>
            """

    trending_html = ""
    for idx, art in enumerate(todas_noticias[1:6], start=1):
        trending_html += f"""
        <li>
            <a href="{art['url']}" target="_blank" rel="noopener noreferrer" class="trending-item">
                <span class="trending-num">0{idx}</span>
                <span class="trending-text">{art['title']}</span>
            </a>
        </li>
        """

    agora = datetime.now()
    html_final = (
        HTML_TEMPLATE
        .replace("{hero_section}", hero_html)
        .replace("{feed_section}", feed_html)
        .replace("{trending_section}", trending_html)
        .replace("{data_atualizacao}", agora.strftime("%d/%m/%Y às %H:%M"))
        .replace("{ano_atual}", str(agora.year))
    )

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_final)
    print("Portal gerado com o anúncio Adsterra integrado!")

if __name__ == "__main__":
    gerar_portal()
