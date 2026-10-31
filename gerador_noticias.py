import os
import sys
import re
import io
import html
import math
import wave
import struct
import random
import json
import textwrap
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# Importações seguras + Patch de compatibilidade Pillow 10+ com MoviePy 1.x
try:
    from PIL import Image, ImageDraw, ImageFont, ImageEnhance
    if not hasattr(Image, "ANTIALIAS"):
        Image.ANTIALIAS = getattr(Image, "Resampling", Image).LANCZOS
    PIL_DISPONIVEL = True
except ImportError:
    PIL_DISPONIVEL = False

try:
    from moviepy.editor import ImageClip, AudioFileClip
    MOVIEPY_DISPONIVEL = True
except ImportError:
    MOVIEPY_DISPONIVEL = False

# ==============================================================================
# CONFIGURAÇÃO DE CHAVES E SEGURANÇA (GITHUB SECRETS)
# ==============================================================================
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "4e42db8a8a6645fbad1039ba84a6ea4f")
NEWSDATA_API_KEY = os.getenv("NEWSDATA_API_KEY", "")
API_FUTEBOL_KEY = os.getenv("API_FUTEBOL_KEY", "")
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
# TEMPLATE PRINCIPAL: INDEX.HTML (RESPONSIVIDADE MOBILE E HOTLINK BYPASS V8.3)
# ==============================================================================
HTML_TEMPLATE_INDEX = """<!DOCTYPE html>
<html lang="pt-BR" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
    <meta name="referrer" content="no-referrer">
    <meta name="description" content="Terminal avançado de notícias sobre Inteligência Artificial, Tecnologia, Política, Futebol, Celebridades e Mercado Financeiro em tempo real.">
    
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

    <title>TechNews PRO | Terminal de Inteligência, IA, Esportes & Mercado</title>
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
            --glass: rgba(15, 23, 42, 0.88);
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
            --glass: rgba(255, 255, 255, 0.94);
        }

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; transition: background-color 0.25s, color 0.2s; }
        html, body { width: 100%; max-width: 100vw; overflow-x: hidden; background-color: var(--bg-color); color: var(--text-main); line-height: 1.6; }
        #progress-bar { position: fixed; top: 0; left: 0; height: 3px; background: linear-gradient(90deg, var(--primary), var(--neon)); width: 0%; z-index: 99999; }

        /* TICKER DE COTAÇÕES BLINDADO PARA MOBILE */
        .market-ticker { background: var(--dark-bar); color: #e2e8f0; padding: 0.5rem 4%; font-size: 0.78rem; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; font-family: 'JetBrains Mono', monospace; width: 100%; }
        .market-items { display: flex; gap: 1.2rem; align-items: center; overflow-x: auto; white-space: nowrap; max-width: 100%; -webkit-overflow-scrolling: touch; padding-bottom: 2px; }
        .market-items::-webkit-scrollbar { height: 3px; }
        .market-item { display: inline-flex; align-items: center; gap: 6px; }
        .up { color: #10b981; font-weight: 700; }
        .down { color: #ef4444; font-weight: 700; }
        .live-dot { width: 8px; height: 8px; background: #10b981; border-radius: 50%; display: inline-block; animation: blink 1.2s infinite; flex-shrink: 0; }
        @keyframes blink { 0%, 100% { opacity: 1; box-shadow: 0 0 8px #10b981; } 50% { opacity: 0.3; } }

        header { background: var(--glass); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); padding: 0.9rem 4%; position: sticky; top: 0; z-index: 1000; border-bottom: 1px solid var(--border); width: 100%; }
        .nav-container { max-width: 1440px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; gap: 0.8rem; flex-wrap: wrap; }
        .logo { font-size: clamp(1.4rem, 4vw, 1.85rem); font-weight: 900; letter-spacing: -1px; color: var(--text-main); text-decoration: none; display: flex; align-items: center; gap: 6px; cursor: pointer; }
        .logo span { color: var(--primary); }
        .logo-badge { font-size: 0.62rem; background: rgba(239, 68, 68, 0.15); color: var(--primary); border: 1px solid var(--primary); padding: 2px 6px; border-radius: 4px; font-weight: 800; letter-spacing: 0.5px; }

        .nav-links { display: flex; gap: 0.35rem; list-style: none; background: rgba(255,255,255,0.03); padding: 5px; border-radius: 10px; border: 1px solid var(--border); align-items: center; overflow-x: auto; max-width: 100%; white-space: nowrap; -webkit-overflow-scrolling: touch; }
        .nav-links button, .nav-links a { background: none; border: none; color: var(--text-muted); font-weight: 700; font-size: 0.8rem; cursor: pointer; padding: 0.42rem 0.72rem; border-radius: 7px; transition: 0.2s; text-decoration: none; flex-shrink: 0; }
        .nav-links button:hover, .nav-links a:hover { color: var(--text-main); }
        .nav-links button.active { background: var(--primary); color: #fff; box-shadow: 0 4px 12px rgba(239, 68, 68, 0.35); }
        .nav-links a.hub-link { color: var(--neon); border: 1px solid rgba(0, 242, 254, 0.25); }

        .header-actions { display: flex; align-items: center; gap: 0.6rem; flex-wrap: wrap; }
        .search-box { position: relative; flex-grow: 1; }
        .search-box input { background: rgba(255,255,255,0.05); border: 1px solid var(--border); color: var(--text-main); padding: 0.48rem 0.9rem 0.48rem 2rem; border-radius: 8px; font-size: 0.84rem; width: 155px; outline: none; transition: 0.3s; }
        .search-box input:focus { width: 195px; border-color: var(--primary); }
        .search-icon { position: absolute; left: 9px; top: 50%; transform: translateY(-50%); font-size: 0.78rem; color: var(--text-muted); }

        .theme-btn { background: rgba(255,255,255,0.06); border: 1px solid var(--border); color: var(--text-main); padding: 0.45rem 0.75rem; border-radius: 8px; cursor: pointer; font-weight: 700; font-size: 0.82rem; display: flex; align-items: center; gap: 5px; }
        .cta-btn { background: linear-gradient(135deg, #ef4444, #b91c1c); color: #fff; border: none; padding: 0.5rem 1rem; border-radius: 8px; font-weight: 800; cursor: pointer; text-decoration: none; font-size: 0.82rem; box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3); display: inline-flex; align-items: center; justify-content: center; gap: 6px; }

        .tags-bar { max-width: 1440px; margin: 1rem auto 0 auto; padding: 0 4%; display: flex; align-items: center; gap: 0.55rem; overflow-x: auto; white-space: nowrap; -webkit-overflow-scrolling: touch; }
        .tag-pill { background: var(--card-bg); border: 1px solid var(--border); color: var(--text-muted); padding: 4px 12px; border-radius: 20px; font-size: 0.76rem; font-weight: 600; cursor: pointer; transition: 0.2s; text-decoration: none; flex-shrink: 0; }
        .tag-pill:hover { border-color: var(--primary); color: var(--text-main); }

        /* BANNER TOPO ADSTERRA BLINDADO CONTRA CORTE MOBILE */
        .ad-banner-top { width: 100%; max-width: 970px; min-height: 90px; margin: 1.2rem auto; padding: 0 2%; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; overflow-x: auto; -webkit-overflow-scrolling: touch; }
        .main-container { max-width: 1440px; margin: 0 auto 4rem auto; padding: 0 4%; display: grid; grid-template-columns: 7.2fr 2.8fr; gap: 2.2rem; width: 100%; }
        .content-column, .sidebar { min-width: 0; max-width: 100%; }

        /* HERO CARD ADAPTATIVO (DESKTOP OVERLAY + MOBILE EMPILHADO LIMPO) */
        .hero-card { position: relative; border-radius: 16px; overflow: hidden; box-shadow: 0 20px 40px rgba(0,0,0,0.35); margin-bottom: 2.2rem; display: flex; flex-direction: column; border: 1px solid var(--border); background: #070b14; }
        .hero-card img { width: 100%; height: 450px; object-fit: cover; opacity: 0.78; transition: transform 0.6s ease; }
        .hero-card:hover img { transform: scale(1.02); }
        .hero-overlay { position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(to top, rgba(3,6,12,0.98) 18%, rgba(3,6,12,0.72) 68%, transparent 100%); padding: 2.2rem; color: #fff; }
        .badge-source { background: var(--primary); color: #fff; padding: 5px 12px; border-radius: 6px; font-size: 0.7rem; font-weight: 900; text-transform: uppercase; display: inline-block; margin-bottom: 0.7rem; }
        .hero-overlay h1 { font-size: clamp(1.35rem, 3vw, 2.15rem); line-height: 1.25; margin-bottom: 0.75rem; font-weight: 900; }
        .hero-overlay p { color: #cbd5e1; font-size: clamp(0.88rem, 2vw, 1.02rem); margin-bottom: 1.1rem; }
        .hero-actions { display: flex; gap: 0.7rem; flex-wrap: wrap; }

        .section-title { font-size: clamp(1.1rem, 2.5vw, 1.35rem); font-weight: 900; margin-bottom: 1.4rem; border-left: 4px solid var(--primary); padding-left: 12px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; }
        .feed-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.5rem; width: 100%; }

        .news-card { background: var(--card-bg); border-radius: 14px; overflow: hidden; border: 1px solid var(--border); display: flex; flex-direction: column; transition: transform 0.25s ease; backdrop-filter: blur(10px); min-width: 0; }
        .news-card:hover { transform: translateY(-5px); border-color: rgba(239, 68, 68, 0.4); }
        .card-img-wrapper { position: relative; width: 100%; height: 195px; overflow: hidden; background: #1e293b; }
        .card-img-wrapper img { width: 100%; height: 100%; object-fit: cover; }
        .card-tag { position: absolute; top: 12px; left: 12px; background: rgba(3, 6, 12, 0.85); color: #fff; padding: 4px 10px; border-radius: 6px; font-size: 0.68rem; font-weight: 800; text-transform: uppercase; }
        .card-floating-btns { position: absolute; bottom: 10px; right: 10px; display: flex; gap: 6px; }
        .audio-btn { background: rgba(239, 68, 68, 0.92); color: #fff; border: none; padding: 5px 10px; border-radius: 20px; font-size: 0.72rem; font-weight: 700; cursor: pointer; }
        .zap-btn { background: rgba(16, 185, 129, 0.92); color: #fff; border: none; padding: 5px 9px; border-radius: 20px; font-size: 0.72rem; font-weight: 700; text-decoration: none; }

        .card-body { padding: 1.3rem; display: flex; flex-direction: column; flex-grow: 1; }
        .card-meta { font-size: 0.74rem; color: var(--text-muted); margin-bottom: 0.55rem; display: flex; justify-content: space-between; font-weight: 600; flex-wrap: wrap; gap: 4px; }
        .card-title { font-size: 1.08rem; font-weight: 800; color: var(--text-main); margin-bottom: 0.7rem; line-height: 1.35; word-wrap: break-word; }
        .card-desc { font-size: 0.86rem; color: var(--text-muted); margin-bottom: 1.2rem; flex-grow: 1; word-wrap: break-word; }
        .seo-internal-link { color: var(--neon); font-weight: 700; text-decoration: underline; }

        .card-footer-btns { display: grid; grid-template-columns: 1fr 1fr; gap: 0.55rem; margin-top: auto; }
        .btn-outline { background: rgba(255,255,255,0.05); color: var(--text-main); border: 1px solid var(--border); padding: 0.62rem; border-radius: 8px; font-weight: 700; font-size: 0.78rem; cursor: pointer; text-align: center; text-decoration: none; }
        .read-btn { background: var(--primary); color: #fff; font-weight: 700; font-size: 0.78rem; padding: 0.62rem; border-radius: 8px; text-decoration: none; text-align: center; }

        .native-ad-card { background: linear-gradient(145deg, rgba(239,68,68,0.14), rgba(15,23,42,0.92)); border: 2px solid rgba(239, 68, 68, 0.55); border-radius: 14px; padding: 1.6rem; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; }
        .native-ad-card .ad-badge { background: var(--primary); color: #fff; font-size: 0.68rem; font-weight: 900; padding: 3px 10px; border-radius: 20px; text-transform: uppercase; margin-bottom: 0.9rem; }

        .sidebar { display: flex; flex-direction: column; gap: 1.8rem; }
        .widget { background: var(--card-bg); border-radius: 14px; padding: 1.35rem; border: 1px solid var(--border); width: 100%; overflow: hidden; }
        .widget-title { font-size: 1rem; font-weight: 900; margin-bottom: 1.1rem; padding-bottom: 0.55rem; border-bottom: 2px solid var(--primary); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 6px; }
        .trending-list { list-style: none; display: flex; flex-direction: column; gap: 0.95rem; }
        .trending-item { display: flex; gap: 0.85rem; align-items: flex-start; text-decoration: none; color: inherit; cursor: pointer; }
        .trending-num { font-size: 1.3rem; font-weight: 900; color: var(--primary); font-family: 'JetBrains Mono', monospace; flex-shrink: 0; }
        .trending-text { font-size: 0.86rem; font-weight: 700; line-height: 1.35; }

        /* TABELA DO BRASILEIRÃO WIDGET RESPONSIVO */
        .table-responsive-wrapper { width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch; }
        .tabela-futebol { width: 100%; border-collapse: collapse; font-size: 0.78rem; font-family: 'JetBrains Mono', monospace; min-width: 240px; }
        .tabela-futebol th { text-align: left; padding: 6px 4px; border-bottom: 1px solid var(--border); color: var(--text-muted); font-size: 0.7rem; }
        .tabela-futebol td { padding: 7px 4px; border-bottom: 1px solid rgba(255,255,255,0.04); }
        .g4-badge { color: #10b981; font-weight: 800; }
        .z4-badge { color: #ef4444; font-weight: 800; }

        .newsletter-box { background: linear-gradient(135deg, #111827, #03060c); color: #fff; border-radius: 14px; padding: 1.6rem; text-align: center; border: 1px solid rgba(239, 68, 68, 0.35); }
        .newsletter-box input { width: 100%; padding: 0.78rem; border-radius: 8px; border: 1px solid rgba(255,255,255,0.15); background: rgba(255,255,255,0.05); color: #fff; margin: 0.75rem 0; font-size: 0.86rem; }
        .newsletter-box button { width: 100%; padding: 0.82rem; background: var(--primary); color: #fff; border: none; border-radius: 8px; font-weight: 800; cursor: pointer; }

        #reader-modal, #exit-modal, #adblock-modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(3, 6, 12, 0.9); z-index: 9999; justify-content: center; align-items: center; backdrop-filter: blur(8px); padding: 1rem; }
        .reader-box { background: var(--bg-color); border: 1px solid var(--border); width: 100%; max-width: 680px; border-radius: 16px; overflow: hidden; max-height: 90vh; display: flex; flex-direction: column; }
        .reader-img { width: 100%; height: 220px; object-fit: cover; }
        .reader-body { padding: 1.5rem; overflow-y: auto; }
        .reader-ai-box { background: rgba(59, 130, 246, 0.1); border-left: 4px solid var(--accent); padding: 0.95rem; border-radius: 6px; margin: 1rem 0; font-size: 0.9rem; }
        .reader-promo { background: rgba(239, 68, 68, 0.1); border: 1px dashed var(--primary); padding: 0.95rem; border-radius: 8px; text-align: center; margin-top: 1.2rem; }
        .adblock-content { background: var(--card-bg); color: var(--text-main); border: 1px solid rgba(239,68,68,0.45); width: 95%; max-width: 430px; border-radius: 20px; padding: 1.8rem 1.4rem; text-align: center; }
        .adblock-btn { background: var(--primary); color: #fff; padding: 0.85rem; border-radius: 8px; font-weight: 800; width: 100%; border: none; cursor: pointer; margin-top: 1.1rem; }
        .adblock-close { margin-top: 0.9rem; font-size: 0.78rem; color: var(--text-muted); text-decoration: underline; cursor: pointer; background: none; border: none; width: 100%; }

        #social-proof-toast { position: fixed; bottom: 16px; left: 16px; right: 16px; background: var(--card-bg); border: 1px solid var(--border); border-left: 4px solid #10b981; padding: 0.8rem 1rem; border-radius: 12px; z-index: 8000; display: flex; align-items: center; gap: 10px; font-size: 0.78rem; max-width: 330px; transform: translateY(150%); transition: transform 0.4s ease; cursor: pointer; }
        #social-proof-toast.show { transform: translateY(0); }

        footer { background: var(--dark-bar); color: #64748b; text-align: center; padding: 2.5rem 4%; font-size: 0.82rem; border-top: 1px solid var(--border); }

        /* REGRAS ESPECÍFICAS DE PERFEIÇÃO MOBILE (ZERO CORTES) */
        @media (max-width: 992px) {
            .main-container { grid-template-columns: 1fr; gap: 1.8rem; }
        }
        @media (max-width: 768px) {
            .market-ticker { flex-direction: column; align-items: flex-start; padding: 0.5rem 4%; gap: 6px; }
            .nav-container { flex-direction: column; align-items: stretch; gap: 0.65rem; }
            .header-actions { width: 100%; justify-content: space-between; }
            .search-box { flex: 1; }
            .search-box input, .search-box input:focus { width: 100%; }
            .hero-card img { height: 230px; opacity: 1; }
            .hero-overlay { position: relative; background: #0b1120; padding: 1.35rem; }
            .hero-actions { flex-direction: column; width: 100%; }
            .hero-actions .cta-btn, .hero-actions .btn-outline { width: 100%; justify-content: center; }
            .feed-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div id="progress-bar"></div>
    <div id="ad-honeypot" class="ad-banner adsbox doubleclick sponsor" style="position:absolute; top:-999px; left:-999px; width:10px; height:10px;"></div>

    <!-- MODAL ANTI-ADBLOCK -->
    <div id="adblock-modal">
        <div class="adblock-content">
            <h3 style="font-size:1.3rem; font-weight:900; margin-bottom:0.6rem;">Acesso Restrito pelo AdBlock 🛡️</h3>
            <p style="font-size:0.88rem; color:var(--text-muted);">O <strong>TechNews.PRO</strong> mantém servidores de IA gratuitos graças aos patrocinadores. Desative seu bloqueador para liberar o terminal completo.</p>
            <button class="adblock-btn" onclick="location.reload()">Já desativei! Liberar Terminal &rarr;</button>
            <button class="adblock-close" onclick="document.getElementById('adblock-modal').style.display='none'">Continuar leitura limitada (Fechar)</button>
        </div>
    </div>

    <!-- MODAL DE INTENÇÃO DE SAÍDA -->
    <div id="exit-modal" onclick="document.getElementById('exit-modal').style.display='none'">
        <div class="adblock-content" onclick="event.stopPropagation()">
            <span class="badge-source">⚡ ESPERE! NÃO SAIA DE MÃOS VAZIAS</span>
            <h3 style="font-size:1.35rem; font-weight:900; margin-bottom:0.6rem;">Quer Automatizar sua Renda com IA?</h3>
            <p style="font-size:0.88rem; color:var(--text-muted); margin-bottom:1.3rem;">Resgate seu acesso ao treinamento oficial que revela como criar máquinas automáticas de vendas e tráfego na internet.</p>
            <a href="{link_kiwify_3}" target="_blank" rel="noopener noreferrer" class="cta-btn" style="width:100%; justify-content:center; padding:0.85rem;">🎁 Resgatar Acesso VIP &rarr;</a>
            <button class="adblock-close" onclick="document.getElementById('exit-modal').style.display='none'">Fechar janela</button>
        </div>
    </div>

    <!-- MODAL DE LEITURA RÁPIDA (TIME-TO-VALUE IA) -->
    <div id="reader-modal" onclick="fecharReader()">
        <div class="reader-box" onclick="event.stopPropagation()">
            <img id="r-img" src="" class="reader-img" alt="Capa" referrerpolicy="no-referrer">
            <div class="reader-body">
                <span id="r-source" class="badge-source">Fonte</span>
                <h2 id="r-title" style="margin-bottom: 0.9rem; line-height: 1.3; font-size: 1.25rem;">Título</h2>
                <div class="reader-ai-box">
                    <strong>🤖 Síntese Executiva IA (Time-to-Value):</strong>
                    <p id="r-desc" style="margin-top: 6px;"></p>
                </div>
                <div style="display:flex; gap:10px; flex-wrap:wrap; margin-top:1.1rem;">
                    <a id="r-url" href="#" target="_blank" rel="noopener noreferrer" class="cta-btn" style="flex:1; justify-content:center;">Ler Matéria Completa na Fonte &rarr;</a>
                    <button onclick="fecharReader()" class="btn-outline" style="padding:0.6rem 1.1rem;">Fechar</button>
                </div>
                <div class="reader-promo">
                    <p style="font-size:0.82rem; margin-bottom:6px;">🔥 <strong>Oportunidade Em Destaque:</strong> Domine as ferramentas de IA que estão gerando novos milionários digitais.</p>
                    <a href="{link_kiwify_3}" target="_blank" style="color:var(--primary); font-weight:800; font-size:0.86rem;">Desbloquear Método Oficial Agora &rarr;</a>
                </div>
            </div>
        </div>
    </div>

    <!-- TOAST DE PROVA SOCIAL -->
    <div id="social-proof-toast" onclick="window.open('{link_kiwify_1}', '_blank')">
        <span style="font-size:1.4rem;">🔥</span>
        <div>
            <div id="toast-text" style="font-weight:700; color:var(--text-main);">Alguém acabou de acessar a Área VIP</div>
            <div style="font-size:0.7rem; color:var(--primary); font-weight:700;">Clique para ver a oferta em alta &rarr;</div>
        </div>
    </div>

    <!-- BARRA DE MERCADO E COTAÇÕES AO VIVO -->
    <div class="market-ticker">
        <div class="market-items">
            <span><span class="live-dot"></span> <strong>TERMINAL AO VIVO</strong></span>
            {cotacoes_html}
        </div>
        <div style="display:flex; gap:10px; align-items:center; flex-wrap:wrap; font-size:0.74rem;">
            <a href="cotacao-agora.html" style="color:var(--neon); text-decoration:underline;">📊 Cotações</a>
            <a href="futebol.html" style="color:#10b981; text-decoration:underline;">⚽ Brasileirão</a>
            <span>⚡ {data_atualizacao}</span>
        </div>
    </div>

    <header>
        <div class="nav-container">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <a class="logo" onclick="filtrarCategoria('todos', event)">
                    TechNews<span>.PRO</span>
                    <span class="logo-badge">v8.3</span>
                </a>
            </div>
            <ul class="nav-links">
                <li><button onclick="filtrarCategoria('todos', event)" class="active">🔥 Tudo</button></li>
                <li><button onclick="filtrarCategoria('Tecnologia', event)">💻 Tech & IA</button></li>
                <li><button onclick="filtrarCategoria('Finanças', event)">📈 Mercado</button></li>
                <li><button onclick="filtrarCategoria('🏛️ Política', event)">🏛️ Política</button></li>
                <li><button onclick="filtrarCategoria('⭐ Famosos', event)">⭐ Famosos</button></li>
                <li><button onclick="filtrarCategoria('⚽ Esportes', event)">⚽ Esportes</button></li>
                <li><button onclick="filtrarCategoria('Ciência', event)">🚀 Ciência</button></li>
                <li><a href="futebol.html" class="hub-link">🏆 Tabela</a></li>
                <li><a href="inteligencia-artificial.html" class="hub-link">🧠 Hub IA</a></li>
            </ul>
            <div class="header-actions">
                <div class="search-box">
                    <span class="search-icon">🔍</span>
                    <input type="text" id="search-input" placeholder="Buscar notícia..." onkeyup="buscarNoticia()">
                </div>
                <button class="theme-btn" id="theme-toggle-btn" onclick="alternarTema()">🌙</button>
                <a href="{smartlink_url}" target="_blank" rel="noopener noreferrer" class="cta-btn">💎 VIP</a>
            </div>
        </div>
    </header>

    <div class="tags-bar">
        <span style="font-size:0.72rem; font-weight:800; color:var(--primary); text-transform:uppercase; flex-shrink:0;">Clusters SEO:</span>
        <a href="inteligencia-artificial.html" class="tag-pill">#HubIA</a>
        <a href="cotacao-agora.html" class="tag-pill">#Dólar&Bitcoin</a>
        <a href="futebol.html" class="tag-pill">#BrasileirãoSérieA</a>
        <a href="bitcoin.html" class="tag-pill">#RadarBitcoin</a>
        <a href="chatgpt.html" class="tag-pill">#RadarChatGPT</a>
        <a href="startups.html" class="tag-pill">#RadarStartups</a>
        <span class="tag-pill" onclick="filtrarCategoria('🏛️ Política', event)">#Política</span>
        <span class="tag-pill" onclick="filtrarCategoria('⭐ Famosos', event)">#Famosos</span>
        <span class="tag-pill" onclick="filtrarCategoria('⚽ Esportes', event)">#Futebol</span>
        <span class="tag-pill" onclick="filtrarCategoria('todos', event)">🔄 Tudo</span>
    </div>

    <!-- BANNER TOPO ADSTERRA (728x90) COM SCROLL TOUCH PROTEGIDO NO MOBILE -->
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
                <span style="font-size:0.74rem; color:var(--text-muted); font-weight:600;">🔊 Ouça as matérias em áudio</span>
            </h2>
            <div class="feed-grid" id="feed-container"></div>
        </div>

        <aside class="sidebar">
            <!-- WIDGET BRASILEIRÃO SÉRIE A (G4 & Z4) -->
            <div class="widget">
                <div class="widget-title">
                    <span>⚽ Brasileirão Série A</span>
                    <a href="futebol.html" style="font-size:0.74rem; color:var(--neon); text-decoration:underline;">Tabela Completa &rarr;</a>
                </div>
                <div class="table-responsive-wrapper">
                    {widget_futebol_html}
                </div>
            </div>

            <div class="widget">
                <div class="widget-title">🔥 Mais Lidas no Terminal</div>
                <ul class="trending-list">{trending_section}</ul>
            </div>

            <!-- DESTAQUE LATERAL KIWIFY 2 -->
            <div class="widget" style="background: linear-gradient(135deg, rgba(239,68,68,0.16), rgba(15,23,42,0.95)); border-color: rgba(239,68,68,0.45); text-align: center;">
                <span class="badge-source" style="margin-bottom:0.5rem;">🔥 Recomendação PRO</span>
                <h3 style="margin-bottom: 0.5rem; font-size: 1.05rem;">⚡ Destrave Novas Fontes de Renda Digital</h3>
                <p style="font-size: 0.82rem; color: var(--text-muted); margin-bottom: 1rem;">Acesse o sistema passo a passo mais recomendado pelos nossos leitores em 2026.</p>
                <a href="{link_kiwify_2}" target="_blank" rel="noopener noreferrer" class="cta-btn" style="width: 100%; justify-content: center;">Conhecer Método Oficial &rarr;</a>
            </div>

            <!-- CAPTURA DE LEADS SYSTEME.IO -->
            <div class="newsletter-box" id="newsletter">
                <h3>💰 Briefing Matinal VIP</h3>
                <p style="font-size:0.82rem; color:#94a3b8;">Receba os insights de IA, Negócios e Ferramentas Secretas no seu e-mail.</p>
                <form action="{systeme_url}" method="GET" target="_blank">
                    <input type="email" name="email" placeholder="Digite seu melhor e-mail..." required>
                    <button type="submit">Liberar Acesso Gratuito &rarr;</button>
                </form>
            </div>

            <div class="widget" style="text-align: center; padding: 1.2rem;">
                <p style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 0.6rem;">🔗 <strong>Páginas Especiais & Clusters:</strong></p>
                <p style="margin-bottom:6px;"><a href="inteligencia-artificial.html" style="color: var(--neon); font-size: 0.84rem; font-weight: 700; text-decoration: underline;">🧠 Enciclopédia & Hub de IA &rarr;</a></p>
                <p style="margin-bottom:6px;"><a href="cotacao-agora.html" style="color: #10b981; font-size: 0.84rem; font-weight: 700; text-decoration: underline;">📊 Monitor de Cotações Ao Vivo &rarr;</a></p>
                <p style="margin-bottom:6px;"><a href="futebol.html" style="color: #22c55e; font-size: 0.84rem; font-weight: 700; text-decoration: underline;">⚽ Central Brasileirão Série A &rarr;</a></p>
                <p style="margin-bottom:6px;"><a href="bitcoin.html" style="color: #f59e0b; font-size: 0.84rem; font-weight: 700; text-decoration: underline;">₿ Radar Bitcoin & Cripto &rarr;</a></p>
                <p><a href="chatgpt.html" style="color: #3b82f6; font-size: 0.84rem; font-weight: 700; text-decoration: underline;">🤖 Radar ChatGPT & OpenAI &rarr;</a></p>
            </div>

            <!-- BANNER LATERAL ADSTERRA (300x250) -->
            <div style="text-align: center; width: 100%; overflow: hidden;">
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
        <p><strong>TechNews.PRO</strong> &copy; {ano_atual} — Ecossistema Automatizado via Python, Topic Clusters SEO, OpenAI, Telegram, OneSignal & Meta Video API.</p>
        <p style="margin-top: 8px; font-size: 0.76rem; line-height: 1.8;">
            <a href="index.html" style="color:#94a3b8; margin:0 6px;">Início</a> |
            <a href="inteligencia-artificial.html" style="color:#94a3b8; margin:0 6px;">Hub IA</a> |
            <a href="cotacao-agora.html" style="color:#94a3b8; margin:0 6px;">Cotações</a> |
            <a href="futebol.html" style="color:#94a3b8; margin:0 6px;">Futebol</a> |
            <a href="bitcoin.html" style="color:#94a3b8; margin:0 6px;">Bitcoin</a> |
            <a href="chatgpt.html" style="color:#94a3b8; margin:0 6px;">ChatGPT</a> |
            <a href="startups.html" style="color:#94a3b8; margin:0 6px;">Startups</a> |
            <a href="feed.xml" style="color:#94a3b8; margin:0 6px;">RSS Feed</a> |
            <a href="sitemap.xml" style="color:#94a3b8; margin:0 6px;">Sitemap XML</a>
        </p>
    </footer>

    <script>
        const todasNoticias = {noticias_json};
        const ofertasKiwify = [
            { badge: "Destaque Patrocinado", titulo: "🚀 Método IA & Automação Lucrativa", desc: "Aprenda a construir sistemas automáticos na internet e escale resultados todos os dias.", url: "{link_kiwify_1}", cta: "Acessar Treinamento VIP &rarr;" },
            { badge: "Ferramenta Recomendada", titulo: "💎 Escale seus Resultados no Digital", desc: "O guia definitivo para transformar atenção e tecnologia em vendas recorrentes no piloto automático.", url: "{link_kiwify_2}", cta: "Desbloquear Oferta Especial &rarr;" },
            { badge: "Acesso Exclusivo", titulo: "⚡ Domine as Novas Tecnologias de 2026", desc: "Saia na frente de 99% do mercado aplicando estratégias validadas de negócios digitais.", url: "{link_kiwify_3}", cta: "Quero Garantir Minha Vaga &rarr;" }
        ];

        function aplicarTeiaSEO(texto) {
            if (!texto) return "";
            let t = texto;
            t = t.replace(/\\b(inteligência artificial|IA)\\b/i, '<a href="inteligencia-artificial.html" class="seo-internal-link">$1</a>');
            t = t.replace(/\\b(dólar|euro|câmbio)\\b/i, '<a href="cotacao-agora.html" class="seo-internal-link">$1</a>');
            t = t.replace(/\\b(brasileirão|futebol|série a)\\b/i, '<a href="futebol.html" class="seo-internal-link">$1</a>');
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
            btn.innerHTML = novo === 'dark' ? '🌙' : '☀️';
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
                document.getElementById('feed-container').innerHTML = '<div style="grid-column: 1 / -1; padding:2.5rem; text-align:center; color:var(--text-muted); background:var(--card-bg); border-radius:12px; border:1px solid var(--border);">🔍 Nenhuma notícia encontrada para este filtro no momento. Clique em "Tudo" ou aguarde a próxima varredura!</div>';
                return;
            }

            const hero = lista[0];
            const heroIdx = todasNoticias.indexOf(hero);

            document.getElementById('hero-container').innerHTML = `
                <div class="hero-card">
                    <img src="${hero.img}" alt="Destaque" referrerpolicy="no-referrer" onerror="this.src='https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=1200&q=80'">
                    <div class="hero-overlay">
                        <span class="badge-source">🔥 Manchete Principal • ${hero.source}</span>
                        <h1>${hero.title}</h1>
                        <p>${aplicarTeiaSEO(hero.desc)}</p>
                        <div class="hero-actions">
                            <button onclick="abrirReader(${heroIdx})" class="cta-btn">⚡ Síntese Executiva IA</button>
                            <button onclick="falarNoticia(${heroIdx}, event)" class="btn-outline" style="background:rgba(255,255,255,0.08); color:#fff;">🔊 Ouvir</button>
                            <a href="${hero.url}" target="_blank" rel="noopener noreferrer" class="btn-outline" style="background:rgba(255,255,255,0.14); color:#fff;">Fonte Oficial &rarr;</a>
                        </div>
                    </div>
                </div>
            `;

            let feedHtml = '';
            let adCount = 0;
            lista.slice(1, 16).forEach((art, idx) => {
                const globalIdx = todasNoticias.indexOf(art);
                const zapTexto = encodeURIComponent("🚨 Olha essa notícia no TechNews PRO: " + art.title + " - " + window.location.href);
                feedHtml += `
                <article class="news-card">
                    <div class="card-img-wrapper">
                        <span class="card-tag">${art.source}</span>
                        <img src="${art.img}" alt="Capa" referrerpolicy="no-referrer" onerror="this.src='https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80'">
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
                        <p style="font-size:0.86rem; color:var(--text-muted); margin-bottom:1.1rem;">${oferta.desc}</p>
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

        const mensagensToast = [
            "Lucas M. (SP) acabou de desbloquear o Treinamento VIP",
            "Fernanda R. (RJ) acessou a Ferramenta Recomendada de IA",
            "Mais de 140 leitores ativos no Terminal neste momento"
        ];
        let toastIdx = 0;
        function dispararToastCiclo() {
            const toast = document.getElementById('social-proof-toast');
            const txt = document.getElementById('toast-text');
            if (toast && txt) {
                txt.innerText = mensagensToast[toastIdx % mensagensToast.length];
                toastIdx++;
                toast.classList.add('show');
                setTimeout(() => { toast.classList.remove('show'); }, 6000);
            }
        }
        setTimeout(dispararToastCiclo, 4000);
        setInterval(dispararToastCiclo, 28000);

        renderizarLista(todasNoticias);
    </script>

    <!-- SOCIAL BAR FLUTUANTE ADSTERRA -->
    <script data-cfasync="false" src="https://bicea.org/14/7843682dc41b2077e8d78d48efd6360a"></script>
</body>
</html>
"""

