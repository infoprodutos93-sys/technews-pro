import os
import sys
import re
import html
import requests
import json
import random
from datetime import datetime

# ==============================================================================
# CONFIGURAÇÃO DE CHAVES E SEGURANÇA (GITHUB SECRETS)
# ==============================================================================
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "4e42db8a8a6645fbad1039ba84a6ea4f")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# CHAVES DA META (FACEBOOK)
META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN", "")
META_PAGE_ID = os.getenv("META_PAGE_ID", "")

# CHAVES DO TELEGRAM (DARK SOCIAL)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# CHAVES DO ONESIGNAL (NOTIFICAÇÕES WEB PUSH)
ONESIGNAL_APP_ID = os.getenv("ONESIGNAL_APP_ID", "")
ONESIGNAL_REST_KEY = os.getenv("ONESIGNAL_REST_KEY", "")

# ARQUIVOS DE CONTROLE E VERIFICAÇÃO GOOGLE
ARQUIVO_MEMORIA_META = ".ultimo_post_meta.txt"
ARQUIVO_FILA_POST = ".fila_post_meta.json"
ARQUIVO_GOOGLE_VERIF = "google28d5384ab7e71bf6.html"

# ==============================================================================
# LINKS OFICIAIS DE MONETIZAÇÃO E FUNIL (100% PRESERVADOS)
# ==============================================================================
URL_PORTAL_OFICIAL = "https://infoprodutos93-sys.github.io/technews-pro/"
SMARTLINK_ADSTERRA = "https://asiafilm.org/4/78ed9deb10feac05c15347b414e171ab"
SYSTEME_OPTIN_URL = "https://devanildobeeny146.systeme.io/3ed9605c"

# 3 OFERTAS KIWIFY ESTRATÉGICAS
LINK_KIWIFY_1 = "https://kiwify.app/bFEoJ38?afid=u7GyGPOM"
LINK_KIWIFY_2 = "https://pay.kiwify.com.br/YUDgPja?afid=yt5zIWrU"
LINK_KIWIFY_3 = "https://kiwify.app/ek8xMMl?afid=1rxg1P58"

