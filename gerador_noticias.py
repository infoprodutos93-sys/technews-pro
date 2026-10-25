import os
import requests
import json
import random
from datetime import datetime

# ==============================================================================
# CONFIGURAÇÃO DE CHAVES E SEGURANÇA (GITHUB SECRETS)
# ==============================================================================
NEWS_API_KEY = "4e42db8a8a6645fbad1039ba84a6ea4f"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
# ==============================================================================

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechNews PRO | Terminal de Inteligência, IA & Mercado</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
    <style>
        :root[data-theme="dark"] {
            --bg-color: #070b14;
            --card-bg: rgba(17, 25, 40, 0.85);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --primary: #ef4444;
            --accent: #3b82f6;
            --neon: #00f2fe;
            --dark-bar: #03060c;
            --border: rgba(255, 255, 255, 0.08);
            --glass: rgba(15, 23, 42, 0.75);
        }
        :root[data-theme="light"] {
            --bg-color: #f1f5f9;
            --card-bg: #ffffff;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --primary: #ef4444;
            --accent: #2563eb;
            --neon: #2563eb;
            --dark-bar: #0f172a;
            --border: #e2e8f0;
            --glass: rgba(255, 255, 255, 0.9);
        }

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; transition: background-color 0.25s, color 0.2s; }
        body { background-color: var(--bg-color); color: var(--text-main); line-height: 1.6; overflow-x: hidden; }

        #progress-bar { position: fixed; top: 0; left: 0; height: 3px; background: linear-gradient(90deg, var(--primary), var(--neon)); width: 0%; z-index: 99999; }

        /* BARRA DE COTAÇÕES FINANCEIRAS AO VIVO */
        .market-ticker { background: var(--dark-bar); color: #e2e8f0; padding: 0.45rem 5%; font-size: 0.8rem; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; font-family: 'JetBrains Mono', monospace; }
        .market-items { display: flex; gap: 1.5rem; align-items: center; overflow-x: auto; white-space: nowrap; }
        .market-item { display: flex; align-items: center; gap: 6px; }
        .up { color: #10b981; font-weight: 700; }
        .down { color: #ef4444; font-weight: 700; }
        .live-dot { width: 8px; height: 8px; background: #10b981; border-radius: 50%; display: inline-block; animation: blink 1.2s infinite; }
        @keyframes blink { 0%, 100% { opacity: 1; box-shadow: 0 0 8px #10b981; } 50% { opacity: 0.3; } }

        /* HEADER GLASSMORPHISM */
        header { background: var(--glass); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); padding: 1rem 5%; position: sticky; top: 0; z-index: 1000; border-bottom: 1px solid var(--border); }
        .nav-container { max-width: 1440px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; gap: 1rem; flex-wrap: wrap; }
        .logo { font-size: 1.85rem; font-weight: 900; letter-spacing: -1px; color: var(--text-main); text-decoration: none; display: flex; align-items: center; gap: 6px; cursor: pointer; }
        .logo span { color: var(--primary); }
        .logo-badge { font-size: 0.65rem; background: rgba(239, 68, 68, 0.15); color: var(--primary); border: 1px solid var(--primary); padding: 2px 6px; border-radius: 4px; font-weight: 800; letter-spacing: 0.5px; }

        .nav-links { display: flex; gap: 0.5rem; list-style: none; background: rgba(255,255,255,0.03); padding: 5px; border-radius: 10px; border: 1px solid var(--border); }
        .nav-links button { background: none; border: none; color: var(--text-muted); font-weight: 700; font-size: 0.88rem; cursor: pointer; padding: 0.45rem 1rem; border-radius: 7px; transition: 0.2s; }
        .nav-links button:hover { color: var(--text-main); }
        .nav-links button.active { background: var(--primary); color: #fff; box-shadow: 0 4px 12px rgba(239, 68, 68, 0.35); }

        .header-actions { display: flex; align-items: center; gap: 0.8rem; }
        .search-box { position: relative; }
        .search-box input { background: rgba(255,255,255,0.05); border: 1px solid var(--border); color: var(--text-main); padding: 0.5rem 1rem 0.5rem 2.2rem; border-radius: 8px; font-size: 0.85rem; width: 190px; outline: none; transition: 0.3s; }
        .search-box input:focus { width: 240px; border-color: var(--primary); }
        .search-icon { position: absolute; left: 10px; top: 50%; transform: translateY(-50%); font-size: 0.8rem; color: var(--text-muted); }

        /* BOTÃO DE TEMA COM SOL / LUA */
        .theme-btn { background: rgba(255,255,255,0.06); border: 1px solid var(--border); color: var(--text-main); padding: 0.45rem 0.8rem; border-radius: 8px; cursor: pointer; font-weight: 700; font-size: 0.85rem; display: flex; align-items: center; gap: 6px; }
        .theme-btn:hover { border-color: var(--primary); }

        .cta-btn { background: linear-gradient(135deg, #ef4444, #b91c1c); color: #fff; border: none; padding: 0.55rem 1.2rem; border-radius: 8px; font-weight: 800; cursor: pointer; text-decoration: none; font-size: 0.85rem; box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3); display: inline-flex; align-items: center; gap: 6px; }
        .cta-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(239, 68, 68, 0.5); }

        /* RADAR DE TAGS QUENTES */
        .tags-bar { max-width: 1440px; margin: 1.2rem auto 0 auto; padding: 0 5%; display: flex; align-items: center; gap: 0.6rem; overflow-x: auto; white-space: nowrap; }
        .tag-pill { background: var(--card-bg); border: 1px solid var(--border); color: var(--text-muted); padding: 4px 12px; border-radius: 20px; font-size: 0.78rem; font-weight: 600; cursor: pointer; transition: 0.2s; }
        .tag-pill:hover { border-color: var(--primary); color: var(--text-main); transform: scale(1.05); }

        .ad-banner-top { max-width: 970px; min-height: 90px; margin: 1.5rem auto; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }

        .main-container { max-width: 1440px; margin: 0 auto 4rem auto; padding: 0 5%; display: grid; grid-template-columns: 7.2fr 2.8fr; gap: 2.5rem; }

        /* HERO CARD */
        .hero-card { position: relative; border-radius: 16px; overflow: hidden; box-shadow: 0 20px 40px rgba(0,0,0,0.35); margin-bottom: 2.5rem; display: block; border: 1px solid var(--border); background: #000; }
        .hero-card img { width: 100%; height: 470px; object-fit: cover; opacity: 0.75; transition: transform 0.6s ease, opacity 0.3s; }
        .hero-card:hover img { transform: scale(1.04); opacity: 0.65; }
        .hero-overlay { position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(to top, rgba(3,6,12,0.98) 15%, rgba(3,6,12,0.65) 65%, transparent 100%); padding: 2.5rem; color: #fff; }
        .badge-source { background: var(--primary); color: #fff; padding: 5px 12px; border-radius: 6px; font-size: 0.72rem; font-weight: 900; text-transform: uppercase; display: inline-block; margin-bottom: 0.8rem; letter-spacing: 0.5px; }
        .hero-overlay h1 { font-size: 2.2rem; line-height: 1.2; margin-bottom: 0.8rem; font-weight: 900; }
        .hero-overlay p { color: #cbd5e1; font-size: 1.02rem; margin-bottom: 1.2rem; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
        .hero-actions { display: flex; gap: 1rem; flex-wrap: wrap; }

        .section-title { font-size: 1.35rem; font-weight: 900; margin-bottom: 1.5rem; border-left: 4px solid var(--primary); padding-left: 12px; display: flex; justify-content: space-between; align-items: center; }
        .feed-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(310px, 1fr)); gap: 1.8rem; }
        
        /* CARDS DE NOTÍCIAS */
        .news-card { background: var(--card-bg); border-radius: 14px; overflow: hidden; border: 1px solid var(--border); display: flex; flex-direction: column; transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s; backdrop-filter: blur(10px); }
        .news-card:hover { transform: translateY(-6px); box-shadow: 0 15px 30px rgba(0,0,0,0.25); border-color: rgba(239, 68, 68, 0.4); }
        .card-img-wrapper { position: relative; width: 100%; height: 195px; overflow: hidden; background: #1e293b; }
        .card-img-wrapper img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.5s ease; }
        .news-card:hover .card-img-wrapper img { transform: scale(1.08); }
        .card-tag { position: absolute; top: 12px; left: 12px; background: rgba(3, 6, 12, 0.85); backdrop-filter: blur(6px); color: #fff; padding: 4px 10px; border-radius: 6px; font-size: 0.68rem; font-weight: 800; text-transform: uppercase; border: 1px solid rgba(255,255,255,0.15); }
        .audio-btn { position: absolute; bottom: 10px; right: 10px; background: rgba(239, 68, 68, 0.9); color: #fff; border: none; padding: 5px 10px; border-radius: 20px; font-size: 0.72rem; font-weight: 700; cursor: pointer; display: flex; align-items: center; gap: 4px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
        .audio-btn:hover { background: #dc2626; transform: scale(1.05); }

        .card-body { padding: 1.4rem; display: flex; flex-direction: column; flex-grow: 1; }
        .card-meta { font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.6rem; display: flex; justify-content: space-between; font-weight: 600; }
        .card-title { font-size: 1.12rem; font-weight: 800; color: var(--text-main); margin-bottom: 0.75rem; line-height: 1.35; }
        .card-desc { font-size: 0.88rem; color: var(--text-muted); margin-bottom: 1.3rem; flex-grow: 1; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
        
        .card-footer-btns { display: grid; grid-template-columns: 1fr 1fr; gap: 0.6rem; margin-top: auto; }
        .btn-outline { background: rgba(255,255,255,0.04); color: var(--text-main); border: 1px solid var(--border); padding: 0.65rem; border-radius: 8px; font-weight: 700; font-size: 0.8rem; cursor: pointer; text-align: center; text-decoration: none; transition: 0.2s; }
        .btn-outline:hover { border-color: var(--primary); color: var(--primary); }
        .read-btn { background: var(--primary); color: #fff; font-weight: 700; font-size: 0.8rem; padding: 0.65rem; border-radius: 8px; text-decoration: none; text-align: center; transition: 0.2s; }
        .read-btn:hover { background: #dc2626; }

        /* NATIVE AD CARD */
        .native-ad-card { background: linear-gradient(145deg, rgba(239,68,68,0.12), rgba(15,23,42,0.9)); border: 2px solid rgba(239, 68, 68, 0.5); border-radius: 14px; padding: 1.8rem; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; position: relative; }
        .native-ad-card .ad-badge { background: var(--primary); color: #fff; font-size: 0.68rem; font-weight: 900; padding: 3px 10px; border-radius: 20px; text-transform: uppercase; margin-bottom: 1rem; }
        .native-ad-card h3 { font-size: 1.22rem; color: var(--text-main); margin-bottom: 0.8rem; font-weight: 900; }
        .native-ad-card p { font-size: 0.88rem; color: var(--text-muted); margin-bottom: 1.4rem; }

        /* SIDEBAR */
        .sidebar { display: flex; flex-direction: column; gap: 2rem; }
        .widget { background: var(--card-bg); border-radius: 14px; padding: 1.5rem; border: 1px solid var(--border); }
        .widget-title { font-size: 1.05rem; font-weight: 900; margin-bottom: 1.2rem; padding-bottom: 0.6rem; border-bottom: 2px solid var(--primary); display: flex; align-items: center; justify-content: space-between; }
        
        .trending-list { list-style: none; display: flex; flex-direction: column; gap: 1rem; }
        .trending-item { display: flex; gap: 0.9rem; align-items: flex-start; text-decoration: none; color: inherit; cursor: pointer; }
        .trending-num { font-size: 1.4rem; font-weight: 900; color: var(--primary); opacity: 0.8; line-height: 1; font-family: 'JetBrains Mono', monospace; }
        .trending-item:hover .trending-text { color: var(--primary); }
        .trending-text { font-size: 0.88rem; font-weight: 700; line-height: 1.35; }

        .newsletter-box { background: linear-gradient(135deg, #111827, #03060c); color: #fff; border-radius: 14px; padding: 1.8rem; text-align: center; border: 1px solid rgba(239, 68, 68, 0.3); }
        .newsletter-box h3 { font-size: 1.2rem; margin-bottom: 0.5rem; }
        .newsletter-box p { font-size: 0.84rem; color: #94a3b8; margin-bottom: 1.2rem; }
        .newsletter-box input { width: 100%; padding: 0.8rem; border-radius: 8px; border: 1px solid rgba(255,255,255,0.15); background: rgba(255,255,255,0.05); color: #fff; margin-bottom: 0.8rem; font-size: 0.88rem; }
        .newsletter-box button { width: 100%; padding: 0.85rem; background: var(--primary); color: #fff; border: none; border-radius: 8px; font-weight: 800; cursor: pointer; }

        .sticky-ad-container { position: sticky; top: 90px; }
        .ad-sidebar-box { width: 100%; min-height: 280px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }

        /* MODAL DE LEITURA RÁPIDA */
        #reader-modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(3, 6, 12, 0.88); z-index: 9999; justify-content: center; align-items: center; backdrop-filter: blur(8px); padding: 1rem; }
        .reader-box { background: var(--bg-color); border: 1px solid var(--border); width: 100%; max-width: 680px; border-radius: 16px; overflow: hidden; box-shadow: 0 25px 50px rgba(0,0,0,0.6); animation: popIn 0.3s ease; max-height: 90vh; display: flex; flex-direction: column; }
        .reader-img { width: 100%; height: 240px; object-fit: cover; }
        .reader-body { padding: 2rem; overflow-y: auto; }
        .reader-ai-box { background: rgba(59, 130, 246, 0.1); border-left: 4px solid var(--accent); padding: 1rem; border-radius: 6px; margin: 1.2rem 0; font-size: 0.92rem; }
        .reader-promo { background: rgba(239, 68, 68, 0.1); border: 1px dashed var(--primary); padding: 1rem; border-radius: 8px; text-align: center; margin-top: 1.5rem; }

        /* MODAL ANTI-ADBLOCK PROFISSIONAL (SEM GIFS QUEBRADOS) */
        #adblock-modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(3, 6, 12, 0.92); z-index: 10000; justify-content: center; align-items: center; backdrop-filter: blur(6px); }
        .adblock-content { background: var(--card-bg); color: var(--text-main); border: 1px solid rgba(239,68,68,0.4); width: 90%; max-width: 420px; border-radius: 20px; padding: 2.5rem 1.8rem; text-align: center; box-shadow: 0 25px 50px rgba(0,0,0,0.5); }
        @keyframes popIn { 0% { transform: scale(0.9); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }
        
        /* ÍCONE SVG DE ALERTA MODERNO E ROBUSTO */
        .adblock-icon-wrapper { width: 80px; height: 80px; background: rgba(239, 68, 68, 0.15); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1.2rem auto; color: var(--primary); }
        
        .adblock-btn { background: var(--primary); color: #fff; padding: 0.85rem; border-radius: 8px; font-weight: 800; width: 100%; border: none; cursor: pointer; margin-top: 1.2rem; transition: 0.2s; }
        .adblock-btn:hover { background: #dc2626; }
        .adblock-close { margin-top: 1rem; font-size: 0.8rem; color: var(--text-muted); text-decoration: underline; cursor: pointer; background: none; border: none; width: 100%; }

        footer { background: var(--dark-bar); color: #64748b; text-align: center; padding: 3rem 5%; font-size: 0.85rem; border-top: 1px solid var(--border); }

        @media (max-width: 992px) {
            .main-container { grid-template-columns: 1fr; }
            .nav-links { width: 100%; overflow-x: auto; justify-content: flex-start; }
            .hero-card img { height: 320px; }
            .hero-overlay h1 { font-size: 1.5rem; }
        }
    </style>
</head>
<body>
    <div id="progress-bar"></div>

    <!-- HONEYPOT DO ADBLOCK -->
    <div id="ad-honeypot" class="ad-banner adsbox doubleclick sponsor" style="position:absolute; top:-999px; left:-999px; width:10px; height:10px;"></div>

    <!-- MODAL ANTI-ADBLOCK MODAL (SVG ROBUSTO) -->
    <div id="adblock-modal">
        <div class="adblock-content">
            <div class="adblock-icon-wrapper">
                <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="4.93" y1="4.93" x2="19.07" y2="19.07"></line></svg>
            </div>
            <h3 style="font-size:1.35rem; font-weight:900; margin-bottom:0.6rem;">Bloqueador de Anúncios Detectado</h3>
            <p style="font-size:0.9rem; color:var(--text-muted); line-height:1.5;">O <strong>TechNews.PRO</strong> é mantido por patrocínios e anúncios para continuar 100% gratuito. Por favor, apoie nosso trabalho desativando o AdBlock.</p>
            <button class="adblock-btn" onclick="location.reload()">Já desativei! (Atualizar página)</button>
            <button class="adblock-close" onclick="fecharAdBlock()">Continuar mesmo assim (Fechar)</button>
        </div>
    </div>

    <!-- MODAL DE LEITURA RÁPIDA -->
    <div id="reader-modal" onclick="fecharReader(event)">
        <div class="reader-box" onclick="event.stopPropagation()">
            <img id="r-img" src="" class="reader-img" alt="Capa">
            <div class="reader-body">
                <span id="r-source" class="badge-source">Fonte</span>
                <h2 id="r-title" style="margin-bottom: 1rem; line-height: 1.3;">Título</h2>
                <div class="reader-ai-box">
                    <strong>🤖 Síntese Executiva IA:</strong>
                    <p id="r-desc" style="margin-top: 6px;"></p>
                </div>
                <div style="display:flex; gap:10px; flex-wrap:wrap; margin-top:1.2rem;">
                    <a id="r-url" href="#" target="_blank" rel="noopener noreferrer" class="cta-btn" style="flex:1; justify-content:center;">Ler Matéria Completa na Fonte &rarr;</a>
                    <button onclick="fecharReader()" class="btn-outline" style="padding:0.6rem 1.2rem;">Fechar</button>
                </div>
                <div class="reader-promo">
                    <p style="font-size:0.82rem; margin-bottom:8px;">🔥 <strong>Recomendado para você:</strong> Domine Inteligência Artificial e multiplique sua produtividade.</p>
                    <a href="https://pay.kiwify.com.br/TO0iLa6" target="_blank" style="color:var(--primary); font-weight:800; font-size:0.85rem;">Acessar Método Oficial com Desconto &rarr;</a>
                </div>
            </div>
        </div>
    </div>

    <!-- BARRA DE MERCADO E COTAÇÕES AO VIVO -->
    <div class="market-ticker">
        <div class="market-items">
            <span><span class="live-dot"></span> <strong>TERMINAL AO VIVO</strong></span>
            {cotacoes_html}
        </div>
        <div>
            <span>⚡ Sincronizado: {data_atualizacao}</span>
        </div>
    </div>

    <header>
        <div class="nav-container">
            <a class="logo" onclick="filtrarCategoria('todos', event)">
                TechNews<span>.PRO</span>
                <span class="logo-badge">IA v3.1</span>
            </a>
            <ul class="nav-links">
                <li><button onclick="filtrarCategoria('todos', event)" class="active">🔥 Tudo</button></li>
                <li><button onclick="filtrarCategoria('Tecnologia', event)">💻 Tech & IA</button></li>
                <li><button onclick="filtrarCategoria('Finanças', event)">📈 Mercado & Cripto</button></li>
                <li><button onclick="filtrarCategoria('Ciência', event)">🚀 Espaço & Ciência</button></li>
            </ul>
            <div class="header-actions">
                <div class="search-box">
                    <span class="search-icon">🔍</span>
                    <input type="text" id="search-input" placeholder="Buscar notícia..." onkeyup="buscarNoticia()">
                </div>
                <!-- BOTÃO DE TEMA SOL / LUA -->
                <button class="theme-btn" id="theme-toggle-btn" onclick="alternarTema()" title="Alternar Modo Escuro / Claro">🌙 Escuro</button>
                <a href="https://asiafilm.org/4/78ed9deb10feac05c15347b414e171ab" target="_blank" rel="noopener noreferrer" class="cta-btn">💎 Área VIP</a>
            </div>
        </div>
    </header>

    <!-- RADAR DE TAGS INTERATIVAS -->
    <div class="tags-bar">
        <span style="font-size:0.75rem; font-weight:800; color:var(--primary); text-transform:uppercase;">Em Alta:</span>
        <span class="tag-pill" onclick="filtrarPorPalavra('Inteligência Artificial')">#InteligênciaArtificial</span>
        <span class="tag-pill" onclick="filtrarPorPalavra('Brasil')">#MercadoBrasil</span>
        <span class="tag-pill" onclick="filtrarPorPalavra('Python')">#Dev&Código</span>
        <span class="tag-pill" onclick="filtrarPorPalavra('Satélite')">#Aeroespacial</span>
        <span class="tag-pill" onclick="filtrarCategoria('todos', event)">🔄 Limpar Filtros</span>
    </div>

    <!-- BANNER TOPO ADSTERRA (728x90) -->
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
            <div id="hero-container"></div>

            <h2 class="section-title">
                <span id="titulo-secao">Radar Global em Tempo Real</span>
                <span style="font-size:0.75rem; color:var(--text-muted); font-weight:600;">🔊 Clique no ícone de áudio para ouvir</span>
            </h2>
            
            <div class="feed-grid" id="feed-container"></div>
        </div>

        <aside class="sidebar">
            <div class="widget">
                <div class="widget-title">
                    <span>🔥 Mais Lidas no Terminal</span>
                </div>
                <ul class="trending-list">
                    {trending_section}
                </ul>
            </div>

            <!-- SMARTLINK DE TEXTO DESTACADO NA LATERAL -->
            <div class="widget" style="background: linear-gradient(135deg, rgba(239,68,68,0.15), rgba(15,23,42,0.95)); border-color: rgba(239,68,68,0.4); text-align: center;">
                <h3 style="margin-bottom: 0.5rem; font-size: 1.05rem;">⚡ Ferramenta Secreta do Dia</h3>
                <p style="font-size: 0.82rem; color: var(--text-muted); margin-bottom: 1rem;">Desbloqueie recursos exclusivos e oportunidades selecionadas pela nossa rede.</p>
                <a href="https://asiafilm.org/4/78ed9deb10feac05c15347b414e171ab" target="_blank" rel="noopener noreferrer" class="cta-btn" style="width: 100%; justify-content: center;">Acessar Agora &rarr;</a>
            </div>

            <!-- NEWSLETTER REAL CONECTADA AO SYSTEME.IO -->
            <div class="newsletter-box" id="newsletter">
                <h3>💰 Briefing Matinal VIP</h3>
                <p>Receba os insights de IA e Negócios antes do mercado abrir.</p>
                <form action="https://devanildobeeny146.systeme.io/3ed9605c" method="GET" target="_blank">
                    <input type="email" name="email" placeholder="Digite seu e-mail principal..." required>
                    <button type="submit">Liberar Acesso Gratuito &rarr;</button>
                </form>
            </div>

            <!-- BANNER LATERAL ADSTERRA (300x250) -->
            <div class="sticky-ad-container">
                <div class="ad-sidebar-box">
                    <span style="font-size: 0.7rem; color: var(--text-muted); display: block; margin-bottom: 5px;">Patrocinado</span>
                    <script type="text/javascript">
                        atOptions = {
                            'key' : '8169727725318cd706b493da46602d6f',
                            'format' : 'iframe',
                            'height' : 250,
                            'width' : 300,
                            'params' : {}
                        };
                    </script>
                    <script type="text/javascript" src="https://bicea.org/22/8169727725318cd706b493da46602d6f"></script>
                </div>
            </div>
        </aside>
    </main>

    <footer>
        <p><strong>TechNews.PRO</strong> &copy; {ano_atual} — Terminal Automatizado via Python, Multi-API & OpenAI.</p>
        <p style="margin-top: 8px; font-size: 0.78rem;">Dados de Mercado: AwesomeAPI • Notícias: NewsAPI, IBGE, Spaceflight, Dev.to</p>
    </footer>

    <script>
        const todasNoticias = {noticias_json};

        // Barra de progresso
        window.onscroll = function() {
            var winScroll = document.body.scrollTop || document.documentElement.scrollTop;
            var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            document.getElementById("progress-bar").style.width = ((winScroll / height) * 100) + "%";
        };

        // Alternar Tema (Sol / Lua com texto)
        function alternarTema() {
            const html = document.documentElement;
            const btn = document.getElementById('theme-toggle-btn');
            const atual = html.getAttribute('data-theme');
            if (atual === 'dark') {
                html.setAttribute('data-theme', 'light');
                btn.innerHTML = '☀️ Claro';
            } else {
                html.setAttribute('data-theme', 'dark');
                btn.innerHTML = '🌙 Escuro';
            }
        }

        // Sintetizador de Voz Nativo (Leitor de Áudio)
        function falarNoticia(idx, event) {
            if (event) event.stopPropagation();
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel();
                const art = todasNoticias[idx];
                const msg = new SpeechSynthesisUtterance(art.title + ". " + art.desc);
                msg.lang = 'pt-BR';
                msg.rate = 1.08;
                window.speechSynthesis.speak(msg);
            } else {
                alert("Seu navegador não suporta leitura por voz.");
            }
        }

        // Modal de Leitura Rápida
        function abrirReader(idx) {
            const art = todasNoticias[idx];
            document.getElementById('r-img').src = art.img;
            document.getElementById('r-source').innerText = art.source + " • " + art.categoria;
            document.getElementById('r-title').innerText = art.title;
            document.getElementById('r-desc').innerText = art.desc;
            document.getElementById('r-url').href = art.url;
            document.getElementById('reader-modal').style.display = 'flex';
        }
        function fecharReader() {
            document.getElementById('reader-modal').style.display = 'none';
            if ('speechSynthesis' in window) window.speechSynthesis.cancel();
        }

        // Renderizador Principal
        function renderizarLista(lista) {
            if (!lista || lista.length === 0) lista = todasNoticias;
            const hero = lista[0];
            const heroIdx = todasNoticias.indexOf(hero);

            document.getElementById('hero-container').innerHTML = `
                <div class="hero-card">
                    <img src="${hero.img}" alt="Destaque" onerror="this.src='https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&q=80'">
                    <div class="hero-overlay">
                        <span class="badge-source">🔥 Destaque • ${hero.source}</span>
                        <h1>${hero.title}</h1>
                        <p>${hero.desc}</p>
                        <div class="hero-actions">
                            <button onclick="abrirReader(${heroIdx})" class="cta-btn">⚡ Resumo Expandido</button>
                            <button onclick="falarNoticia(${heroIdx}, event)" class="btn-outline" style="background:rgba(0,0,0,0.6); color:#fff;">🔊 Ouvir Notícia</button>
                            <a href="${hero.url}" target="_blank" rel="noopener noreferrer" class="btn-outline" style="background:rgba(255,255,255,0.1); color:#fff;">Fonte Oficial &rarr;</a>
                        </div>
                    </div>
                </div>
            `;

            let feedHtml = '';
            lista.slice(1, 10).forEach((art, idx) => {
                const globalIdx = todasNoticias.indexOf(art);
                feedHtml += `
                <article class="news-card">
                    <div class="card-img-wrapper">
                        <span class="card-tag">${art.source}</span>
                        <img src="${art.img}" alt="Capa" onerror="this.src='https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=800&q=80'">
                        <button class="audio-btn" onclick="falarNoticia(${globalIdx}, event)">🔊 Ouvir</button>
                    </div>
                    <div class="card-body">
                        <div class="card-meta">
                            <span>📅 ${art.date}</span>
                            <span style="color:var(--primary)">● ${art.categoria}</span>
                        </div>
                        <h3 class="card-title">${art.title}</h3>
                        <p class="card-desc">${art.desc}</p>
                        <div class="card-footer-btns">
                            <button onclick="abrirReader(${globalIdx})" class="btn-outline">⚡ Resumo IA</button>
                            <a href="${art.url}" target="_blank" rel="noopener noreferrer" class="read-btn">Ler Fonte &rarr;</a>
                        </div>
                    </div>
                </article>
                `;

                if (idx === 1) {
                    feedHtml += `
                    <div class="native-ad-card">
                        <span class="ad-badge">Destaque Patrocinado</span>
                        <h3>🚀 Domine Inteligência Artificial e Automação</h3>
                        <p>Descubra o método completo para criar sistemas automáticos e escalar seus resultados em tecnologia.</p>
                        <a href="https://pay.kiwify.com.br/TO0iLa6" target="_blank" rel="noopener noreferrer" class="cta-btn" style="width: 100%; justify-content:center;">Acessar Oferta Oficial &rarr;</a>
                    </div>
                    `;
                }
            });
            document.getElementById('feed-container').innerHTML = feedHtml;
        }

        function filtrarCategoria(categoria, event) {
            if (event) {
                event.preventDefault();
                document.querySelectorAll('.nav-links button').forEach(btn => btn.classList.remove('active'));
                if (event.target.tagName === 'BUTTON') event.target.classList.add('active');
            }
            document.getElementById('titulo-secao').innerText = categoria === 'todos' ? 'Radar Global em Tempo Real' : 'Setor: ' + categoria;
            const filtradas = categoria === 'todos' ? todasNoticias : todasNoticias.filter(n => n.categoria === categoria);
            renderizarLista(filtradas);
        }

        function buscarNoticia() {
            const termo = document.getElementById('search-input').value.toLowerCase();
            const filtradas = todasNoticias.filter(n => n.title.toLowerCase().includes(termo) || n.desc.toLowerCase().includes(termo));
            document.getElementById('titulo-secao').innerText = termo ? 'Resultados para: "' + termo + '"' : 'Radar Global em Tempo Real';
            renderizarLista(filtradas);
        }

        function filtrarPorPalavra(palavra) {
            document.getElementById('search-input').value = palavra;
            buscarNoticia();
        }

        // DETETOR DE ADBLOCK
        setTimeout(function() {
            var honeypot = document.getElementById('ad-honeypot');
            if (!honeypot || honeypot.offsetHeight === 0 || window.getComputedStyle(honeypot).display === 'none') {
                document.getElementById('adblock-modal').style.display = 'flex';
            }
        }, 1800);

        function fecharAdBlock() {
            document.getElementById('adblock-modal').style.display = 'none';
        }

        // Inicializar Portal
        renderizarLista(todasNoticias);
    </script>

    <!-- SOCIAL BAR FLUTUANTE ADSTERRA -->
    <script data-cfasync="false" src="https://bicea.org/14/7843682dc41b2077e8d78d48efd6360a"></script>
</body>
</html>
"""

def fetch_cotacoes():
    try:
        url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL"
        r = requests.get(url, timeout=6)
        if r.status_code == 200:
            d = r.json()
            itens = []
            for par, nome in [("USDBRL", "💵 Dólar"), ("EURBRL", "💶 Euro"), ("BTCBRL", "₿ Bitcoin")]:
                if par in d:
                    val = float(d[par]["bid"])
                    pct = float(d[par]["pctChange"])
                    classe = "up" if pct >= 0 else "down"
                    sinal = "+" if pct >= 0 else ""
                    val_fmt = f"R$ {val:,.2f}" if par != "BTCBRL" else f"R$ {val:,.0f}"
                    itens.append(f'<span class="market-item">{nome}: <strong>{val_fmt}</strong> <span class="{classe}">({sinal}{pct:.2f}%)</span></span>')
            return " • ".join(itens)
    except:
        pass
    return '<span class="market-item">💵 Dólar Comercial • 💶 Euro • ₿ Bitcoin em monitoramento</span>'

def reescrever_com_ia(texto):
    if not OPENAI_API_KEY or not texto or len(texto) < 15:
        return texto 
    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {OPENAI_API_KEY}"}
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "Você é um editor-chefe de um portal de tecnologia e finanças. Reescreva este resumo de forma analítica, impactante e direta em até 2 frases."},
                {"role": "user", "content": texto}
            ],
            "max_tokens": 80,
            "temperature": 0.7
        }
        resposta = requests.post(url, headers=headers, json=payload, timeout=8)
        if resposta.status_code == 200:
            return resposta.json()["choices"][0]["message"]["content"].strip().replace('"', '')
    except:
        pass 
    return texto 

def classificar_noticia(titulo):
    t = titulo.lower()
    if any(k in t for k in ["finança", "banco", "mercado", "ação", "investimento", "startup", "economia", "negócio", "dólar", "cripto", "bitcoin", "ibge"]):
        return "Finanças"
    elif any(k in t for k in ["espaço", "nasa", "satélite", "ciência", "física", "astronomia", "foguete"]):
        return "Ciência"
    return "Tecnologia"

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
                titulo = item.get("titulo")
                noticias.append({
                    "title": titulo,
                    "desc": item.get("introducao", "Confira os dados completos divulgados pelo portal oficial."),
                    "img": img_url,
                    "url": item.get("link", "#"),
                    "source": "IBGE Oficial",
                    "date": item.get("data_publicacao", "Hoje")[:10],
                    "categoria": classificar_noticia(titulo)
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
                titulo = item.get("title")
                noticias.append({
                    "title": titulo,
                    "desc": item.get("description") or "Artigo técnico publicado na comunidade global de desenvolvedores.",
                    "img": item.get("cover_image") or item.get("social_image") or "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=800&q=80",
                    "url": item.get("url", "#"),
                    "source": "Dev.to Brasil",
                    "date": item.get("readable_publish_date", "Recente"),
                    "categoria": "Tecnologia"
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
                titulo = item.get("title")
                noticias.append({
                    "title": titulo,
                    "desc": item.get("summary", ""),
                    "img": item.get("image_url") or "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=800&q=80",
                    "url": item.get("url", "#"),
                    "source": "SpaceTech",
                    "date": item.get("published_at", "")[:10],
                    "categoria": "Ciência"
                })
    except:
        pass
    return noticias

def fetch_newsapi():
    noticias = []
    if not NEWS_API_KEY:
        return noticias
    try:
        url = f"https://newsapi.org/v2/everything?q=tecnologia OR inteligencia artificial OR mercado&language=pt&sortBy=publishedAt&pageSize=8&apiKey={NEWS_API_KEY}"
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=8)
        if r.status_code == 200:
            for item in r.json().get("articles", []):
                if item.get("title") and item.get("title") != "[Removed]":
                    titulo = item.get("title")
                    noticias.append({
                        "title": titulo,
                        "desc": item.get("description") or "Clique para ler a matéria completa na fonte oficial.",
                        "img": item.get("urlToImage") or "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=800&q=80",
                        "url": item.get("url", "#"),
                        "source": item.get("source", {}).get("name", "TechPress"),
                        "date": item.get("publishedAt", "")[:10],
                        "categoria": classificar_noticia(titulo)
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
        "date": "Hoje",
        "categoria": "Tecnologia"
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
        
    print("Iniciando reescrita de notícias com IA (ChatGPT)...")
    limite = min(len(todas_noticias), 10)
    for i in range(limite):
        todas_noticias[i]['desc'] = reescrever_com_ia(todas_noticias[i]['desc'])

    trending_html = ""
    for idx, art in enumerate(todas_noticias[1:6], start=1):
        trending_html += f"""
        <li>
            <a onclick="abrirReader({idx})" class="trending-item">
                <span class="trending-num">0{idx}</span>
                <span class="trending-text">{art['title']}</span>
            </a>
        </li>
        """

    agora = datetime.now()
    noticias_json_str = json.dumps(todas_noticias, ensure_ascii=False)
    cotacoes_html = fetch_cotacoes()

    html_final = (
        HTML_TEMPLATE
        .replace("{cotacoes_html}", cotacoes_html)
        .replace("{trending_section}", trending_html)
        .replace("{noticias_json}", noticias_json_str)
        .replace("{data_atualizacao}", agora.strftime("%d/%m/%Y às %H:%M"))
        .replace("{ano_atual}", str(agora.year))
    )

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_final)
    print("Terminal TechNews PRO v3.1 gerado com sucesso!")

if __name__ == "__main__":
    gerar_portal()