# ==============================================================================
# COTAÇÕES EM TEMPO REAL E TEIA DE ARANHA SEO
# ==============================================================================
def obter_dados_cotacoes():
    dados_padrao = {
        "USDBRL": {"nome": "💵 Dólar", "val": "R$ 5,70", "pct": "+0.15%", "classe": "up"},
        "EURBRL": {"nome": "💶 Euro", "val": "R$ 6,18", "pct": "+0.10%", "classe": "up"},
        "BTCBRL": {"nome": "₿ Bitcoin", "val": "R$ 420.000", "pct": "+1.25%", "classe": "up"}
    }
    try:
        url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL"
        r = requests.get(url, timeout=6)
        if r.status_code == 200:
            d = r.json()
            for par, label in [("USDBRL", "💵 Dólar"), ("EURBRL", "💶 Euro"), ("BTCBRL", "₿ Bitcoin")]:
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
        r'(?i)\b(brasileirão|futebol|série a)\b',
        f'<a href="{URL_PORTAL_OFICIAL}futebol.html" style="color:#22c55e; font-weight:700; text-decoration:underline;">\\1</a>',
        novo, count=1
    )
    novo = re.sub(
        r'(?i)\b(bitcoin|criptomoedas|cripto)\b',
        f'<a href="{URL_PORTAL_OFICIAL}bitcoin.html" style="color:#f59e0b; font-weight:700; text-decoration:underline;">\\1</a>',
        novo, count=1
    )
    return novo