# ==============================================================================
# TEMPLATE PRINCIPAL: INDEX.HTML (MONETIZAÇÃO, ÁUDIO, MODAIS E ABAS CORRIGIDAS)
# ==============================================================================
HTML_TEMPLATE_INDEX = """<!DOCTYPE html>
<html lang="pt-BR" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Terminal avançado de notícias sobre Inteligência Artificial, Tecnologia, Ciência e Mercado Financeiro em tempo real.">
    
    <!-- REGRA DE OURO GOOGLE DISCOVER (IMAGENS GIGANTES NO MOBILE) -->
    <meta name="robots" content="max-image-preview:large, index, follow">
    <link rel="canonical" href="{url_portal}">
    <link rel="alternate" type="application/rss+xml" title="TechNews PRO RSS Feed" href="{url_portal}feed.xml">

    <!-- META TAGS OPEN GRAPH PARA CARD CLICÁVEL NO FACEBOOK E WHATSAPP -->
    <meta property="og:title" content="{og_title}">
    <meta property="og:description" content="{og_desc}">
    <meta property="og:image" content="{og_img}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:url" content="{url_portal}">
    <meta property="og:type" content="website">
    <meta name="twitter:card" content="summary_large_image">

    <title>TechNews PRO | Terminal de Inteligência, IA & Mercado</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">

    <!-- ONESIGNAL WEB PUSH SDK -->
    <script src="https://cdn.onesignal.com/sdks/web/v16/OneSignalSDK.page.js" defer></script>
    <script>
      window.OneSignalDeferred = window.OneSignalDeferred || [];
      OneSignalDeferred.push(async function(OneSignal) {
        const appId = "{onesignal_id}";
        if (appId && appId.length > 10) {
          await OneSignal.init({
            appId: appId,
            notifyButton: { enable: true }
          });
        }
      });
    </script>

    <style>
        :root[data-theme="dark"] {
            --bg-color: #070b14;
            --card-bg: rgba(17, 25, 40, 0.88);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --primary: #ef4444;
            --accent: #3b82f6;
            --neon: #00f2fe;
            --dark-bar: #03060c;
            --border: rgba(255, 255, 255, 0.08);
            --glass: rgba(15, 23, 42, 0.82);
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
            --glass: rgba(255, 255, 255, 0.92);
        }

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; transition: background-color 0.25s, color 0.2s; }
        body { background-color: var(--bg-color); color: var(--text-main); line-height: 1.6; overflow-x: hidden; }
        #progress-bar { position: fixed; top: 0; left: 0; height: 3px; background: linear-gradient(90deg, var(--primary), var(--neon)); width: 0%; z-index: 99999; }

        .market-ticker { background: var(--dark-bar); color: #e2e8f0; padding: 0.45rem 5%; font-size: 0.8rem; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; font-family: 'JetBrains Mono', monospace; }
        .market-items { display: flex; gap: 1.5rem; align-items: center; overflow-x: auto; white-space: nowrap; }
        .market-item { display: flex; align-items: center; gap: 6px; }
        .up { color: #10b981; font-weight: 700; }
        .down { color: #ef4444; font-weight: 700; }
        .live-dot { width: 8px; height: 8px; background: #10b981; border-radius: 50%; display: inline-block; animation: blink 1.2s infinite; }
        @keyframes blink { 0%, 100% { opacity: 1; box-shadow: 0 0 8px #10b981; } 50% { opacity: 0.3; } }

        header { background: var(--glass); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); padding: 1rem 5%; position: sticky; top: 0; z-index: 1000; border-bottom: 1px solid var(--border); }
        .nav-container { max-width: 1440px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; gap: 1rem; flex-wrap: wrap; }
        .logo { font-size: 1.85rem; font-weight: 900; letter-spacing: -1px; color: var(--text-main); text-decoration: none; display: flex; align-items: center; gap: 6px; cursor: pointer; }
        .logo span { color: var(--primary); }
        .logo-badge { font-size: 0.65rem; background: rgba(239, 68, 68, 0.15); color: var(--primary); border: 1px solid var(--primary); padding: 2px 6px; border-radius: 4px; font-weight: 800; letter-spacing: 0.5px; }

        .nav-links { display: flex; gap: 0.4rem; list-style: none; background: rgba(255,255,255,0.03); padding: 5px; border-radius: 10px; border: 1px solid var(--border); align-items: center; flex-wrap: wrap; }
        .nav-links button, .nav-links a { background: none; border: none; color: var(--text-muted); font-weight: 700; font-size: 0.84rem; cursor: pointer; padding: 0.45rem 0.85rem; border-radius: 7px; transition: 0.2s; text-decoration: none; }
        .nav-links button:hover, .nav-links a:hover { color: var(--text-main); }
        .nav-links button.active { background: var(--primary); color: #fff; box-shadow: 0 4px 12px rgba(239, 68, 68, 0.35); }
        .nav-links a.hub-link { color: var(--neon); border: 1px solid rgba(0, 242, 254, 0.25); }

        .header-actions { display: flex; align-items: center; gap: 0.8rem; }
        .search-box { position: relative; }
        .search-box input { background: rgba(255,255,255,0.05); border: 1px solid var(--border); color: var(--text-main); padding: 0.5rem 1rem 0.5rem 2.2rem; border-radius: 8px; font-size: 0.85rem; width: 175px; outline: none; transition: 0.3s; }
        .search-box input:focus { width: 220px; border-color: var(--primary); }
        .search-icon { position: absolute; left: 10px; top: 50%; transform: translateY(-50%); font-size: 0.8rem; color: var(--text-muted); }

        .theme-btn { background: rgba(255,255,255,0.06); border: 1px solid var(--border); color: var(--text-main); padding: 0.45rem 0.85rem; border-radius: 8px; cursor: pointer; font-weight: 700; font-size: 0.85rem; display: flex; align-items: center; gap: 6px; }
        .cta-btn { background: linear-gradient(135deg, #ef4444, #b91c1c); color: #fff; border: none; padding: 0.55rem 1.2rem; border-radius: 8px; font-weight: 800; cursor: pointer; text-decoration: none; font-size: 0.85rem; box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3); display: inline-flex; align-items: center; gap: 6px; }

        .tags-bar { max-width: 1440px; margin: 1.2rem auto 0 auto; padding: 0 5%; display: flex; align-items: center; gap: 0.6rem; overflow-x: auto; white-space: nowrap; }
        .tag-pill { background: var(--card-bg); border: 1px solid var(--border); color: var(--text-muted); padding: 4px 12px; border-radius: 20px; font-size: 0.78rem; font-weight: 600; cursor: pointer; transition: 0.2s; text-decoration: none; }
        .tag-pill:hover { border-color: var(--primary); color: var(--text-main); }

        .ad-banner-top { max-width: 970px; min-height: 90px; margin: 1.5rem auto; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }
        .main-container { max-width: 1440px; margin: 0 auto 4rem auto; padding: 0 5%; display: grid; grid-template-columns: 7.2fr 2.8fr; gap: 2.5rem; }

        .hero-card { position: relative; border-radius: 16px; overflow: hidden; box-shadow: 0 20px 40px rgba(0,0,0,0.35); margin-bottom: 2.5rem; display: block; border: 1px solid var(--border); background: #000; }
        .hero-card img { width: 100%; height: 470px; object-fit: cover; opacity: 0.75; transition: transform 0.6s ease; }
        .hero-card:hover img { transform: scale(1.03); }
        .hero-overlay { position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(to top, rgba(3,6,12,0.98) 15%, rgba(3,6,12,0.65) 65%, transparent 100%); padding: 2.5rem; color: #fff; }
        .badge-source { background: var(--primary); color: #fff; padding: 5px 12px; border-radius: 6px; font-size: 0.72rem; font-weight: 900; text-transform: uppercase; display: inline-block; margin-bottom: 0.8rem; }
        .hero-overlay h1 { font-size: 2.15rem; line-height: 1.2; margin-bottom: 0.8rem; font-weight: 900; }
        .hero-overlay p { color: #cbd5e1; font-size: 1.02rem; margin-bottom: 1.2rem; }
        .hero-actions { display: flex; gap: 0.8rem; flex-wrap: wrap; }

        .section-title { font-size: 1.35rem; font-weight: 900; margin-bottom: 1.5rem; border-left: 4px solid var(--primary); padding-left: 12px; display: flex; justify-content: space-between; align-items: center; }
        .feed-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(310px, 1fr)); gap: 1.8rem; }

        .news-card { background: var(--card-bg); border-radius: 14px; overflow: hidden; border: 1px solid var(--border); display: flex; flex-direction: column; transition: transform 0.25s ease; backdrop-filter: blur(10px); }
        .news-card:hover { transform: translateY(-6px); border-color: rgba(239, 68, 68, 0.4); }
        .card-img-wrapper { position: relative; width: 100%; height: 195px; overflow: hidden; background: #1e293b; }
        .card-img-wrapper img { width: 100%; height: 100%; object-fit: cover; }
        .card-tag { position: absolute; top: 12px; left: 12px; background: rgba(3, 6, 12, 0.85); color: #fff; padding: 4px 10px; border-radius: 6px; font-size: 0.68rem; font-weight: 800; text-transform: uppercase; }
        .card-floating-btns { position: absolute; bottom: 10px; right: 10px; display: flex; gap: 6px; }
        .audio-btn { background: rgba(239, 68, 68, 0.92); color: #fff; border: none; padding: 5px 10px; border-radius: 20px; font-size: 0.72rem; font-weight: 700; cursor: pointer; }
        .zap-btn { background: rgba(16, 185, 129, 0.92); color: #fff; border: none; padding: 5px 9px; border-radius: 20px; font-size: 0.72rem; font-weight: 700; text-decoration: none; }

        .card-body { padding: 1.4rem; display: flex; flex-direction: column; flex-grow: 1; }
        .card-meta { font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.6rem; display: flex; justify-content: space-between; font-weight: 600; }
        .card-title { font-size: 1.12rem; font-weight: 800; color: var(--text-main); margin-bottom: 0.75rem; line-height: 1.35; }
        .card-desc { font-size: 0.88rem; color: var(--text-muted); margin-bottom: 1.3rem; flex-grow: 1; }
        .seo-internal-link { color: var(--neon); font-weight: 700; text-decoration: underline; }

        .card-footer-btns { display: grid; grid-template-columns: 1fr 1fr; gap: 0.6rem; margin-top: auto; }
        .btn-outline { background: rgba(255,255,255,0.04); color: var(--text-main); border: 1px solid var(--border); padding: 0.65rem; border-radius: 8px; font-weight: 700; font-size: 0.8rem; cursor: pointer; text-align: center; text-decoration: none; }
        .read-btn { background: var(--primary); color: #fff; font-weight: 700; font-size: 0.8rem; padding: 0.65rem; border-radius: 8px; text-decoration: none; text-align: center; }

        .native-ad-card { background: linear-gradient(145deg, rgba(239,68,68,0.14), rgba(15,23,42,0.92)); border: 2px solid rgba(239, 68, 68, 0.55); border-radius: 14px; padding: 1.8rem; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; }
        .native-ad-card .ad-badge { background: var(--primary); color: #fff; font-size: 0.68rem; font-weight: 900; padding: 3px 10px; border-radius: 20px; text-transform: uppercase; margin-bottom: 1rem; }

        .sidebar { display: flex; flex-direction: column; gap: 2rem; }
        .widget { background: var(--card-bg); border-radius: 14px; padding: 1.5rem; border: 1px solid var(--border); }
        .widget-title { font-size: 1.05rem; font-weight: 900; margin-bottom: 1.2rem; padding-bottom: 0.6rem; border-bottom: 2px solid var(--primary); }
        .trending-list { list-style: none; display: flex; flex-direction: column; gap: 1rem; }
        .trending-item { display: flex; gap: 0.9rem; align-items: flex-start; text-decoration: none; color: inherit; cursor: pointer; }
        .trending-num { font-size: 1.4rem; font-weight: 900; color: var(--primary); font-family: 'JetBrains Mono', monospace; }
        .trending-text { font-size: 0.88rem; font-weight: 700; line-height: 1.35; }

        .newsletter-box { background: linear-gradient(135deg, #111827, #03060c); color: #fff; border-radius: 14px; padding: 1.8rem; text-align: center; border: 1px solid rgba(239, 68, 68, 0.35); }
        .newsletter-box input { width: 100%; padding: 0.8rem; border-radius: 8px; border: 1px solid rgba(255,255,255,0.15); background: rgba(255,255,255,0.05); color: #fff; margin: 0.8rem 0; font-size: 0.88rem; }
        .newsletter-box button { width: 100%; padding: 0.85rem; background: var(--primary); color: #fff; border: none; border-radius: 8px; font-weight: 800; cursor: pointer; }

        #reader-modal, #exit-modal, #adblock-modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(3, 6, 12, 0.9); z-index: 9999; justify-content: center; align-items: center; backdrop-filter: blur(8px); padding: 1rem; }
        .reader-box { background: var(--bg-color); border: 1px solid var(--border); width: 100%; max-width: 680px; border-radius: 16px; overflow: hidden; max-height: 90vh; display: flex; flex-direction: column; }
        .reader-img { width: 100%; height: 240px; object-fit: cover; }
        .reader-body { padding: 2rem; overflow-y: auto; }
        .reader-ai-box { background: rgba(59, 130, 246, 0.1); border-left: 4px solid var(--accent); padding: 1rem; border-radius: 6px; margin: 1.2rem 0; font-size: 0.92rem; }
        .reader-promo { background: rgba(239, 68, 68, 0.1); border: 1px dashed var(--primary); padding: 1rem; border-radius: 8px; text-align: center; margin-top: 1.5rem; }
        .adblock-content { background: var(--card-bg); color: var(--text-main); border: 1px solid rgba(239,68,68,0.45); width: 90%; max-width: 440px; border-radius: 20px; padding: 2.2rem 1.8rem; text-align: center; }
        .adblock-btn { background: var(--primary); color: #fff; padding: 0.9rem; border-radius: 8px; font-weight: 800; width: 100%; border: none; cursor: pointer; margin-top: 1.2rem; }
        .adblock-close { margin-top: 1rem; font-size: 0.8rem; color: var(--text-muted); text-decoration: underline; cursor: pointer; background: none; border: none; width: 100%; }

        #social-proof-toast { position: fixed; bottom: 20px; left: 20px; background: var(--card-bg); border: 1px solid var(--border); border-left: 4px solid #10b981; padding: 0.85rem 1.2rem; border-radius: 12px; z-index: 8000; display: flex; align-items: center; gap: 12px; font-size: 0.8rem; max-width: 340px; transform: translateY(150%); transition: transform 0.4s ease; cursor: pointer; }
        #social-proof-toast.show { transform: translateY(0); }

        footer { background: var(--dark-bar); color: #64748b; text-align: center; padding: 3rem 5%; font-size: 0.85rem; border-top: 1px solid var(--border); }
        @media (max-width: 992px) { .main-container { grid-template-columns: 1fr; } .hero-card img { height: 320px; } .hero-overlay h1 { font-size: 1.5rem; } }
    </style>
</head>
<body>
    <div id="progress-bar"></div>
    <div id="ad-honeypot" class="ad-banner adsbox doubleclick sponsor" style="position:absolute; top:-999px; left:-999px; width:10px; height:10px;"></div>

    <!-- MODAL ANTI-ADBLOCK -->
    <div id="adblock-modal">
        <div class="adblock-content">
            <h3 style="font-size:1.35rem; font-weight:900; margin-bottom:0.6rem;">Acesso Restrito pelo AdBlock 🛡️</h3>
            <p style="font-size:0.9rem; color:var(--text-muted);">O <strong>TechNews.PRO</strong> mantém servidores de IA gratuitos graças aos patrocinadores. Desative seu bloqueador para liberar o terminal completo.</p>
            <button class="adblock-btn" onclick="location.reload()">Já desativei! Liberar Terminal &rarr;</button>
            <button class="adblock-close" onclick="document.getElementById('adblock-modal').style.display='none'">Continuar leitura limitada (Fechar)</button>
        </div>
    </div>

    <!-- MODAL DE INTENÇÃO DE SAÍDA -->
    <div id="exit-modal" onclick="document.getElementById('exit-modal').style.display='none'">
        <div class="adblock-content" onclick="event.stopPropagation()">
            <span class="badge-source">⚡ ESPERE! NÃO SAIA DE MÃOS VAZIAS</span>
            <h3 style="font-size:1.4rem; font-weight:900; margin-bottom:0.6rem;">Quer Automatizar sua Renda com IA?</h3>
            <p style="font-size:0.9rem; color:var(--text-muted); margin-bottom:1.4rem;">Resgate seu acesso ao treinamento oficial que revela como criar máquinas automáticas de vendas e tráfego na internet.</p>
            <a href="{link_kiwify_3}" target="_blank" rel="noopener noreferrer" class="cta-btn" style="width:100%; justify-content:center; padding:0.9rem;">🎁 Resgatar Acesso VIP &rarr;</a>
            <button class="adblock-close" onclick="document.getElementById('exit-modal').style.display='none'">Fechar janela</button>
        </div>
    </div>

    <!-- MODAL DE LEITURA RÁPIDA (TIME-TO-VALUE IA) -->
    <div id="reader-modal" onclick="fecharReader()">
        <div class="reader-box" onclick="event.stopPropagation()">
            <img id="r-img" src="" class="reader-img" alt="Capa">
            <div class="reader-body">
                <span id="r-source" class="badge-source">Fonte</span>
                <h2 id="r-title" style="margin-bottom: 1rem; line-height: 1.3;">Título</h2>
                <div class="reader-ai-box">
                    <strong>🤖 Síntese Executiva IA (Time-to-Value):</strong>
                    <p id="r-desc" style="margin-top: 6px;"></p>
                </div>
                <div style="display:flex; gap:10px; flex-wrap:wrap; margin-top:1.2rem;">
                    <a id="r-url" href="#" target="_blank" rel="noopener noreferrer" class="cta-btn" style="flex:1; justify-content:center;">Ler Matéria Completa na Fonte &rarr;</a>
                    <button onclick="fecharReader()" class="btn-outline" style="padding:0.6rem 1.2rem;">Fechar</button>
                </div>
                <div class="reader-promo">
                    <p style="font-size:0.84rem; margin-bottom:8px;">🔥 <strong>Oportunidade Em Destaque:</strong> Domine as ferramentas de IA que estão gerando novos milionários digitais.</p>
                    <a href="{link_kiwify_3}" target="_blank" style="color:var(--primary); font-weight:800; font-size:0.88rem;">Desbloquear Método Oficial Agora &rarr;</a>
                </div>
            </div>
        </div>
    </div>

    <!-- TOAST DE PROVA SOCIAL -->
    <div id="social-proof-toast" onclick="window.open('{link_kiwify_1}', '_blank')">
        <span style="font-size:1.5rem;">🔥</span>
        <div>
            <div id="toast-text" style="font-weight:700; color:var(--text-main);">Alguém acabou de acessar a Área VIP</div>
            <div style="font-size:0.72rem; color:var(--primary); font-weight:700;">Clique para ver a oferta em alta &rarr;</div>
        </div>
    </div>

    <!-- BARRA DE MERCADO E COTAÇÕES AO VIVO -->
    <div class="market-ticker">
        <div class="market-items">
            <span><span class="live-dot"></span> <strong>TERMINAL AO VIVO</strong></span>
            {cotacoes_html}
        </div>
        <div>
            <a href="cotacao-agora.html" style="color:var(--neon); text-decoration:underline; margin-right:12px;">📊 Abrir Dashboard de Cotações</a>
            <span>⚡ Sincronizado: {data_atualizacao}</span>
        </div>
    </div>

    <header>
        <div class="nav-container">
            <a class="logo" onclick="filtrarCategoria('todos', event)">
                TechNews<span>.PRO</span>
                <span class="logo-badge">IA v7.5</span>
            </a>
            <ul class="nav-links">
                <li><button onclick="filtrarCategoria('todos', event)" class="active">🔥 Tudo</button></li>
                <li><button onclick="filtrarCategoria('Tecnologia', event)">💻 Tech & IA</button></li>
                <li><button onclick="filtrarCategoria('Finanças', event)">📈 Mercado</button></li>
                <li><button onclick="filtrarCategoria('Ciência', event)">🚀 Ciência</button></li>
                <li><a href="inteligencia-artificial.html" class="hub-link">🧠 Dossiê IA</a></li>
                <li><a href="cotacao-agora.html" class="hub-link">💵 Cotações</a></li>
            </ul>
            <div class="header-actions">
                <div class="search-box">
                    <span class="search-icon">🔍</span>
                    <input type="text" id="search-input" placeholder="Buscar notícia..." onkeyup="buscarNoticia()">
                </div>
                <button class="theme-btn" id="theme-toggle-btn" onclick="alternarTema()">🌙 Escuro</button>
                <a href="{smartlink_url}" target="_blank" rel="noopener noreferrer" class="cta-btn">💎 Área VIP</a>
            </div>
        </div>
    </header>

    <div class="tags-bar">
        <span style="font-size:0.75rem; font-weight:800; color:var(--primary); text-transform:uppercase;">Topic Clusters SEO:</span>
        <a href="inteligencia-artificial.html" class="tag-pill">#HubInteligênciaArtificial</a>
        <a href="cotacao-agora.html" class="tag-pill">#TerminalDólar&Bitcoin</a>
        <a href="bitcoin.html" class="tag-pill">#RadarBitcoin</a>
        <a href="chatgpt.html" class="tag-pill">#RadarChatGPT</a>
        <a href="startups.html" class="tag-pill">#RadarStartups</a>
        <span class="tag-pill" onclick="filtrarPorPalavra('Python')">#Dev&Automação</span>
        <span class="tag-pill" onclick="filtrarCategoria('todos', event)">🔄 Mostrar Tudo</span>
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
                <span style="font-size:0.75rem; color:var(--text-muted); font-weight:600;">🔊 Ouça as matérias em áudio</span>
            </h2>
            <div class="feed-grid" id="feed-container"></div>
        </div>

        <aside class="sidebar">
            <div class="widget">
                <div class="widget-title">🔥 Mais Lidas no Terminal</div>
                <ul class="trending-list">{trending_section}</ul>
            </div>

            <!-- DESTAQUE LATERAL KIWIFY 2 -->
            <div class="widget" style="background: linear-gradient(135deg, rgba(239,68,68,0.16), rgba(15,23,42,0.95)); border-color: rgba(239,68,68,0.45); text-align: center;">
                <span class="badge-source" style="margin-bottom:0.5rem;">🔥 Recomendação PRO</span>
                <h3 style="margin-bottom: 0.5rem; font-size: 1.08rem;">⚡ Destrave Novas Fontes de Renda Digital</h3>
                <p style="font-size: 0.82rem; color: var(--text-muted); margin-bottom: 1rem;">Acesse o sistema passo a passo mais recomendado pelos nossos leitores em 2026.</p>
                <a href="{link_kiwify_2}" target="_blank" rel="noopener noreferrer" class="cta-btn" style="width: 100%; justify-content: center;">Conhecer Método Oficial &rarr;</a>
            </div>

            <!-- CAPTURA DE LEADS SYSTEME.IO -->
            <div class="newsletter-box" id="newsletter">
                <h3>💰 Briefing Matinal VIP</h3>
                <p style="font-size:0.84rem; color:#94a3b8;">Receba os insights de IA, Negócios e Ferramentas Secretas no seu e-mail.</p>
                <form action="{systeme_url}" method="GET" target="_blank">
                    <input type="email" name="email" placeholder="Digite seu melhor e-mail..." required>
                    <button type="submit">Liberar Acesso Gratuito &rarr;</button>
                </form>
            </div>

            <div class="widget" style="text-align: center; padding: 1.2rem;">
                <p style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 0.6rem;">🔗 <strong>Páginas Especiais & Clusters:</strong></p>
                <p style="margin-bottom:6px;"><a href="inteligencia-artificial.html" style="color: var(--neon); font-size: 0.84rem; font-weight: 700; text-decoration: underline;">🧠 Enciclopédia & Hub de IA &rarr;</a></p>
                <p style="margin-bottom:6px;"><a href="cotacao-agora.html" style="color: #10b981; font-size: 0.84rem; font-weight: 700; text-decoration: underline;">📊 Monitor de Cotações Ao Vivo &rarr;</a></p>
                <p style="margin-bottom:6px;"><a href="bitcoin.html" style="color: #f59e0b; font-size: 0.84rem; font-weight: 700; text-decoration: underline;">₿ Radar Bitcoin & Cripto &rarr;</a></p>
                <p><a href="chatgpt.html" style="color: #3b82f6; font-size: 0.84rem; font-weight: 700; text-decoration: underline;">🤖 Radar ChatGPT & OpenAI &rarr;</a></p>
            </div>

            <!-- BANNER LATERAL ADSTERRA (300x250) -->
            <div style="position: sticky; top: 90px; text-align: center;">
                <span style="font-size: 0.7rem; color: var(--text-muted); display: block; margin-bottom: 5px;">Publicidade</span>
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
        </aside>
    </main>

    <footer>
        <p><strong>TechNews.PRO</strong> &copy; {ano_atual} — Ecossistema Automatizado via Python, Topic Clusters SEO, OpenAI, Telegram, OneSignal & Meta Graph API.</p>
        <p style="margin-top: 8px; font-size: 0.78rem;">
            <a href="index.html" style="color:#94a3b8; margin:0 8px;">Início</a> |
            <a href="inteligencia-artificial.html" style="color:#94a3b8; margin:0 8px;">Hub IA</a> |
            <a href="cotacao-agora.html" style="color:#94a3b8; margin:0 8px;">Cotações</a> |
            <a href="bitcoin.html" style="color:#94a3b8; margin:0 8px;">Bitcoin</a> |
            <a href="chatgpt.html" style="color:#94a3b8; margin:0 8px;">ChatGPT</a> |
            <a href="startups.html" style="color:#94a3b8; margin:0 8px;">Startups</a> |
            <a href="feed.xml" style="color:#94a3b8; margin:0 8px;">RSS Feed</a> |
            <a href="sitemap.xml" style="color:#94a3b8; margin:0 8px;">Sitemap XML</a>
        </p>
    </footer>

    <script>
        const todasNoticias = {noticias_json};
        const ofertasKiwify = [
            { badge: "Destaque Patrocinado", titulo: "🚀 Método IA & Automação Lucrativa", desc: "Aprenda a construir sistemas automáticos na internet e escale resultados todos os dias.", url: "{link_kiwify_1}", cta: "Acessar Treinamento VIP &rarr;" },
            { badge: "Ferramenta Recomendada", titulo: "💎 Escale seus Resultados no Digital", desc: "O guia definitivo para transformar atenção e tecnologia em vendas recorrentes no piloto automático.", url: "{link_kiwify_2}", cta: "Desbloquear Oferta Especial &rarr;" },
            { badge: "Acesso Exclusivo", titulo: "⚡ Domine as Novas Tecnologias de 2026", desc: "Saia na frente de 99% do mercado aplicando estratégias validadas de negócios digitais.", url: "{link_kiwify_3}", cta: "Quero Garantir Minha Vaga &rarr;" }
        ];

        // TEIA DE ARANHA SEO AUTOMÁTICA NOS TEXTOS
        function aplicarTeiaSEO(texto) {
            if (!texto) return "";
            let t = texto;
            t = t.replace(/\\b(inteligência artificial|IA)\\b/i, '<a href="inteligencia-artificial.html" class="seo-internal-link">$1</a>');
            t = t.replace(/\\b(dólar|euro|câmbio)\\b/i, '<a href="cotacao-agora.html" class="seo-internal-link">$1</a>');
            t = t.replace(/\\b(bitcoin|criptomoedas|cripto)\\b/i, '<a href="bitcoin.html" class="seo-internal-link">$1</a>');
            t = t.replace(/\\b(chatgpt|openai)\\b/i, '<a href="chatgpt.html" class="seo-internal-link">$1</a>');
            t = t.replace(/\\b(startup|startups)\\b/i, '<a href="startups.html" class="seo-internal-link">$1</a>');
            return t;
        }

        window.onscroll = function() {
            var winScroll = document.body.scrollTop || document.documentElement.scrollTop;
            var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            document.getElementById("progress-bar").style.width = ((winScroll / height) * 100) + "%";
        };

        function alternarTema() {
            const htmlEl = document.documentElement;
            const btn = document.getElementById('theme-toggle-btn');
            const novo = htmlEl.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
            htmlEl.setAttribute('data-theme', novo);
            btn.innerHTML = novo === 'dark' ? '🌙 Escuro' : '☀️ Claro';
            localStorage.setItem('technews_theme', novo);
        }

        function falarNoticia(idx, event) {
            if (event) event.stopPropagation();
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel();
                const art = todasNoticias[idx];
                const msg = new SpeechSynthesisUtterance(art.title + ". " + art.desc);
                msg.lang = 'pt-BR';
                msg.rate = 1.08;
                window.speechSynthesis.speak(msg);
            }
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
        function fecharReader() {
            document.getElementById('reader-modal').style.display = 'none';
            if ('speechSynthesis' in window) window.speechSynthesis.cancel();
        }

        function renderizarLista(lista) {
            if (!lista || lista.length === 0) {
                document.getElementById('hero-container').innerHTML = '';
                document.getElementById('feed-container').innerHTML = '<div style="grid-column: 1 / -1; padding:3rem; text-align:center; color:var(--text-muted); background:var(--card-bg); border-radius:12px; border:1px solid var(--border);">🔍 Nenhuma notícia encontrada para este filtro no momento. Clique em "Mostrar Tudo" ou aguarde a próxima varredura!</div>';
                return;
            }

            const hero = lista[0];
            const heroIdx = todasNoticias.indexOf(hero);

            document.getElementById('hero-container').innerHTML = `
                <div class="hero-card">
                    <img src="${hero.img}" alt="Destaque" onerror="this.src='https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=1200&q=80'">
                    <div class="hero-overlay">
                        <span class="badge-source">🔥 Manchete Principal • ${hero.source}</span>
                        <h1>${hero.title}</h1>
                        <p>${aplicarTeiaSEO(hero.desc)}</p>
                        <div class="hero-actions">
                            <button onclick="abrirReader(${heroIdx})" class="cta-btn">⚡ Síntese Executiva IA</button>
                            <button onclick="falarNoticia(${heroIdx}, event)" class="btn-outline" style="background:rgba(0,0,0,0.65); color:#fff;">🔊 Ouvir</button>
                            <a href="${hero.url}" target="_blank" rel="noopener noreferrer" class="btn-outline" style="background:rgba(255,255,255,0.12); color:#fff;">Fonte Oficial &rarr;</a>
                        </div>
                    </div>
                </div>
            `;

            let feedHtml = '';
            let adCount = 0;
            lista.slice(1, 11).forEach((art, idx) => {
                const globalIdx = todasNoticias.indexOf(art);
                const zapTexto = encodeURIComponent("🚨 Olha essa notícia no TechNews PRO: " + art.title + " - " + window.location.href);
                feedHtml += `
                <article class="news-card">
                    <div class="card-img-wrapper">
                        <span class="card-tag">${art.source}</span>
                        <img src="${art.img}" alt="Capa" onerror="this.src='https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80'">
                        <div class="card-floating-btns">
                            <button class="audio-btn" onclick="falarNoticia(${globalIdx}, event)">🔊 Ouvir</button>
                            <a href="https://api.whatsapp.com/send?text=${zapTexto}" target="_blank" class="zap-btn" title="Compartilhar no WhatsApp">📲</a>
                        </div>
                    </div>
                    <div class="card-body">
                        <div class="card-meta">
                            <span>📅 ${art.date}</span>
                            <span style="color:var(--primary)">● ${art.categoria}</span>
                        </div>
                        <h3 class="card-title">${art.title}</h3>
                        <p class="card-desc">${aplicarTeiaSEO(art.desc)}</p>
                        <div class="card-footer-btns">
                            <button onclick="abrirReader(${globalIdx})" class="btn-outline">⚡ Resumo IA</button>
                            <a href="${art.url}" target="_blank" rel="noopener noreferrer" class="read-btn">Ler Fonte &rarr;</a>
                        </div>
                    </div>
                </article>
                `;

                if (idx === 1 || idx === 4 || idx === 7) {
                    const oferta = ofertasKiwify[adCount % ofertasKiwify.length];
                    adCount++;
                    feedHtml += `
                    <div class="native-ad-card">
                        <span class="ad-badge">${oferta.badge}</span>
                        <h3 style="margin-bottom:0.6rem;">${oferta.titulo}</h3>
                        <p style="font-size:0.88rem; color:var(--text-muted); margin-bottom:1.2rem;">${oferta.desc}</p>
                        <a href="${oferta.url}" target="_blank" rel="noopener noreferrer" class="cta-btn" style="width: 100%; justify-content:center;">${oferta.cta}</a>
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
                if (event.currentTarget && event.currentTarget.tagName === 'BUTTON') {
                    event.currentTarget.classList.add('active');
                }
            }
            document.getElementById('titulo-secao').innerText = categoria === 'todos' ? 'Radar Global em Tempo Real' : 'Setor: ' + categoria;
            const filtradas = categoria === 'todos' ? todasNoticias : todasNoticias.filter(n => n.categoria === categoria);
            renderizarLista(filtradas);
        }

        function buscarNoticia() {
            const termo = document.getElementById('search-input').value.toLowerCase();
            const filtradas = todasNoticias.filter(n => n.title.toLowerCase().includes(termo) || n.desc.toLowerCase().includes(termo));
            renderizarLista(filtradas);
        }

        function filtrarPorPalavra(palavra) {
            document.getElementById('search-input').value = palavra;
            buscarNoticia();
        }

        setTimeout(function() {
            var honeypot = document.getElementById('ad-honeypot');
            if (!honeypot || honeypot.offsetHeight === 0 || window.getComputedStyle(honeypot).display === 'none') {
                document.getElementById('adblock-modal').style.display = 'flex';
            }
        }, 1800);

        let exitMostrado = false;
        document.addEventListener('mouseleave', function(e) {
            if (e.clientY < 0 && !exitMostrado) {
                exitMostrado = true;
                document.getElementById('exit-modal').style.display = 'flex';
            }
        });

        setTimeout(function() {
            const toast = document.getElementById('social-proof-toast');
            if (toast) toast.classList.add('show');
            setTimeout(() => { if (toast) toast.classList.remove('show'); }, 6500);
        }, 4000);

        renderizarLista(todasNoticias);
    </script>

    <!-- SOCIAL BAR FLUTUANTE ADSTERRA -->
    <script data-cfasync="false" src="https://bicea.org/14/7843682dc41b2077e8d78d48efd6360a"></script>
</body>
</html>
"""

