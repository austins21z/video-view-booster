@echo off
chcp 65001 >nul
title Video View Booster - EXE Builder
color 0A

echo.
echo ╔═══════════════════════════════════════════╗
echo ║   🔨 EXE বিল্ডার                         ║
echo ║   Video View Booster                      ║
echo ╚═══════════════════════════════════════════╝
echo.

echo [1/3] Dependencies ইনস্টল হচ্ছে...
pip install -r requirements.txt
pip install pyinstaller

echo.
echo [2/3] EXE বিল্ড হচ্ছে...
echo       এটি কয়েক মিনিট সময় নিতে পারে...
echo.

pyinstaller --onefile ^
    --name "VideoViewBooster" ^
    --icon "NONE" ^
    --console ^
    --add-data "config.py;." ^
    --add-data "user_agents.py;." ^
    --add-data "proxy_engine.py;." ^
    --add-data "viewer_engine.py;." ^
    --hidden-import requests ^
    --hidden-import colorama ^
    --hidden-import queue ^
    --hidden-import threading ^
    --hidden-import hashlib ^
    --hidden-import socks ^
    --collect-all requests ^
    --collect-all certifi ^
    --collect-all urllib3 ^
    --noupx ^
    main.py

echo.
echo [3/3] বিল্ড সম্পন্ন!
echo.

if exist "dist\VideoViewBooster.exe" (
    echo ╔═══════════════════════════════════════════╗
    echo ║  ✅ EXE ফাইল তৈরি হয়েছে!                ║
    echo ║                                           ║
    echo ║  📂 লোকেশন: dist\VideoViewBooster.exe     ║
    echo ║                                           ║
    echo ║  এটি ডাবল ক্লিক করেই চালাতে পারবেন       ║
    echo ╚═══════════════════════════════════════════╝
    echo.
    echo dist ফোল্ডার ওপেন করা হচ্ছে...
    explorer dist
) else (
    echo ╔═══════════════════════════════════════════╗
    echo ║  ❌ বিল্ড ব্যর্থ হয়েছে!                  ║
    echo ║  নিচের এরর চেক করুন                      ║
    echo ╚═══════════════════════════════════════════╝
)

echo.
pause