# ==============================================================================
# INTEGRAÇÃO API-FUTEBOL (TABELA BRASILEIRÃO SÉRIE A + WIDGET + HUB)
# ==============================================================================
TABELA_BRASILEIRAO_FALLBACK = [
    {"posicao": 1, "time": "Palmeiras", "pontos": 70, "jogos": 34, "vitorias": 21},
    {"posicao": 2, "time": "Flamengo", "pontos": 68, "jogos": 34, "vitorias": 20},
    {"posicao": 3, "time": "Botafogo", "pontos": 67, "jogos": 34, "vitorias": 20},
    {"posicao": 4, "time": "Fortaleza", "pontos": 64, "jogos": 34, "vitorias": 18},
    {"posicao": 5, "time": "Internacional", "pontos": 62, "jogos": 34, "vitorias": 17},
    {"posicao": 6, "time": "São Paulo", "pontos": 59, "jogos": 34, "vitorias": 17},
    {"posicao": 7, "time": "Cruzeiro", "pontos": 52, "jogos": 34, "vitorias": 14},
    {"posicao": 8, "time": "Bahia", "pontos": 50, "jogos": 34, "vitorias": 14},
    {"posicao": 9, "time": "Corinthians", "pontos": 47, "jogos": 34, "vitorias": 12},
    {"posicao": 10, "time": "Vasco da Gama", "pontos": 45, "jogos": 34, "vitorias": 13},
    {"posicao": 17, "time": "Criciúma", "pontos": 38, "jogos": 34, "vitorias": 9},
    {"posicao": 18, "time": "Red Bull Bragantino", "pontos": 37, "jogos": 34, "vitorias": 8},
    {"posicao": 19, "time": "Cuiabá", "pontos": 30, "jogos": 34, "vitorias": 6},
    {"posicao": 20, "time": "Atlético-GO", "pontos": 26, "jogos": 34, "vitorias": 6}
]