# ==============================================================================
# COTAÇÕES EM TEMPO REAL E UTILITÁRIOS DE SEO
# ==============================================================================
def obter_dados_cotacoes():
    dados_padrao = {
        "USDBRL": {"nome": "💵 Dólar Comercial", "val": "R$ 5,70", "pct": "+0.15%", "classe": "up"},
        "EURBRL": {"nome": "💶 Euro Oficial", "val": "R$ 6,18", "pct": "+0.10%", "classe": "up"},
        "BTCBRL": {"nome": "₿ Bitcoin (BTC)", "val": "R$ 420.000", "pct": "+1.25%", "classe": "up"}
    }
    try:
        url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL"
        r = requests.get(url, timeout=6)
        if r.status_code == 200:
            d = r.json()
            for par, label in [("USDBRL", "💵 Dólar Comercial"), ("EURBRL", "💶 Euro Oficial"), ("BTCBRL", "₿ Bitcoin (BTC)")]:
                if par in d:
                    val = float(d[par]["bid"])
                    pct = float(d[par]["pctChange"])
                    classe = "up" if pct >= 0 else "down"
                    sinal = "+" if pct >= 0 else ""
                    val_fmt = f"R$ {val:,.2f}" if par != "BTCBRL" else f"R$ {val:,.0f}"
                    dados_padrao[par] = {"nome": label, "val": val_fmt, "pct": f"{sinal}{pct:.2f}%", "classe": classe}
    except:
        pass

    itens_ticker = [
        f'<span class="market-item">{v["nome"]}: <strong>{v["val"]}</strong> <span class="{v["classe"]}">({v["pct"]})</span></span>'
        for v in dados_padrao.values()
    ]
    return " • ".join(itens_ticker), dados_padrao

