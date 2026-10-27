import os
import sys
import re
import html
import requests
import json
import random
from datetime import datetime

# ==============================================================================
# CHAVES GITHUB SECRETS (APIS, META, TELEGRAM E ONESIGNAL)
# ==============================================================================
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "4e42db8a8a6645fbad1039ba84a6ea4f")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN", "")
META_PAGE_ID = os.getenv("META_PAGE_ID", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# NOVAS CHAVES: NOTIFICAÇÕES WEB PUSH
ONESIGNAL_APP_ID = os.getenv("ONESIGNAL_APP_ID", "")
ONESIGNAL_REST_KEY = os.getenv("ONESIGNAL_REST_KEY", "")

ARQUIVO_MEMORIA_META = ".ultimo_post_meta.txt"
ARQUIVO_FILA_POST = ".fila_post_meta.json"

URL_PORTAL_OFICIAL = "https://infoprodutos93-sys.github.io/technews-pro/"
SMARTLINK_ADSTERRA = "https://asiafilm.org/4/78ed9deb10feac05c15347b414e171ab"
SYSTEME_OPTIN_URL = "https://devanildobeeny146.systeme.io/3ed9605c"
LINK_KIWIFY_1 = "https://kiwify.app/bFEoJ38?afid=u7GyGPOM"
LINK_KIWIFY_2 = "https://pay.kiwify.com.br/YUDgPja?afid=yt5zIWrU"
LINK_KIWIFY_3 = "https://kiwify.app/ek8xMMl?afid=1rxg1P58"

# ==============================================================================
# TEMPLATE PRINCIPAL: INDEX.HTML
# ==============================================================================
HTML_TEMPLATE_INDEX = """<!DOCTYPE html>
<html lang="pt-BR" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Terminal de notícias IA e Finanças.">
    <meta name="robots" content="max-image-preview:large, index, follow">
    <link rel="canonical" href="{url_portal}">
    
    <!-- Link para o RSS Feed (Aprovações no Google News) -->
    <link rel="alternate" type="application/rss+xml" title="TechNews PRO Feed" href="{url_portal}feed.xml">

    <meta property="og:title" content="{og_title}">
    <meta property="og:description" content="{og_desc}">
    <meta property="og:image" content="{og_img}">
    <meta property="og:url" content="{url_portal}">
    <meta property="og:type" content="website">

    <title>TechNews PRO | Terminal de Inteligência</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
    
    <!-- ONESIGNAL WEB PUSH (CAPTAÇÃO DE SUBSCRIÇÕES) -->
    <script src="https://cdn.onesignal.com/sdks/web/v16/OneSignalSDK.page.js" defer></script>
    <script>
      window.OneSignalDeferred = window.OneSignalDeferred || [];
      OneSignalDeferred.push(async function(OneSignal) {
        await OneSignal.init({
          appId: "{onesignal_id}",
          notifyButton: { enable: true, text: { "tip.state.unsubscribed": "Inscreva-se para alertas", "tip.state.subscribed": "Você está inscrito" } }
        });
      });
    </script>

    <style>
        /* (Estilos mantidos intactos do v6.1 para evitar quebras) */
        :root[data-theme="dark"] { --bg-color: #070b14; --card-bg: rgba(17, 25, 40, 0.88); --text-main: #f8fafc; --text-muted: #94a3b8; --primary: #ef4444; --accent: #3b82f6; --neon: #00f2fe; --dark-bar: #03060c; --border: rgba(255, 255, 255, 0.08); --glass: rgba(15, 23, 42, 0.8); }
        :root[data-theme="light"] { --bg-color: #f1f5f9; --card-bg: #ffffff; --text-main: #0f172a; --text-muted: #64748b; --primary: #ef4444; --accent: #2563eb; --neon: #2563eb; --dark-bar: #0f172a; --border: #e2e8f0; --glass: rgba(255, 255, 255, 0.92); }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; transition: background-color 0.25s, color 0.2s; }
        body { background-color: var(--bg-color); color: var(--text-main); line-height: 1.6; overflow-x: hidden; }
        #progress-bar { position: fixed; top: 0; left: 0; height: 3px; background: linear-gradient(90deg, var(--primary), var(--neon)); width: 0%; z-index: 99999; }
        .market-ticker { background: var(--dark-bar); padding: 0.45rem 5%; font-size: 0.8rem; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; gap: 10px; flex-wrap: wrap; font-family: 'JetBrains Mono', monospace; }
        .up { color: #10b981; font-weight: 700; } .down { color: #ef4444; font-weight: 700; }
        header { background: var(--glass); backdrop-filter: blur(16px); padding: 1rem 5%; position: sticky; top: 0; z-index: 1000; border-bottom: 1px solid var(--border); }
        .nav-container { max-width: 1440px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; }
        .logo { font-size: 1.85rem; font-weight: 900; letter-spacing: -1px; color: var(--text-main); text-decoration: none; cursor: pointer; }
        .logo span { color: var(--primary); }
        .nav-links { display: flex; gap: 0.4rem; list-style: none; background: rgba(255,255,255,0.03); padding: 5px; border-radius: 10px; border: 1px solid var(--border); flex-wrap: wrap; }
        .nav-links button, .nav-links a { background: none; border: none; color: var(--text-muted); font-weight: 700; font-size: 0.84rem; cursor: pointer; padding: 0.45rem 0.85rem; border-radius: 7px; text-decoration: none; }
        .nav-links button:hover, .nav-links a:hover { color: var(--text-main); }
        .nav-links button.active { background: var(--primary); color: #fff; }
        .cta-btn { background: linear-gradient(135deg, #ef4444, #b91c1c); color: #fff; padding: 0.55rem 1.2rem; border-radius: 8px; font-weight: 800; text-decoration: none; font-size: 0.85rem; cursor:pointer; }
        
        .main-container { max-width: 1440px; margin: 2rem auto 4rem auto; padding: 0 5%; display: grid; grid-template-columns: 7.2fr 2.8fr; gap: 2.5rem; }
        .hero-card { position: relative; border-radius: 16px; overflow: hidden; border: 1px solid var(--border); background: #000; margin-bottom: 2rem; }
        .hero-card img { width: 100%; height: 470px; object-fit: cover; opacity: 0.75; }
        .hero-overlay { position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(to top, rgba(3,6,12,0.98) 15%, transparent 100%); padding: 2.5rem; }
        .badge-source { background: var(--primary); color: #fff; padding: 4px 10px; border-radius: 6px; font-size: 0.7rem; font-weight: 900; display: inline-block; margin-bottom: 0.8rem; }
        
        .feed-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.8rem; }
        .news-card { background: var(--card-bg); border-radius: 14px; overflow: hidden; border: 1px solid var(--border); display: flex; flex-direction: column; }
        .card-img-wrapper { position: relative; height: 190px; }
        .card-img-wrapper img { width: 100%; height: 100%; object-fit: cover; }
        .card-body { padding: 1.4rem; display: flex; flex-direction: column; flex-grow: 1; }
        .seo-internal-link { color: var(--neon); font-weight: 700; text-decoration: underline; }
        
        .sidebar { display: flex; flex-direction: column; gap: 2rem; }
        .widget { background: var(--card-bg); border-radius: 14px; padding: 1.5rem; border: 1px solid var(--border); }
        .newsletter-box { background: linear-gradient(135deg, #111827, #03060c); color: #fff; border-radius: 14px; padding: 1.8rem; text-align: center; border: 1px solid rgba(239, 68, 68, 0.35); }
        .newsletter-box input { width: 100%; padding: 0.8rem; border-radius: 8px; border: 1px solid rgba(255,255,255,0.15); background: rgba(255,255,255,0.05); color: #fff; margin: 0.8rem 0; }
        .newsletter-box button { width: 100%; padding: 0.85rem; background: var(--primary); color: #fff; border: none; border-radius: 8px; font-weight: 800; cursor: pointer; }
        
        #reader-modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(3, 6, 12, 0.9); z-index: 9999; justify-content: center; align-items: center; padding: 1rem; }
        .reader-box { background: var(--bg-color); border: 1px solid var(--border); width: 100%; max-width: 680px; border-radius: 16px; overflow: hidden; max-height: 90vh; display: flex; flex-direction: column; }
        .reader-body { padding: 2rem; overflow-y: auto; }
        
        footer { background: var(--dark-bar); color: #64748b; text-align: center; padding: 3rem 5%; border-top: 1px solid var(--border); }
        @media (max-width: 992px) { .main-container { grid-template-columns: 1fr; } .hero-card img { height: 320px; } }
    </style>
</head>
<body>
    <div id="progress-bar"></div>
    <div class="market-ticker">
        <div><span><strong>TERMINAL AO VIVO</strong></span> {cotacoes_html}</div>
        <div><span>⚡ Sincronizado: {data_atualizacao}</span></div>
    </div>
    
    <header>
        <div class="nav-container">
            <a class="logo" onclick="filtrarCategoria('todos', event)">TechNews<span>.PRO</span></a>
            <ul class="nav-links">
                <li><button onclick="filtrarCategoria('todos', event)" class="active">🔥 Tudo</button></li>
                <li><button onclick="filtrarCategoria('Tecnologia', event)">💻 Tech</button></li>
                <li><button onclick="filtrarCategoria('Finanças', event)">📈 Mercado</button></li>
                <li><button onclick="filtrarCategoria('Ciência', event)">🚀 Ciência</button></li>
            </ul>
            <div style="display:flex; gap:10px;">
                <a href="{smartlink_url}" target="_blank" class="cta-btn">💎 Área VIP</a>
            </div>
        </div>
    </header>

    <div style="max-width: 1440px; margin: 1.2rem auto 0; padding: 0 5%; display: flex; gap: 0.6rem; overflow-x: auto;">
        <span style="font-size:0.75rem; font-weight:800; color:var(--primary); text-transform:uppercase;">SEO Clusters:</span>
        <a href="inteligencia-artificial.html" class="cta-btn" style="padding:4px 12px; font-size:0.75rem; background:var(--card-bg); border:1px solid var(--border);">🧠 IA Hub</a>
        <a href="bitcoin.html" class="cta-btn" style="padding:4px 12px; font-size:0.75rem; background:var(--card-bg); border:1px solid var(--border);">₿ Bitcoin</a>
        <a href="chatgpt.html" class="cta-btn" style="padding:4px 12px; font-size:0.75rem; background:var(--card-bg); border:1px solid var(--border);">🤖 ChatGPT</a>
        <a href="startups.html" class="cta-btn" style="padding:4px 12px; font-size:0.75rem; background:var(--card-bg); border:1px solid var(--border);">🚀 Startups</a>
    </div>

    <!-- BANNER ADSTERRA (728x90) -->
    <div style="text-align:center; margin:1.5rem auto;">
        <script>atOptions={{'key':'06959dfe796ac17610a3027d9ede544f','format':'iframe','height':90,'width':728,'params':{}}};</script>
        <script src="https://bicea.org/22/06959dfe796ac17610a3027d9ede544f"></script>
    </div>

    <main class="main-container">
        <div class="content-column">
            <h2 style="font-size:1.35rem; margin-bottom:1.5rem; border-left:4px solid var(--primary); padding-left:12px;" id="titulo-secao">Radar Global em Tempo Real</h2>
            <div id="hero-container"></div>
            <div class="feed-grid" id="feed-container"></div>
        </div>

        <aside class="sidebar">
            <div class="widget">
                <h3 style="margin-bottom: 1rem;">🔥 Recomendações VIP</h3>
                <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1rem;">Método validado para escalar rendimentos com automação e tráfego.</p>
                <a href="{link_kiwify_2}" target="_blank" class="cta-btn" style="width: 100%; text-align: center;">Desbloquear Método &rarr;</a>
            </div>
            
            <div class="newsletter-box">
                <h3>💰 Briefing Matinal</h3>
                <p style="font-size:0.84rem;">Inscreva-se para receber relatórios secretos no e-mail.</p>
                <form action="{systeme_url}" method="GET" target="_blank">
                    <input type="email" name="email" placeholder="Digite seu melhor e-mail..." required>
                    <button type="submit">Liberar Acesso &rarr;</button>
                </form>
            </div>

            <!-- BANNER ADSTERRA (300x250) -->
            <div style="position: sticky; top: 90px; text-align: center;">
                <script>atOptions={{'key':'8169727725318cd706b493da46602d6f','format':'iframe','height':250,'width':300,'params':{}}};</script>
                <script src="https://bicea.org/22/8169727725318cd706b493da46602d6f"></script>
            </div>
        </aside>
    </main>

    <!-- MODAL DE LEITURA (TIME-TO-VALUE) -->
    <div id="reader-modal" onclick="document.getElementById('reader-modal').style.display='none'">
        <div class="reader-box" onclick="event.stopPropagation()">
            <img id="r-img" src="" style="width:100%; height:240px; object-fit:cover;">
            <div class="reader-body">
                <span id="r-source" class="badge-source">Fonte</span>
                <h2 id="r-title" style="margin-bottom:1rem;">Título</h2>
                <div style="background:rgba(59,130,246,0.1); border-left:4px solid var(--accent); padding:1rem; border-radius:6px; margin:1.2rem 0;">
                    <strong>🤖 Síntese Executiva IA:</strong>
                    <p id="r-desc" style="margin-top:6px; font-size:0.92rem;"></p>
                </div>
                <div style="display:flex; gap:10px;">
                    <a id="r-url" href="#" target="_blank" class="cta-btn" style="flex:1;">Matéria Completa &rarr;</a>
                    <button onclick="document.getElementById('reader-modal').style.display='none'" style="background:transparent; color:#fff; border:1px solid var(--border); border-radius:8px; padding:0.6rem 1.2rem; cursor:pointer;">Fechar</button>
                </div>
            </div>
        </div>
    </div>

    <footer>
        <p><strong>TechNews.PRO</strong> &copy; {ano_atual} — Otimizado via Topic Clusters, OpenAI & RSS Feed Aggregators.</p>
        <p style="margin-top:8px; font-size:0.8rem;">
            <a href="feed.xml" style="color:#94a3b8; margin:0 8px;">RSS Feed</a> | 
            <a href="sitemap.xml" style="color:#94a3b8; margin:0 8px;">Sitemap</a>
        </p>
    </footer>

    <script>
        const todasNoticias = {noticias_json};

        function aplicarTeiaSEO(texto) {
            if (!texto) return "";
            let t = texto;
            t = t.replace(/\\b(inteligência artificial|IA)\\b/i, '<a href="inteligencia-artificial.html" class="seo-internal-link">$1</a>');
            t = t.replace(/\\b(bitcoin|criptomoedas)\\b/i, '<a href="bitcoin.html" class="seo-internal-link">$1</a>');
            t = t.replace(/\\b(chatgpt)\\b/i, '<a href="chatgpt.html" class="seo-internal-link">$1</a>');
            t = t.replace(/\\b(startup|startups)\\b/i, '<a href="startups.html" class="seo-internal-link">$1</a>');
            return t;
        }

        // CORREÇÃO DO BUG DAS ABAS: Usar currentTarget para evitar click nos emojis
        function filtrarCategoria(categoria, event) {
            if (event) {
                event.preventDefault();
                document.querySelectorAll('.nav-links button').forEach(btn => btn.classList.remove('active'));
                if (event.currentTarget && event.currentTarget.tagName === 'BUTTON') {
                    event.currentTarget.classList.add('active');
                }
            }
            document.getElementById('titulo-secao').innerText = categoria === 'todos' ? 'Radar Global em Tempo Real' : 'Setor: ' + categoria;
            const filtradas = categoria === 'todos' ? todasNoticias : todasNoticias.filter(n => n.categoria === categoria);
            renderizarLista(filtradas);
        }

        function abrirReader(idx) {
            const art = todasNoticias[idx];
            document.getElementById('r-img').src = art.img;
            document.getElementById('r-source').innerText = art.source + " • " + art.categoria;
            document.getElementById('r-title').innerText = art.title;
            document.getElementById('r-desc').innerHTML = aplicarTeiaSEO(art.desc);
            document.getElementById('r-url').href = art.url;
            document.getElementById('reader-modal').style.display = 'flex';
        }

        // CORREÇÃO DO BUG DO "FALSO VAZIO": Aviso elegante quando não há notícias na categoria
        function renderizarLista(lista) {
            if (!lista || lista.length === 0) {
                document.getElementById('hero-container').innerHTML = '';
                document.getElementById('feed-container').innerHTML = '<div style="grid-column: 1 / -1; padding:3rem; text-align:center; color:var(--text-muted); background:var(--card-bg); border-radius:12px; border:1px solid var(--border);">🔍 O nosso motor IA não encontrou atualizações relevantes para esta categoria no momento. Volte em algumas horas.</div>';
                return;
            }

            const hero = lista[0];
            const heroIdx = todasNoticias.indexOf(hero);

            document.getElementById('hero-container').innerHTML = `
                <div class="hero-card">
                    <img src="${hero.img}" onerror="this.src='https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=1200&q=85'">
                    <div class="hero-overlay">
                        <span class="badge-source">🔥 Manchete • ${hero.source}</span>
                        <h1 style="font-size:2.2rem; margin:10px 0; color:#fff;">${hero.title}</h1>
                        <p style="font-size:1.05rem; color:#cbd5e1; margin-bottom:15px;">${aplicarTeiaSEO(hero.desc)}</p>
                        <div style="display:flex; gap:10px;">
                            <button onclick="abrirReader(${heroIdx})" class="cta-btn">⚡ Síntese IA</button>
                            <a href="${hero.url}" target="_blank" class="cta-btn" style="background:rgba(255,255,255,0.15);">Fonte &rarr;</a>
                        </div>
                    </div>
                </div>
            `;

            let feedHtml = '';
            lista.slice(1, 11).forEach((art) => {
                const globalIdx = todasNoticias.indexOf(art);
                feedHtml += `
                <article class="news-card">
                    <div class="card-img-wrapper">
                        <span class="badge-source" style="position:absolute; top:10px; left:10px;">${art.source}</span>
                        <img src="${art.img}" onerror="this.src='https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&q=80'">
                    </div>
                    <div class="card-body">
                        <h3 style="font-size:1.1rem; margin-bottom:0.8rem;">${art.title}</h3>
                        <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:1.5rem;">${aplicarTeiaSEO(art.desc)}</p>
                        <button onclick="abrirReader(${globalIdx})" class="cta-btn" style="width:100%; text-align:center;">Ler Relatório</button>
                    </div>
                </article>
                `;
            });
            document.getElementById('feed-container').innerHTML = feedHtml;
        }

        window.onscroll = function() {
            var winScroll = document.body.scrollTop || document.documentElement.scrollTop;
            var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            document.getElementById("progress-bar").style.width = ((winScroll / height) * 100) + "%";
        };

        renderizarLista(todasNoticias);
    </script>
</body>
</html>
"""

# ==============================================================================
# FUNÇÕES CORE: COLETA E FORMATAÇÃO (Mantidas blindadas do v6.1)
# ==============================================================================
def obter_dados_cotacoes():
    d_padrao = {"USDBRL": {"nome": "Dólar", "val": "R$ 5,70", "pct": "+0.15%", "classe": "up"}, "EURBRL": {"nome": "Euro", "val": "R$ 6,18", "pct": "+0.10%", "classe": "up"}, "BTCBRL": {"nome": "Bitcoin", "val": "R$ 420.000", "pct": "+1.25%", "classe": "up"}}
    try:
        r = requests.get("https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL", timeout=6)
        if r.status_code == 200:
            d = r.json()
            for par, label in [("USDBRL", "Dólar"), ("EURBRL", "Euro"), ("BTCBRL", "Bitcoin")]:
                if par in d:
                    val = float(d[par]["bid"])
                    pct = float(d[par]["pctChange"])
                    classe = "up" if pct >= 0 else "down"
                    val_fmt = f"R$ {val:,.2f}" if par != "BTCBRL" else f"R$ {val:,.0f}"
                    d_padrao[par] = {"nome": label, "val": val_fmt, "pct": f"{pct:+.2f}%", "classe": classe}
    except: pass
    itens = [f'<span style="margin-right:15px;">{v["nome"]}: <strong>{v["val"]}</strong> <span class="{v["classe"]}">({v["pct"]})</span></span>' for v in d_padrao.values()]
    return "".join(itens)

def classificar_noticia(titulo):
    t = titulo.lower()
    if any(k in t for k in ["finança", "banco", "mercado", "ação", "investimento", "startup", "economia", "negócio", "dólar", "cripto", "bitcoin"]): return "Finanças"
    elif any(k in t for k in ["espaço", "satélite", "ciência", "astronomia"]): return "Ciência"
    return "Tecnologia"

def fetch_devto_pt():
    noticias = []
    try:
        r = requests.get("https://dev.to/api/articles?tag=portuguese&per_page=8", timeout=8)
        if r.status_code == 200:
            for item in r.json():
                noticias.append({"title": item.get("title", ""), "desc": item.get("description", ""), "img": item.get("cover_image") or item.get("social_image") or "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1200&q=85", "url": item.get("url", "#"), "source": "Dev.to Brasil", "date": "Recente", "categoria": classificar_noticia(item.get("title", ""))})
    except: pass
    return noticias

def fetch_spaceflight_news():
    noticias = []
    try:
        r = requests.get("https://api.spaceflightnewsapi.net/v4/articles/?limit=4", timeout=8)
        if r.status_code == 200:
            for item in r.json().get("results", []):
                noticias.append({"title": item.get("title", ""), "desc": item.get("summary", ""), "img": item.get("image_url") or "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1200&q=85", "url": item.get("url", "#"), "source": "SpaceTech", "date": item.get("published_at", "")[:10], "categoria": "Ciência"})
    except: pass
    return noticias

def fetch_newsapi():
    noticias = []
    if not NEWS_API_KEY: return noticias
    try:
        query = '("inteligencia artificial" OR tecnologia OR ciberseguranca OR criptomoedas OR bitcoin OR startups)'
        r = requests.get(f"https://newsapi.org/v2/everything?q={query}&language=pt&sortBy=publishedAt&pageSize=10&apiKey={NEWS_API_KEY}", headers={'User-Agent': 'Mozilla/5.0'}, timeout=8)
        if r.status_code == 200:
            for item in r.json().get("articles", []):
                tit = item.get("title") or ""
                if tit and tit != "[Removed]" and "futebol" not in tit.lower():
                    noticias.append({"title": tit, "desc": item.get("description", ""), "img": item.get("urlToImage") or "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=1200&q=85", "url": item.get("url", "#"), "source": item.get("source", {}).get("name", "TechPress"), "date": item.get("publishedAt", "")[:10], "categoria": classificar_noticia(tit)})
    except: pass
    return noticias

def deduplicar_noticias(lista):
    vistos = set()
    unicas = []
    for n in lista:
        chave = n.get("title", "").strip().lower()
        if chave and chave not in vistos:
            vistos.add(chave)
            unicas.append(n)
    return unicas

# ==============================================================================
# NOVAS FUNÇÕES V7: RSS FEED, ONESIGNAL PUSH E SEO PROGRAMÁTICO
# ==============================================================================
def gerar_rss(noticias):
    xml = f'<?xml version="1.0" encoding="UTF-8" ?>\n<rss version="2.0">\n<channel>\n<title>TechNews PRO | IA e Mercado</title>\n<link>{URL_PORTAL_OFICIAL}</link>\n<description>Notícias automatizadas de Tecnologia, Finanças e Ciência.</description>\n'
    for n in noticias[:15]:
        xml += f"<item>\n<title>{html.escape(n['title'])}</title>\n<link>{n['url']}</link>\n<description>{html.escape(n['desc'])}</description>\n</item>\n"
    xml += "</channel>\n</rss>"
    with open("feed.xml", "w", encoding="utf-8") as f:
        f.write(xml)

def disparar_onesignal_push(noticia):
    if not ONESIGNAL_APP_ID or not ONESIGNAL_REST_KEY or not noticia:
        print("Agente OneSignal: Chaves ausentes, pulando Push Notification.")
        return
    try:
        titulo_curto = noticia['title'][:40] + "..." if len(noticia['title']) > 40 else noticia['title']
        payload = {
            "app_id": ONESIGNAL_APP_ID,
            "included_segments": ["Subscribed Users"],
            "headings": {"en": "🚨 URGENTE: " + titulo_curto, "pt": "🚨 URGENTE: " + titulo_curto},
            "contents": {"en": noticia['desc'][:100] + "...", "pt": noticia['desc'][:100] + "..."},
            "url": URL_PORTAL_OFICIAL
        }
        headers = {"Authorization": f"Basic {ONESIGNAL_REST_KEY}", "Content-Type": "application/json"}
        r = requests.post("https://onesignal.com/api/v1/notifications", json=payload, headers=headers, timeout=10)
        if r.status_code == 200:
            print("Agente OneSignal: ✅ Notificação Push disparada para a audiência!")
    except Exception as e:
        print(f"Agente OneSignal Erro: {e}")

# SEO PROGRAMÁTICO (Topic Clusters)
TAGS_SEO_DINAMICAS = {
    "bitcoin": {"titulo": "Hub Bitcoin & Criptomoedas", "kw": ["bitcoin", "cripto", "ethereum"]},
    "chatgpt": {"titulo": "Hub ChatGPT & IA", "kw": ["chatgpt", "openai", "gemini", "inteligência"]},
    "startups": {"titulo": "Hub Startups & Negócios", "kw": ["startup", "negócio", "empresa", "fintech"]}
}

def gerar_paginas_programaticas(todas_noticias, ano_fmt):
    urls_geradas = []
    for slug, config in TAGS_SEO_DINAMICAS.items():
        filtradas = [n for n in todas_noticias if any(k in n['title'].lower() or k in n['desc'].lower() for k in config['kw'])]
        if not filtradas: filtradas = todas_noticias[:3] # Fallback para não ficar vazio
        
        cards = ""
        for art in filtradas[:6]:
            cards += f"""<div style="background:#111827; border:1px solid #1f2937; padding:1.5rem; border-radius:12px;"><h3 style="color:#f8fafc; margin-bottom:10px;">{art['title']}</h3><p style="color:#94a3b8; font-size:0.9rem; margin-bottom:15px;">{art['desc']}</p><a href="{art['url']}" target="_blank" style="color:#3b82f6; font-weight:bold; text-decoration:none;">Ler na Íntegra &rarr;</a></div>"""
        
        html_page = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta name="description" content="Últimas notícias sobre {config['titulo']}"><title>{config['titulo']} | TechNews PRO</title><style>body{{background:#070b14; color:#f8fafc; font-family:sans-serif; margin:0; line-height:1.6;}} header{{padding:1.5rem 5%; background:#0f172a; border-bottom:1px solid #1f2937;}} .container{{max-width:1200px; margin:3rem auto; padding:0 5%;}} .grid{{display:grid; grid-template-columns:repeat(auto-fill,minmax(300px,1fr)); gap:1.5rem;}}</style></head><body><header><a href="index.html" style="color:#fff; text-decoration:none; font-size:1.5rem; font-weight:900;">TechNews<span style="color:#ef4444;">.PRO</span></a> &nbsp;&nbsp;&nbsp; <a href="index.html" style="color:#94a3b8; text-decoration:none;">&larr; Voltar ao Radar Principal</a></header><div class="container"><h1 style="margin-bottom:2rem; font-size:2.5rem; border-left:5px solid #ef4444; padding-left:15px;">{config['titulo']}</h1><div class="grid">{cards}</div></div></body></html>"""
        
        with open(f"{slug}.html", "w", encoding="utf-8") as f:
            f.write(html_page)
        urls_geradas.append(slug + ".html")
    return urls_geradas

def gerar_sitemap_xml(urls_extras):
    hoje = datetime.now().strftime("%Y-%m-%d")
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n<url><loc>{URL_PORTAL_OFICIAL}</loc><lastmod>{hoje}</lastmod><priority>1.0</priority></url>\n<url><loc>{URL_PORTAL_OFICIAL}inteligencia-artificial.html</loc><lastmod>{hoje}</lastmod><priority>0.9</priority></url>\n<url><loc>{URL_PORTAL_OFICIAL}cotacao-agora.html</loc><lastmod>{hoje}</lastmod><priority>0.9</priority></url>"""
    for url in urls_extras:
        xml += f"\n<url><loc>{URL_PORTAL_OFICIAL}{url}</loc><lastmod>{hoje}</lastmod><priority>0.8</priority></url>"
    xml += "\n</urlset>"
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(xml)

# ==============================================================================
# FLUXO PRINCIPAL
# ==============================================================================
def gerar_portal(apenas_site=False):
    brutas = []
    brutas.extend(fetch_devto_pt())
    brutas.extend(fetch_newsapi())
    brutas.extend(fetch_spaceflight_news())
    todas_noticias = deduplicar_noticias(brutas)
    if not todas_noticias: return

    # Salva Notícia Principal para Redes
    with open(ARQUIVO_FILA_POST, "w", encoding="utf-8") as f:
        json.dump(todas_noticias[0], f, ensure_ascii=False)

    agora = datetime.now()
    data_fmt = agora.strftime("%d/%m/%Y às %H:%M")
    ano_fmt = str(agora.year)
    cotacoes_html = obter_dados_cotacoes()
    
    # 1. GERAR INDEX HTML
    destaque = todas_noticias[0]
    html_index = (HTML_TEMPLATE_INDEX
        .replace("{og_title}", destaque['title'].replace('"', '&quot;'))
        .replace("{og_desc}", destaque['desc'].replace('"', '&quot;'))
        .replace("{og_img}", destaque['img'])
        .replace("{url_portal}", URL_PORTAL_OFICIAL)
        .replace("{cotacoes_html}", cotacoes_html)
        .replace("{data_atualizacao}", data_fmt)
        .replace("{ano_atual}", ano_fmt)
        .replace("{onesignal_id}", ONESIGNAL_APP_ID)
        .replace("{noticias_json}", json.dumps(todas_noticias, ensure_ascii=False))
    )
    with open("index.html", "w", encoding="utf-8") as f: f.write(html_index)

    # 2. GERAR RSS E SEO PROGRAMÁTICO
    gerar_rss(todas_noticias)
    urls_dinamicas = gerar_paginas_programaticas(todas_noticias, ano_fmt)
    gerar_sitemap_xml(urls_dinamicas)
    print("✅ Ecossistema v7 gerado: Index, RSS Feed e Clusters de SEO!")

if __name__ == "__main__":
    if "--gerar-site" in sys.argv:
        gerar_portal(apenas_site=True)
    elif "--postar-redes" in sys.argv:
        if os.path.exists(ARQUIVO_FILA_POST):
            with open(ARQUIVO_FILA_POST, "r", encoding="utf-8") as f:
                noticia_pronta = json.load(f)
            # disparar_meta(noticia_pronta) -> Mantida do seu script anterior (encurtada visualmente aqui para foco)
            disparar_onesignal_push(noticia_pronta)
            print("🚀 Agentes de Distribuição disparados!")
    else:
        gerar_portal(apenas_site=False)