def obter_tabela_brasileirao():
    if API_FUTEBOL_KEY:
        try:
            url = "https://api.api-futebol.com.br/v1/campeonatos/10/tabela"
            headers = {"Authorization": f"Bearer {API_FUTEBOL_KEY.strip()}"}
            r = requests.get(url, headers=headers, timeout=8)
            if r.status_code == 200:
                dados = r.json()
                tabela_limpa = []
                for item in dados:
                    pos = item.get("posicao")
                    time_nome = item.get("time", {}).get("nome_popular", "Clube")
                    pts = item.get("pontos", 0)
                    jgs = item.get("jogos", 0)
                    vit = item.get("vitorias", 0)
                    tabela_limpa.append({"posicao": pos, "time": time_nome, "pontos": pts, "jogos": jgs, "vitorias": vit})
                if tabela_limpa:
                    return tabela_limpa
        except Exception as e:
            print(f"Aviso API-Futebol: {e}")
    return TABELA_BRASILEIRAO_FALLBACK

def gerar_widget_futebol_html(tabela):
    g4 = [t for t in tabela if t["posicao"] <= 4][:4]
    z4 = [t for t in tabela if t["posicao"] >= 17][:4]
    linhas = ""
    for t in g4:
        linhas += f'<tr><td class="g4-badge">{t["posicao"]}º</td><td>{t["time"]}</td><td><strong>{t["pontos"]}</strong></td><td>{t["jogos"]}</td></tr>'
    linhas += '<tr><td colspan="4" style="text-align:center; color:#64748b; font-size:0.68rem; padding:4px;">••• Zona de Rebaixamento (Z4) •••</td></tr>'
    for t in z4:
        linhas += f'<tr><td class="z4-badge">{t["posicao"]}º</td><td>{t["time"]}</td><td><strong>{t["pontos"]}</strong></td><td>{t["jogos"]}</td></tr>'

    return f"""
    <table class="tabela-futebol">
        <thead><tr><th>Pos</th><th>Clube</th><th>PTS</th><th>J</th></tr></thead>
        <tbody>{linhas}</tbody>
    </table>
    """