def aplicar_teia_seo_estatico(texto):
    if not texto:
        return ""
    novo = re.sub(
        r'(?i)\b(inteligência artificial|IA)\b',
        f'<a href="{URL_PORTAL_OFICIAL}inteligencia-artificial.html" style="color:#00f2fe; font-weight:700; text-decoration:underline;">\\1</a>',
        texto, count=1
    )
    novo = re.sub(
        r'(?i)\b(dólar|euro|câmbio)\b',
        f'<a href="{URL_PORTAL_OFICIAL}cotacao-agora.html" style="color:#10b981; font-weight:700; text-decoration:underline;">\\1</a>',
        novo, count=1
    )
    novo = re.sub(
        r'(?i)\b(bitcoin|criptomoedas|cripto)\b',
        f'<a href="{URL_PORTAL_OFICIAL}bitcoin.html" style="color:#f59e0b; font-weight:700; text-decoration:underline;">\\1</a>',
        novo, count=1
    )
    return novo

# ==============================================================================
# INTELIGÊNCIA ARTIFICIAL: DISSONÂNCIA COGNITIVA (DISCOVER) & TIME-TO-VALUE
# ==============================================================================
def otimizar_noticia_com_ia(noticia):
    if not OPENAI_API_KEY:
        return noticia
    titulo_orig = noticia.get("title", "")
    desc_orig = noticia.get("desc", "")
    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {OPENAI_API_KEY}"}
        prompt = (
            f"Título original: {titulo_orig}\nResumo original: {desc_orig}\n\n"
            "Retorne um JSON estrito com duas chaves: 'titulo' e 'resumo'.\n"
            "1. Em 'titulo': Reescreva o título para o Google Discover usando 'Dissonância Cognitiva' e curiosidade específica (quebrando a expectativa sem perder a verdade do fato, máx 110 caracteres).\n"
            "2. Em 'resumo': Entregue o 'Time-to-Value' (a resposta direta e o impacto prático no bolso/carreira) logo na primeira frase e finalize com uma segunda frase analítica."
        )
        payload = {
            "model": "gpt-4o-mini",
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": "Você é um especialista em Google Discover, SEO e retenção de leitores (Time-to-Value). Responda apenas em JSON válido."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 180,
            "temperature": 0.75
        }
        r = requests.post(url, headers=headers, json=payload, timeout=10)
        if r.status_code == 200:
            dados_ia = json.loads(r.json()["choices"][0]["message"]["content"])
            if dados_ia.get("titulo"):
                noticia["title"] = dados_ia["titulo"].strip()
            if dados_ia.get("resumo"):
                noticia["desc"] = dados_ia["resumo"].strip()
    except Exception as e:
        print(f"Aviso IA otimização: {e}")
    return noticia

