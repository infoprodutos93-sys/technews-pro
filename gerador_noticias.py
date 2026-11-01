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
import urllib.parse
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta

# Fuso Horário Oficial de Brasília (BRT / UTC-3)
FUSO_BRASIL = timezone(timedelta(hours=-3))

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

META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN", "")
META_PAGE_ID = os.getenv("META_PAGE_ID", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
ONESIGNAL_APP_ID = os.getenv("ONESIGNAL_APP_ID", "")
ONESIGNAL_REST_KEY = os.getenv("ONESIGNAL_REST_KEY", "")

ARQUIVO_MEMORIA_META = ".ultimo_post_meta.txt"
ARQUIVO_FILA_POST = ".fila_post_meta.json"
ARQUIVO_GOOGLE_VERIF = "google28d5384ab7e71bf6.html"
CAMINHO_API_JSON = "api/v1/noticias.json"

# ==============================================================================
# LINKS OFICIAIS DE MONETIZAÇÃO E FUNIL (V10.1)
# ==============================================================================
URL_PORTAL_OFICIAL = "https://infoprodutos93-sys.github.io/technews-pro/"
SMARTLINK_ADSTERRA = "https://asiafilm.org/4/78ed9deb10feac05c15347b414e171ab"
SYSTEME_OPTIN_URL = "https://devanildobeeny146.systeme.io/3ed9605c"

LINK_KIWIFY_1 = "https://pay.kiwify.com.br/TO0iLa6"
LINK_KIWIFY_2 = "https://pay.kiwify.com.br/BZcBEAI?afid=WXidNwGv"
LINK_KIWIFY_3 = "https://pay.kiwify.com.br/jKot3Dn?afid=VDZB2ind"

IMAGENS_FALLBACK_CATEGORIA = {
    "⚽ Esportes": "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?auto=format&fit=crop&w=1200&q=85",
    "🏛️ Política": "https://images.unsplash.com/photo-1541872703-74c5e44368f9?auto=format&fit=crop&w=1200&q=85",
    "⭐ Famosos": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=1200&q=85",
    "Finanças": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=1200&q=85",
    "Ciência": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&q=85",
    "Tecnologia": "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=1200&q=85"
}

# ==============================================================================
# TEMPLATE PRINCIPAL: INDEX.HTML (V10.1 ULTIMATE)
# ==============================================================================
HTML_TEMPLATE_INDEX = """<!DOCTYPE html>
<html lang="pt-BR" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
    <meta name="referrer" content="no-referrer">
    <meta name="description" content="Terminal avançado de notícias sobre Inteligência Artificial, Tecnologia, Política, Futebol, Celebridades e Mercado Financeiro em tempo real.">
    <meta name="robots" content="max-image-preview:large, index, follow">
    <link rel="canonical" href="{url_portal}">
    <link rel="alternate" type="application/rss+xml" title="TechNews PRO RSS Feed" href="{url_portal}feed.xml">

    <!-- OPEN GRAPH -->
    <meta property="og:title" content="{og_title}">
    <meta property="og:description" content="{og_desc}">
    <meta property="og:image" content="{og_img}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:url" content="{url_portal}">
    <meta property="og:type" content="website">
    <meta name="twitter:card" content="summary_large_image">

    <title>TechNews PRO | Terminal Cinematográfico de IA, Esportes & Mercado</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">

    <!-- GSAP CDN -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" defer></script>

    <!-- SCHEMA JSON-LD -->
    {schema_json_ld}

    <!-- ONESIGNAL PUSH -->
    <script src="https://cdn.onesignal.com/sdks/web/v16/OneSignalSDK.page.js" defer></script>
    <script>
      window.OneSignalDeferred = window.OneSignalDeferred || [];
      OneSignalDeferred.push(async function(OneSignal) {{
        const appId = "{onesignal_id}";
        if (appId && appId.length > 10) {{
          await OneSignal.init({{ appId: appId, notifyButton: {{ enable: true }} }});
        }}
      }});
    </script>

    <style>
        :root[data-theme="dark"] {{ --bg-color: #070b14; --card-bg: rgba(17, 25, 40, 0.88); --text-main: #f8fafc; --text-muted: #94a3b8; --primary: #ef4444; --accent: #3b82f6; --neon: #00f2fe; --dark-bar: #03060c; --border: rgba(255, 255, 255, 0.08); --glass: rgba(15, 23, 42, 0.88); }}
        :root[data-theme="light"] {{ --bg-color: #f1f5f9; --card-bg: #ffffff; --text-main: #0f172a; --text-muted: #64748b; --primary: #ef4444; --accent: #2563eb; --neon: #2563eb; --dark-bar: #0f172a; --border: #e2e8f0; --glass: rgba(255, 255, 255, 0.94); }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; transition: background-color 0.25s, color 0.2s; }}
        html, body {{ width: 100%; max-width: 100vw; overflow-x: hidden; background-color: var(--bg-color); color: var(--text-main); line-height: 1.6; touch-action: manipulation; }}
        #progress-bar {{ position: fixed; top: 0; left: 0; height: 3px; background: linear-gradient(90deg, var(--primary), var(--neon)); width: 0%; z-index: 99999; }}

        .market-ticker {{ background: var(--dark-bar); color: #e2e8f0; padding: 0.5rem 4%; font-size: 0.78rem; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; font-family: 'JetBrains Mono', monospace; width: 100%; }}
        .market-items {{ display: flex; gap: 1.2rem; align-items: center; overflow-x: auto; white-space: nowrap; max-width: 100%; -webkit-overflow-scrolling: touch; padding-bottom: 2px; }}
        .market-items::-webkit-scrollbar {{ height: 3px; }}
        .market-item {{ display: inline-flex; align-items: center; gap: 6px; }}
        .up {{ color: #10b981; font-weight: 700; }}
        .down {{ color: #ef4444; font-weight: 700; }}
        .live-dot {{ width: 8px; height: 8px; background: #10b981; border-radius: 50%; display: inline-block; animation: blink 1.2s infinite; flex-shrink: 0; }}
        @keyframes blink {{ 0%, 100% {{ opacity: 1; box-shadow: 0 0 8px #10b981; }} 50% {{ opacity: 0.3; }} }}

        header {{ background: var(--glass); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); padding: 0.9rem 4%; position: sticky; top: 0; z-index: 1000; border-bottom: 1px solid var(--border); width: 100%; }}
        .nav-container {{ max-width: 1440px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; gap: 0.8rem; flex-wrap: wrap; }}
        .logo {{ font-size: clamp(1.4rem, 4vw, 1.85rem); font-weight: 900; letter-spacing: -1px; color: var(--text-main); text-decoration: none; display: flex; align-items: center; gap: 6px; cursor: pointer; }}
        .logo span {{ color: var(--primary); }}
        .logo-badge {{ font-size: 0.62rem; background: rgba(239, 68, 68, 0.15); color: var(--primary); border: 1px solid var(--primary); padding: 2px 6px; border-radius: 4px; font-weight: 800; letter-spacing: 0.5px; }}

        /* LIQUID GOOEY MENU LAYERED */
        .gooey-nav-wrapper {{ position: relative; display: flex; align-items: center; background: rgba(255,255,255,0.03); border-radius: 12px; border: 1px solid var(--border); padding: 6px; overflow-x: auto; max-width: 100%; -webkit-overflow-scrolling: touch; scroll-behavior: smooth; }}
        .gooey-filter-layer {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 1; filter: url('#gooey-effect'); }}
        .gooey-blob {{ position: absolute; height: calc(100% - 12px); width: 80px; background: var(--primary); border-radius: 9px; top: 6px; left: 6px; transition: transform 0.3s ease-out, width 0.3s ease-out; will-change: transform, width; }}
        .nav-links {{ display: flex; gap: 0.4rem; list-style: none; margin: 0; padding: 0; position: relative; z-index: 2; }}
        .nav-links button, .nav-links a {{ background: transparent; border: none; color: var(--text-muted); font-weight: 700; font-size: 0.8rem; cursor: pointer; padding: 0.45rem 0.78rem; border-radius: 9px; text-decoration: none; flex-shrink: 0; transition: color 0.3s; }}
        .nav-links button:hover, .nav-links a:hover, .nav-links button.active, .nav-links a.active {{ color: #fff; }}

        .header-actions {{ display: flex; align-items: center; gap: 0.6rem; flex-wrap: wrap; }}
        .search-box {{ position: relative; flex-grow: 1; }}
        .search-box input {{ background: rgba(255,255,255,0.05); border: 1px solid var(--border); color: var(--text-main); padding: 0.48rem 0.9rem 0.48rem 2rem; border-radius: 8px; font-size: 0.84rem; width: 155px; outline: none; transition: 0.3s; }}
        .search-box input:focus {{ width: 195px; border-color: var(--primary); }}
        .search-icon {{ position: absolute; left: 9px; top: 50%; transform: translateY(-50%); font-size: 0.78rem; color: var(--text-muted); }}

        .theme-btn {{ background: rgba(255,255,255,0.06); border: 1px solid var(--border); color: var(--text-main); padding: 0.45rem 0.75rem; border-radius: 8px; cursor: pointer; font-weight: 700; font-size: 0.82rem; display: flex; align-items: center; gap: 5px; }}
        .cta-btn {{ background: linear-gradient(135deg, #ef4444, #b91c1c); color: #fff; border: none; padding: 0.5rem 1rem; border-radius: 8px; font-weight: 800; cursor: pointer; text-decoration: none; font-size: 0.82rem; box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3); display: inline-flex; align-items: center; justify-content: center; gap: 6px; }}

        .tags-bar {{ max-width: 1440px; margin: 1rem auto 0 auto; padding: 0 4%; display: flex; align-items: center; gap: 0.55rem; overflow-x: auto; white-space: nowrap; -webkit-overflow-scrolling: touch; }}
        .tag-pill {{ background: var(--card-bg); border: 1px solid var(--border); color: var(--text-muted); padding: 4px 12px; border-radius: 20px; font-size: 0.76rem; font-weight: 600; cursor: pointer; transition: 0.2s; text-decoration: none; flex-shrink: 0; }}
        .tag-pill:hover {{ border-color: var(--primary); color: var(--text-main); }}

        .ad-banner-top {{ width: 100%; max-width: 970px; min-height: 90px; margin: 1.2rem auto; padding: 0 2%; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; overflow-x: auto; -webkit-overflow-scrolling: touch; }}
        .main-container {{ max-width: 1440px; margin: 0 auto 4rem auto; padding: 0 4%; display: grid; grid-template-columns: 7.2fr 2.8fr; gap: 2.2rem; width: 100%; }}
        .content-column, .sidebar {{ min-width: 0; max-width: 100%; }}

        /* HERO CARROSSEL GSAP (COM SWIPE) */
        .hero-card {{ position: relative; border-radius: 18px; overflow: hidden; box-shadow: 0 24px 48px rgba(0,0,0,0.45); margin-bottom: 2.2rem; display: flex; flex-direction: column; border: 1px solid var(--border); background: #070b14; touch-action: pan-y; }}
        .hero-progress-wrap {{ position: absolute; top: 0; left: 0; right: 0; height: 4px; background: rgba(255,255,255,0.12); z-index: 20; }}
        .hero-progress-bar {{ height: 100%; width: 0%; background: linear-gradient(90deg, var(--primary), var(--neon)); box-shadow: 0 0 12px var(--neon); }}
        .hero-card img {{ width: 100%; height: 460px; object-fit: cover; opacity: 0.8; will-change: transform, opacity; }}
        .hero-overlay {{ position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(to top, rgba(3,6,12,0.98) 18%, rgba(3,6,12,0.75) 68%, transparent 100%); padding: 2.2rem; color: #fff; z-index: 10; pointer-events: none; }}
        .hero-top-meta {{ display: flex; justify-content: space-between; align-items: center; gap: 10px; margin-bottom: 0.7rem; flex-wrap: wrap; pointer-events: auto; }}
        .badge-source {{ background: var(--primary); color: #fff; padding: 5px 12px; border-radius: 6px; font-size: 0.7rem; font-weight: 900; text-transform: uppercase; display: inline-block; }}
        .hero-nav-controls {{ display: flex; align-items: center; gap: 8px; }}
        .hero-nav-btn {{ background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.22); color: #fff; width: 34px; height: 34px; border-radius: 50%; cursor: pointer; font-weight: 900; display: inline-flex; align-items: center; justify-content: center; backdrop-filter: blur(6px); transition: 0.2s; }}
        .hero-nav-btn:hover {{ background: var(--primary); border-color: var(--primary); transform: scale(1.08); }}
        .hero-slide-dots {{ display: flex; gap: 6px; align-items: center; margin: 0 6px; }}
        .hero-dot {{ width: 8px; height: 8px; border-radius: 50%; background: rgba(255,255,255,0.3); cursor: pointer; transition: 0.25s; }}
        .hero-dot.active {{ width: 22px; border-radius: 10px; background: var(--neon); }}
        .hero-overlay h1 {{ font-size: clamp(1.35rem, 3vw, 2.15rem); line-height: 1.25; margin-bottom: 0.75rem; font-weight: 900; pointer-events: auto; }}
        .hero-overlay p {{ color: #cbd5e1; font-size: clamp(0.88rem, 2vw, 1.02rem); margin-bottom: 1.1rem; pointer-events: auto; }}
        .hero-actions {{ display: flex; gap: 0.7rem; flex-wrap: wrap; pointer-events: auto; }}

        .section-title {{ font-size: clamp(1.1rem, 2.5vw, 1.35rem); font-weight: 900; margin-bottom: 1.4rem; border-left: 4px solid var(--primary); padding-left: 12px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; }}
        .feed-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.5rem; width: 100%; }}

        .news-card {{ background: var(--card-bg); border-radius: 14px; overflow: hidden; border: 1px solid var(--border); display: flex; flex-direction: column; transition: transform 0.25s ease; backdrop-filter: blur(10px); min-width: 0; }}
        .news-card:hover {{ transform: translateY(-5px); border-color: rgba(239, 68, 68, 0.4); }}
        .card-img-wrapper {{ position: relative; width: 100%; height: 195px; overflow: hidden; background: #1e293b; }}
        .card-img-wrapper img {{ width: 100%; height: 100%; object-fit: cover; }}
        .card-tag {{ position: absolute; top: 12px; left: 12px; background: rgba(3, 6, 12, 0.85); color: #fff; padding: 4px 10px; border-radius: 6px; font-size: 0.68rem; font-weight: 800; text-transform: uppercase; }}
        .card-floating-btns {{ position: absolute; bottom: 10px; right: 10px; display: flex; gap: 6px; }}
        .audio-btn {{ background: rgba(239, 68, 68, 0.92); color: #fff; border: none; padding: 5px 10px; border-radius: 20px; font-size: 0.72rem; font-weight: 700; cursor: pointer; }}
        .zap-btn {{ background: rgba(16, 185, 129, 0.92); color: #fff; border: none; padding: 5px 9px; border-radius: 20px; font-size: 0.72rem; font-weight: 700; text-decoration: none; }}

        .card-body {{ padding: 1.3rem; display: flex; flex-direction: column; flex-grow: 1; }}
        .card-meta {{ font-size: 0.74rem; color: var(--text-muted); margin-bottom: 0.55rem; display: flex; justify-content: space-between; font-weight: 600; flex-wrap: wrap; gap: 4px; }}
        .card-title {{ font-size: 1.08rem; font-weight: 800; color: var(--text-main); margin-bottom: 0.7rem; line-height: 1.35; word-wrap: break-word; }}
        .card-desc {{ font-size: 0.86rem; color: var(--text-muted); margin-bottom: 1.2rem; flex-grow: 1; word-wrap: break-word; }}
        .seo-internal-link {{ color: var(--neon); font-weight: 700; text-decoration: underline; }}

        .card-footer-btns {{ display: grid; grid-template-columns: 1fr 1fr; gap: 0.55rem; margin-top: auto; }}
        .btn-outline {{ background: rgba(255,255,255,0.05); color: var(--text-main); border: 1px solid var(--border); padding: 0.62rem; border-radius: 8px; font-weight: 700; font-size: 0.78rem; cursor: pointer; text-align: center; text-decoration: none; }}
        .read-btn {{ background: var(--primary); color: #fff; font-weight: 700; font-size: 0.78rem; padding: 0.62rem; border-radius: 8px; text-decoration: none; text-align: center; }}

        .native-ad-card {{ background: linear-gradient(145deg, rgba(239,68,68,0.14), rgba(15,23,42,0.92)); border: 2px solid rgba(239, 68, 68, 0.55); border-radius: 14px; padding: 1.6rem; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; }}
        .native-ad-card .ad-badge {{ background: var(--primary); color: #fff; font-size: 0.68rem; font-weight: 900; padding: 3px 10px; border-radius: 20px; text-transform: uppercase; margin-bottom: 0.9rem; }}

        /* MINI-QUIZ INTERATIVO */
        .quiz-card {{ background: linear-gradient(145deg, rgba(59,130,246,0.18), rgba(15,23,42,0.96)); border: 2px solid rgba(0, 242, 254, 0.45); border-radius: 14px; padding: 1.5rem; display: flex; flex-direction: column; justify-content: center; }}
        .quiz-badge {{ background: linear-gradient(90deg, #3b82f6, #06b6d4); color: #fff; font-size: 0.68rem; font-weight: 900; padding: 4px 10px; border-radius: 20px; text-transform: uppercase; align-self: flex-start; margin-bottom: 0.75rem; }}
        .quiz-btn {{ width: 100%; text-align: left; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.14); color: var(--text-main); padding: 0.72rem 0.9rem; border-radius: 9px; font-size: 0.8rem; font-weight: 700; cursor: pointer; margin-top: 0.5rem; transition: 0.2s; display: flex; justify-content: space-between; align-items: center; }}
        .quiz-btn:hover {{ background: var(--primary); color: #fff; border-color: var(--primary); transform: translateX(4px); }}

        .sidebar {{ display: flex; flex-direction: column; gap: 1.8rem; }}
        .widget {{ background: var(--card-bg); border-radius: 14px; padding: 1.35rem; border: 1px solid var(--border); width: 100%; overflow: hidden; }}
        .widget-title {{ font-size: 1rem; font-weight: 900; margin-bottom: 1.1rem; padding-bottom: 0.55rem; border-bottom: 2px solid var(--primary); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 6px; }}
        .trending-list {{ list-style: none; display: flex; flex-direction: column; gap: 0.95rem; }}
        .trending-item {{ display: flex; gap: 0.85rem; align-items: flex-start; text-decoration: none; color: inherit; cursor: pointer; }}
        .trending-num {{ font-size: 1.3rem; font-weight: 900; color: var(--primary); font-family: 'JetBrains Mono', monospace; flex-shrink: 0; }}
        .trending-text {{ font-size: 0.86rem; font-weight: 700; line-height: 1.35; }}

        .table-responsive-wrapper {{ width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch; }}
        .tabela-futebol {{ width: 100%; border-collapse: collapse; font-size: 0.78rem; font-family: 'JetBrains Mono', monospace; min-width: 240px; }}
        .tabela-futebol th {{ text-align: left; padding: 6px 4px; border-bottom: 1px solid var(--border); color: var(--text-muted); font-size: 0.7rem; }}
        .tabela-futebol td {{ padding: 7px 4px; border-bottom: 1px solid rgba(255,255,255,0.04); }}
        .g4-badge {{ color: #10b981; font-weight: 800; }}
        .z4-badge {{ color: #ef4444; font-weight: 800; }}

        /* OPT-IN VIP LÚDICO SVG TRACKING */
        .newsletter-box {{ background: linear-gradient(135deg, #111827, #03060c); color: #fff; border-radius: 16px; padding: 1.6rem; text-align: center; border: 1px solid rgba(239, 68, 68, 0.4); position: relative; overflow: hidden; transition: border-color 0.3s, box-shadow 0.3s; }}
        .newsletter-box.focused {{ border-color: var(--neon); box-shadow: 0 0 25px rgba(0, 242, 254, 0.25); }}
        .optin-avatar-wrap {{ width: 64px; height: 64px; margin: 0 auto 0.65rem auto; position: relative; }}
        .optin-svg {{ width: 100%; height: 100%; transition: transform 0.3s; }}
        .newsletter-box.focused .optin-svg {{ transform: scale(1.1); }}
        .optin-status {{ font-size: 0.72rem; font-family: 'JetBrains Mono', monospace; color: var(--neon); margin-bottom: 0.4rem; min-height: 18px; }}
        .newsletter-box input {{ width: 100%; padding: 0.8rem; border-radius: 8px; border: 1px solid rgba(255,255,255,0.18); background: rgba(255,255,255,0.06); color: #fff; margin: 0.6rem 0; font-size: 0.86rem; outline: none; transition: 0.25s; position: relative; z-index: 2; }}
        .newsletter-box input:focus {{ border-color: var(--neon); background: rgba(0, 242, 254, 0.06); }}
        .newsletter-box button {{ width: 100%; padding: 0.84rem; background: linear-gradient(135deg, var(--primary), #b91c1c); color: #fff; border: none; border-radius: 8px; font-weight: 800; cursor: pointer; transition: transform 0.2s; position: relative; z-index: 2; }}
        .newsletter-box button:hover {{ transform: translateY(-2px); }}

        #reader-modal, #exit-modal, #adblock-modal {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(3, 6, 12, 0.9); z-index: 9999; justify-content: center; align-items: center; backdrop-filter: blur(8px); padding: 1rem; }}
        .reader-box {{ background: var(--bg-color); border: 1px solid var(--border); width: 100%; max-width: 680px; border-radius: 16px; overflow: hidden; max-height: 90vh; display: flex; flex-direction: column; }}
        .reader-img {{ width: 100%; height: 220px; object-fit: cover; }}
        .reader-body {{ padding: 1.5rem; overflow-y: auto; }}
        .reader-ai-box {{ background: rgba(59, 130, 246, 0.1); border-left: 4px solid var(--accent); padding: 0.95rem; border-radius: 6px; margin: 1rem 0; font-size: 0.9rem; }}
        .reader-promo {{ background: rgba(239, 68, 68, 0.1); border: 1px dashed var(--primary); padding: 0.95rem; border-radius: 8px; text-align: center; margin-top: 1.2rem; }}
        .adblock-content {{ background: var(--card-bg); color: var(--text-main); border: 1px solid rgba(239,68,68,0.45); width: 95%; max-width: 430px; border-radius: 20px; padding: 1.8rem 1.4rem; text-align: center; }}
        .adblock-btn {{ background: var(--primary); color: #fff; padding: 0.85rem; border-radius: 8px; font-weight: 800; width: 100%; border: none; cursor: pointer; margin-top: 1.1rem; }}
        .adblock-close {{ margin-top: 0.9rem; font-size: 0.78rem; color: var(--text-muted); text-decoration: underline; cursor: pointer; background: none; border: none; width: 100%; }}

        #social-proof-toast {{ position: fixed; bottom: 16px; left: 16px; right: 16px; background: var(--card-bg); border: 1px solid var(--border); border-left: 4px solid #10b981; padding: 0.8rem 1rem; border-radius: 12px; z-index: 8000; display: flex; align-items: center; gap: 10px; font-size: 0.78rem; max-width: 330px; transform: translateY(150%); transition: transform 0.4s ease; cursor: pointer; }}
        #social-proof-toast.show {{ transform: translateY(0); }}

        footer {{ background: var(--dark-bar); color: #64748b; text-align: center; padding: 2.5rem 4%; font-size: 0.82rem; border-top: 1px solid var(--border); }}

        @media (max-width: 992px) {{ .main-container {{ grid-template-columns: 1fr; gap: 1.8rem; }} }}
        @media (max-width: 768px) {{
            .market-ticker {{ flex-direction: column; align-items: flex-start; padding: 0.5rem 4%; gap: 6px; }}
            .nav-container {{ flex-direction: column; align-items: stretch; gap: 0.65rem; }}
            .header-actions {{ width: 100%; justify-content: space-between; }}
            .search-box {{ flex: 1; }}
            .search-box input, .search-box input:focus {{ width: 100%; }}
            .hero-card img {{ height: 235px; opacity: 1; }}
            .hero-overlay {{ position: relative; background: #0b1120; padding: 1.35rem; }}
            .hero-actions {{ flex-direction: column; width: 100%; }}
            .hero-actions .cta-btn, .hero-actions .btn-outline {{ width: 100%; justify-content: center; }}
            .feed-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <!-- SVG FILTERS (LIQUID GOOEY) -->
    <svg style="width:0;height:0;position:absolute;" aria-hidden="true">
        <defs>
            <filter id="gooey-effect">
                <feGaussianBlur in="SourceGraphic" stdDeviation="4" result="blur" />
                <feColorMatrix in="blur" mode="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 18 -7" result="goo" />
                <feBlend in="SourceGraphic" in2="goo" />
            </filter>
        </defs>
    </svg>

    <div id="progress-bar"></div>
    <div id="ad-honeypot" class="ad-banner adsbox doubleclick sponsor" style="position:absolute; top:-999px; left:-999px; width:10px; height:10px;"></div>

    <!-- MODAIS E COMPONENTES OCULTOS... (Mantidos Intactos) -->
    <div id="adblock-modal"><div class="adblock-content"><h3 style="font-size:1.3rem; font-weight:900; margin-bottom:0.6rem;">Acesso Restrito pelo AdBlock 🛡️</h3><p style="font-size:0.88rem; color:var(--text-muted);">O <strong>TechNews.PRO</strong> mantém servidores de IA e API pública gratuitos graças aos patrocinadores. Desative seu bloqueador para liberar o terminal completo.</p><button class="adblock-btn" onclick="location.reload()">Já desativei! Liberar Terminal &rarr;</button><button class="adblock-close" onclick="document.getElementById('adblock-modal').style.display='none'">Continuar leitura limitada (Fechar)</button></div></div>
    <div id="exit-modal" onclick="document.getElementById('exit-modal').style.display='none'"><div class="adblock-content" onclick="event.stopPropagation()"><span class="badge-source">⚡ ESPERE! NÃO SAIA DE MÃOS VAZIAS</span><h3 style="font-size:1.35rem; font-weight:900; margin-bottom:0.6rem;">Quer Multiplicar seu Alcance com Posts Virais?</h3><p style="font-size:0.88rem; color:var(--text-muted); margin-bottom:1.3rem;">Descubra a estrutura secreta dos Posts Virais © para atrair milhares de seguidores e vendas todos os dias nas redes sociais.</p><a href="{link_kiwify_3}" target="_blank" rel="noopener noreferrer" class="cta-btn" style="width:100%; justify-content:center; padding:0.85rem;">🎁 Desbloquear Posts Virais © Agora &rarr;</a><button class="adblock-close" onclick="document.getElementById('exit-modal').style.display='none'">Fechar janela</button></div></div>
    <div id="reader-modal" onclick="fecharReader()"><div class="reader-box" onclick="event.stopPropagation()"><img id="r-img" src="" class="reader-img" alt="Capa" referrerpolicy="no-referrer"><div class="reader-body"><span id="r-source" class="badge-source">Fonte</span><h2 id="r-title" style="margin-bottom: 0.9rem; line-height: 1.3; font-size: 1.25rem;">Título</h2><div class="reader-ai-box"><strong>🤖 Síntese Executiva IA (Time-to-Value):</strong><p id="r-desc" style="margin-top: 6px;"></p></div><div style="display:flex; gap:10px; flex-wrap:wrap; margin-top:1.1rem;"><a id="r-url" href="#" target="_blank" rel="noopener noreferrer" class="cta-btn" style="flex:1; justify-content:center;">Ler Matéria Completa na Fonte &rarr;</a><button onclick="fecharReader()" class="btn-outline" style="padding:0.6rem 1.1rem;">Fechar</button></div><div class="reader-promo"><p style="font-size:0.82rem; margin-bottom:6px;">🔥 <strong>Destaque PRO:</strong> Crie conteúdos magnéticos e escale vendas com a metodologia <strong>Posts Virais ©</strong>.</p><a href="{link_kiwify_3}" target="_blank" style="color:var(--primary); font-weight:800; font-size:0.86rem;">Acessar Método Oficial Agora &rarr;</a></div></div></div></div>
    <div id="social-proof-toast" onclick="window.open('{link_kiwify_1}', '_blank')"><span style="font-size:1.4rem;">🔥</span><div><div id="toast-text" style="font-weight:700; color:var(--text-main);">Alguém acabou de acessar a Área VIP</div><div style="font-size:0.7rem; color:var(--primary); font-weight:700;">Clique para conhecer o treinamento &rarr;</div></div></div>

    <!-- TICKER E HEADER -->
    <div class="market-ticker">
        <div class="market-items">
            <span><span class="live-dot"></span> <strong>TERMINAL AO VIVO</strong></span>
            {cotacoes_html}
        </div>
        <div style="display:flex; gap:10px; align-items:center; flex-wrap:wrap; font-size:0.74rem;">
            <a href="cotacao-agora.html" style="color:var(--neon); text-decoration:underline;">📊 Calculadora & Cotações</a>
            <a href="futebol.html" style="color:#10b981; text-decoration:underline;">⚽ Brasileirão</a>
            <a href="api/v1/noticias.json" target="_blank" style="color:#f59e0b; text-decoration:underline;">🔌 API v1 JSON</a>
            <span>⚡ {data_atualizacao} (BRT)</span>
        </div>
    </div>

    <header>
        <div class="nav-container">
            <a class="logo" onclick="filtrarCategoria('todos', event)">TechNews<span>.PRO</span> <span class="logo-badge">v10.1</span></a>
            
            <div class="gooey-nav-wrapper" id="main-nav-wrapper">
                <div class="gooey-filter-layer">
                    <div class="gooey-blob" id="gooey-blob"></div>
                </div>
                <ul class="nav-links" id="nav-ul-links">
                    <li><button onclick="filtrarCategoria('todos', event)" class="active">🔥 Tudo</button></li>
                    <li><button onclick="filtrarCategoria('Tecnologia', event)">💻 Tech & IA</button></li>
                    <li><button onclick="filtrarCategoria('Finanças', event)">📈 Mercado</button></li>
                    <li><button onclick="filtrarCategoria('🏛️ Política', event)">🏛️ Política</button></li>
                    <li><button onclick="filtrarCategoria('⭐ Famosos', event)">⭐ Famosos</button></li>
                    <li><button onclick="filtrarCategoria('⚽ Esportes', event)">⚽ Esportes</button></li>
                    <li><button onclick="filtrarCategoria('Ciência', event)">🚀 Ciência</button></li>
                    <li><a href="futebol.html" class="hub-link">🏆 Tabela</a></li>
                    <li><a href="inteligencia-artificial.html" class="hub-link">🧠 Hub IA 3D</a></li>
                </ul>
            </div>
            
            <div class="header-actions">
                <div class="search-box">
                    <span class="search-icon">🔍</span>
                    <input type="text" id="search-input" placeholder="Buscar notícia..." onkeyup="buscarNoticia()">
                </div>
                <button class="theme-btn" id="theme-toggle-btn" onclick="alternarTema()">🌙</button>
                <a href="{link_kiwify_1}" target="_blank" rel="noopener noreferrer" class="cta-btn">💎 Área VIP</a>
            </div>
        </div>
    </header>

    <div class="tags-bar">
        <span style="font-size:0.72rem; font-weight:800; color:var(--primary); text-transform:uppercase; flex-shrink:0;">Clusters SEO:</span>
        <a href="inteligencia-artificial.html" class="tag-pill">#HubIA3D</a>
        <a href="cotacao-agora.html" class="tag-pill">#CalculadoraCâmbio</a>
        <a href="futebol.html" class="tag-pill">#BrasileirãoSérieA</a>
        <a href="bitcoin.html" class="tag-pill">#RadarBitcoin</a>
        <a href="chatgpt.html" class="tag-pill">#RadarChatGPT</a>
        <a href="startups.html" class="tag-pill">#RadarStartups</a>
        <a href="api/v1/noticias.json" target="_blank" class="tag-pill">#OpenAPI</a>
        <a href="{smartlink_url}" target="_blank" class="tag-pill" style="border-color:var(--neon); color:var(--neon);">⚡ Recursos Patrocinados</a>
    </div>

    <!-- BANNER TOPO ADSTERRA -->
    <div class="ad-banner-top">
        <script>
          atOptions = {{
            'key' : '06959dfe796ac17610a3027d9ede544f',
            'format' : 'iframe',
            'height' : 90,
            'width' : 728,
            'params' : {{}}
          }};
        </script>
        <script src="https://bicea.org/22/06959dfe796ac17610a3027d9ede544f"></script>
    </div>

    <main class="main-container">
        <div class="content-column">
            <!-- HERO GSAP CAROUSEL -->
            <div id="hero-container"></div>

            <h2 class="section-title">
                <span id="titulo-secao">Radar Global em Tempo Real</span>
                <span style="font-size:0.74rem; color:var(--text-muted); font-weight:600;">🔊 Ouça as matérias em áudio</span>
            </h2>
            <div class="feed-grid" id="feed-container"></div>
        </div>

        <aside class="sidebar">
            <div class="widget">
                <div class="widget-title">
                    <span>⚽ Brasileirão Série A</span>
                    <a href="futebol.html" style="font-size:0.74rem; color:var(--neon); text-decoration:underline;">Tabela Completa &rarr;</a>
                </div>
                <div class="table-responsive-wrapper">{widget_futebol_html}</div>
            </div>

            <div class="widget">
                <div class="widget-title">🔥 Mais Lidas no Terminal</div>
                <ul class="trending-list">{trending_section}</ul>
            </div>

            <div class="widget" style="background: linear-gradient(135deg, rgba(239,68,68,0.16), rgba(15,23,42,0.95)); border-color: rgba(239,68,68,0.45); text-align: center;">
                <span class="badge-source" style="margin-bottom:0.5rem;">🤖 LUMI • Ofertas com IA</span>
                <h3 style="margin-bottom: 0.5rem; font-size: 1.05rem;">⚡ Crie Ofertas Irresistíveis com Inteligência Artificial</h3>
                <p style="font-size: 0.82rem; color: var(--text-muted); margin-bottom: 1rem;">Use o sistema LUMI para estruturar, validar e escalar ofertas altamente lucrativas em minutos.</p>
                <a href="{link_kiwify_2}" target="_blank" rel="noopener noreferrer" class="cta-btn" style="width: 100%; justify-content: center; margin-bottom: 8px;">Conhecer o LUMI Agora &rarr;</a>
                <a href="{smartlink_url}" target="_blank" rel="noopener noreferrer" style="font-size:0.74rem; color:var(--text-muted); text-decoration:underline;">Explorar Ferramentas Patrocinadas &rarr;</a>
            </div>

            <!-- OPT-IN VIP LÚDICO SVG -->
            <div class="newsletter-box" id="newsletter-box">
                <div class="optin-avatar-wrap" id="optin-avatar-wrap">
                    <svg viewBox="0 0 100 100" class="optin-svg">
                        <circle cx="50" cy="50" r="45" fill="rgba(255,255,255,0.06)" stroke="var(--primary)" stroke-width="4"/>
                        <circle cx="35" cy="45" r="10" fill="#fff"/>
                        <circle id="pupil-l" cx="35" cy="45" r="4" fill="#03060c"/>
                        <circle cx="65" cy="45" r="10" fill="#fff"/>
                        <circle id="pupil-r" cx="65" cy="45" r="4" fill="#03060c"/>
                        <path id="mouth" d="M 35 70 Q 50 80 65 70" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round"/>
                    </svg>
                </div>
                <div class="optin-status" id="optin-status">AGUARDANDO CREDENCIAIS VIP...</div>
                <h3>💰 Briefing Matinal VIP</h3>
                <p style="font-size:0.82rem; color:#94a3b8;">Receba os insights de IA, Negócios e Ferramentas Secretas no seu e-mail.</p>
                <form action="{systeme_url}" method="GET" target="_blank">
                    <input type="email" id="optin-email-input" name="email" placeholder="Digite seu melhor e-mail..." required
                           onfocus="animarOptinFoco(true)" onblur="animarOptinFoco(false)" oninput="animarOptinDigitacao(this.value)">
                    <button type="submit">Liberar Acesso Gratuito &rarr;</button>
                </form>
            </div>

            <div class="widget" style="text-align: center; padding: 1.2rem;">
                <p style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 0.6rem;">🔗 <strong>Infraestrutura & Clusters:</strong></p>
                <p style="margin-bottom:6px;"><a href="inteligencia-artificial.html" style="color: var(--neon); font-size: 0.84rem; font-weight: 700; text-decoration: underline;">🧠 Hub IA 3D (WebGL Neural) &rarr;</a></p>
                <p style="margin-bottom:6px;"><a href="cotacao-agora.html" style="color: #10b981; font-size: 0.84rem; font-weight: 700; text-decoration: underline;">📊 Calculadora & Cotações Ao Vivo &rarr;</a></p>
                <p style="margin-bottom:6px;"><a href="futebol.html" style="color: #22c55e; font-size: 0.84rem; font-weight: 700; text-decoration: underline;">⚽ Central Brasileirão Série A &rarr;</a></p>
                <p style="margin-bottom:6px;"><a href="api/v1/noticias.json" target="_blank" style="color: #f59e0b; font-size: 0.84rem; font-weight: 700; text-decoration: underline;">🔌 API Pública JSON (/api/v1/) &rarr;</a></p>
                <p><a href="chatgpt.html" style="color: #3b82f6; font-size: 0.84rem; font-weight: 700; text-decoration: underline;">🤖 Radar ChatGPT & OpenAI &rarr;</a></p>
            </div>

            <div style="text-align: center; width: 100%; overflow: hidden;">
                <span style="font-size: 0.7rem; color: var(--text-muted); display: block; margin-bottom: 5px;">Publicidade</span>
                <script type="text/javascript">
                    atOptions = {{ 'key' : '8169727725318cd706b493da46602d6f', 'format' : 'iframe', 'height' : 250, 'width' : 300, 'params' : {{}} }};
                </script>
                <script type="text/javascript" src="https://bicea.org/22/8169727725318cd706b493da46602d6f"></script>
            </div>
        </aside>
    </main>

    <footer>
        <p><strong>TechNews.PRO</strong> &copy; {ano_atual} — Ecossistema Automatizado v10.1 Ultimate (Awwwards UI, Three.js WebGL, API Pública v1, Telegram Video & Meta Video API).</p>
        <p style="margin-top: 8px; font-size: 0.76rem; line-height: 1.8;">
            <a href="index.html" style="color:#94a3b8; margin:0 6px;">Início</a> | <a href="inteligencia-artificial.html" style="color:#94a3b8; margin:0 6px;">Hub IA 3D</a> | <a href="cotacao-agora.html" style="color:#94a3b8; margin:0 6px;">Cotações</a> | <a href="futebol.html" style="color:#94a3b8; margin:0 6px;">Futebol</a> | <a href="api/v1/noticias.json" style="color:#00f2fe; margin:0 6px;">API v1 JSON</a> | <a href="feed.xml" style="color:#94a3b8; margin:0 6px;">RSS Feed</a> | <a href="sitemap.xml" style="color:#94a3b8; margin:0 6px;">Sitemap XML</a>
        </p>
    </footer>

    <script>
        const todasNoticias = {noticias_json};
        const ofertasKiwify = [
            {{ badge: "Desenvolvimento Pessoal PRO", titulo: "🧠 Destrave Sua Mentalidade e Alta Performance", desc: "O guia prático de desenvolvimento pessoal para eliminar bloqueios, elevar seu foco e atingir resultados extraordinários.", url: "{link_kiwify_1}", cta: "Acessar Treinamento VIP &rarr;" }},
            {{ badge: "LUMI • Inteligência Artificial", titulo: "🤖 LUMI: Crie Ofertas Lucrativas com IA", desc: "Descubra como usar Inteligência Artificial para modelar, estruturar e escalar ofertas de alta conversão no digital.", url: "{link_kiwify_2}", cta: "Desbloquear Acesso ao LUMI &rarr;" }},
            {{ badge: "Crescimento Acelerado", titulo: "🔥 Posts Virais © — Domine o Algoritmo", desc: "Copie e aplique os padrões exatos dos conteúdos mais virais da internet para atrair audiência qualificada e vender todos os dias.", url: "{link_kiwify_3}", cta: "Garantir Acesso aos Posts Virais &rarr;" }}
        ];

        (function restaurarTemaSalvo() {{
            try {{
                const salvo = localStorage.getItem('technews_theme');
                if (salvo === 'light' || salvo === 'dark') {{
                    document.documentElement.setAttribute('data-theme', salvo);
                    const btn = document.getElementById('theme-toggle-btn');
                    if (btn) btn.innerHTML = salvo === 'dark' ? '🌙' : '☀️';
                }}
            }} catch (e) {{}}
        }})();

        /* LIQUID GOOEY MENU INTERACTION (COM SCROLL TRACKING MOBILE) */
        const navWrapper = document.getElementById('main-nav-wrapper');
        const navUl = document.getElementById('nav-ul-links');
        
        function moverGooeyBlob(btnTarget) {{
            const blob = document.getElementById('gooey-blob');
            if(!blob || !navWrapper || !btnTarget || window.innerWidth < 768) return;
            const btnRect = btnTarget.getBoundingClientRect();
            const wrapRect = navWrapper.getBoundingClientRect();
            const leftPos = btnRect.left - wrapRect.left + navWrapper.scrollLeft;
            blob.style.transform = `translateX(${{leftPos - 6}}px)`;
            blob.style.width = `${{btnRect.width}}px`;
        }}

        if(navWrapper) {{
            navWrapper.addEventListener('scroll', () => {{
                const activeBtn = navUl.querySelector('button.active') || navUl.querySelector('a.active');
                if(activeBtn) moverGooeyBlob(activeBtn);
            }}, {{ passive: true }});
        }}

        /* MICRO-INTERAÇÃO LÚDICA DO OPT-IN VIP (MATH AVATAR) */
        function animarOptinFoco(ativo) {{
            const box = document.getElementById('newsletter-box');
            const status = document.getElementById('optin-status');
            const mouth = document.getElementById('mouth');
            if (!box || !status) return;
            if (ativo) {{
                box.classList.add('focused');
                status.innerText = 'ANALISANDO DIGITAÇÃO...';
                mouth.setAttribute('d', 'M 35 75 Q 50 65 65 75');
            }} else {{
                box.classList.remove('focused');
                status.innerText = 'AGUARDANDO CREDENCIAIS VIP...';
                mouth.setAttribute('d', 'M 35 70 Q 50 80 65 70');
                document.getElementById('pupil-l').setAttribute('cx', '35');
                document.getElementById('pupil-r').setAttribute('cx', '65');
            }}
        }}
        function animarOptinDigitacao(valor) {{
            const status = document.getElementById('optin-status');
            const pL = document.getElementById('pupil-l');
            const pR = document.getElementById('pupil-r');
            const mouth = document.getElementById('mouth');
            if (!status || !pL || !pR) return;
            
            const maxOffset = 6;
            const chars = Math.min(valor.length, 25);
            const offset = (chars / 25) * maxOffset * 2 - maxOffset;
            pL.setAttribute('cx', 35 + offset);
            pR.setAttribute('cx', 65 + offset);

            if (valor.includes('@') && valor.includes('.')) {{
                status.innerText = 'E-MAIL VIP VALIDADO! CLIQUE PARA LIBERAR';
                status.style.color = '#10b981';
                mouth.setAttribute('d', 'M 35 65 Q 50 85 65 65');
            }} else if (valor.length > 2) {{
                status.innerText = 'SINCRONIZANDO TERMINAL...';
                status.style.color = '#00f2fe';
                mouth.setAttribute('d', 'M 35 75 Q 50 65 65 75'); 
            }} else {{
                status.innerText = 'DIGITE SEU MELHOR E-MAIL...';
                status.style.color = 'var(--neon)';
            }}
        }}

        function aplicarTeiaSEO(texto) {{
            if (!texto) return "";
            let t = texto;
            t = t.replace(/\\b(inteligência artificial|IA)\\b/i, '<a href="inteligencia-artificial.html" class="seo-internal-link">$1</a>');
            t = t.replace(/\\b(dólar|euro|câmbio)\\b/i, '<a href="cotacao-agora.html" class="seo-internal-link">$1</a>');
            t = t.replace(/\\b(brasileirão|futebol|série a)\\b/i, '<a href="futebol.html" class="seo-internal-link">$1</a>');
            t = t.replace(/\\b(bitcoin|criptomoedas|cripto)\\b/i, '<a href="bitcoin.html" class="seo-internal-link">$1</a>');
            t = t.replace(/\\b(chatgpt|openai)\\b/i, '<a href="chatgpt.html" class="seo-internal-link">$1</a>');
            t = t.replace(/\\b(startup|startups)\\b/i, '<a href="startups.html" class="seo-internal-link">$1</a>');
            return t;
        }}

        window.onscroll = function() {{
            var winScroll = document.body.scrollTop || document.documentElement.scrollTop;
            var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            document.getElementById("progress-bar").style.width = ((winScroll / height) * 100) + "%";
        }};

        function alternarTema() {{
            const htmlEl = document.documentElement;
            const btn = document.getElementById('theme-toggle-btn');
            const novo = htmlEl.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
            htmlEl.setAttribute('data-theme', novo);
            btn.innerHTML = novo === 'dark' ? '🌙' : '☀️';
            try {{ localStorage.setItem('technews_theme', novo); }} catch (e) {{}}
        }}

        function falarNoticia(idx, event) {{
            if (event) event.stopPropagation();
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                const art = todasNoticias[idx];
                const msg = new SpeechSynthesisUtterance(art.title + ". " + art.desc);
                msg.lang = 'pt-BR';
                msg.rate = 1.08;
                window.speechSynthesis.speak(msg);
            }}
        }}

        function abrirReader(idx) {{
            const art = todasNoticias[idx];
            document.getElementById('r-img').src = art.img;
            document.getElementById('r-source').innerText = art.source + " • " + art.categoria;
            document.getElementById('r-title').innerText = art.title;
            document.getElementById('r-desc').innerHTML = aplicarTeiaSEO(art.desc);
            document.getElementById('r-url').href = art.url;
            document.getElementById('reader-modal').style.display = 'flex';
        }}
        function fecharReader() {{
            document.getElementById('reader-modal').style.display = 'none';
            if ('speechSynthesis' in window) window.speechSynthesis.cancel();
        }}

        function responderQuiz(urlDestino, btnEl) {{
            const originalText = btnEl.innerHTML;
            btnEl.innerHTML = "<span>⏳ Calculando sua rota ideal...</span>";
            btnEl.style.background = "#10b981";
            btnEl.style.color = "#fff";
            setTimeout(function() {{
                window.open(urlDestino, '_blank');
                btnEl.innerHTML = originalText;
                btnEl.style.background = "";
                btnEl.style.color = "";
            }}, 450);
        }}

        /* ==================================================================
           MOTOR DE CARROSSEL HERO GSAP COM SWIPE DETECTION
        ================================================================== */
        let heroSlides = [];
        let heroIndex = 0;
        let mainHeroTimeline = null;
        let heroCycleId = 0;
        let heroHoverPausado = false;
        let touchStartX = 0;
        let touchEndX = 0;

        function pararCicloHero() {{
            heroCycleId++;
            if (mainHeroTimeline) {{
                mainHeroTimeline.kill();
                mainHeroTimeline = null;
            }}
            if(window.gsap) {{
                gsap.killTweensOf("#hero-gsap-bar");
                gsap.set("#hero-gsap-bar", {clearProps: "all"});
            }}
        }}

        function renderizarSlideHero(idx) {{
            pararCicloHero();
            if (!heroSlides || heroSlides.length === 0) return;
            heroIndex = (idx + heroSlides.length) % heroSlides.length;
            const slide = heroSlides[heroIndex];
            const globalIdx = todasNoticias.indexOf(slide);
            const container = document.getElementById('hero-container');
            if (!container) return;

            let dotsHtml = '';
            heroSlides.forEach((_, dIdx) => {{
                dotsHtml += `<span class="hero-dot ${dIdx === heroIndex ? 'active' : ''}" onclick="irParaSlideHero(${dIdx})"></span>`;
            }});

            container.innerHTML = `
                <div class="hero-card" id="hero-swipe-area" 
                     onmouseenter="pausarHero(true)" onmouseleave="pausarHero(false)">
                    <div class="hero-progress-wrap"><div class="hero-progress-bar" id="hero-gsap-bar"></div></div>
                    <img id="hero-gsap-img" src="${slide.img}" alt="Destaque" referrerpolicy="no-referrer" onerror="this.src='https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=1200&q=80'">
                    <div class="hero-overlay" id="hero-gsap-content">
                        <div class="hero-top-meta">
                            <span class="badge-source">🔥 Destaque ${heroIndex + 1}/${heroSlides.length} • ${slide.source}</span>
                            <div class="hero-nav-controls">
                                <button class="hero-nav-btn" onclick="mudarSlideHero(-1)" title="Anterior">&larr;</button>
                                <div class="hero-slide-dots">${dotsHtml}</div>
                                <button class="hero-nav-btn" onclick="mudarSlideHero(1)" title="Próxima">&rarr;</button>
                            </div>
                        </div>
                        <h1>${slide.title}</h1>
                        <p>${aplicarTeiaSEO(slide.desc)}</p>
                        <div class="hero-actions">
                            <button onclick="abrirReader(${globalIdx})" class="cta-btn">⚡ Síntese Executiva IA</button>
                            <button onclick="falarNoticia(${globalIdx}, event)" class="btn-outline" style="background:rgba(255,255,255,0.08); color:#fff;">🔊 Ouvir</button>
                            <a href="${slide.url}" target="_blank" rel="noopener noreferrer" class="btn-outline" style="background:rgba(255,255,255,0.14); color:#fff;">Fonte Oficial &rarr;</a>
                        </div>
                    </div>
                </div>
            `;

            const swipeArea = document.getElementById('hero-swipe-area');
            if (swipeArea) {{
                swipeArea.addEventListener('touchstart', e => {{
                    touchStartX = e.changedTouches[0].screenX;
                    pausarHero(true);
                }}, {{passive: true}});
                swipeArea.addEventListener('touchend', e => {{
                    touchEndX = e.changedTouches[0].screenX;
                    pausarHero(false);
                    handleSwipe();
                }}, {{passive: true}});
            }}

            iniciarCicloTimelineHero(heroCycleId);
        }}

        function handleSwipe() {{
            const swipeThreshold = 40;
            if (touchEndX < touchStartX - swipeThreshold) mudarSlideHero(1); // Swipe Left
            if (touchEndX > touchStartX + swipeThreshold) mudarSlideHero(-1); // Swipe Right
        }}

        function iniciarCicloTimelineHero(idAtual) {{
            if (!window.gsap || heroSlides.length <= 1) return;
            const bar = document.getElementById('hero-gsap-bar');
            if (!bar) return;

            gsap.fromTo("#hero-gsap-img", { scale: 1.08, opacity: 0.35 }, { scale: 1, opacity: 0.82, duration: 0.8, ease: "power2.out" });
            gsap.fromTo("#hero-gsap-content", { y: 25, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: "power2.out" });

            mainHeroTimeline = gsap.timeline({
                onComplete: () => {{
                    if (idAtual === heroCycleId && !heroHoverPausado) {{
                        renderizarSlideHero(heroIndex + 1);
                    }}
                }},
                paused: heroHoverPausado
            });

            mainHeroTimeline.fromTo(bar, { width: "0%" }, { width: "100%", duration: 5.5, ease: "none" });
        }}

        function mudarSlideHero(delta) {{ renderizarSlideHero(heroIndex + delta); }}
        function irParaSlideHero(idx) {{ renderizarSlideHero(idx); }}
        function pausarHero(estado) {{
            heroHoverPausado = estado;
            if (mainHeroTimeline) {{
                estado ? mainHeroTimeline.pause() : mainHeroTimeline.play();
            }}
        }}

        function renderizarLista(lista) {{
            if (!lista || lista.length === 0) {{
                pararCicloHero();
                document.getElementById('hero-container').innerHTML = '';
                document.getElementById('feed-container').innerHTML = '<div style="grid-column: 1 / -1; padding:2.5rem; text-align:center; color:var(--text-muted); background:var(--card-bg); border-radius:12px; border:1px solid var(--border);">🔍 Nenhuma notícia encontrada para este filtro no momento. Clique em "Tudo" ou aguarde a próxima varredura!</div>';
                return;
            }}

            heroSlides = lista.slice(0, Math.min(4, lista.length));
            renderizarSlideHero(0);

            let feedHtml = '';
            let adCount = 0;
            lista.slice(1, 16).forEach((art, idx) => {{
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

                if (idx === 0) {{
                    feedHtml += `
                    <div class="quiz-card">
                        <span class="quiz-badge">🎯 Interativo • Recomendação IA</span>
                        <h3 style="font-size:1.05rem; margin-bottom:0.35rem;">Qual é a sua meta número #1 para os próximos 30 dias?</h3>
                        <p style="font-size:0.78rem; color:var(--text-muted); margin-bottom:0.6rem;">Toque na sua prioridade para destravar a ferramenta recomendada:</p>
                        <button class="quiz-btn" onclick="responderQuiz('{link_kiwify_1}', this)">
                            <span>🧠 1. Destravar Mentalidade & Desenvolvimento Pessoal</span>
                            <span>&rarr;</span>
                        </button>
                        <button class="quiz-btn" onclick="responderQuiz('{link_kiwify_2}', this)">
                            <span>🤖 2. Criar Ofertas Lucrativas com IA (LUMI)</span>
                            <span>&rarr;</span>
                        </button>
                        <button class="quiz-btn" onclick="responderQuiz('{link_kiwify_3}', this)">
                            <span>🔥 3. Multiplicar Alcance e Vendas com Posts Virais</span>
                            <span>&rarr;</span>
                        </button>
                    </div>
                    `;
                }}

                if (idx === 2 || idx === 5 || idx === 8) {{
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
                }}
            }});
            document.getElementById('feed-container').innerHTML = feedHtml;
        }}

        function filtrarCategoria(categoria, event) {{
            if (event) {{
                event.preventDefault();
                document.querySelectorAll('.nav-links button').forEach(btn => btn.classList.remove('active'));
                if (event.currentTarget && event.currentTarget.tagName === 'BUTTON') {{
                    event.currentTarget.classList.add('active');
                    moverGooeyBlob(event.currentTarget);
                }}
            }}
            document.getElementById('titulo-secao').innerText = categoria === 'todos' ? 'Radar Global em Tempo Real' : 'Setor: ' + categoria;
            const filtradas = categoria === 'todos' ? todasNoticias : todasNoticias.filter(n => n.categoria === categoria);
            renderizarLista(filtradas);
        }}

        function buscarNoticia() {{
            const termo = document.getElementById('search-input').value.toLowerCase();
            const filtradas = todasNoticias.filter(n => n.title.toLowerCase().includes(termo) || n.desc.toLowerCase().includes(termo));
            renderizarLista(filtradas);
        }}

        setTimeout(function() {{
            var honeypot = document.getElementById('ad-honeypot');
            if (!honeypot || honeypot.offsetHeight === 0 || window.getComputedStyle(honeypot).display === 'none') {{
                document.getElementById('adblock-modal').style.display = 'flex';
            }}
            moverGooeyBlob(document.querySelector('.nav-links button.active'));
        }}, 1800);

        let exitMostrado = false;
        document.addEventListener('mouseleave', function(e) {{
            if (e.clientY < 0 && !exitMostrado) {{
                exitMostrado = true;
                document.getElementById('exit-modal').style.display = 'flex';
            }}
        }});

        /* ESTRATÉGIA GRINGA 1: BACK-BUTTON REDIRECT SUAVE (1x POR SESSÃO) */
        (function() {{
            try {{
                if (!sessionStorage.getItem('tn_back_vip')) {{
                    window.history.pushState({{ page: 'tn_entry' }}, '', window.location.href);
                    window.addEventListener('popstate', function() {{
                        if (!sessionStorage.getItem('tn_back_vip')) {{
                            sessionStorage.setItem('tn_back_vip', '1');
                            window.location.href = "{link_kiwify_1}";
                        }}
                    }});
                }}
            }} catch (e) {{}}
        }})();

        const mensagensToast = [
            "Lucas M. (SP) acabou de acessar o treinamento de Desenvolvimento Pessoal",
            "Fernanda R. (RJ) desbloqueou o sistema LUMI — Ofertas com IA",
            "Rafael S. (MG) garantiu acesso ao método Posts Virais ©"
        ];
        let toastIdx = 0;
        function dispararToastCiclo() {{
            const toast = document.getElementById('social-proof-toast');
            const txt = document.getElementById('toast-text');
            if (toast && txt) {{
                txt.innerText = mensagensToast[toastIdx % mensagensToast.length];
                toastIdx++;
                toast.classList.add('show');
                setTimeout(() => {{ toast.classList.remove('show'); }}, 6000);
            }}
        }}
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
# COTAÇÕES EM TEMPO REAL, SCHEMA.ORG (GEO), API PÚBLICA V1 & TEIA DE ARANHA SEO
# ==============================================================================
def obter_dados_cotacoes():
    dados_padrao = {
        "USDBRL": {"nome": "💵 Dólar", "val": "R$ 5,70", "raw": 5.70, "pct": "+0.15%", "classe": "up"},
        "EURBRL": {"nome": "💶 Euro", "val": "R$ 6,18", "raw": 6.18, "pct": "+0.10%", "classe": "up"},
        "BTCBRL": {"nome": "₿ Bitcoin", "val": "R$ 420.000", "raw": 420000.0, "pct": "+1.25%", "classe": "up"}
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
                    dados_padrao[par] = {"nome": label, "val": val_fmt, "raw": val, "pct": f"{sinal}{pct:.2f}%", "classe": classe}
    except:
        pass

    itens_ticker = [
        f'<span class="market-item">{v["nome"]}: <strong>{v["val"]}</strong> <span class="{v["classe"]}">({v["pct"]})</span></span>'
        for v in dados_padrao.values()
    ]
    return " • ".join(itens_ticker), dados_padrao

def exportar_api_publica_json(todas_noticias, dados_cot, tabela_futebol, data_iso):
    try:
        os.makedirs("api/v1", exist_ok=True)
        payload_api = {
            "status": "ok",
            "version": "10.1",
            "portal": "TechNews PRO",
            "documentation_and_source": URL_PORTAL_OFICIAL,
            "updated_at_brt": data_iso,
            "market_rates": {
                "USD_BRL": dados_cot["USDBRL"]["raw"],
                "EUR_BRL": dados_cot["EURBRL"]["raw"],
                "BTC_BRL": dados_cot["BTCBRL"]["raw"]
            },
            "brasileirao_serie_a_top4": tabela_futebol[:4],
            "total_articles": len(todas_noticias),
            "articles": todas_noticias
        }
        with open(CAMINHO_API_JSON, "w", encoding="utf-8") as f:
            json.dump(payload_api, f, ensure_ascii=False, indent=2)
        print(f"API Pública: ✅ Endpoint '{CAMINHO_API_JSON}' exportado com sucesso!")
    except Exception as e:
        print(f"Erro ao exportar API JSON: {e}")

def gerar_schema_json_ld(destaque, dados_cot, data_iso):
    usd_val = dados_cot["USDBRL"]["val"]
    eur_val = dados_cot["EURBRL"]["val"]
    btc_val = dados_cot["BTCBRL"]["val"]
    schema_obj = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebSite",
                "name": "TechNews PRO",
                "url": URL_PORTAL_OFICIAL,
                "description": "Terminal em tempo real de notícias sobre Inteligência Artificial, Economia, Política e Esportes."
            },
            {
                "@type": "NewsArticle",
                "headline": destaque.get("title", "Notícias em Tempo Real")[:110],
                "description": destaque.get("desc", ""),
                "image": [destaque.get("img", IMAGENS_FALLBACK_CATEGORIA["Tecnologia"])],
                "datePublished": data_iso,
                "dateModified": data_iso,
                "author": {"@type": "Organization", "name": "TechNews PRO"},
                "publisher": {"@type": "Organization", "name": "TechNews PRO"}
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": "Qual a cotação do Dólar, Euro e Bitcoin hoje?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": f"Hoje no terminal TechNews PRO, o Dólar comercial opera a {usd_val}, o Euro está cotado a {eur_val} e o Bitcoin negocia em {btc_val}."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": "Qual a principal notícia do momento no radar TechNews PRO?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": f"{destaque.get('title', '')} — {destaque.get('desc', '')}"
                        }
                    }
                ]
            }
        ]
    }
    return f'<script type="application/ld+json">{json.dumps(schema_obj, ensure_ascii=False)}</script>'

def aplicar_teia_seo_estatico(texto):
    if not texto:
        return ""
    novo = re.sub(r'(?i)\b(inteligência artificial|IA)\b', f'<a href="{URL_PORTAL_OFICIAL}inteligencia-artificial.html" style="color:#00f2fe; font-weight:700; text-decoration:underline;">\\1</a>', texto, count=1)
    novo = re.sub(r'(?i)\b(dólar|euro|câmbio)\b', f'<a href="{URL_PORTAL_OFICIAL}cotacao-agora.html" style="color:#10b981; font-weight:700; text-decoration:underline;">\\1</a>', novo, count=1)
    novo = re.sub(r'(?i)\b(brasileirão|futebol|série a)\b', f'<a href="{URL_PORTAL_OFICIAL}futebol.html" style="color:#22c55e; font-weight:700; text-decoration:underline;">\\1</a>', novo, count=1)
    novo = re.sub(r'(?i)\b(bitcoin|criptomoedas|cripto)\b', f'<a href="{URL_PORTAL_OFICIAL}bitcoin.html" style="color:#f59e0b; font-weight:700; text-decoration:underline;">\\1</a>', novo, count=1)
    return novo

# ==============================================================================
# TRADUÇÃO AUTOMÁTICA PT-BR AUDITADA & SANITIZAÇÃO DE FRASES DO WORDPRESS
# ==============================================================================
def limpar_html_rss(texto_bruto):
    if not texto_bruto:
        return ""
    sem_tags = re.sub(r'<[^>]+>', ' ', texto_bruto)
    limpo = html.unescape(sem_tags)
    limpo = re.sub(r'(?i)O post .*? apareceu primeiro em.*', '', limpo)
    limpo = re.sub(r'(?i)The post .*? appeared first on.*', '', limpo)
    limpo = re.sub(r'(?i)Leia mais em.*', '', limpo)
    limpo = re.sub(r'\s+', ' ', limpo).strip()

    if len(limpo) > 230:
        corte = limpo[:230]
        ultimo_ponto = max(corte.rfind('. '), corte.rfind('! '), corte.rfind('? '))
        if ultimo_ponto > 110:
            limpo = corte[:ultimo_ponto + 1]
        else:
            ultimo_espaco = corte.rfind(' ')
            if ultimo_espaco > 80:
                limpo = corte[:ultimo_espaco].rstrip(',;:-') + "..."
            else:
                limpo = corte + "..."
    return limpo

def detectar_texto_em_ingles(texto):
    if not texto:
        return False
    t = f" {texto.lower()} "
    sinais_pt = ["ã", "õ", "ç", " não ", " para ", " mais ", " sobre ", " após ", " está ", " são "]
    pontos_pt = sum(1 for s in sinais_pt if s in t)
    marcadores_en = [
        " the ", " and ", " with ", " from ", " launches ", " launch ", " announces ", " space ",
        " new ", " how ", " why ", " into ", " after ", " over ", " under ", " between ",
        " could ", " would ", " should ", " their ", " about ", " first ", " next ", "flight",
        "rocket", "satellite", "nasa", "spacex", "developer", "software", "building", "guide",
        "using", "learn", "world", "report", "update", "market", "future", "system", "model"
    ]
    pontos_en = sum(1 for m in marcadores_en if m in t)
    if pontos_en >= 2 and pontos_pt == 0:
        return True
    if pontos_en >= 1 and pontos_pt == 0 and not any(c in t for c in "áéíóúâêôãõç"):
        return True
    return False

def traduzir_fallback_gratuito(texto):
    if not texto:
        return texto
    try:
        q = urllib.parse.quote(texto)
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=pt&dt=t&q={q}"
        r = requests.get(url, timeout=6)
        if r.status_code == 200:
            dados = r.json()
            traduzido = "".join([bloco[0] for bloco in dados[0] if bloco and bloco[0]])
            if traduzido:
                return traduzido.strip()
    except:
        pass
    return texto

def garantir_portugues(texto):
    if not texto:
        return ""
    if not detectar_texto_em_ingles(texto):
        return texto
    if OPENAI_API_KEY:
        try:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {"Content-Type": "application/json", "Authorization": f"Bearer {OPENAI_API_KEY}"}
            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "Traduza o texto jornalístico abaixo para Português do Brasil (PT-BR) natural e fluente. Retorne apenas a tradução exata, sem aspas extras."},
                    {"role": "user", "content": texto}
                ],
                "max_tokens": 200,
                "temperature": 0.3
            }
            r = requests.post(url, headers=headers, json=payload, timeout=8)
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"].strip()
        except:
            pass
    return traduzir_fallback_gratuito(texto)

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
                    tabela_limpa.append({
                        "posicao": item.get("posicao"),
                        "time": item.get("time", {}).get("nome_popular", "Clube"),
                        "pontos": item.get("pontos", 0),
                        "jogos": item.get("jogos", 0),
                        "vitorias": item.get("vitorias", 0)
                    })
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

    return f"""<table class="tabela-futebol"><thead><tr><th>Pos</th><th>Clube</th><th>PTS</th><th>J</th></tr></thead><tbody>{linhas}</tbody></table>"""

def gerar_pagina_futebol(tabela, todas_noticias, cotacoes_html, data_fmt, ano_fmt, schema_ld):
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
    {schema_ld}
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
        <p style="color:#94a3b8; margin-bottom:1.8rem; font-size:0.92rem;">Acompanhe a disputa pelo título, vaga na Libertadores (G4) e luta contra o rebaixamento (Z4). Atualizado em: {data_fmt} (BRT).</p>
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
# INTELIGÊNCIA ARTIFICIAL: TRADUÇÃO PT-BR + DISCOVER + TIME-TO-VALUE
# ==============================================================================
def otimizar_noticia_com_ia(noticia):
    noticia["title"] = garantir_portugues(noticia.get("title", ""))
    noticia["desc"] = limpar_html_rss(garantir_portugues(noticia.get("desc", "")))

    if not OPENAI_API_KEY:
        return noticia

    titulo_orig = noticia.get("title", "")
    desc_orig = noticia.get("desc", "")
    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {OPENAI_API_KEY}"}
        prompt = (
            f"Título original: {titulo_orig}\nResumo original: {desc_orig}\n\n"
            "Retorne um JSON estrito em Português do Brasil (PT-BR) com duas chaves: 'titulo' e 'resumo'.\n"
            "1. Se o conteúdo estiver em inglês ou outro idioma, traduza 100% para Português do Brasil.\n"
            "2. Em 'titulo': Reescreva o título para o Google Discover usando Dissonância Cognitiva e curiosidade jornalística (máximo 100 caracteres, frase completa).\n"
            "3. Em 'resumo': Entregue o 'Time-to-Value' (o fato principal e o impacto prático imediato) em 2 frases completas e sem cortar palavras no final."
        )
        payload = {
            "model": "gpt-4o-mini",
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": "Você é um editor-chefe especialista em Google Discover e SEO no Brasil. Responda sempre em Português do Brasil e apenas em JSON válido."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 200,
            "temperature": 0.7
        }
        r = requests.post(url, headers=headers, json=payload, timeout=10)
        if r.status_code == 200:
            dados_ia = json.loads(r.json()["choices"][0]["message"]["content"])
            if dados_ia.get("titulo"):
                noticia["title"] = dados_ia["titulo"].strip()
            if dados_ia.get("resumo"):
                noticia["desc"] = limpar_html_rss(dados_ia["resumo"].strip())
    except Exception as e:
        print(f"Aviso IA otimização: {e}")
    return noticia

# ==============================================================================
# FÁBRICA DE VÍDEOS 9:16 SPLIT-SCREEN (ZERO ESPAÇO AZUL + MARGENS LARGAS)
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
    x = max(55, (largura_canvas - larg_texto) // 2)
    draw.text((x, y), texto, fill=cor, font=fonte)

def baixar_imagem_validada(url):
    if not url or not url.startswith("http"):
        return None
    headers_img = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
        "Referer": "https://www.google.com/"
    }
    try:
        r = requests.get(url, headers=headers_img, timeout=10, allow_redirects=True)
        if r.status_code == 200 and len(r.content) > 2500:
            im = Image.open(io.BytesIO(r.content)).convert("RGB")
            if im.width >= 150 and im.height >= 150:
                return im
    except:
        pass
    return None

def criar_painel_grafico_emergencia(largura, altura_metade, texto_tarja, cor_tarja):
    im = Image.new("RGB", (largura, altura_metade), (12, 18, 34))
    dr = ImageDraw.Draw(im, "RGBA")
    for y in range(0, altura_metade, 60):
        dr.line([(0, y), (largura, y)], fill=(255, 255, 255, 18), width=1)
    for x in range(0, largura, 60):
        dr.line([(x, 0), (x, altura_metade)], fill=(255, 255, 255, 18), width=1)
    dr.ellipse([(290, 230), (790, 730)], outline=cor_tarja, width=8)
    f_grande = obter_fonte_segura(56)
    f_sub = obter_fonte_segura(34)
    desenhar_texto_centralizado(dr, 420, "TECHNEWS.PRO", f_grande, (255, 255, 255, 255), largura)
    desenhar_texto_centralizado(dr, 500, texto_tarja, f_sub, cor_tarja, largura)
    return im

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
        print("Fábrica de Vídeos: Pillow ou MoviePy não disponíveis. Pulando.")
        return None
    try:
        largura, altura = 1080, 1920
        altura_metade = 960
        canvas = Image.new("RGB", (largura, altura), (7, 11, 20))

        categoria_not = noticia.get("categoria", "Tecnologia")
        texto_tarja, cor_tarja = obter_config_visual_editoria(categoria_not)

        # ------------------------------------------------------------------
        # 1. METADE SUPERIOR (0 a 960px): DUPLO DOWNLOAD + FALLBACK GARANTIDO
        # ------------------------------------------------------------------
        img_topo = baixar_imagem_validada(noticia.get("img", ""))
        if img_topo is None:
            url_reserva = IMAGENS_FALLBACK_CATEGORIA.get(categoria_not, IMAGENS_FALLBACK_CATEGORIA["Tecnologia"])
            print(f"Fábrica de Vídeos: Aplicando Fallback HD da categoria '{categoria_not}'...")
            img_topo = baixar_imagem_validada(url_reserva)

        if img_topo is None:
            img_topo = criar_painel_grafico_emergencia(largura, altura_metade, texto_tarja, cor_tarja)
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
        # 2. METADE INFERIOR (960px a 1920px) + MARGENS LATERAIS AMPLAS
        # ------------------------------------------------------------------
        draw = ImageDraw.Draw(canvas, "RGBA")
        draw.rectangle([(0, altura_metade), (largura, altura)], fill=(7, 11, 20, 255))

        draw.rectangle([(0, 954), (largura, 966)], fill=cor_tarja)
        draw.rectangle([(85, 916), (largura - 85, 1008)], fill=cor_tarja)

        fonte_tarja = obter_fonte_segura(38)
        fonte_titulo = obter_fonte_segura(50)
        fonte_fonte = obter_fonte_segura(27)
        fonte_cta = obter_fonte_segura(33)

        desenhar_texto_centralizado(draw, 938, f"• {texto_tarja} | TECHNEWS.PRO •", fonte_tarja, (255, 255, 255, 255), largura)

        fonte_org = limpar_emojis_para_pillow(noticia.get("source", "Portal Oficial")).upper()
        desenhar_texto_centralizado(draw, 1036, f"FONTE: {fonte_org}  •  COBERTURA EM TEMPO REAL", fonte_fonte, (148, 163, 184, 255), largura)

        titulo_pt = garantir_portugues(noticia.get("title", "Notícia Urgente em Tempo Real"))
        titulo_limpo = limpar_emojis_para_pillow(titulo_pt).upper()
        linhas = textwrap.wrap(titulo_limpo, width=20)[:6]
        y_texto = 1108
        for idx_l, linha in enumerate(linhas):
            cor_linha = (255, 215, 0, 255) if idx_l < 2 else (248, 250, 252, 255)
            desenhar_texto_centralizado(draw, y_texto, linha, fonte_titulo, cor_linha, largura)
            y_texto += 78

        # Botão de Rodapé Fixo Centralizado (1685px a 1800px)
        draw.rectangle([(85, 1685), (largura - 85, 1800)], fill=(16, 185, 129, 255))
        desenhar_texto_centralizado(draw, 1723, "LEIA COMPLETO NO LINK DOS COMENTÁRIOS", fonte_cta, (255, 255, 255, 255), largura)

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
            print(f"Fábrica de Vídeos: ✅ Reel Split-Screen 9:16 gerado com sucesso!")
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
# AGENTES SOCIAIS OMNICHANNEL: ONESIGNAL, TELEGRAM VIDEO & FACEBOOK REELS
# ==============================================================================
def disparar_onesignal_push(noticia):
    if not ONESIGNAL_APP_ID or not ONESIGNAL_REST_KEY or not noticia:
        return False
    try:
        titulo_pt = garantir_portugues(noticia.get("title", ""))
        desc_pt = limpar_html_rss(garantir_portugues(noticia.get("desc", "")))
        titulo_curto = titulo_pt[:55] + "..." if len(titulo_pt) > 55 else titulo_pt
        payload = {
            "app_id": ONESIGNAL_APP_ID.strip(),
            "included_segments": ["Subscribed Users"],
            "headings": {"en": "🚨 URGENTE: " + titulo_curto, "pt": "🚨 URGENTE: " + titulo_curto},
            "contents": {"en": desc_pt[:110], "pt": desc_pt[:110]},
            "url": URL_PORTAL_OFICIAL
        }
        headers = {"Authorization": f"Basic {ONESIGNAL_REST_KEY.strip()}", "Content-Type": "application/json"}
        r = requests.post("https://onesignal.com/api/v1/notifications", json=payload, headers=headers, timeout=10)
        if r.status_code == 200:
            print("Agente OneSignal: ✅ Notificação enviada!")
            return True
    except Exception as e:
        print(f"Agente OneSignal Erro: {e}")
    return False

def publicar_no_telegram(noticia, caminho_video=None):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID or not noticia:
        return False
    try:
        titulo_pt = html.escape(garantir_portugues(noticia.get("title", ""))[:180])
        desc_pt = html.escape(limpar_html_rss(garantir_portugues(noticia.get("desc", "")))[:260])
        stamp = datetime.now(FUSO_BRASIL).strftime("%Y%m%d%H%M")
        link_track = f"{URL_PORTAL_OFICIAL}?utm_source=telegram_vip&v={stamp}"

        texto_alerta = (
            f"🚨 <b>[URGENTE] Acabou de sair no Terminal:</b>\n\n"
            f"🔥 <b>{titulo_pt}</b>\n\n"
            f"💡 <i>{desc_pt}</i>\n\n"
            f"👉 <b>Leia a cobertura completa no portal:</b>\n"
            f"🔗 {link_track}\n\n"
            f"💎 <a href=\"{LINK_KIWIFY_1}\">Acessar Área VIP: Desenvolvimento Pessoal PRO</a>\n"
            f"🤖 <a href=\"{LINK_KIWIFY_2}\">Conhecer LUMI — Ofertas com IA</a>"
        )

        if caminho_video and os.path.exists(caminho_video):
            try:
                url_vid = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendVideo"
                with open(caminho_video, "rb") as f_v:
                    files = {"video": ("noticia_urgente.mp4", f_v, "video/mp4")}
                    data_v = {
                        "chat_id": TELEGRAM_CHAT_ID.strip(),
                        "caption": texto_alerta,
                        "parse_mode": "HTML",
                        "supports_streaming": "true"
                    }
                    r_v = requests.post(url_vid, data=data_v, files=files, timeout=90)
                if r_v.status_code == 200:
                    print("Agente Telegram: ✅ VÍDEO NATIVO 9:16 enviado com sucesso!")
                    return True
                else:
                    print(f"Aviso Vídeo Telegram ({r_v.status_code}): {r_v.text}")
            except Exception as e_vid:
                print(f"Aviso envio de vídeo Telegram: {e_vid}")

        url_msg = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID.strip(), "text": texto_alerta, "parse_mode": "HTML", "disable_web_page_preview": False}
        r = requests.post(url_msg, json=payload, timeout=12)
        if r.status_code == 200:
            print("Agente Telegram: ✅ Alerta em texto enviado com sucesso!")
            return True
    except Exception as e:
        print(f"Agente Telegram Erro: {e}")
    return False

def gerar_copy_persuasiva_meta(noticia):
    titulo = garantir_portugues(noticia.get("title", ""))
    resumo = limpar_html_rss(garantir_portugues(noticia.get("desc", "")))
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
            "Crie uma legenda em Português do Brasil (PT-BR) altamente magnética para o Facebook seguindo esta estrutura exata e sem cortar frases no meio:\n"
            "1. GANCHO EXPLOSIVO com emojis na primeira linha (1 frase completa).\n"
            f"2. LOGO ABAIXO DO GANCHO, coloque: 👉 Leia completo no portal: {URL_PORTAL_OFICIAL}\n"
            "3. CURIOSIDADE (2 frases curtas e completas de até 260 caracteres no total): Contextualize o impacto da notícia sem jamais deixar palavras pela metade.\n"
            f"4. FECHAMENTO: Convide a clicar no link ({URL_PORTAL_OFICIAL}) e peça para comentarem 'LINK' ou 'VIP' para receberem nossa ferramenta recomendada."
        )
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "Você é um copywriter brasileiro sênior. Escreva 100% em Português do Brasil e nunca deixe frases incompletas."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 240,
            "temperature": 0.7
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

def publicar_no_facebook(noticia, caminho_video=None):
    if not META_ACCESS_TOKEN or not noticia:
        print("Agente Meta: META_ACCESS_TOKEN ausente nos Secrets. Pulando.")
        return False

    alvo_id, token_pagina = obter_credenciais_pagina(META_ACCESS_TOKEN)
    mensagem = gerar_copy_persuasiva_meta(noticia)
    alvos_tentativa = [alvo_id]
    if "me" not in alvos_tentativa:
        alvos_tentativa.append("me")

    if caminho_video and os.path.exists(caminho_video):
        for alvo in alvos_tentativa:
            try:
                url_video = f"https://graph-video.facebook.com/v20.0/{alvo}/videos"
                with open(caminho_video, "rb") as f_vid:
                    files = {"source": ("noticia_urgente.mp4", f_vid, "video/mp4")}
                    data_vid = {
                        "title": garantir_portugues(noticia.get("title", "Plantão TechNews PRO"))[:95],
                        "description": mensagem,
                        "access_token": token_pagina
                    }
                    r_vid = requests.post(url_video, data=data_vid, files=files, timeout=90)
                if r_vid.status_code == 200:
                    vid_id = r_vid.json().get("id")
                    salvar_memoria_meta(noticia.get("title", ""))
                    print(f"Agente Meta: ✅ VÍDEO SPLIT-SCREEN 9:16 publicado via '{alvo}'! ID: {vid_id}")
                    try:
                        requests.post(
                            f"https://graph.facebook.com/v20.0/{vid_id}/comments",
                            data={"message": f"📖 Leia a matéria completa aqui: {URL_PORTAL_OFICIAL}\n💎 Conheça também nossa Área VIP: {LINK_KIWIFY_1}", "access_token": token_pagina},
                            timeout=10
                        )
                    except:
                        pass
                    return True
                else:
                    print(f"Aviso Upload Vídeo Meta ({r_vid.status_code}): {r_vid.text}")
            except Exception as e:
                print(f"Erro tentativa de vídeo Meta: {e}")

    stamp = datetime.now(FUSO_BRASIL).strftime("%Y%m%d%H%M")
    link_com_cache_buster = f"{URL_PORTAL_OFICIAL}?v={stamp}"

    for alvo in alvos_tentativa:
        try:
            url_feed = f"https://graph.facebook.com/v20.0/{alvo}/feed"
            payload_feed = {"message": mensagem, "link": link_com_cache_buster, "access_token": token_pagina}
            r_feed = requests.post(url_feed, data=payload_feed, timeout=15)
            if r_feed.status_code == 200:
                salvar_memoria_meta(noticia.get("title", ""))
                print(f"Agente Meta: ✅ Card de Link Clicável publicado via '{alvo}'!")
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

def disparar_redes_omnichannel(noticia):
    noticia["title"] = garantir_portugues(noticia.get("title", ""))
    noticia["desc"] = limpar_html_rss(garantir_portugues(noticia.get("desc", "")))
    caminho_video = gerar_video_reel_noticia(noticia)
    publicar_no_facebook(noticia, caminho_video)
    publicar_no_telegram(noticia, caminho_video)
    disparar_onesignal_push(noticia)
    limpar_arquivos_temporarios_midia()

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

def url_imagem_valida_e_limpa(url_cand):
    if not url_cand or not url_cand.startswith("http"):
        return False
    u = url_cand.lower()
    termos_lixo = ["1x1", "pixel", "avatar", "emoji", "s.w.org", "gravatar", "icon", "logo", ".svg", ".gif"]
    if any(t in u for t in termos_lixo):
        return False
    return True

def extrair_imagem_item_rss(item_xml, texto_bruto_html, fallback_img):
    if item_xml is not None:
        for elem in item_xml.iter():
            tag_l = elem.tag.lower()
            if "enclosure" in tag_l or "content" in tag_l or "thumbnail" in tag_l:
                url_cand = (elem.attrib.get("url") or elem.attrib.get("href") or "").strip()
                tipo_mime = (elem.attrib.get("type") or "").lower()
                if url_imagem_valida_e_limpa(url_cand):
                    if "image" in tipo_mime or any(ext in url_cand.lower() for ext in [".jpg", ".jpeg", ".png", ".webp", "imguol", "metropoles", "gazetaesportiva", "wp-content"]):
                        return url_cand
    for m in re.finditer(r'<img[^>]+src=["\'](https?://[^"\']+)["\']', texto_bruto_html or "", re.IGNORECASE):
        url_cand = m.group(1).strip()
        if url_imagem_valida_e_limpa(url_cand):
            return url_cand
    return fallback_img

def fetch_rss_massa():
    feeds = [
        {"url": "https://www.metropoles.com/brasil/politica-brasil/feed", "source": "Metrópoles", "cat": "🏛️ Política", "fallback_img": IMAGENS_FALLBACK_CATEGORIA["🏛️ Política"]},
        {"url": "https://www.metropoles.com/colunas/leo-dias/feed", "source": "Coluna Famosos", "cat": "⭐ Famosos", "fallback_img": IMAGENS_FALLBACK_CATEGORIA["⭐ Famosos"]},
        {"url": "https://rss.uol.com.br/feed/splash.xml", "source": "UOL Splash", "cat": "⭐ Famosos", "fallback_img": "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?auto=format&fit=crop&w=1200&q=85"},
        {"url": "https://www.gazetaesportiva.com/feed/", "source": "Gazeta Esportiva", "cat": "⚽ Esportes", "fallback_img": IMAGENS_FALLBACK_CATEGORIA["⚽ Esportes"]}
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
    termos_quentes = ["inteligência artificial", "reforma tributária", "bitcoin", "stf", "brasileirão", "famosos"]
    indice_ciclo = (datetime.now(FUSO_BRASIL).hour // 6) % len(termos_quentes)
    termo_atual = termos_quentes[indice_ciclo]
    try:
        url = "https://newsdata.io/api/1/news"
        params = {"apikey": NEWSDATA_API_KEY.strip(), "country": "br", "language": "pt", "q": termo_atual}
        r = requests.get(url, params=params, timeout=8)
        if r.status_code == 200:
            for item in r.json().get("results", [])[:6]:
                titulo = item.get("title") or ""
                desc = item.get("description") or "Leia a cobertura completa e os desdobramentos no portal."
                if titulo and noticia_segura_adsterra(titulo, desc):
                    cat_det = classificar_noticia(titulo)
                    noticias.append({
                        "title": titulo,
                        "desc": limpar_html_rss(desc),
                        "img": item.get("image_url") or IMAGENS_FALLBACK_CATEGORIA.get(cat_det, IMAGENS_FALLBACK_CATEGORIA["Tecnologia"]),
                        "url": item.get("link", "#"),
                        "source": item.get("source_id", "Radar Brasil").upper(),
                        "date": (item.get("pubDate") or "Hoje")[:10],
                        "categoria": cat_det
                    })
    except Exception as e:
        pass
    return noticias

def fetch_ibge_noticias():
    noticias = []
    try:
        r = requests.get("https://servicodados.ibge.gov.br/api/v3/noticias/?qtd=5", timeout=8)
        if r.status_code == 200:
            for item in r.json().get("items", []):
                titulo = item.get("titulo", "")
                desc = limpar_html_rss(item.get("introducao", "Confira os dados completos divulgados pelo portal oficial."))
                if not noticia_segura_adsterra(titulo, desc):
                    continue
                img_url = IMAGENS_FALLBACK_CATEGORIA["Finanças"]
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
                titulo = garantir_portugues(item.get("title", ""))
                desc = limpar_html_rss(garantir_portugues(item.get("description") or "Artigo técnico sobre tecnologia e desenvolvimento."))
                if not noticia_segura_adsterra(titulo, desc):
                    continue
                noticias.append({
                    "title": titulo, "desc": desc,
                    "img": item.get("cover_image") or item.get("social_image") or IMAGENS_FALLBACK_CATEGORIA["Tecnologia"],
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
                titulo_pt = garantir_portugues(item.get("title", ""))
                desc_pt = limpar_html_rss(garantir_portugues(item.get("summary", "")))
                noticias.append({
                    "title": titulo_pt, "desc": desc_pt,
                    "img": item.get("image_url") or IMAGENS_FALLBACK_CATEGORIA["Ciência"],
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
                titulo = garantir_portugues(item.get("title") or "")
                desc = limpar_html_rss(garantir_portugues(item.get("description") or "Clique para ler a matéria completa na fonte oficial."))
                if titulo and titulo != "[Removed]" and noticia_segura_adsterra(titulo, desc):
                    cat_det = classificar_noticia(titulo)
                    noticias.append({
                        "title": titulo, "desc": desc,
                        "img": item.get("urlToImage") or IMAGENS_FALLBACK_CATEGORIA.get(cat_det, IMAGENS_FALLBACK_CATEGORIA["Tecnologia"]),
                        "url": item.get("url", "#"), "source": item.get("source", {}).get("name", "TechPress"),
                        "date": item.get("publishedAt", "")[:10], "categoria": cat_det
                    })
    except:
        pass
    return noticias

FALLBACK_NEWS = [
    {
        "title": "Inteligência Artificial Generativa redefine o mercado de tecnologia e cria novas profissões em alta",
        "desc": "Grandes corporações aceleram a adoção de agentes autônomos para otimizar processos e escalar produtos digitais.",
        "img": IMAGENS_FALLBACK_CATEGORIA["Tecnologia"],
        "url": "https://news.google.com", "source": "Destaque IA", "date": "Hoje", "categoria": "Tecnologia"
    },
    {
        "title": "Bastidores de Brasília: Novas medidas econômicas movimentam o Congresso e o mercado financeiro",
        "desc": "Parlamentares debatem pacote fiscal e impactos diretos nas taxas de juros e investimentos no país.",
        "img": IMAGENS_FALLBACK_CATEGORIA["🏛️ Política"],
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
# GERAÇÃO DE RSS FEED, HUB IA 3D, CALCULADORA DE COTAÇÕES E SITEMAP
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

def gerar_hub_ia(todas_noticias, cotacoes_html, data_fmt, ano_fmt, schema_ld):
    cards_ia = ""
    noticias_ia = [n for n in todas_noticias if n.get("categoria") == "Tecnologia" or "ia" in n.get("title", "").lower()]
    if not noticias_ia:
        noticias_ia = todas_noticias[:6]

    for art in noticias_ia[:8]:
        cards_ia += f"""
        <article style="background:rgba(17,25,40,0.86); backdrop-filter:blur(10px); border:1px solid rgba(0,242,254,0.18); border-radius:14px; overflow:hidden; display:flex; flex-direction:column; position:relative; z-index:2;">
            <img src="{art['img']}" alt="{html.escape(art['title'])}" referrerpolicy="no-referrer" style="width:100%; height:190px; object-fit:cover;" onerror="this.src='https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=1200&q=85'">
            <div style="padding:1.3rem; display:flex; flex-direction:column; flex-grow:1;">
                <span style="font-size:0.72rem; color:#00f2fe; font-weight:800; text-transform:uppercase;">{art['source']} • {art['date']}</span>
                <h3 style="font-size:1.1rem; margin:0.5rem 0 0.8rem 0; color:#f8fafc;">{art['title']}</h3>
                <p style="font-size:0.86rem; color:#cbd5e1; margin-bottom:1.2rem; flex-grow:1;">{aplicar_teia_seo_estatico(art['desc'])}</p>
                <a href="{art['url']}" target="_blank" rel="noopener noreferrer" style="background:linear-gradient(135deg,#ef4444,#b91c1c); color:#fff; text-align:center; padding:0.65rem; border-radius:8px; font-weight:700; font-size:0.82rem; text-decoration:none;">Ler Relatório Completo &rarr;</a>
            </div>
        </article>
        """

    html_hub = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="referrer" content="no-referrer">
    <meta name="description" content="Hub Oficial 3D de Inteligência Artificial: Guia definitivo, ferramentas generativas, automação e notícias em tempo real sobre IA.">
    <meta name="robots" content="max-image-preview:large, index, follow">
    <link rel="canonical" href="{URL_PORTAL_OFICIAL}inteligencia-artificial.html">
    <title>Inteligência Artificial (Hub 3D WebGL) | Guia, Ferramentas & Notícias | TechNews PRO</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
    <!-- THREE.JS WEBGL NEURAL NETWORK -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js" defer></script>
    {schema_ld}
    <style>
        * {{ box-sizing: border-box; }}
        body {{ background:#050811; color:#f8fafc; font-family:'Inter',sans-serif; margin:0; line-height:1.65; overflow-x:hidden; position:relative; touch-action: manipulation; }}
        #neural-webgl-canvas {{ position:fixed; top:0; left:0; width:100vw; height:100vh; z-index:0; pointer-events:none; opacity:0.85; }}
        .ticker {{ position:relative; z-index:2; background:rgba(3,6,12,0.9); padding:0.5rem 4%; font-size:0.78rem; font-family:'JetBrains Mono',monospace; border-bottom:1px solid rgba(255,255,255,0.08); display:flex; justify-content:space-between; flex-wrap:wrap; gap:8px; }}
        .up {{ color:#10b981; font-weight:700; }} .down {{ color:#ef4444; font-weight:700; }}
        header {{ position:relative; z-index:2; background:rgba(15,23,42,0.82); backdrop-filter:blur(14px); padding:1rem 4%; border-bottom:1px solid rgba(255,255,255,0.08); display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem; }}
        .container {{ position:relative; z-index:2; max-width:1360px; margin:2rem auto; padding:0 4%; }}
        .pillar-box {{ background:linear-gradient(145deg, rgba(15,23,42,0.88), rgba(7,11,20,0.92)); backdrop-filter:blur(12px); border:1px solid rgba(0,242,254,0.4); border-radius:18px; padding:clamp(1.3rem, 4vw, 2.5rem); margin-bottom:2.2rem; box-shadow:0 20px 50px rgba(0,0,0,0.5); }}
        .grid {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(280px, 1fr)); gap:1.5rem; }}
        .ad-top {{ position:relative; z-index:2; width:100%; overflow-x:auto; text-align:center; margin:1.2rem auto; padding:0 2%; }}
        footer {{ position:relative; z-index:2; background:#03060c; color:#64748b; text-align:center; padding:2.5rem 4%; margin-top:4rem; border-top:1px solid rgba(255,255,255,0.08); }}
    </style>
</head>
<body>
    <!-- CANVAS WEBGL THREE.JS (INTERAÇÃO TOUCH & MOUSE) -->
    <canvas id="neural-webgl-canvas"></canvas>

    <div class="ticker">
        <div style="overflow-x:auto; white-space:nowrap; max-width:100%;">{cotacoes_html}</div>
        <div>⚡ Atualizado: {data_fmt} (BRT)</div>
    </div>
    <header>
        <a href="index.html" style="font-size:1.6rem; font-weight:900; color:#fff; text-decoration:none;">TechNews<span style="color:#ef4444;">.PRO</span></a>
        <div style="display:flex; gap:12px; align-items:center; flex-wrap:wrap;">
            <a href="index.html" style="color:#94a3b8; text-decoration:none; font-weight:700; font-size:0.85rem;">&larr; Radar Principal</a>
            <a href="cotacao-agora.html" style="color:#10b981; text-decoration:none; font-weight:700; font-size:0.85rem;">📊 Cotações</a>
            <a href="api/v1/noticias.json" target="_blank" style="color:#00f2fe; text-decoration:none; font-weight:700; font-size:0.85rem;">🔌 API JSON</a>
            <a href="{LINK_KIWIFY_1}" target="_blank" style="background:#ef4444; color:#fff; padding:0.5rem 1rem; border-radius:8px; font-weight:800; text-decoration:none; font-size:0.82rem;">💎 Área VIP</a>
        </div>
    </header>

    <div class="ad-top">
        <script>atOptions={{'key':'06959dfe796ac17610a3027d9ede544f','format':'iframe','height':90,'width':728,'params':{{}}}};</script>
        <script src="https://bicea.org/22/06959dfe796ac17610a3027d9ede544f"></script>
    </div>

    <main class="container">
        <section class="pillar-box">
            <span style="background:linear-gradient(90deg,#3b82f6,#00f2fe); color:#03060c; padding:4px 12px; border-radius:20px; font-size:0.7rem; font-weight:900; text-transform:uppercase;">WebGL Neural Cluster • Enciclopédia & Hub Oficial</span>
            <h1 style="font-size:clamp(1.5rem, 4vw, 2.3rem); margin:0.8rem 0; font-weight:900;">Inteligência Artificial em 2026: O Guia Central de Automação e Disrupção</h1>
            <p style="color:#cbd5e1; font-size:0.95rem; margin-bottom:1rem;">A <strong>Inteligência Artificial (IA)</strong> deixou de ser uma promessa futurista para se tornar a infraestrutura central da economia global. Mova o cursor (ou deslize na tela) para interagir com a malha neural 3D em tempo real enquanto explora os relatórios mais recentes do setor.</p>
            <div style="display:flex; gap:10px; flex-wrap:wrap; margin-top:1.3rem;">
                <a href="{LINK_KIWIFY_2}" target="_blank" style="background:#ef4444; color:#fff; padding:0.7rem 1.2rem; border-radius:8px; font-weight:800; text-decoration:none; font-size:0.86rem;">🤖 Conhecer LUMI — Ofertas com IA &rarr;</a>
                <a href="{LINK_KIWIFY_3}" target="_blank" style="background:#3b82f6; color:#fff; padding:0.7rem 1.2rem; border-radius:8px; font-weight:800; text-decoration:none; font-size:0.86rem;">🔥 Método Posts Virais © &rarr;</a>
                <a href="{SMARTLINK_ADSTERRA}" target="_blank" style="background:rgba(255,255,255,0.08); color:#fff; padding:0.7rem 1.2rem; border-radius:8px; font-weight:700; text-decoration:none; font-size:0.86rem;">⚡ Recursos Patrocinados</a>
            </div>
        </section>

        <h2 style="font-size:1.3rem; margin-bottom:1.4rem; border-left:4px solid #00f2fe; padding-left:12px;">Últimas Notícias e Descobertas de Inteligência Artificial</h2>
        <div class="grid">{cards_ia}</div>
    </main>
    <footer>
        <p><strong>TechNews.PRO</strong> &copy; {ano_fmt} — Hub Interativo 3D de Autoridade em Inteligência Artificial.</p>
    </footer>

    <!-- SCRIPT THREE.JS REDE NEURAL 3D INTERATIVA (MOUSE & TOUCH) -->
    <script>
        window.addEventListener('DOMContentLoaded', function() {{
            if (!window.THREE) return;
            const canvas = document.getElementById('neural-webgl-canvas');
            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(65, window.innerWidth / window.innerHeight, 0.1, 1000);
            camera.position.z = 32;

            const renderer = new THREE.WebGLRenderer({{ canvas: canvas, alpha: true, antialias: true }});
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

            const particleCount = 200;
            const geometry = new THREE.BufferGeometry();
            const positions = new Float32Array(particleCount * 3);
            const colors = new Float32Array(particleCount * 3);

            for (let i = 0; i < particleCount * 3; i += 3) {{
                positions[i] = (Math.random() - 0.5) * 70;
                positions[i + 1] = (Math.random() - 0.5) * 70;
                positions[i + 2] = (Math.random() - 0.5) * 45;
                if (i % 6 === 0) {{
                    colors[i] = 0.0; colors[i + 1] = 0.95; colors[i + 2] = 1.0;
                }} else {{
                    colors[i] = 0.93; colors[i + 1] = 0.26; colors[i + 2] = 0.26;
                }}
            }}
            geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
            geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

            const material = new THREE.PointsMaterial({{ size: 0.5, vertexColors: true, transparent: true, opacity: 0.9, blending: THREE.AdditiveBlending }});
            const particles = new THREE.Points(geometry, material);
            scene.add(particles);

            const wireGeo = new THREE.IcosahedronGeometry(16, 1);
            const wireMat = new THREE.MeshBasicMaterial({{ color: 0x00f2fe, wireframe: true, transparent: true, opacity: 0.15 }});
            const wireMesh = new THREE.Mesh(wireGeo, wireMat);
            scene.add(wireMesh);

            let mouseX = 0, mouseY = 0;
            function updateMousePos(clientX, clientY) {{
                mouseX = (clientX / window.innerWidth - 0.5) * 2;
                mouseY = -(clientY / window.innerHeight - 0.5) * 2;
            }}
            window.addEventListener('mousemove', e => updateMousePos(e.clientX, e.clientY));
            window.addEventListener('touchmove', e => {{
                if (e.touches.length > 0) updateMousePos(e.touches[0].clientX, e.touches[0].clientY);
            }}, {{passive: true}});

            window.addEventListener('resize', function() {{
                camera.aspect = window.innerWidth / window.innerHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(window.innerWidth, window.innerHeight);
            }});

            let isRenderActive = true;
            document.addEventListener('visibilitychange', function() {{ isRenderActive = !document.hidden; }});

            function animate() {{
                requestAnimationFrame(animate);
                if (!isRenderActive) return;
                
                particles.rotation.y += 0.0015;
                particles.rotation.x += 0.0007;
                wireMesh.rotation.y -= 0.0020;
                
                wireMesh.rotation.x += (mouseY * 0.4 - wireMesh.rotation.x) * 0.04;
                particles.position.x += (mouseX * 4 - particles.position.x) * 0.04;
                particles.position.y += (mouseY * 4 - particles.position.y) * 0.04;
                
                renderer.render(scene, camera);
            }}
            animate();
        }});
    </script>
    <script data-cfasync="false" src="https://bicea.org/14/7843682dc41b2077e8d78d48efd6360a"></script>
</body>
</html>"""
    with open("inteligencia-artificial.html", "w", encoding="utf-8") as f:
        f.write(html_hub)

def gerar_pagina_cotacoes(dados_cot, cotacoes_html, data_fmt, ano_fmt, schema_ld):
    usd = dados_cot["USDBRL"]
    eur = dados_cot["EURBRL"]
    btc = dados_cot["BTCBRL"]

    html_cot = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Calculadora e Conversor de Dólar, Euro e Bitcoin hoje em tempo real. Dashboard financeiro gratuito para investidores e analistas.">
    <meta name="robots" content="max-image-preview:large, index, follow">
    <link rel="canonical" href="{URL_PORTAL_OFICIAL}cotacao-agora.html">
    <title>Calculadora e Cotação Dólar, Euro e Bitcoin Hoje Ao Vivo | TechNews PRO</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
    {schema_ld}
    <style>
        * {{ box-sizing: border-box; }}
        body {{ background:#070b14; color:#f8fafc; font-family:'Inter',sans-serif; margin:0; line-height:1.6; overflow-x:hidden; }}
        header {{ background:rgba(15,23,42,0.9); padding:1rem 4%; border-bottom:1px solid rgba(255,255,255,0.08); display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem; }}
        .container {{ max-width:1200px; margin:2rem auto; padding:0 4%; }}
        .cards {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(260px, 1fr)); gap:1.5rem; margin:2rem 0; }}
        .card {{ background:linear-gradient(145deg, #111827, #03060c); border:1px solid rgba(255,255,255,0.1); border-radius:16px; padding:1.8rem; text-align:center; box-shadow:0 15px 30px rgba(0,0,0,0.4); }}
        .price {{ font-size:clamp(1.8rem, 5vw, 2.4rem); font-weight:900; font-family:'JetBrains Mono',monospace; margin:0.7rem 0; }}
        .up {{ color:#10b981; }} .down {{ color:#ef4444; }}
        .calc-box {{ background:linear-gradient(145deg, rgba(16,185,129,0.12), rgba(15,23,42,0.95)); border:1px solid rgba(16,185,129,0.4); border-radius:16px; padding:1.8rem; margin:2rem 0; }}
        .calc-grid {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(210px, 1fr)); gap:1rem; margin-top:1.2rem; }}
        .calc-input-group {{ display:flex; flex-direction:column; gap:6px; }}
        .calc-input-group label {{ font-size:0.78rem; color:#94a3b8; font-weight:700; }}
        .calc-input-group input {{ background:#03060c; border:1px solid rgba(255,255,255,0.18); color:#00f2fe; padding:0.8rem; border-radius:10px; font-size:1.05rem; font-family:'JetBrains Mono',monospace; font-weight:700; width:100%; }}
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
            <a href="inteligencia-artificial.html" style="color:#00f2fe; text-decoration:none; font-weight:700; font-size:0.85rem;">🧠 Hub IA 3D</a>
            <a href="api/v1/noticias.json" target="_blank" style="color:#f59e0b; text-decoration:none; font-weight:700; font-size:0.85rem;">🔌 API JSON</a>
            <a href="{LINK_KIWIFY_1}" target="_blank" style="background:#ef4444; color:#fff; padding:0.5rem 1rem; border-radius:8px; font-weight:800; text-decoration:none; font-size:0.82rem;">💎 Área VIP</a>
        </div>
    </header>

    <div class="ad-top">
        <script>atOptions={{'key':'06959dfe796ac17610a3027d9ede544f','format':'iframe','height':90,'width':728,'params':{{}}}};</script>
        <script src="https://bicea.org/22/06959dfe796ac17610a3027d9ede544f"></script>
    </div>

    <main class="container">
        <div style="text-align:center; max-width:780px; margin:0 auto;">
            <span style="background:rgba(16,185,129,0.15); color:#10b981; border:1px solid #10b981; padding:4px 12px; border-radius:20px; font-size:0.72rem; font-weight:800;">🟢 TERMINAL FINANCEIRO & CONVERSOR AO VIVO</span>
            <h1 style="font-size:clamp(1.6rem, 4vw, 2.5rem); margin:0.9rem 0 0.5rem 0; font-weight:900;">Cotação e Calculadora Hoje: Dólar, Euro e Bitcoin</h1>
            <p style="color:#94a3b8; font-size:0.94rem;">Painel interativo sincronizado via API oficial de câmbio e criptoativos. Última aferição: <strong>{data_fmt} (BRT)</strong>.</p>
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

        <section class="calc-box">
            <h2 style="font-size:1.25rem; font-weight:900; margin-bottom:0.3rem;">⚡ Calculadora Conversora Instantânea (Câmbio & Cripto)</h2>
            <p style="font-size:0.84rem; color:#94a3b8;">Digite qualquer valor em Reais (BRL) ou Dólares (USD) para converter automaticamente na cotação oficial do dia:</p>
            <div class="calc-grid">
                <div class="calc-input-group">
                    <label>🇧🇷 Valor em Reais (R$ BRL)</label>
                    <input type="number" id="in-brl" value="1000" step="any" oninput="converterDeBRL()">
                </div>
                <div class="calc-input-group">
                    <label>🇺🇸 Equivalente em Dólar ($ USD)</label>
                    <input type="number" id="in-usd" step="any" oninput="converterDeUSD()">
                </div>
                <div class="calc-input-group">
                    <label>🇪🇺 Equivalente em Euro (€ EUR)</label>
                    <input type="text" id="out-eur" readonly>
                </div>
                <div class="calc-input-group">
                    <label>₿ Equivalente em Bitcoin (BTC)</label>
                    <input type="text" id="out-btc" readonly>
                </div>
            </div>
        </section>

        <div class="cite-box">
            <h3 style="margin-bottom:0.4rem; font-size:1.05rem;">🔗 API Pública Gratuita & Código de Citação para Desenvolvedores</h3>
            <p style="color:#94a3b8; font-size:0.85rem;">Consuma nosso endpoint JSON gratuito (<code>{URL_PORTAL_OFICIAL}api/v1/noticias.json</code>) ou incorpore o código de atribuição abaixo:</p>
            <code id="embed-code">&lt;a href="{URL_PORTAL_OFICIAL}cotacao-agora.html" target="_blank"&gt;Fonte: Terminal de Cotações &amp; API TechNews PRO&lt;/a&gt;</code>
            <br>
            <button onclick="navigator.clipboard.writeText(document.getElementById('embed-code').innerText); this.innerText='✅ Código Copiado!';" style="margin-top:8px; background:#3b82f6; color:#fff; border:none; padding:0.55rem 1.2rem; border-radius:6px; font-weight:700; cursor:pointer;">📋 Copiar Link de Citação</button>
        </div>
    </main>
    <footer>
        <p><strong>TechNews.PRO</strong> &copy; {ano_fmt} — Dados fornecidos para fins informativos e jornalísticos.</p>
    </footer>
    <script>
        const taxaUSD = {usd['raw']};
        const taxaEUR = {eur['raw']};
        const taxaBTC = {btc['raw']};

        function converterDeBRL() {{
            const brl = parseFloat(document.getElementById('in-brl').value) || 0;
            document.getElementById('in-usd').value = (brl / taxaUSD).toFixed(2);
            document.getElementById('out-eur').value = "€ " + (brl / taxaEUR).toFixed(2);
            document.getElementById('out-btc').value = (brl / taxaBTC).toFixed(6) + " BTC";
        }}
        function converterDeUSD() {{
            const usdVal = parseFloat(document.getElementById('in-usd').value) || 0;
            const brl = usdVal * taxaUSD;
            document.getElementById('in-brl').value = brl.toFixed(2);
            document.getElementById('out-eur').value = "€ " + (brl / taxaEUR).toFixed(2);
            document.getElementById('out-btc').value = (brl / taxaBTC).toFixed(6) + " BTC";
        }}
        converterDeBRL();
    </script>
    <script data-cfasync="false" src="https://bicea.org/14/7843682dc41b2077e8d78d48efd6360a"></script>
</body>
</html>"""
    with open("cotacao-agora.html", "w", encoding="utf-8") as f:
        f.write(html_cot)

def gerar_paginas_programaticas(todas_noticias, cotacoes_html, data_fmt, ano_fmt):
    urls_geradas = []
    TAGS_SEO = {
        "bitcoin": {"titulo": "Radar Bitcoin & Criptomoedas em Tempo Real", "kw": ["bitcoin", "cripto", "btc", "blockchain"]},
        "chatgpt": {"titulo": "Radar ChatGPT, OpenAI & LLMs", "kw": ["chatgpt", "openai", "gpt", "ia"]},
        "startups": {"titulo": "Radar Startups & Fintechs", "kw": ["startup", "fintech", "negócio", "empresa"]}
    }
    for slug, cfg in TAGS_SEO.items():
        filtradas = [n for n in todas_noticias if any(k in n.get('title', '').lower() for k in cfg['kw'])]
        if not filtradas: filtradas = todas_noticias[:6]
        
        cards = "".join([f"""<article style="background:rgba(17,25,40,0.88); border:1px solid rgba(255,255,255,0.08); border-radius:14px; overflow:hidden; display:flex; flex-direction:column;"><img src="{art['img']}" alt="{html.escape(art['title'])}" referrerpolicy="no-referrer" style="width:100%; height:185px; object-fit:cover;" onerror="this.src='https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=85'"><div style="padding:1.3rem; display:flex; flex-direction:column; flex-grow:1;"><span style="font-size:0.72rem; color:#ef4444; font-weight:800;">{art['source']} • {art['date']}</span><h3 style="font-size:1.08rem; margin:0.5rem 0 0.8rem 0; color:#f8fafc;">{art['title']}</h3><p style="font-size:0.85rem; color:#94a3b8; margin-bottom:1.1rem; flex-grow:1;">{art['desc']}</p><a href="{art['url']}" target="_blank" class="read-btn" style="background:#ef4444; color:#fff; text-align:center; padding:0.65rem; border-radius:8px; font-weight:700; text-decoration:none;">Ler Matéria Completa &rarr;</a></div></article>""" for art in filtradas[:8]])
        
        html_cluster = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{cfg['titulo']} | TechNews PRO</title><style>* {{ box-sizing: border-box; }} body {{ background:#070b14; color:#f8fafc; font-family:sans-serif; margin:0; line-height:1.6; overflow-x:hidden; }} header {{ background:#0f172a; padding:1rem 4%; display:flex; justify-content:space-between; flex-wrap:wrap; gap:1rem; }} .container {{ max-width:1360px; margin:2rem auto; padding:0 4%; }} .grid {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(280px, 1fr)); gap:1.5rem; }}</style></head><body><header><a href="index.html" style="font-size:1.6rem; font-weight:900; color:#fff; text-decoration:none;">TechNews<span style="color:#ef4444;">.PRO</span></a><div style="display:flex; gap:12px; align-items:center; flex-wrap:wrap;"><a href="index.html" style="color:#94a3b8; text-decoration:none;">&larr; Voltar</a><a href="{LINK_KIWIFY_1}" target="_blank" style="background:#ef4444; color:#fff; padding:0.5rem 1rem; border-radius:8px; text-decoration:none;">💎 Área VIP</a></div></header><main class="container"><h1 style="font-size:clamp(1.5rem, 4vw, 2.2rem); border-left:5px solid #ef4444; padding-left:14px;">{cfg['titulo']}</h1><div class="grid">{cards}</div></main></body></html>"""
        nome_arq = f"{slug}.html"
        with open(nome_arq, "w", encoding="utf-8") as f:
            f.write(html_cluster)
        urls_geradas.append(nome_arq)
    return urls_geradas

def gerar_sitemap_xml(urls_extras):
    hoje = datetime.now(FUSO_BRASIL).strftime("%Y-%m-%d")
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>{URL_PORTAL_OFICIAL}</loc><lastmod>{hoje}</lastmod><changefreq>hourly</changefreq><priority>1.0</priority></url>
  <url><loc>{URL_PORTAL_OFICIAL}inteligencia-artificial.html</loc><lastmod>{hoje}</lastmod><changefreq>hourly</changefreq><priority>0.9</priority></url>
  <url><loc>{URL_PORTAL_OFICIAL}cotacao-agora.html</loc><lastmod>{hoje}</lastmod><changefreq>hourly</changefreq><priority>0.9</priority></url>
  <url><loc>{URL_PORTAL_OFICIAL}futebol.html</loc><lastmod>{hoje}</lastmod><changefreq>hourly</changefreq><priority>0.9</priority></url>
  <url><loc>{URL_PORTAL_OFICIAL}api/v1/noticias.json</loc><lastmod>{hoje}</lastmod><changefreq>hourly</changefreq><priority>0.8</priority></url>
  <url><loc>{URL_PORTAL_OFICIAL}feed.xml</loc><lastmod>{hoje}</lastmod><changefreq>hourly</changefreq><priority>0.8</priority></url>"""
    for u in urls_extras:
        xml += f"\n  <url><loc>{URL_PORTAL_OFICIAL}{u}</loc><lastmod>{hoje}</lastmod><changefreq>hourly</changefreq><priority>0.8</priority></url>"
    xml += "\n</urlset>"
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(xml)

def garantir_verificacao_google():
    with open(ARQUIVO_GOOGLE_VERIF, "w", encoding="utf-8") as f:
        f.write("google-site-verification: google28d5384ab7e71bf6.html")

# ==============================================================================
# FLUXO PRINCIPAL DE GERAÇÃO DO ECOSSISTEMA V10.1 ULTIMATE
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

    print("Traduzindo e enriquecendo títulos com IA...")
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

    agora = datetime.now(FUSO_BRASIL)
    data_fmt = agora.strftime("%d/%m/%Y às %H:%M")
    data_iso = agora.strftime("%Y-%m-%dT%H:%M:%S-03:00")
    ano_fmt = str(agora.year)
    cotacoes_html, dados_cot = obter_dados_cotacoes()
    tabela_futebol = obter_tabela_brasileirao()
    widget_futebol_html = gerar_widget_futebol_html(tabela_futebol)
    noticias_json_str = json.dumps(todas_noticias, ensure_ascii=False)

    exportar_api_publica_json(todas_noticias, dados_cot, tabela_futebol, data_iso)

    destaque = todas_noticias[0]
    schema_ld = gerar_schema_json_ld(destaque, dados_cot, data_iso)

    og_title = destaque.get("title", "TechNews PRO").replace('"', '&quot;')
    og_desc = destaque.get("desc", "").replace('"', '&quot;')
    og_img = destaque.get("img", IMAGENS_FALLBACK_CATEGORIA["Tecnologia"])

    html_index = (
        HTML_TEMPLATE_INDEX
        .replace("{og_title}", og_title)
        .replace("{og_desc}", og_desc)
        .replace("{og_img}", og_img)
        .replace("{url_portal}", URL_PORTAL_OFICIAL)
        .replace("{schema_json_ld}", schema_ld)
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

    gerar_hub_ia(todas_noticias, cotacoes_html, data_fmt, ano_fmt, schema_ld)
    gerar_pagina_cotacoes(dados_cot, cotacoes_html, data_fmt, ano_fmt, schema_ld)
    gerar_pagina_futebol(tabela_futebol, todas_noticias, cotacoes_html, data_fmt, ano_fmt, schema_ld)
    urls_extras = gerar_paginas_programaticas(todas_noticias, cotacoes_html, data_fmt, ano_fmt)
    gerar_sitemap_xml(urls_extras)
    gerar_rss(todas_noticias)
    garantir_verificacao_google()

    print("✅ Ecossistema v10.1 Ultimate (Awwwards UI, Three.js Touch, GSAP Swipe, API & GEO) gerado com sucesso!")

    if not apenas_site:
        disparar_redes_omnichannel(todas_noticias[0])

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
        disparar_redes_omnichannel(noticia_pronta)
    else:
        gerar_portal(apenas_site=False)