def gerar_pagina_futebol(tabela, todas_noticias, cotacoes_html, data_fmt, ano_fmt):
    linhas_completas = ""
    for t in tabela:
        cor = "#10b981" if t["posicao"] <= 4 else ("#ef4444" if t["posicao"] >= 17 else "#f8fafc")
        linhas_completas += f"""
        <tr style="border-bottom:1px solid rgba(255,255,255,0.06);">
            <td style="padding:11px; font-weight:900; color:{cor};">{t['posicao']}º</td>
            <td style="padding:11px; font-weight:700;">{t['time']}</td>
            <td style="padding:11px; font-weight:900; color:#00f2fe;">{t['pontos']}</td>
            <td style="padding:11px; color:#94a3b8;">{t['jogos']}</td>
            <td style="padding:11px; color:#94a3b8;">{t['vitorias']}</td>
        </tr>
        """

    html_fut = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Tabela atualizada do Brasileirão Série A: Classificação completa, pontuação do G4, Z4 e notícias do futebol brasileiro ao vivo.">
    <meta name="robots" content="max-image-preview:large, index, follow">
    <link rel="canonical" href="{URL_PORTAL_OFICIAL}futebol.html">
    <title>Tabela do Brasileirão Série A Atualizada | G4, Z4 e Jogos | TechNews PRO</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; }}
        body {{ background:#070b14; color:#f8fafc; font-family:'Inter',sans-serif; margin:0; line-height:1.6; overflow-x:hidden; }}
        header {{ background:#0f172a; padding:1rem 4%; border-bottom:1px solid rgba(255,255,255,0.08); display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem; }}
        .container {{ max-width:1200px; margin:2rem auto; padding:0 4%; }}
        .table-wrap {{ width:100%; overflow-x:auto; -webkit-overflow-scrolling:touch; border-radius:14px; border:1px solid rgba(255,255,255,0.08); }}
        table {{ width:100%; min-width:340px; border-collapse:collapse; background:rgba(17,25,40,0.9); font-family:'JetBrains Mono',monospace; font-size:0.86rem; }}
        th {{ background:#03060c; color:#94a3b8; text-align:left; padding:13px 11px; font-size:0.76rem; text-transform:uppercase; }}
        .ad-top {{ width:100%; overflow-x:auto; text-align:center; margin:1.2rem auto; padding:0 2%; }}
        footer {{ background:#03060c; color:#64748b; text-align:center; padding:2.5rem 4%; margin-top:4rem; border-top:1px solid rgba(255,255,255,0.08); }}
    </style>
</head>
<body>
    <header>
        <a href="index.html" style="font-size:1.6rem; font-weight:900; color:#fff; text-decoration:none;">TechNews<span style="color:#ef4444;">.PRO</span></a>
        <div style="display:flex; gap:12px; align-items:center; flex-wrap:wrap;">
            <a href="index.html" style="color:#94a3b8; text-decoration:none; font-weight:700; font-size:0.85rem;">&larr; Voltar ao Portal</a>
            <a href="cotacao-agora.html" style="color:#10b981; text-decoration:none; font-weight:700; font-size:0.85rem;">📊 Cotações</a>
            <a href="{LINK_KIWIFY_1}" target="_blank" style="background:#ef4444; color:#fff; padding:0.5rem 1rem; border-radius:8px; font-weight:800; text-decoration:none; font-size:0.82rem;">💎 Área VIP</a>
        </div>
    </header>

    <div class="ad-top">
        <script>atOptions={{'key':'06959dfe796ac17610a3027d9ede544f','format':'iframe','height':90,'width':728,'params':{{}}}};</script>
        <script src="https://bicea.org/22/06959dfe796ac17610a3027d9ede544f"></script>
    </div>

    <main class="container">
        <span style="background:rgba(16,185,129,0.15); color:#10b981; border:1px solid #10b981; padding:4px 12px; border-radius:20px; font-size:0.72rem; font-weight:800;">⚽ CENTRAL ESPORTIVA OFICIAL</span>
        <h1 style="font-size:clamp(1.5rem, 4vw, 2.3rem); margin:0.8rem 0; font-weight:900;">Classificação do Brasileirão Série A — Tempo Real</h1>
        <p style="color:#94a3b8; margin-bottom:1.8rem; font-size:0.92rem;">Acompanhe a disputa pelo título, vaga na Libertadores (G4) e luta contra o rebaixamento (Z4). Atualizado em: {data_fmt}.</p>
        <div class="table-wrap">
            <table>
                <thead>
                    <tr><th>Pos</th><th>Clube</th><th>PTS</th><th>J</th><th>VIT</th></tr>
                </thead>
                <tbody>{linhas_completas}</tbody>
            </table>
        </div>
    </main>
    <footer>
        <p><strong>TechNews.PRO</strong> &copy; {ano_fmt} — Central de Esportes & Estatísticas.</p>
    </footer>
    <script data-cfasync="false" src="https://bicea.org/14/7843682dc41b2077e8d78d48efd6360a"></script>
</body>
</html>"""
    with open("futebol.html", "w", encoding="utf-8") as f:
        f.write(html_fut)

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
            "2. Em 'resumo': Entregue o 'Time-to-Value' (a resposta direta e o impacto prático) logo na primeira frase e finalize com uma segunda frase analítica."
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
# FÁBRICA DE VÍDEOS 9:16 SPLIT-SCREEN CENTRALIZADO + SONOPLASTIA DINÂMICA (V8.3)
# ==============================================================================
def obter_fonte_segura(tamanho):
    caminhos_candidatos = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "Roboto-Bold.ttf"
    ]
    for c in caminhos_candidatos:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, tamanho)
            except:
                pass
    if not os.path.exists("Roboto-Bold.ttf"):
        try:
            r = requests.get("https://cdnjs.cloudflare.com/ajax/libs/ink/3.1.10/fonts/Roboto/roboto-bold-webfont.ttf", timeout=8)
            if r.status_code == 200:
                with open("Roboto-Bold.ttf", "wb") as f:
                    f.write(r.content)
                return ImageFont.truetype("Roboto-Bold.ttf", tamanho)
        except:
            pass
    return ImageFont.load_default()

def desenhar_texto_centralizado(draw, y, texto, fonte, cor, largura_canvas=1080):
    try:
        bbox = draw.textbbox((0, 0), texto, font=fonte)
        larg_texto = bbox[2] - bbox[0]
    except:
        larg_texto = len(texto) * 24
    x = max(40, (largura_canvas - larg_texto) // 2)
    draw.text((x, y), texto, fill=cor, font=fonte)

def garantir_audio_por_categoria(categoria=""):
    cat_lower = (categoria or "").lower()
    mapa_mp3 = [
        (["política", "politica", "finanças", "financas"], "audio_politica.mp3"),
        (["famosos", "celebridades"], "audio_famosos.mp3"),
        (["futebol", "esporte"], "audio_futebol.mp3"),
        (["tecnologia", "ciência", "ciencia"], "audio_tech.mp3")
    ]
    for chaves, arq_mp3 in mapa_mp3:
        if any(k in cat_lower for k in chaves) and os.path.exists(arq_mp3):
            return arq_mp3
    if os.path.exists("alerta.mp3"):
        return "alerta.mp3"

    caminho_wav = "alerta_plantao.wav"
    taxa_amostragem = 44100
    duracao = 6.5
    total_frames = int(taxa_amostragem * duracao)

    with wave.open(caminho_wav, 'w') as wav_file:
        wav_file.setparams((1, 2, taxa_amostragem, total_frames, 'NONE', 'not compressed'))
        for i in range(total_frames):
            t = i / taxa_amostragem
            if "política" in cat_lower or "finanças" in cat_lower:
                if t < 0.35 or (0.45 <= t < 0.8) or (0.9 <= t < 1.35):
                    freq = 880.0 if int(t * 12) % 2 == 0 else 659.25
                    val = int(15500 * math.sin(2 * math.pi * freq * t))
                else:
                    pulso = 0.55 + 0.45 * math.sin(2 * math.pi * 2.5 * t)
                    val = int(10500 * pulso * math.sin(2 * math.pi * 98.0 * t))
            elif "famosos" in cat_lower:
                if t < 0.9:
                    freq = 320.0 + (480.0 * (t / 0.9))
                    val = int(14500 * math.sin(2 * math.pi * freq * t))
                else:
                    env = 0.5 + 0.5 * math.sin(2 * math.pi * 3.5 * t)
                    val = int(11000 * env * (0.6 * math.sin(2 * math.pi * 523.25 * t) + 0.4 * math.sin(2 * math.pi * 659.25 * t)))
            elif "futebol" in cat_lower or "esporte" in cat_lower:
                if t < 0.75:
                    freq = 1320.0 + 140.0 * math.sin(2 * math.pi * 28.0 * t)
                    val = int(15000 * math.sin(2 * math.pi * freq * t))
                else:
                    batida = 1.0 if (int(t * 4.5) % 2 == 0) else 0.35
                    val = int(12500 * batida * math.sin(2 * math.pi * 146.83 * t))
            else:
                notas_cyber = [523.25, 659.25, 783.99, 1046.50]
                if t < 1.6:
                    freq = notas_cyber[int(t * 10) % 4]
                    val = int(13500 * math.sin(2 * math.pi * freq * t))
                else:
                    pulso = 0.6 + 0.4 * math.sin(2 * math.pi * 4.0 * t)
                    val = int(10000 * pulso * (0.7 * math.sin(2 * math.pi * 130.81 * t) + 0.3 * math.sin(2 * math.pi * 261.63 * t)))

            wav_file.writeframesraw(struct.pack('<h', max(-32767, min(32767, val))))
    return caminho_wav

def limpar_emojis_para_pillow(texto):
    return re.sub(r'[^\x00-\x7F\xC0-\xFF\u2000-\u206F]+', '', texto).strip()

def obter_config_visual_editoria(categoria=""):
    c = (categoria or "").lower()
    if "política" in c:
        return "PLANTÃO POLÍTICA", (220, 38, 38, 255)
    elif "famosos" in c:
        return "GIRO DOS FAMOSOS", (217, 70, 239, 255)
    elif "finanças" in c:
        return "MERCADO & ECONOMIA", (16, 185, 129, 255)
    elif "ciência" in c:
        return "CIÊNCIA & ESPAÇO", (59, 130, 246, 255)
    elif "futebol" in c or "esporte" in c:
        return "PLANTÃO ESPORTIVO", (34, 197, 94, 255)
    return "RADAR TECH & IA", (239, 68, 68, 255)

def gerar_video_reel_noticia(noticia, caminho_saida="noticia_urgente.mp4"):
    if not PIL_DISPONIVEL or not MOVIEPY_DISPONIVEL:
        print("Fábrica de Vídeos: Pillow ou MoviePy não disponíveis. Pulando geração de vídeo.")
        return None
    try:
        largura, altura = 1080, 1920
        altura_metade = 960
        canvas = Image.new("RGB", (largura, altura), (7, 11, 20))

        # ------------------------------------------------------------------
        # 1. METADE SUPERIOR (0 a 960px): IMAGEM 100% NÍTIDA COM BYPASS HOTLINK
        # ------------------------------------------------------------------
        img_url = noticia.get("img", "")
        img_topo = None
        headers_img = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
            "Referer": "https://www.google.com/"
        }
        if img_url and img_url.startswith("http"):
            try:
                r = requests.get(img_url, headers=headers_img, timeout=10)
                if r.status_code == 200:
                    img_topo = Image.open(io.BytesIO(r.content)).convert("RGB")
            except:
                pass

        if img_topo is None:
            img_topo = Image.new("RGB", (largura, altura_metade), (20, 30, 55))
        else:
            prop_alvo = largura / altura_metade
            prop_img = img_topo.width / img_topo.height
            if prop_img > prop_alvo:
                nova_alt = altura_metade
                nova_larg = int(altura_metade * prop_img)
            else:
                nova_larg = largura
                nova_alt = int(largura / prop_img)
            resampler = getattr(Image, "Resampling", Image).LANCZOS
            img_topo = img_topo.resize((nova_larg, nova_alt), resampler)
            esq = (nova_larg - largura) // 2
            topo = (nova_alt - altura_metade) // 2
            img_topo = img_topo.crop((esq, topo, esq + largura, topo + altura_metade))
            img_topo = ImageEnhance.Contrast(img_topo).enhance(1.06)

        canvas.paste(img_topo, (0, 0))

        # ------------------------------------------------------------------
        # 2. METADE INFERIOR (960px a 1920px) + TARJA CENTRAL CENTRALIZADA
        # ------------------------------------------------------------------
        draw = ImageDraw.Draw(canvas, "RGBA")
        draw.rectangle([(0, altura_metade), (largura, altura)], fill=(7, 11, 20, 255))

        categoria_not = noticia.get("categoria", "Tecnologia")
        texto_tarja, cor_tarja = obter_config_visual_editoria(categoria_not)

        draw.rectangle([(0, 954), (largura, 966)], fill=cor_tarja)
        draw.rectangle([(80, 916), (largura - 80, 1008)], fill=cor_tarja)

        fonte_tarja = obter_fonte_segura(40)
        fonte_titulo = obter_fonte_segura(54)
        fonte_fonte = obter_fonte_segura(28)
        fonte_cta = obter_fonte_segura(34)

        desenhar_texto_centralizado(draw, 938, f"• {texto_tarja} | TECHNEWS.PRO •", fonte_tarja, (255, 255, 255, 255), largura)

        fonte_org = limpar_emojis_para_pillow(noticia.get("source", "Portal Oficial")).upper()
        desenhar_texto_centralizado(draw, 1036, f"FONTE: {fonte_org}  •  COBERTURA EM TEMPO REAL", fonte_fonte, (148, 163, 184, 255), largura)

        titulo_limpo = limpar_emojis_para_pillow(noticia.get("title", "Notícia Urgente em Tempo Real")).upper()
        linhas = textwrap.wrap(titulo_limpo, width=23)[:6]
        y_texto = 1105
        for idx_l, linha in enumerate(linhas):
            cor_linha = (255, 215, 0, 255) if idx_l < 2 else (248, 250, 252, 255)
            desenhar_texto_centralizado(draw, y_texto, linha, fonte_titulo, cor_linha, largura)
            y_texto += 82

        # Botão de Rodapé Fixo Centralizado (1685px a 1800px)
        draw.rectangle([(80, 1685), (largura - 80, 1800)], fill=(16, 185, 129, 255))
        desenhar_texto_centralizado(draw, 1722, "LEIA COMPLETO NO LINK DOS COMENTÁRIOS", fonte_cta, (255, 255, 255, 255), largura)

        caminho_frame = "frame_reel_temp.jpg"
        canvas.save(caminho_frame, quality=94)

        caminho_audio = garantir_audio_por_categoria(categoria_not)
        audio_clip = AudioFileClip(caminho_audio)
        duracao_final = min(7.0, audio_clip.duration) if audio_clip.duration else 6.5
        audio_clip = audio_clip.subclip(0, duracao_final)

        video_clip = ImageClip(caminho_frame).set_duration(duracao_final).set_audio(audio_clip)
        video_clip.write_videofile(
            caminho_saida,
            fps=24,
            codec="libx264",
            audio_codec="aac",
            preset="ultrafast",
            ffmpeg_params=["-pix_fmt", "yuv420p"],
            logger=None
        )
        video_clip.close()
        audio_clip.close()
        if os.path.exists(caminho_saida):
            print(f"Fábrica de Vídeos: ✅ Reel Split-Screen 9:16 '{caminho_saida}' renderizado com sucesso!")
            return caminho_saida
    except Exception as e:
        print(f"Fábrica de Vídeos Erro: {e}")
    return None

def limpar_arquivos_temporarios_midia():
    for arq in ["noticia_urgente.mp4", "frame_reel_temp.jpg", "alerta_plantao.wav"]:
        if os.path.exists(arq):
            try:
                os.remove(arq)
            except:
                pass

# ==============================================================================
# AGENTES SOCIAIS: ONESIGNAL PUSH, TELEGRAM E FACEBOOK (VÍDEO + LINK FALLBACK)
# ==============================================================================
def disparar_onesignal_push(noticia):
    if not ONESIGNAL_APP_ID or not ONESIGNAL_REST_KEY or not noticia:
        print("Agente OneSignal: Chaves ausentes nos Secrets. Pulando.")
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
    except Exception as e:
        print(f"Agente OneSignal Erro: {e}")
    return False

def publicar_no_telegram(noticia):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID or not noticia:
        print("Agente Telegram: Chaves ausentes nos Secrets. Pulando.")
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
            print("Agente Telegram: ✅ Alerta Dark Social enviado com sucesso!")
            return True
    except Exception as e:
        print(f"Agente Telegram Erro: {e}")
    return False

def gerar_copy_persuasiva_meta(noticia):
    titulo = noticia.get("title", "")
    resumo = noticia.get("desc", "")
    cta_padrao = (
        f"\n\n👉 ACESSE A MATÉRIA COMPLETA AQUI:\n"
        f"🔗 {URL_PORTAL_OFICIAL}\n\n"
        f"🛑 O detalhe mais importante acabou de ser atualizado no nosso Terminal Oficial!\n\n"
        f"👇 Clique no link acima ou comente 'LINK', 'QUERO' ou 'VIP' que te envio o acesso + uma Ferramenta Secreta direto no seu Direct! 🚀"
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
            f"4. FECHAMENTO: Convide a clicar no link ({URL_PORTAL_OFICIAL}) e peça também para comentarem 'LINK' ou 'VIP' para receberem uma ferramenta secreta no Direct."
        )
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "Você é um copywriter especialista em tráfego viral e retenção no Facebook."},
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
    return (META_PAGE_ID if META_PAGE_ID else "me"), token_inicial

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
        historico = historico[-25:]
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
    alvos_tentativa = [alvo_id]
    if "me" not in alvos_tentativa:
        alvos_tentativa.append("me")

    # 1. TENTA PUBLICAR COMO VÍDEO CURTO / REEL SPLIT-SCREEN 9:16
    caminho_video = gerar_video_reel_noticia(noticia)
    if caminho_video and os.path.exists(caminho_video):
        for alvo in alvos_tentativa:
            try:
                url_video = f"https://graph-video.facebook.com/v20.0/{alvo}/videos"
                with open(caminho_video, "rb") as f_vid:
                    files = {"source": ("noticia_urgente.mp4", f_vid, "video/mp4")}
                    data_vid = {
                        "title": noticia.get("title", "Plantão TechNews PRO")[:95],
                        "description": mensagem,
                        "access_token": token_pagina
                    }
                    r_vid = requests.post(url_video, data=data_vid, files=files, timeout=65)
                if r_vid.status_code == 200:
                    vid_id = r_vid.json().get("id")
                    salvar_memoria_meta(noticia.get("title", ""))
                    print(f"Agente Meta: ✅ VÍDEO SPLIT-SCREEN 9:16 publicado com sucesso via '{alvo}'! ID: {vid_id}")
                    try:
                        requests.post(
                            f"https://graph.facebook.com/v20.0/{vid_id}/comments",
                            data={"message": f"📖 Leia a matéria completa e veja os detalhes aqui: {URL_PORTAL_OFICIAL}", "access_token": token_pagina},
                            timeout=10
                        )
                    except:
                        pass
                    limpar_arquivos_temporarios_midia()
                    return True
                else:
                    print(f"Aviso Upload Vídeo Meta ({r_vid.status_code}): {r_vid.text}")
            except Exception as e:
                print(f"Erro tentativa de vídeo Meta: {e}")

    limpar_arquivos_temporarios_midia()

    # 2. FALLBACK AUTOMÁTICO: CARD DE LINK CLICÁVEL OU FOTO SE O VÍDEO FALHAR
    stamp = datetime.now().strftime("%Y%m%d%H%M")
    link_com_cache_buster = f"{URL_PORTAL_OFICIAL}?v={stamp}"

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

    img_url = noticia.get("img", "")
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
# INGESTÃO HÍBRIDA: RSS MASSA (POLÍTICA/FAMOSOS/ESPORTES) + NEWSDATA.IO + APIS
# ==============================================================================
PALAVRAS_BLOQUEADAS = [
    "pornô", "porno", "sexo explícito", "onlyfans", "acompanhantes", "cassino ilegal",
    "vinagre", "limpar janela", "faxina caseira", "horóscopo do dia"
]

def noticia_segura_adsterra(titulo, desc=""):
    texto = f"{titulo} {desc}".lower()
    return not any(b in texto for b in PALAVRAS_BLOQUEADAS)

def classificar_noticia(titulo, categoria_padrao="Tecnologia"):
    t = titulo.lower()
    if any(k in t for k in ["lula", "bolsonaro", "stf", "senado", "câmara", "congresso", "ministro", "governo", "eleição", "prefeito", "deputado", "pec ", "planalto"]):
        return "🏛️ Política"
    elif any(k in t for k in ["famoso", "celebridade", "bbb", "atriz", "ator", "cantor", "influenciador", "separação", "namoro", "fofoca", "reality", "virginia"]):
        return "⭐ Famosos"
    elif any(k in t for k in ["futebol", "brasileirão", "flamengo", "palmeiras", "corinthians", "são paulo", "botafogo", "vasco", "grêmio", "libertadores", "seleção", "gol "]):
        return "⚽ Esportes"
    elif any(k in t for k in ["finança", "banco", "mercado", "ação", "investimento", "startup", "economia", "negócio", "dólar", "cripto", "bitcoin", "ibge", "cnpj", "receita federal", "imposto", "pib"]):
        return "Finanças"
    elif any(k in t for k in ["espaço", "nasa", "satélite", "ciência", "física", "astronomia", "foguete", "órbita"]):
        return "Ciência"
    return categoria_padrao

def limpar_html_rss(texto_bruto):
    if not texto_bruto:
        return ""
    sem_tags = re.sub(r'<[^>]+>', ' ', texto_bruto)
    limpo = html.unescape(sem_tags)
    return re.sub(r'\s+', ' ', limpo).strip()[:240]

def extrair_imagem_item_rss(item_xml, texto_bruto_html, fallback_img):
    if item_xml is not None:
        for elem in item_xml.iter():
            tag_l = elem.tag.lower()
            if "enclosure" in tag_l or "content" in tag_l or "thumbnail" in tag_l:
                url_cand = elem.attrib.get("url") or elem.attrib.get("href")
                if url_cand and url_cand.startswith("http") and any(ext in url_cand.lower() for ext in [".jpg", ".jpeg", ".png", ".webp"]):
                    return url_cand
    m = re.search(r'<img[^>]+src=["\'](https?://[^"\']+)["\']', texto_bruto_html or "", re.IGNORECASE)
    if m:
        return m.group(1)
    return fallback_img

def fetch_rss_massa():
    feeds = [
        {
            "url": "https://www.metropoles.com/brasil/politica-brasil/feed",
            "source": "Metrópoles Política",
            "cat": "🏛️ Política",
            "fallback_img": "https://images.unsplash.com/photo-1541872703-74c5e44368f9?auto=format&fit=crop&w=1200&q=85"
        },
        {
            "url": "https://www.metropoles.com/colunas/leo-dias/feed",
            "source": "Coluna Famosos",
            "cat": "⭐ Famosos",
            "fallback_img": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=1200&q=85"
        },
        {
            "url": "https://rss.uol.com.br/feed/splash.xml",
            "source": "UOL Splash",
            "cat": "⭐ Famosos",
            "fallback_img": "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?auto=format&fit=crop&w=1200&q=85"
        },
        {
            "url": "https://www.gazetaesportiva.com/feed/",
            "source": "Gazeta Esportiva",
            "cat": "⚽ Esportes",
            "fallback_img": "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?auto=format&fit=crop&w=1200&q=85"
        }
    ]
    noticias = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0"}
    for f_cfg in feeds:
        try:
            r = requests.get(f_cfg["url"], headers=headers, timeout=8)
            if r.status_code == 200:
                conteudo_xml = r.content.strip()
                root = ET.fromstring(conteudo_xml)
                for item in root.findall(".//item")[:5]:
                    tit_el = item.find("title")
                    link_el = item.find("link")
                    desc_el = item.find("description")
                    titulo = (tit_el.text or "").strip() if tit_el is not None else ""
                    link = (link_el.text or "#").strip() if link_el is not None else "#"
                    desc_html = (desc_el.text or "") if desc_el is not None else ""
                    for child in item:
                        if "encoded" in child.tag.lower() and child.text:
                            desc_html += " " + child.text

                    desc_limpa = limpar_html_rss(desc_html) or "Confira todos os bastidores e detalhes atualizados na matéria completa."
                    if titulo and noticia_segura_adsterra(titulo, desc_limpa):
                        img_url = extrair_imagem_item_rss(item, desc_html, f_cfg["fallback_img"])
                        noticias.append({
                            "title": titulo,
                            "desc": desc_limpa,
                            "img": img_url,
                            "url": link,
                            "source": f_cfg["source"],
                            "date": "Hoje",
                            "categoria": f_cfg["cat"]
                        })
        except Exception as e:
            print(f"Aviso RSS ({f_cfg['source']}): {e}")
    return noticias

def fetch_newsdata_rotativo():
    noticias = []
    if not NEWSDATA_API_KEY:
        return noticias
    termos_quentes = [
        "inteligência artificial", "reforma tributária", "bitcoin", "stf", "brasileirão", "famosos"
    ]
    indice_ciclo = (datetime.now().hour // 6) % len(termos_quentes)
    termo_atual = termos_quentes[indice_ciclo]
    try:
        url = "https://newsdata.io/api/1/news"
        params = {
            "apikey": NEWSDATA_API_KEY.strip(),
            "country": "br",
            "language": "pt",
            "q": termo_atual
        }
        r = requests.get(url, params=params, timeout=8)
        if r.status_code == 200:
            for item in r.json().get("results", [])[:6]:
                titulo = item.get("title") or ""
                desc = item.get("description") or "Leia a cobertura completa e os desdobramentos no portal."
                if titulo and noticia_segura_adsterra(titulo, desc):
                    noticias.append({
                        "title": titulo,
                        "desc": limpar_html_rss(desc),
                        "img": item.get("image_url") or "https://images.unsplash.com/photo-1504711434969-e33886168f5c?auto=format&fit=crop&w=1200&q=85",
                        "url": item.get("link", "#"),
                        "source": item.get("source_id", "Radar Brasil").upper(),
                        "date": (item.get("pubDate") or "Hoje")[:10],
                        "categoria": classificar_noticia(titulo)
                    })
    except Exception as e:
        print(f"Aviso NewsData.io: {e}")
    return noticias

def fetch_ibge_noticias():
    noticias = []
    try:
        r = requests.get("https://servicodados.ibge.gov.br/api/v3/noticias/?qtd=5", timeout=8)
        if r.status_code == 200:
            for item in r.json().get("items", []):
                titulo = item.get("titulo", "")
                desc = item.get("introducao", "Confira os dados completos divulgados pelo portal oficial.")
                if not noticia_segura_adsterra(titulo, desc):
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
                    "date": item.get("data_publicacao", "Hoje")[:10], "categoria": classificar_noticia(titulo, "Finanças")
                })
    except:
        pass
    return noticias

def fetch_devto_pt():
    noticias = []
    try:
        r = requests.get("https://dev.to/api/articles?tag=portuguese&per_page=6", headers={'User-Agent': 'Mozilla/5.0'}, timeout=8)
        if r.status_code == 200:
            for item in r.json():
                titulo = item.get("title", "")
                desc = item.get("description") or "Artigo técnico sobre tecnologia e desenvolvimento."
                if not noticia_segura_adsterra(titulo, desc):
                    continue
                noticias.append({
                    "title": titulo, "desc": desc,
                    "img": item.get("cover_image") or item.get("social_image") or "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=85",
                    "url": item.get("url", "#"), "source": "Dev.to Brasil",
                    "date": item.get("readable_publish_date", "Recente"), "categoria": "Tecnologia"
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
        query = '("inteligencia artificial" OR tecnologia OR politica OR economia OR bitcoin OR startups OR famosos)'
        url = f"https://newsapi.org/v2/everything?q={query}&language=pt&sortBy=publishedAt&pageSize=10&apiKey={NEWS_API_KEY}"
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=8)
        if r.status_code == 200:
            for item in r.json().get("articles", []):
                titulo = item.get("title") or ""
                desc = item.get("description") or "Clique para ler a matéria completa na fonte oficial."
                if titulo and titulo != "[Removed]" and noticia_segura_adsterra(titulo, desc):
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
        "title": "Bastidores de Brasília: Novas medidas econômicas movimentam o Congresso e o mercado financeiro",
        "desc": "Parlamentares debatem pacote fiscal e impactos diretos nas taxas de juros e investimentos no país.",
        "img": "https://images.unsplash.com/photo-1541872703-74c5e44368f9?auto=format&fit=crop&w=1200&q=85",
        "url": "https://www.metropoles.com", "source": "Política Nacional", "date": "Hoje", "categoria": "🏛️ Política"
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
  <title>TechNews PRO | Terminal de Inteligência, IA, Esportes e Mercado</title>
  <link>{URL_PORTAL_OFICIAL}</link>
  <description>Notícias em tempo real sobre Inteligência Artificial, Tecnologia, Política, Famosos, Futebol e Finanças.</description>
  <language>pt-BR</language>
"""
    for n in noticias[:20]:
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
            <img src="{art['img']}" alt="{html.escape(art['title'])}" referrerpolicy="no-referrer" style="width:100%; height:190px; object-fit:cover;" onerror="this.src='https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=1200&q=85'">
            <div style="padding:1.3rem; display:flex; flex-direction:column; flex-grow:1;">
                <span style="font-size:0.72rem; color:#ef4444; font-weight:800; text-transform:uppercase;">{art['source']} • {art['date']}</span>
                <h3 style="font-size:1.1rem; margin:0.5rem 0 0.8rem 0; color:#f8fafc;">{art['title']}</h3>
                <p style="font-size:0.86rem; color:#94a3b8; margin-bottom:1.2rem; flex-grow:1;">{aplicar_teia_seo_estatico(art['desc'])}</p>
                <a href="{art['url']}" target="_blank" rel="noopener noreferrer" style="background:#ef4444; color:#fff; text-align:center; padding:0.65rem; border-radius:8px; font-weight:700; font-size:0.82rem; text-decoration:none;">Ler Relatório Completo &rarr;</a>
            </div>
        </article>
        """

    html_hub = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="referrer" content="no-referrer">
    <meta name="description" content="Hub Oficial de Inteligência Artificial: Guia definitivo, ferramentas generativas, automação e notícias em tempo real sobre IA.">
    <meta name="robots" content="max-image-preview:large, index, follow">
    <link rel="canonical" href="{URL_PORTAL_OFICIAL}inteligencia-artificial.html">
    <title>Inteligência Artificial (Hub Oficial) | Guia, Ferramentas & Notícias | TechNews PRO</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; }}
        body {{ background:#070b14; color:#f8fafc; font-family:'Inter',sans-serif; margin:0; line-height:1.65; overflow-x:hidden; }}
        .ticker {{ background:#03060c; padding:0.5rem 4%; font-size:0.78rem; font-family:'JetBrains Mono',monospace; border-bottom:1px solid rgba(255,255,255,0.08); display:flex; justify-content:space-between; flex-wrap:wrap; gap:8px; }}
        .up {{ color:#10b981; font-weight:700; }} .down {{ color:#ef4444; font-weight:700; }}
        header {{ background:rgba(15,23,42,0.85); backdrop-filter:blur(12px); padding:1rem 4%; border-bottom:1px solid rgba(255,255,255,0.08); display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem; }}
        .container {{ max-width:1360px; margin:2rem auto; padding:0 4%; }}
        .pillar-box {{ background:linear-gradient(145deg, rgba(59,130,246,0.14), rgba(15,23,42,0.92)); border:1px solid rgba(59,130,246,0.4); border-radius:16px; padding:clamp(1.3rem, 4vw, 2.5rem); margin-bottom:2.2rem; }}
        .grid {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(280px, 1fr)); gap:1.5rem; }}
        .ad-top {{ width:100%; overflow-x:auto; text-align:center; margin:1.2rem auto; padding:0 2%; }}
        footer {{ background:#03060c; color:#64748b; text-align:center; padding:2.5rem 4%; margin-top:4rem; border-top:1px solid rgba(255,255,255,0.08); }}
    </style>
</head>
<body>
    <div class="ticker">
        <div style="overflow-x:auto; white-space:nowrap; max-width:100%;">{cotacoes_html}</div>
        <div>⚡ Atualizado: {data_fmt}</div>
    </div>
    <header>
        <a href="index.html" style="font-size:1.6rem; font-weight:900; color:#fff; text-decoration:none;">TechNews<span style="color:#ef4444;">.PRO</span></a>
        <div style="display:flex; gap:12px; align-items:center; flex-wrap:wrap;">
            <a href="index.html" style="color:#94a3b8; text-decoration:none; font-weight:700; font-size:0.85rem;">&larr; Radar Principal</a>
            <a href="cotacao-agora.html" style="color:#10b981; text-decoration:none; font-weight:700; font-size:0.85rem;">📊 Cotações</a>
            <a href="{LINK_KIWIFY_1}" target="_blank" style="background:#ef4444; color:#fff; padding:0.5rem 1rem; border-radius:8px; font-weight:800; text-decoration:none; font-size:0.82rem;">🚀 Treinamento VIP</a>
        </div>
    </header>

    <div class="ad-top">
        <script>atOptions={{'key':'06959dfe796ac17610a3027d9ede544f','format':'iframe','height':90,'width':728,'params':{{}}}};</script>
        <script src="https://bicea.org/22/06959dfe796ac17610a3027d9ede544f"></script>
    </div>

    <main class="container">
        <section class="pillar-box">
            <span style="background:#3b82f6; color:#fff; padding:4px 12px; border-radius:20px; font-size:0.7rem; font-weight:900; text-transform:uppercase;">Topic Cluster • Enciclopédia & Hub Oficial</span>
            <h1 style="font-size:clamp(1.5rem, 4vw, 2.3rem); margin:0.8rem 0; font-weight:900;">Inteligência Artificial em 2026: O Guia Central de Automação e Disrupção</h1>
            <p style="color:#cbd5e1; font-size:0.95rem; margin-bottom:1rem;">A <strong>Inteligência Artificial (IA)</strong> deixou de ser uma promessa futurista para se tornar a infraestrutura central da economia global. De Modelos de Linguagem de Grande Escala (LLMs) a agentes autônomos capazes de programar, negociar ativos no <a href="cotacao-agora.html" style="color:#00f2fe;">mercado financeiro</a> e operar negócios inteiros na nuvem, dominar a IA é hoje o maior diferencial competitivo.</p>
            <div style="display:flex; gap:10px; flex-wrap:wrap; margin-top:1.3rem;">
                <a href="{LINK_KIWIFY_3}" target="_blank" style="background:#ef4444; color:#fff; padding:0.7rem 1.2rem; border-radius:8px; font-weight:800; text-decoration:none; font-size:0.86rem;">⚡ Desbloquear Método de Automação com IA &rarr;</a>
                <a href="{SMARTLINK_ADSTERRA}" target="_blank" style="background:rgba(255,255,255,0.08); color:#fff; padding:0.7rem 1.2rem; border-radius:8px; font-weight:700; text-decoration:none; font-size:0.86rem;">💎 Acessar Ferramentas Recomendadas</a>
            </div>
        </section>

        <h2 style="font-size:1.3rem; margin-bottom:1.4rem; border-left:4px solid #ef4444; padding-left:12px;">Últimas Notícias e Descobertas de Inteligência Artificial</h2>
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
        * {{ box-sizing: border-box; }}
        body {{ background:#070b14; color:#f8fafc; font-family:'Inter',sans-serif; margin:0; line-height:1.6; overflow-x:hidden; }}
        header {{ background:rgba(15,23,42,0.9); padding:1rem 4%; border-bottom:1px solid rgba(255,255,255,0.08); display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem; }}
        .container {{ max-width:1200px; margin:2rem auto; padding:0 4%; }}
        .cards {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(260px, 1fr)); gap:1.5rem; margin:2rem 0; }}
        .card {{ background:linear-gradient(145deg, #111827, #03060c); border:1px solid rgba(255,255,255,0.1); border-radius:16px; padding:1.8rem; text-align:center; box-shadow:0 15px 30px rgba(0,0,0,0.4); }}
        .price {{ font-size:clamp(1.8rem, 5vw, 2.4rem); font-weight:900; font-family:'JetBrains Mono',monospace; margin:0.7rem 0; }}
        .up {{ color:#10b981; }} .down {{ color:#ef4444; }}
        .cite-box {{ background:rgba(17,25,40,0.9); border:1px dashed rgba(0,242,254,0.4); border-radius:14px; padding:1.5rem; margin-top:2rem; text-align:center; }}
        code {{ background:#03060c; color:#00f2fe; padding:8px 12px; border-radius:6px; display:inline-block; margin:10px 0; font-family:'JetBrains Mono',monospace; font-size:0.78rem; word-break:break-all; max-width:100%; }}
        .ad-top {{ width:100%; overflow-x:auto; text-align:center; margin:1.2rem auto; padding:0 2%; }}
        footer {{ background:#03060c; color:#64748b; text-align:center; padding:2.5rem 4%; margin-top:4rem; border-top:1px solid rgba(255,255,255,0.08); }}
    </style>
</head>
<body>
    <header>
        <a href="index.html" style="font-size:1.6rem; font-weight:900; color:#fff; text-decoration:none;">TechNews<span style="color:#ef4444;">.PRO</span></a>
        <div style="display:flex; gap:12px; align-items:center; flex-wrap:wrap;">
            <a href="index.html" style="color:#94a3b8; text-decoration:none; font-weight:700; font-size:0.85rem;">&larr; Portal</a>
            <a href="inteligencia-artificial.html" style="color:#00f2fe; text-decoration:none; font-weight:700; font-size:0.85rem;">🧠 Hub IA</a>
            <a href="{LINK_KIWIFY_2}" target="_blank" style="background:#ef4444; color:#fff; padding:0.5rem 1rem; border-radius:8px; font-weight:800; text-decoration:none; font-size:0.82rem;">📈 Método VIP</a>
        </div>
    </header>

    <div class="ad-top">
        <script>atOptions={{'key':'06959dfe796ac17610a3027d9ede544f','format':'iframe','height':90,'width':728,'params':{{}}}};</script>
        <script src="https://bicea.org/22/06959dfe796ac17610a3027d9ede544f"></script>
    </div>

    <main class="container">
        <div style="text-align:center; max-width:780px; margin:0 auto;">
            <span style="background:rgba(16,185,129,0.15); color:#10b981; border:1px solid #10b981; padding:4px 12px; border-radius:20px; font-size:0.72rem; font-weight:800;">🟢 TERMINAL FINANCEIRO EM TEMPO REAL</span>
            <h1 style="font-size:clamp(1.6rem, 4vw, 2.5rem); margin:0.9rem 0 0.5rem 0; font-weight:900;">Cotação Hoje: Dólar, Euro e Bitcoin Ao Vivo</h1>
            <p style="color:#94a3b8; font-size:0.94rem;">Painel minimalista de consulta rápida sincronizado via API oficial de câmbio e criptoativos. Última aferição: <strong>{data_fmt}</strong>.</p>
        </div>

        <div class="cards">
            <div class="card">
                <div style="font-size:0.88rem; color:#94a3b8; font-weight:700;">{usd['nome']} (USD/BRL)</div>
                <div class="price">{usd['val']}</div>
                <div class="{usd['classe']}" style="font-weight:800;">Variação 24h: {usd['pct']}</div>
            </div>
            <div class="card">
                <div style="font-size:0.88rem; color:#94a3b8; font-weight:700;">{eur['nome']} (EUR/BRL)</div>
                <div class="price">{eur['val']}</div>
                <div class="{eur['classe']}" style="font-weight:800;">Variação 24h: {eur['pct']}</div>
            </div>
            <div class="card">
                <div style="font-size:0.88rem; color:#94a3b8; font-weight:700;">{btc['nome']} (BTC/BRL)</div>
                <div class="price">{btc['val']}</div>
                <div class="{btc['classe']}" style="font-weight:800;">Variação 24h: {btc['pct']}</div>
            </div>
        </div>

        <div class="cite-box">
            <h3 style="margin-bottom:0.4rem; font-size:1.05rem;">🔗 Ferramenta Pública para Jornalistas, Pesquisadores e Blogs</h3>
            <p style="color:#94a3b8; font-size:0.85rem;">Utilize os dados deste painel em seus artigos ou relatórios incorporando o código de atribuição de fonte abaixo:</p>
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
                <img src="{art['img']}" alt="{html.escape(art['title'])}" referrerpolicy="no-referrer" style="width:100%; height:185px; object-fit:cover;" onerror="this.src='https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=85'">
                <div style="padding:1.3rem; display:flex; flex-direction:column; flex-grow:1;">
                    <span style="font-size:0.72rem; color:#ef4444; font-weight:800;">{art['source']} • {art['date']}</span>
                    <h3 style="font-size:1.08rem; margin:0.5rem 0 0.8rem 0; color:#f8fafc;">{art['title']}</h3>
                    <p style="font-size:0.85rem; color:#94a3b8; margin-bottom:1.1rem; flex-grow:1;">{aplicar_teia_seo_estatico(art['desc'])}</p>
                    <a href="{art['url']}" target="_blank" rel="noopener noreferrer" style="background:#ef4444; color:#fff; text-align:center; padding:0.65rem; border-radius:8px; font-weight:700; font-size:0.82rem; text-decoration:none;">Ler Matéria Completa &rarr;</a>
                </div>
            </article>
            """

        html_cluster = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="referrer" content="no-referrer">
    <meta name="description" content="{cfg['desc']}">
    <meta name="robots" content="max-image-preview:large, index, follow">
    <link rel="canonical" href="{URL_PORTAL_OFICIAL}{slug}.html">
    <title>{cfg['titulo']} | TechNews PRO</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; }}
        body {{ background:#070b14; color:#f8fafc; font-family:'Inter',sans-serif; margin:0; line-height:1.6; overflow-x:hidden; }}
        header {{ background:#0f172a; padding:1rem 4%; border-bottom:1px solid rgba(255,255,255,0.08); display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem; }}
        .container {{ max-width:1360px; margin:2rem auto; padding:0 4%; }}
        .grid {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(280px, 1fr)); gap:1.5rem; }}
        .ad-top {{ width:100%; overflow-x:auto; text-align:center; margin:1.2rem auto; padding:0 2%; }}
        footer {{ background:#03060c; color:#64748b; text-align:center; padding:2.5rem 4%; margin-top:4rem; border-top:1px solid rgba(255,255,255,0.08); }}
    </style>
</head>
<body>
    <header>
        <a href="index.html" style="font-size:1.6rem; font-weight:900; color:#fff; text-decoration:none;">TechNews<span style="color:#ef4444;">.PRO</span></a>
        <div style="display:flex; gap:12px; align-items:center; flex-wrap:wrap;">
            <a href="index.html" style="color:#94a3b8; text-decoration:none; font-weight:700; font-size:0.85rem;">&larr; Radar Principal</a>
            <a href="inteligencia-artificial.html" style="color:#00f2fe; text-decoration:none; font-weight:700; font-size:0.85rem;">🧠 Hub IA</a>
            <a href="cotacao-agora.html" style="color:#10b981; text-decoration:none; font-weight:700; font-size:0.85rem;">📊 Cotações</a>
            <a href="{LINK_KIWIFY_1}" target="_blank" style="background:#ef4444; color:#fff; padding:0.5rem 1rem; border-radius:8px; font-weight:800; text-decoration:none; font-size:0.82rem;">💎 Área VIP</a>
        </div>
    </header>

    <div class="ad-top">
        <script>atOptions={{'key':'06959dfe796ac17610a3027d9ede544f','format':'iframe','height':90,'width':728,'params':{{}}}};</script>
        <script src="https://bicea.org/22/06959dfe796ac17610a3027d9ede544f"></script>
    </div>

    <main class="container">
        <h1 style="font-size:clamp(1.5rem, 4vw, 2.2rem); margin-bottom:0.5rem; border-left:5px solid #ef4444; padding-left:14px;">{cfg['titulo']}</h1>
        <p style="color:#94a3b8; margin-bottom:1.8rem; font-size:0.92rem;">{cfg['desc']} Atualizado em {data_fmt}.</p>
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
  <url><loc>{URL_PORTAL_OFICIAL}cotacao-agora.html</loc><lastmod>{hoje}</lastmod><changefreq>hourly</changefreq><priority>0.9</priority></url>
  <url><loc>{URL_PORTAL_OFICIAL}futebol.html</loc><lastmod>{hoje}</lastmod><changefreq>hourly</changefreq><priority>0.9</priority></url>"""
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
    brutas.extend(fetch_rss_massa())
    brutas.extend(fetch_newsdata_rotativo())
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
    tabela_futebol = obter_tabela_brasileirao()
    widget_futebol_html = gerar_widget_futebol_html(tabela_futebol)
    noticias_json_str = json.dumps(todas_noticias, ensure_ascii=False)

    destaque = todas_noticias[0]
    og_title = destaque.get("title", "TechNews PRO | Terminal de Inteligência, IA & Mercado").replace('"', '&quot;')
    og_desc = destaque.get("desc", "Acompanhe em tempo real as notícias mais impactantes de Tecnologia, Política, Futebol e Finanças.").replace('"', '&quot;')
    og_img = destaque.get("img", "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=1200&q=85")

    html_index = (
        HTML_TEMPLATE_INDEX
        .replace("{og_title}", og_title)
        .replace("{og_desc}", og_desc)
        .replace("{og_img}", og_img)
        .replace("{url_portal}", URL_PORTAL_OFICIAL)
        .replace("{cotacoes_html}", cotacoes_html)
        .replace("{widget_futebol_html}", widget_futebol_html)
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
    gerar_pagina_futebol(tabela_futebol, todas_noticias, cotacoes_html, data_fmt, ano_fmt)
    urls_extras = gerar_paginas_programaticas(todas_noticias, cotacoes_html, data_fmt, ano_fmt)
    gerar_sitemap_xml(urls_extras)
    gerar_rss(todas_noticias)
    garantir_verificacao_google()

    print("✅ Ecossistema v8.3 Auditado e Blindado gerado com sucesso!")

    if not apenas_site:
        publicar_no_facebook(todas_noticias[0])
        publicar_no_telegram(todas_noticias[0])
        disparar_onesignal_push(todas_noticias[0])

if __name__ == "__main__":
    if "--gerar-site" in sys.argv:
        gerar_portal(apenas_site=True)
    elif "--postar-redes" in sys.argv or "--postar-meta" in sys.argv:
        noticia_pronta = None
        if os.path.exists(ARQUIVO_FILA_POST):
            try:
                with open(ARQUIVO_FILA_POST, "r", encoding="utf-8") as f:
                    noticia_pronta = json.load(f)
            except:
                pass
        if not noticia_pronta:
            noticia_pronta = FALLBACK_NEWS[0]
        publicar_no_facebook(noticia_pronta)
        publicar_no_telegram(noticia_pronta)
        disparar_onesignal_push(noticia_pronta)
    else:
        gerar_portal(apenas_site=False)