# ==============================================================================
# AGENTES SOCIAIS: ONESIGNAL PUSH, TELEGRAM E FACEBOOK (COMPLETOS)
# ==============================================================================
def disparar_onesignal_push(noticia):
    if not ONESIGNAL_APP_ID or not ONESIGNAL_REST_KEY or not noticia:
        print("Agente OneSignal: ONESIGNAL_APP_ID ou ONESIGNAL_REST_KEY ausentes nos Secrets. Pulando.")
        return False
    try:
        titulo_curto = noticia['title'][:55] + "..." if len(noticia['title']) > 55 else noticia['title']
        payload = {
            "app_id": ONESIGNAL_APP_ID.strip(),
            "included_segments": ["Subscribed Users"],
            "headings": {"en": "🚨 URGENTE: " + titulo_curto, "pt": "🚨 URGENTE: " + titulo_curto},
            "contents": {"en": noticia['desc'][:110] + "...", "pt": noticia['desc'][:110] + "..."},
            "url": URL_PORTAL_OFICIAL
        }
        headers = {"Authorization": f"Basic {ONESIGNAL_REST_KEY.strip()}", "Content-Type": "application/json"}
        r = requests.post("https://onesignal.com/api/v1/notifications", json=payload, headers=headers, timeout=10)
        if r.status_code == 200:
            print("Agente OneSignal: ✅ Notificação Web Push enviada para os subscritores!")
            return True
        else:
            print(f"Agente OneSignal Aviso ({r.status_code}): {r.text}")
    except Exception as e:
        print(f"Agente OneSignal Erro: {e}")
    return False

def publicar_no_telegram(noticia):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID or not noticia:
        print("Agente Telegram: TELEGRAM_BOT_TOKEN ou TELEGRAM_CHAT_ID ausentes nos Secrets. Pulando.")
        return False
    try:
        titulo_limpo = html.escape(noticia.get("title", ""))
        desc_limpa = html.escape(noticia.get("desc", ""))
        stamp = datetime.now().strftime("%Y%m%d%H%M")
        link_track = f"{URL_PORTAL_OFICIAL}?utm_source=telegram_vip&v={stamp}"

        texto_alerta = (
            f"🚨 <b>[URGENTE] Acabou de sair no Terminal:</b>\n\n"
            f"🔥 <b>{titulo_limpo}</b>\n\n"
            f"💡 <i>{desc_limpa}</i>\n\n"
            f"👉 <b>Leia a análise completa antes que saia do ar:</b>\n"
            f"🔗 {link_track}\n\n"
            f"💎 <a href=\"{LINK_KIWIFY_1}\">Acesse também a Ferramenta VIP do Dia</a>"
        )
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID.strip(),
            "text": texto_alerta,
            "parse_mode": "HTML",
            "disable_web_page_preview": False
        }
        r = requests.post(url, json=payload, timeout=12)
        if r.status_code == 200:
            print("Agente Telegram: ✅ Alerta Dark Social enviado com sucesso para o Canal VIP!")
            return True
        else:
            print(f"Agente Telegram Aviso ({r.status_code}): {r.text}")
    except Exception as e:
        print(f"Agente Telegram Erro: {e}")
    return False

def gerar_copy_persuasiva_meta(noticia):
    titulo = noticia.get("title", "")
    resumo = noticia.get("desc", "")
    cta_padrao = (
        f"\n\n👉 ACESSE A MATÉRIA COMPLETA AQUI:\n"
        f"🔗 {URL_PORTAL_OFICIAL}\n\n"
        f"🛑 O detalhe mais importante (e como isso impacta o mercado) acabou de ser atualizado no nosso Terminal Oficial!\n\n"
        f"👇 Clique no Card/Link acima ou comente 'LINK', 'QUERO' ou 'VIP' que te envio o acesso + uma Ferramenta Secreta direto no seu Direct! 🚀"
    )
    if not OPENAI_API_KEY:
        return f"🚨 URGENTE: {titulo}!\n\n{resumo}{cta_padrao}"
    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {OPENAI_API_KEY}"}
        prompt = (
            f"Notícia: {titulo}. Resumo: {resumo}.\n"
            f"Link Oficial do Portal: {URL_PORTAL_OFICIAL}\n\n"
            "Crie um post altamente magnético para o Facebook seguindo esta estrutura exata:\n"
            "1. GANCHO EXPLOSIVO com emojis na primeira linha.\n"
            f"2. LOGO ABAIXO DO GANCHO, coloque: 👉 Leia completo no portal: {URL_PORTAL_OFICIAL}\n"
            "3. OPEN LOOP (Curiosidade): Conte o início da notícia de forma envolvente, mas pare no melhor momento dizendo que os detalhes completos estão no portal.\n"
            f"4. FECHAMENTO: Convide a clicar na imagem/card abaixo ou no link ({URL_PORTAL_OFICIAL}) e peça também para comentarem 'LINK' ou 'VIP' para receberem uma ferramenta secreta no Direct."
        )
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "Você é um copywriter especialista em tráfego direto, retenção e cliques no Facebook."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 250,
            "temperature": 0.75
        }
        r = requests.post(url, headers=headers, json=payload, timeout=10)
        if r.status_code == 200:
            copy_ia = r.json()["choices"][0]["message"]["content"].strip().replace('"', '')
            if URL_PORTAL_OFICIAL not in copy_ia:
                copy_ia += f"\n\n👉 Acesse a matéria completa aqui: {URL_PORTAL_OFICIAL}"
            return copy_ia
    except:
        pass
    return f"🚨 URGENTE: {titulo}!\n\n{resumo}{cta_padrao}"

def obter_credenciais_pagina(token_inicial):
    try:
        url_acc = "https://graph.facebook.com/v20.0/me/accounts"
        r = requests.get(url_acc, params={"access_token": token_inicial}, timeout=10)
        if r.status_code == 200:
            dados = r.json().get("data", [])
            if len(dados) > 0:
                pagina = dados[0]
                return pagina.get("id"), pagina.get("access_token", token_inicial)
    except:
        pass
    return "me", token_inicial

def escolher_noticia_inedita(lista_noticias):
    historico = []
    if os.path.exists(ARQUIVO_MEMORIA_META):
        try:
            with open(ARQUIVO_MEMORIA_META, "r", encoding="utf-8") as f:
                historico = [linha.strip().lower() for linha in f.readlines() if linha.strip()]
        except:
            pass
    for n in lista_noticias:
        tit = n.get("title", "").strip().lower()
        if tit and tit not in historico:
            return n
    return lista_noticias[0]

def salvar_memoria_meta(titulo):
    try:
        historico = []
        if os.path.exists(ARQUIVO_MEMORIA_META):
            with open(ARQUIVO_MEMORIA_META, "r", encoding="utf-8") as f:
                historico = [linha.strip() for linha in f.readlines() if linha.strip()]
        if titulo.strip() not in historico:
            historico.append(titulo.strip())
        historico = historico[-20:]
        with open(ARQUIVO_MEMORIA_META, "w", encoding="utf-8") as f:
            f.write("\n".join(historico))
    except:
        pass

def publicar_no_facebook(noticia):
    if not META_ACCESS_TOKEN or not noticia:
        print("Agente Meta: META_ACCESS_TOKEN ausente nos Secrets. Pulando.")
        return False

    alvo_id, token_pagina = obter_credenciais_pagina(META_ACCESS_TOKEN)
    mensagem = gerar_copy_persuasiva_meta(noticia)
    img_url = noticia.get("img", "")

    stamp = datetime.now().strftime("%Y%m%d%H%M")
    link_com_cache_buster = f"{URL_PORTAL_OFICIAL}?v={stamp}"

    try:
        requests.post("https://graph.facebook.com/v20.0/", data={"id": link_com_cache_buster, "scrape": "true", "access_token": token_pagina}, timeout=10)
        requests.post("https://graph.facebook.com/v20.0/", data={"id": URL_PORTAL_OFICIAL, "scrape": "true", "access_token": token_pagina}, timeout=10)
    except:
        pass

    alvos_tentativa = [alvo_id]
    if "me" not in alvos_tentativa:
        alvos_tentativa.append("me")

    for alvo in alvos_tentativa:
        try:
            url_feed = f"https://graph.facebook.com/v20.0/{alvo}/feed"
            payload_feed = {"message": mensagem, "link": link_com_cache_buster, "access_token": token_pagina}
            r_feed = requests.post(url_feed, data=payload_feed, timeout=15)
            if r_feed.status_code == 200:
                salvar_memoria_meta(noticia.get("title", ""))
                print(f"Agente Meta: ✅ Card de Link Clicável publicado via '{alvo}'! ID: {r_feed.json().get('id')}")
                return True
        except:
            pass

    if img_url and img_url.startswith("http"):
        for alvo in alvos_tentativa:
            try:
                url_photo = f"https://graph.facebook.com/v20.0/{alvo}/photos"
                r_photo = requests.post(url_photo, data={"url": img_url, "caption": mensagem, "access_token": token_pagina}, timeout=15)
                if r_photo.status_code == 200:
                    salvar_memoria_meta(noticia.get("title", ""))
                    print(f"Agente Meta: ✅ Post com IMAGEM + Link publicado via '{alvo}'!")
                    return True
            except:
                pass
    return False

# ==============================================================================
# COLETA MULTI-APIS COM FILTRO DE NICHO E IMAGENS 1200PX
# ==============================================================================
PALAVRAS_BLOQUEADAS = [
    "futebol", "gol", "campeonato", "brasileirão", "z-4", "botafogo", "flamengo",
    "corinthians", "palmeiras", "grêmio", "inter ", "internacional", "vinagre",
    "limpar janela", "faxina", "receita caseira", "fofoca", "bbb", "novela",
    "horóscopo", "astrologia", "manifestantes", "cacetadas"
]

def noticia_relevante_nicho(titulo, desc=""):
    texto = f"{titulo} {desc}".lower()
    return not any(b in texto for b in PALAVRAS_BLOQUEADAS)

def classificar_noticia(titulo):
    t = titulo.lower()
    if any(k in t for k in ["finança", "banco", "mercado", "ação", "investimento", "startup", "economia", "negócio", "dólar", "cripto", "bitcoin", "ibge", "cnpj", "receita federal", "imposto", "pib"]):
        return "Finanças"
    elif any(k in t for k in ["espaço", "nasa", "satélite", "ciência", "física", "astronomia", "foguete", "órbita"]):
        return "Ciência"
    return "Tecnologia"

def fetch_ibge_noticias():
    noticias = []
    try:
        r = requests.get("https://servicodados.ibge.gov.br/api/v3/noticias/?qtd=6", timeout=8)
        if r.status_code == 200:
            for item in r.json().get("items", []):
                titulo = item.get("titulo", "")
                desc = item.get("introducao", "Confira os dados completos divulgados pelo portal oficial.")
                if not noticia_relevante_nicho(titulo, desc):
                    continue
                img_url = "https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?auto=format&fit=crop&w=1200&q=85"
                try:
                    imagens_json = json.loads(item.get("imagens", "{}"))
                    if imagens_json.get("image_intro"):
                        img_url = "https://agenciadenoticias.ibge.gov.br/" + imagens_json["image_intro"]
                except:
                    pass
                noticias.append({
                    "title": titulo, "desc": desc, "img": img_url,
                    "url": item.get("link", "#"), "source": "IBGE Oficial",
                    "date": item.get("data_publicacao", "Hoje")[:10], "categoria": classificar_noticia(titulo)
                })
    except:
        pass
    return noticias

def fetch_devto_pt():
    noticias = []
    try:
        r = requests.get("https://dev.to/api/articles?tag=portuguese&per_page=8", headers={'User-Agent': 'Mozilla/5.0'}, timeout=8)
        if r.status_code == 200:
            for item in r.json():
                titulo = item.get("title", "")
                desc = item.get("description") or "Artigo técnico sobre tecnologia e desenvolvimento."
                if not noticia_relevante_nicho(titulo, desc):
                    continue
                noticias.append({
                    "title": titulo, "desc": desc,
                    "img": item.get("cover_image") or item.get("social_image") or "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=85",
                    "url": item.get("url", "#"), "source": "Dev.to Brasil",
                    "date": item.get("readable_publish_date", "Recente"), "categoria": classificar_noticia(titulo)
                })
    except:
        pass
    return noticias

def fetch_spaceflight_news():
    noticias = []
    try:
        r = requests.get("https://api.spaceflightnewsapi.net/v4/articles/?limit=4", timeout=8)
        if r.status_code == 200:
            for item in r.json().get("results", []):
                noticias.append({
                    "title": item.get("title", ""), "desc": item.get("summary", ""),
                    "img": item.get("image_url") or "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&q=85",
                    "url": item.get("url", "#"), "source": "SpaceTech",
                    "date": item.get("published_at", "")[:10], "categoria": "Ciência"
                })
    except:
        pass
    return noticias

def fetch_newsapi():
    noticias = []
    if not NEWS_API_KEY:
        return noticias
    try:
        query = '("inteligencia artificial" OR tecnologia OR ciberseguranca OR criptomoedas OR bitcoin OR startups OR software)'
        url = f"https://newsapi.org/v2/everything?q={query}&language=pt&sortBy=publishedAt&pageSize=10&apiKey={NEWS_API_KEY}"
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=8)
        if r.status_code == 200:
            for item in r.json().get("articles", []):
                titulo = item.get("title") or ""
                desc = item.get("description") or "Clique para ler a matéria completa na fonte oficial."
                if titulo and titulo != "[Removed]" and noticia_relevante_nicho(titulo, desc):
                    noticias.append({
                        "title": titulo, "desc": desc,
                        "img": item.get("urlToImage") or "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=1200&q=85",
                        "url": item.get("url", "#"), "source": item.get("source", {}).get("name", "TechPress"),
                        "date": item.get("publishedAt", "")[:10], "categoria": classificar_noticia(titulo)
                    })
    except:
        pass
    return noticias

FALLBACK_NEWS = [
    {
        "title": "Inteligência Artificial Generativa redefine o mercado de tecnologia e cria novas profissões em alta",
        "desc": "Grandes corporações aceleram a adoção de agentes autônomos para otimizar processos e escalar produtos digitais.",
        "img": "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=1200&q=85",
        "url": "https://news.google.com", "source": "Destaque IA", "date": "Hoje", "categoria": "Tecnologia"
    },
    {
        "title": "Fintechs brasileiras batem recorde de captação e expandem soluções de pagamento instantâneo",
        "desc": "Novos relatórios apontam crescimento expressivo no setor financeiro digital com foco em crédito inteligente e dólar.",
        "img": "https://images.unsplash.com/photo-1559526324-4b87b5e36e44?auto=format&fit=crop&w=1200&q=85",
        "url": "https://agenciadenoticias.ibge.gov.br", "source": "Finanças & Negócios", "date": "Hoje", "categoria": "Finanças"
    }
]

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
# GERAÇÃO DE RSS FEED, HUB IA, COTAÇÕES, CLUSTERS SEO E SITEMAP XML
# ==============================================================================
def gerar_rss(noticias):
    xml = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
  <title>TechNews PRO | Terminal de Inteligência, IA e Mercado</title>
  <link>{URL_PORTAL_OFICIAL}</link>
  <description>Notícias em tempo real sobre Inteligência Artificial, Tecnologia, Ciência e Mercado Financeiro.</description>
  <language>pt-BR</language>
"""
    for n in noticias[:15]:
        xml += f"""  <item>
    <title>{html.escape(n.get('title', ''))}</title>
    <link>{html.escape(n.get('url', URL_PORTAL_OFICIAL))}</link>
    <description>{html.escape(n.get('desc', ''))}</description>
  </item>\n"""
    xml += "</channel>\n</rss>"
    with open("feed.xml", "w", encoding="utf-8") as f:
        f.write(xml)

def gerar_hub_ia(todas_noticias, cotacoes_html, data_fmt, ano_fmt):
    cards_ia = ""
    noticias_ia = [n for n in todas_noticias if n.get("categoria") == "Tecnologia" or "ia" in n.get("title", "").lower()]
    if not noticias_ia:
        noticias_ia = todas_noticias[:6]

    for art in noticias_ia[:8]:
        cards_ia += f"""
        <article style="background:rgba(17,25,40,0.88); border:1px solid rgba(255,255,255,0.08); border-radius:14px; overflow:hidden; display:flex; flex-direction:column;">
            <img src="{art['img']}" alt="{html.escape(art['title'])}" style="width:100%; height:190px; object-fit:cover;" onerror="this.src='https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=1200&q=85'">
            <div style="padding:1.4rem; display:flex; flex-direction:column; flex-grow:1;">
                <span style="font-size:0.72rem; color:#ef4444; font-weight:800; text-transform:uppercase;">{art['source']} • {art['date']}</span>
                <h3 style="font-size:1.12rem; margin:0.5rem 0 0.8rem 0; color:#f8fafc;">{art['title']}</h3>
                <p style="font-size:0.88rem; color:#94a3b8; margin-bottom:1.2rem; flex-grow:1;">{aplicar_teia_seo_estatico(art['desc'])}</p>
                <a href="{art['url']}" target="_blank" rel="noopener noreferrer" style="background:#ef4444; color:#fff; text-align:center; padding:0.65rem; border-radius:8px; font-weight:700; font-size:0.82rem; text-decoration:none;">Ler Relatório Completo &rarr;</a>
            </div>
        </article>
        """

    html_hub = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Hub Oficial de Inteligência Artificial: Guia definitivo, ferramentas generativas, automação e notícias em tempo real sobre IA.">
    <meta name="robots" content="max-image-preview:large, index, follow">
    <link rel="canonical" href="{URL_PORTAL_OFICIAL}inteligencia-artificial.html">
    <title>Inteligência Artificial (Hub Oficial) | Guia, Ferramentas & Notícias | TechNews PRO</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
    <style>
        body {{ background:#070b14; color:#f8fafc; font-family:'Inter',sans-serif; margin:0; line-height:1.65; }}
        .ticker {{ background:#03060c; padding:0.45rem 5%; font-size:0.8rem; font-family:'JetBrains Mono',monospace; border-bottom:1px solid rgba(255,255,255,0.08); display:flex; justify-content:space-between; flex-wrap:wrap; }}
        .up {{ color:#10b981; font-weight:700; }} .down {{ color:#ef4444; font-weight:700; }}
        header {{ background:rgba(15,23,42,0.85); backdrop-filter:blur(12px); padding:1rem 5%; border-bottom:1px solid rgba(255,255,255,0.08); display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem; }}
        .container {{ max-width:1360px; margin:2rem auto; padding:0 5%; }}
        .pillar-box {{ background:linear-gradient(145deg, rgba(59,130,246,0.14), rgba(15,23,42,0.92)); border:1px solid rgba(59,130,246,0.4); border-radius:16px; padding:2.5rem; margin-bottom:2.5rem; }}
        .grid {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(300px, 1fr)); gap:1.8rem; }}
        footer {{ background:#03060c; color:#64748b; text-align:center; padding:3rem 5%; margin-top:4rem; border-top:1px solid rgba(255,255,255,0.08); }}
    </style>
</head>
<body>
    <div class="ticker">
        <div>{cotacoes_html}</div>
        <div>⚡ Atualizado: {data_fmt}</div>
    </div>
    <header>
        <a href="index.html" style="font-size:1.8rem; font-weight:900; color:#fff; text-decoration:none;">TechNews<span style="color:#ef4444;">.PRO</span></a>
        <div style="display:flex; gap:14px; align-items:center; flex-wrap:wrap;">
            <a href="index.html" style="color:#94a3b8; text-decoration:none; font-weight:700; font-size:0.88rem;">&larr; Voltar ao Radar Principal</a>
            <a href="cotacao-agora.html" style="color:#10b981; text-decoration:none; font-weight:700; font-size:0.88rem;">📊 Cotações Ao Vivo</a>
            <a href="{LINK_KIWIFY_1}" target="_blank" style="background:#ef4444; color:#fff; padding:0.55rem 1.1rem; border-radius:8px; font-weight:800; text-decoration:none; font-size:0.85rem;">🚀 Treinamento VIP de IA</a>
        </div>
    </header>

    <!-- BANNER TOPO ADSTERRA -->
    <div style="text-align:center; margin:1.5rem auto;">
        <script>atOptions={{'key':'06959dfe796ac17610a3027d9ede544f','format':'iframe','height':90,'width':728,'params':{{}}}};</script>
        <script src="https://bicea.org/22/06959dfe796ac17610a3027d9ede544f"></script>
    </div>

    <main class="container">
        <section class="pillar-box">
            <span style="background:#3b82f6; color:#fff; padding:4px 12px; border-radius:20px; font-size:0.72rem; font-weight:900; text-transform:uppercase;">Topic Cluster • Enciclopédia & Hub Oficial</span>
            <h1 style="font-size:2.3rem; margin:0.8rem 0; font-weight:900;">Inteligência Artificial em 2026: O Guia Central de Automação e Disrupção</h1>
            <p style="color:#cbd5e1; font-size:1rem; margin-bottom:1rem;">A <strong>Inteligência Artificial (IA)</strong> deixou de ser uma promessa futurista para se tornar a infraestrutura central da economia global. De Modelos de Linguagem de Grande Escala (LLMs) a agentes autônomos capazes de programar, negociar ativos no <a href="cotacao-agora.html" style="color:#00f2fe;">mercado financeiro</a> e operar negócios inteiros na nuvem, dominar a IA é hoje o maior diferencial competitivo.</p>
            <div style="display:flex; gap:12px; flex-wrap:wrap; margin-top:1.5rem;">
                <a href="{LINK_KIWIFY_3}" target="_blank" style="background:#ef4444; color:#fff; padding:0.75rem 1.4rem; border-radius:8px; font-weight:800; text-decoration:none;">⚡ Desbloquear Método de Automação com IA &rarr;</a>
                <a href="{SMARTLINK_ADSTERRA}" target="_blank" style="background:rgba(255,255,255,0.08); color:#fff; padding:0.75rem 1.4rem; border-radius:8px; font-weight:700; text-decoration:none;">💎 Acessar Ferramentas Recomendadas</a>
            </div>
        </section>

        <h2 style="font-size:1.4rem; margin-bottom:1.5rem; border-left:4px solid #ef4444; padding-left:12px;">Últimas Notícias e Descobertas de Inteligência Artificial</h2>
        <div class="grid">{cards_ia}</div>
    </main>
    <footer>
        <p><strong>TechNews.PRO</strong> &copy; {ano_fmt} — Hub de Autoridade em Inteligência Artificial.</p>
    </footer>
    <script data-cfasync="false" src="https://bicea.org/14/7843682dc41b2077e8d78d48efd6360a"></script>
</body>
</html>"""
    with open("inteligencia-artificial.html", "w", encoding="utf-8") as f:
        f.write(html_hub)

def gerar_pagina_cotacoes(dados_cot, cotacoes_html, data_fmt, ano_fmt):
    usd = dados_cot["USDBRL"]
    eur = dados_cot["EURBRL"]
    btc = dados_cot["BTCBRL"]

    html_cot = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Cotação do Dólar, Euro e Bitcoin hoje em tempo real. Dashboard financeiro minimalista e gratuito para jornalistas, analistas e investidores.">
    <meta name="robots" content="max-image-preview:large, index, follow">
    <link rel="canonical" href="{URL_PORTAL_OFICIAL}cotacao-agora.html">
    <title>Cotação Dólar, Euro e Bitcoin Hoje Ao Vivo | Terminal TechNews PRO</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
    <style>
        body {{ background:#070b14; color:#f8fafc; font-family:'Inter',sans-serif; margin:0; line-height:1.6; }}
        header {{ background:rgba(15,23,42,0.9); padding:1rem 5%; border-bottom:1px solid rgba(255,255,255,0.08); display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem; }}
        .container {{ max-width:1200px; margin:2.5rem auto; padding:0 5%; }}
        .cards {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:1.8rem; margin:2.5rem 0; }}
        .card {{ background:linear-gradient(145deg, #111827, #03060c); border:1px solid rgba(255,255,255,0.1); border-radius:16px; padding:2.2rem; text-align:center; box-shadow:0 15px 30px rgba(0,0,0,0.4); }}
        .price {{ font-size:2.4rem; font-weight:900; font-family:'JetBrains Mono',monospace; margin:0.8rem 0; }}
        .up {{ color:#10b981; }} .down {{ color:#ef4444; }}
        .cite-box {{ background:rgba(17,25,40,0.9); border:1px dashed rgba(0,242,254,0.4); border-radius:14px; padding:1.8rem; margin-top:2.5rem; text-align:center; }}
        code {{ background:#03060c; color:#00f2fe; padding:8px 14px; border-radius:6px; display:inline-block; margin:10px 0; font-family:'JetBrains Mono',monospace; font-size:0.82rem; word-break:break-all; }}
        footer {{ background:#03060c; color:#64748b; text-align:center; padding:3rem 5%; margin-top:4rem; border-top:1px solid rgba(255,255,255,0.08); }}
    </style>
</head>
<body>
    <header>
        <a href="index.html" style="font-size:1.8rem; font-weight:900; color:#fff; text-decoration:none;">TechNews<span style="color:#ef4444;">.PRO</span></a>
        <div style="display:flex; gap:14px; align-items:center; flex-wrap:wrap;">
            <a href="index.html" style="color:#94a3b8; text-decoration:none; font-weight:700; font-size:0.88rem;">&larr; Portal de Notícias</a>
            <a href="inteligencia-artificial.html" style="color:#00f2fe; text-decoration:none; font-weight:700; font-size:0.88rem;">🧠 Hub de IA</a>
            <a href="{LINK_KIWIFY_2}" target="_blank" style="background:#ef4444; color:#fff; padding:0.55rem 1.1rem; border-radius:8px; font-weight:800; text-decoration:none; font-size:0.85rem;">📈 Método Renda Digital</a>
        </div>
    </header>

    <!-- BANNER TOPO ADSTERRA -->
    <div style="text-align:center; margin:1.5rem auto;">
        <script>atOptions={{'key':'06959dfe796ac17610a3027d9ede544f','format':'iframe','height':90,'width':728,'params':{{}}}};</script>
        <script src="https://bicea.org/22/06959dfe796ac17610a3027d9ede544f"></script>
    </div>

    <main class="container">
        <div style="text-align:center; max-width:780px; margin:0 auto;">
            <span style="background:rgba(16,185,129,0.15); color:#10b981; border:1px solid #10b981; padding:4px 12px; border-radius:20px; font-size:0.75rem; font-weight:800;">🟢 TERMINAL FINANCEIRO EM TEMPO REAL</span>
            <h1 style="font-size:2.5rem; margin:1rem 0 0.5rem 0; font-weight:900;">Cotação Hoje: Dólar, Euro e Bitcoin Ao Vivo</h1>
            <p style="color:#94a3b8; font-size:1rem;">Painel minimalista de consulta rápida sincronizado via API oficial de câmbio e criptoativos. Última aferição: <strong>{data_fmt}</strong>.</p>
        </div>

        <div class="cards">
            <div class="card">
                <div style="font-size:0.9rem; color:#94a3b8; font-weight:700;">{usd['nome']} (USD/BRL)</div>
                <div class="price">{usd['val']}</div>
                <div class="{usd['classe']}" style="font-weight:800;">Variação 24h: {usd['pct']}</div>
            </div>
            <div class="card">
                <div style="font-size:0.9rem; color:#94a3b8; font-weight:700;">{eur['nome']} (EUR/BRL)</div>
                <div class="price">{eur['val']}</div>
                <div class="{eur['classe']}" style="font-weight:800;">Variação 24h: {eur['pct']}</div>
            </div>
            <div class="card">
                <div style="font-size:0.9rem; color:#94a3b8; font-weight:700;">{btc['nome']} (BTC/BRL)</div>
                <div class="price">{btc['val']}</div>
                <div class="{btc['classe']}" style="font-weight:800;">Variação 24h: {btc['pct']}</div>
            </div>
        </div>

        <div class="cite-box">
            <h3 style="margin-bottom:0.4rem;">🔗 Ferramenta Pública para Jornalistas, Pesquisadores e Blogs</h3>
            <p style="color:#94a3b8; font-size:0.88rem;">Utilize os dados deste painel em seus artigos ou relatórios incorporando o código de atribuição de fonte abaixo:</p>
            <code id="embed-code">&lt;a href="{URL_PORTAL_OFICIAL}cotacao-agora.html" target="_blank"&gt;Fonte: Terminal de Cotações TechNews PRO&lt;/a&gt;</code>
            <br>
            <button onclick="navigator.clipboard.writeText(document.getElementById('embed-code').innerText); this.innerText='✅ Código Copiado!';" style="margin-top:8px; background:#3b82f6; color:#fff; border:none; padding:0.55rem 1.2rem; border-radius:6px; font-weight:700; cursor:pointer;">📋 Copiar Link de Citação</button>
        </div>
    </main>
    <footer>
        <p><strong>TechNews.PRO</strong> &copy; {ano_fmt} — Dados fornecidos para fins informativos e jornalísticos.</p>
    </footer>
    <script data-cfasync="false" src="https://bicea.org/14/7843682dc41b2077e8d78d48efd6360a"></script>
</body>
</html>"""
    with open("cotacao-agora.html", "w", encoding="utf-8") as f:
        f.write(html_cot)

# SEO PROGRAMÁTICO EM ESCALA (CLUSTERS COM MONETIZAÇÃO INCLUÍDA)
TAGS_SEO_DINAMICAS = {
    "bitcoin": {
        "titulo": "Radar Bitcoin & Criptomoedas em Tempo Real",
        "desc": "Acompanhe as últimas notícias, análises de mercado e movimentações sobre Bitcoin, Ethereum e ativos digitais.",
        "kw": ["bitcoin", "cripto", "btc", "blockchain", "moeda", "dólar", "finança"]
    },
    "chatgpt": {
        "titulo": "Radar ChatGPT, OpenAI & LLMs Generativos",
        "desc": "Cobertura completa sobre atualizações do ChatGPT, OpenAI, agentes autônomos e novas ferramentas de IA.",
        "kw": ["chatgpt", "openai", "gpt", "ia", "inteligência", "algoritmo", "software"]
    },
    "startups": {
        "titulo": "Radar Startups, Fintechs & Negócios Digitais",
        "desc": "Inovação, rodadas de investimento, crescimento de fintechs e estratégias de negócios de alto impacto.",
        "kw": ["startup", "fintech", "negócio", "empresa", "mercado", "investimento", "tecnologia"]
    }
}

def gerar_paginas_programaticas(todas_noticias, cotacoes_html, data_fmt, ano_fmt):
    urls_geradas = []
    for slug, cfg in TAGS_SEO_DINAMICAS.items():
        filtradas = [
            n for n in todas_noticias
            if any(k in n.get('title', '').lower() or k in n.get('desc', '').lower() for k in cfg['kw'])
        ]
        if not filtradas:
            filtradas = todas_noticias[:6]

        cards = ""
        for art in filtradas[:8]:
            cards += f"""
            <article style="background:rgba(17,25,40,0.88); border:1px solid rgba(255,255,255,0.08); border-radius:14px; overflow:hidden; display:flex; flex-direction:column;">
                <img src="{art['img']}" alt="{html.escape(art['title'])}" style="width:100%; height:185px; object-fit:cover;" onerror="this.src='https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=85'">
                <div style="padding:1.4rem; display:flex; flex-direction:column; flex-grow:1;">
                    <span style="font-size:0.72rem; color:#ef4444; font-weight:800;">{art['source']} • {art['date']}</span>
                    <h3 style="font-size:1.1rem; margin:0.5rem 0 0.8rem 0; color:#f8fafc;">{art['title']}</h3>
                    <p style="font-size:0.86rem; color:#94a3b8; margin-bottom:1.2rem; flex-grow:1;">{aplicar_teia_seo_estatico(art['desc'])}</p>
                    <a href="{art['url']}" target="_blank" rel="noopener noreferrer" style="background:#ef4444; color:#fff; text-align:center; padding:0.65rem; border-radius:8px; font-weight:700; font-size:0.82rem; text-decoration:none;">Ler Matéria Completa &rarr;</a>
                </div>
            </article>
            """

        html_cluster = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{cfg['desc']}">
    <meta name="robots" content="max-image-preview:large, index, follow">
    <link rel="canonical" href="{URL_PORTAL_OFICIAL}{slug}.html">
    <title>{cfg['titulo']} | TechNews PRO</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap" rel="stylesheet">
    <style>
        body {{ background:#070b14; color:#f8fafc; font-family:'Inter',sans-serif; margin:0; line-height:1.6; }}
        header {{ background:#0f172a; padding:1rem 5%; border-bottom:1px solid rgba(255,255,255,0.08); display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem; }}
        .container {{ max-width:1360px; margin:2rem auto; padding:0 5%; }}
        .grid {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(300px, 1fr)); gap:1.8rem; }}
        footer {{ background:#03060c; color:#64748b; text-align:center; padding:3rem 5%; margin-top:4rem; border-top:1px solid rgba(255,255,255,0.08); }}
    </style>
</head>
<body>
    <header>
        <a href="index.html" style="font-size:1.8rem; font-weight:900; color:#fff; text-decoration:none;">TechNews<span style="color:#ef4444;">.PRO</span></a>
        <div style="display:flex; gap:14px; align-items:center; flex-wrap:wrap;">
            <a href="index.html" style="color:#94a3b8; text-decoration:none; font-weight:700; font-size:0.88rem;">&larr; Radar Principal</a>
            <a href="inteligencia-artificial.html" style="color:#00f2fe; text-decoration:none; font-weight:700; font-size:0.88rem;">🧠 Hub IA</a>
            <a href="cotacao-agora.html" style="color:#10b981; text-decoration:none; font-weight:700; font-size:0.88rem;">📊 Cotações</a>
            <a href="{LINK_KIWIFY_1}" target="_blank" style="background:#ef4444; color:#fff; padding:0.55rem 1.1rem; border-radius:8px; font-weight:800; text-decoration:none; font-size:0.85rem;">💎 Área VIP</a>
        </div>
    </header>

    <!-- BANNER TOPO ADSTERRA -->
    <div style="text-align:center; margin:1.5rem auto;">
        <script>atOptions={{'key':'06959dfe796ac17610a3027d9ede544f','format':'iframe','height':90,'width':728,'params':{{}}}};</script>
        <script src="https://bicea.org/22/06959dfe796ac17610a3027d9ede544f"></script>
    </div>

    <main class="container">
        <h1 style="font-size:2.2rem; margin-bottom:0.5rem; border-left:5px solid #ef4444; padding-left:14px;">{cfg['titulo']}</h1>
        <p style="color:#94a3b8; margin-bottom:2rem;">{cfg['desc']} Atualizado em {data_fmt}.</p>
        <div class="grid">{cards}</div>
    </main>
    <footer>
        <p><strong>TechNews.PRO</strong> &copy; {ano_fmt} — Topic Cluster Automatizado.</p>
    </footer>
    <script data-cfasync="false" src="https://bicea.org/14/7843682dc41b2077e8d78d48efd6360a"></script>
</body>
</html>"""
        nome_arq = f"{slug}.html"
        with open(nome_arq, "w", encoding="utf-8") as f:
            f.write(html_cluster)
        urls_geradas.append(nome_arq)
    return urls_geradas

def gerar_sitemap_xml(urls_extras):
    hoje = datetime.now().strftime("%Y-%m-%d")
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>{URL_PORTAL_OFICIAL}</loc><lastmod>{hoje}</lastmod><changefreq>hourly</changefreq><priority>1.0</priority></url>
  <url><loc>{URL_PORTAL_OFICIAL}inteligencia-artificial.html</loc><lastmod>{hoje}</lastmod><changefreq>hourly</changefreq><priority>0.9</priority></url>
  <url><loc>{URL_PORTAL_OFICIAL}cotacao-agora.html</loc><lastmod>{hoje}</lastmod><changefreq>hourly</changefreq><priority>0.9</priority></url>"""
    for u in urls_extras:
        xml += f"\n  <url><loc>{URL_PORTAL_OFICIAL}{u}</loc><lastmod>{hoje}</lastmod><changefreq>hourly</changefreq><priority>0.8</priority></url>"
    xml += "\n</urlset>"
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(xml)

def garantir_verificacao_google():
    with open(ARQUIVO_GOOGLE_VERIF, "w", encoding="utf-8") as f:
        f.write("google-site-verification: google28d5384ab7e71bf6.html")

# ==============================================================================
# FLUXO PRINCIPAL DE GERAÇÃO DO ECOSSISTEMA
# ==============================================================================
def gerar_portal(apenas_site=False):
    brutas = []
    brutas.extend(fetch_devto_pt())
    brutas.extend(fetch_newsapi())
    brutas.extend(fetch_ibge_noticias())
    brutas.extend(fetch_spaceflight_news())

    todas_noticias = deduplicar_noticias(brutas)

    if len(todas_noticias) < 4:
        todas_noticias.extend(FALLBACK_NEWS)
    else:
        random.shuffle(todas_noticias)

    noticia_destaque = escolher_noticia_inedita(todas_noticias)
    if noticia_destaque in todas_noticias:
        todas_noticias.remove(noticia_destaque)
    todas_noticias.insert(0, noticia_destaque)

    print("Otimizando títulos (Dissonância Cognitiva Discover) e resumos (Time-to-Value) com IA...")
    limite = min(len(todas_noticias), 8)
    for i in range(limite):
        todas_noticias[i] = otimizar_noticia_com_ia(todas_noticias[i])

    salvar_memoria_meta(todas_noticias[0].get("title", ""))
    with open(ARQUIVO_FILA_POST, "w", encoding="utf-8") as f:
        json.dump(todas_noticias[0], f, ensure_ascii=False)

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
    data_fmt = agora.strftime("%d/%m/%Y às %H:%M")
    ano_fmt = str(agora.year)
    cotacoes_html, dados_cot = obter_dados_cotacoes()
    noticias_json_str = json.dumps(todas_noticias, ensure_ascii=False)

    destaque = todas_noticias[0]
    og_title = destaque.get("title", "TechNews PRO | Terminal de Inteligência, IA & Mercado").replace('"', '&quot;')
    og_desc = destaque.get("desc", "Acompanhe em tempo real as notícias mais impactantes de Tecnologia, IA e Finanças.").replace('"', '&quot;')
    og_img = destaque.get("img", "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=1200&q=85")

    html_index = (
        HTML_TEMPLATE_INDEX
        .replace("{og_title}", og_title)
        .replace("{og_desc}", og_desc)
        .replace("{og_img}", og_img)
        .replace("{url_portal}", URL_PORTAL_OFICIAL)
        .replace("{cotacoes_html}", cotacoes_html)
        .replace("{trending_section}", trending_html)
        .replace("{noticias_json}", noticias_json_str)
        .replace("{data_atualizacao}", data_fmt)
        .replace("{ano_atual}", ano_fmt)
        .replace("{smartlink_url}", SMARTLINK_ADSTERRA)
        .replace("{systeme_url}", SYSTEME_OPTIN_URL)
        .replace("{link_kiwify_1}", LINK_KIWIFY_1)
        .replace("{link_kiwify_2}", LINK_KIWIFY_2)
        .replace("{link_kiwify_3}", LINK_KIWIFY_3)
        .replace("{onesignal_id}", ONESIGNAL_APP_ID)
    )

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_index)

    gerar_hub_ia(todas_noticias, cotacoes_html, data_fmt, ano_fmt)
    gerar_pagina_cotacoes(dados_cot, cotacoes_html, data_fmt, ano_fmt)
    urls_extras = gerar_paginas_programaticas(todas_noticias, cotacoes_html, data_fmt, ano_fmt)
    gerar_sitemap_xml(urls_extras)
    gerar_rss(todas_noticias)
    garantir_verificacao_google()

    print("✅ Ecossistema v7.5 Master gerado com 100% da monetização, SEO Clusters, RSS e Sitemap!")

    if not apenas_site:
        publicar_no_facebook(todas_noticias[0])
        publicar_no_telegram(todas_noticias[0])
        disparar_onesignal_push(todas_noticias[0])

if __name__ == "__main__":
    if "--gerar-site" in sys.argv:
        gerar_portal(apenas_site=True)
    elif "--postar-redes" in sys.argv or "--postar-meta" in sys.argv:
        if os.path.exists(ARQUIVO_FILA_POST):
            with open(ARQUIVO_FILA_POST, "r", encoding="utf-8") as f:
                noticia_pronta = json.load(f)
            publicar_no_facebook(noticia_pronta)
            publicar_no_telegram(noticia_pronta)
            disparar_onesignal_push(noticia_pronta)
        else:
            print("Agentes Sociais: Fila de postagem não encontrada.")
    else:
        gerar_portal(apenas_site=False)
