#!/usr/bin/env python3
"""
🎬 Video View Booster - UNLIMITED Edition
Windows Optimized CLI Version
"""

import os
import sys
import time
import threading

# Windows console fix
if os.name == 'nt':
    os.system('chcp 65001 >nul 2>&1')
    os.system('color')

from colorama import Fore, Back, Style, init
init(autoreset=True, convert=True)

from viewer_engine import ViewerEngine
from config import OPTIMAL_THREADS


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def banner():
    print(f"""{Fore.CYAN}
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   ██╗   ██╗██╗███████╗██╗    ██╗  ██████╗  ██████╗       ║
    ║   ██║   ██║██║██╔════╝██║    ██║  ██╔══██╗██╔═══██╗      ║
    ║   ██║   ██║██║█████╗  ██║ █╗ ██║  ██████╔╝██║   ██║      ║
    ║   ╚██╗ ██╔╝██║██╔══╝  ██║███╗██║  ██╔══██╗██║   ██║      ║
    ║    ╚████╔╝ ██║███████╗╚███╔███╔╝  ██████╔╝╚██████╔╝      ║
    ║     ╚═══╝  ╚═╝╚══════╝ ╚══╝╚══╝  ╚═════╝  ╚═════╝       ║
    ║                                                           ║
    ║     🎬  UNLIMITED Video View Booster v3.0                 ║
    ║     🌐  Auto Free VPN/Proxy System                        ║
    ║     💻  Windows Optimized                                 ║
    ║     ∞   No View Limit                                     ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    {Style.RESET_ALL}""")


def menu():
    print(f"""
    {Fore.YELLOW}╔═══════════════════════════════════════════╗
    ║           📋 মেইন মেনু                    ║
    ╠═══════════════════════════════════════════╣
    ║                                           ║
    ║  {Fore.GREEN}[1]{Fore.YELLOW} 🚀 UNLIMITED ভিউ বুস্ট শুরু        ║
    ║  {Fore.GREEN}[2]{Fore.YELLOW} 🌐 অটো ফ্রি VPN/প্রক্সি সংগ্রহ     ║
    ║  {Fore.GREEN}[3]{Fore.YELLOW} ✅ প্রক্সি ভেরিফাই                  ║
    ║  {Fore.GREEN}[4]{Fore.YELLOW} ➕ কাস্টম প্রক্সি/IP যোগ           ║
    ║  {Fore.GREEN}[5]{Fore.YELLOW} 📂 ফাইল থেকে প্রক্সি লোড           ║
    ║  {Fore.GREEN}[6]{Fore.YELLOW} 📊 সিস্টেম স্ট্যাটাস               ║
    ║  {Fore.GREEN}[7]{Fore.YELLOW} 🔄 সব একসাথে (Auto Setup + Run)    ║
    ║  {Fore.GREEN}[8]{Fore.YELLOW} 💾 ওয়ার্কিং প্রক্সি সেভ           ║
    ║  {Fore.GREEN}[9]{Fore.YELLOW} ❓ সাহায্য                          ║
    ║  {Fore.GREEN}[0]{Fore.YELLOW} 🚪 বের হন                          ║
    ║                                           ║
    ╚═══════════════════════════════════════════╝{Style.RESET_ALL}
    """)


def log_callback(msg_type, message):
    """প্রক্সি ফেচ/ভেরিফাই লগ"""
    colors = {
        "status": Fore.CYAN,
        "progress": Fore.GREEN,
        "done": Fore.YELLOW,
        "error": Fore.RED,
    }
    color = colors.get(msg_type, Fore.WHITE)
    print(f"    {color}{message}{Style.RESET_ALL}")


def live_log_thread(engine):
    """লাইভ লগ দেখায়"""
    while engine.is_running():
        try:
            level, timestamp, message = engine.log_queue.get(timeout=1)
            colors = {
                "success": Fore.GREEN,
                "fail": Fore.RED,
                "warn": Fore.YELLOW,
                "info": Fore.CYAN,
                "error": Fore.RED,
            }
            color = colors.get(level, Fore.WHITE)
            print(f"    {Fore.WHITE}[{timestamp}] {color}{message}{Style.RESET_ALL}")
        except:
            pass


def main():
    clear()
    banner()

    engine = ViewerEngine()

    while True:
        menu()

        try:
            choice = input(f"    {Fore.GREEN}👉 পছন্দ করুন: {Style.RESET_ALL}").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n    {Fore.YELLOW}👋 বিদায়!{Style.RESET_ALL}")
            engine.proxy_engine.stop()
            sys.exit(0)

        # ─────────────────────────────────────────
        # [1] UNLIMITED ভিউ বুস্ট
        # ─────────────────────────────────────────
        if choice == "1":
            print(f"\n    {Fore.CYAN}🎬 UNLIMITED ভিউ বুস্টার সেটআপ{Style.RESET_ALL}")
            print(f"    {Fore.CYAN}{'─'*45}{Style.RESET_ALL}")

            url = input(f"\n    {Fore.WHITE}📌 ভিডিও URL: {Style.RESET_ALL}").strip()
            if not url:
                print(f"    {Fore.RED}❌ URL দিতে হবে!{Style.RESET_ALL}")
                continue
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url

            platform = engine.detect_platform(url)
            print(f"    {Fore.GREEN}🌐 Platform: {platform.upper()}{Style.RESET_ALL}")

            # ভিউ টার্গেট
            view_input = input(f"    {Fore.WHITE}🎯 ভিউ সংখ্যা (0=UNLIMITED ∞): {Style.RESET_ALL}").strip()
            try:
                target = int(view_input) if view_input else 0
            except:
                target = 0

            # থ্রেড
            thread_input = input(f"    {Fore.WHITE}🧵 থ্রেড সংখ্যা (ডিফল্ট={OPTIMAL_THREADS}, সর্বোচ্চ সুপারিশ=50): {Style.RESET_ALL}").strip()
            try:
                threads = int(thread_input) if thread_input else OPTIMAL_THREADS
                threads = min(threads, 100)  # সেফটি লিমিট
            except:
                threads = OPTIMAL_THREADS

            # প্রক্সি চেক
            stats = engine.proxy_engine.get_stats()
            if stats['working'] == 0 and stats['total_fetched'] == 0 and stats['custom'] == 0:
                print(f"\n    {Fore.YELLOW}⚠️ কোনো প্রক্সি লোড করা হয়নি!{Style.RESET_ALL}")
                auto = input(f"    {Fore.WHITE}অটো সংগ্রহ করতে চান? (y/n): {Style.RESET_ALL}").strip().lower()
                if auto == 'y':
                    engine.proxy_engine.fetch_all_proxies(log_callback)
                    engine.proxy_engine.verify_proxies(max_check=300, callback=log_callback)
                else:
                    no_proxy = input(f"    {Fore.WHITE}প্রক্সি ছাড়াই চালাতে চান? (y/n): {Style.RESET_ALL}").strip().lower()
                    if no_proxy != 'y':
                        continue

            # কনফার্ম
            print(f"\n    {Fore.YELLOW}{'─'*45}")
            print(f"    📌 URL: {url}")
            print(f"    🎯 Target: {'UNLIMITED ∞' if target == 0 else target}")
            print(f"    🧵 Threads: {threads}")
            print(f"    🌐 Working Proxies: {engine.proxy_engine.get_stats()['working']}")
            print(f"    {'─'*45}{Style.RESET_ALL}")
            
            confirm = input(f"\n    {Fore.WHITE}▶️ শুরু করতে চান? (y/n): {Style.RESET_ALL}").strip().lower()
            if confirm != 'y':
                continue

            print(f"\n    {Fore.GREEN}🚀 শুরু হচ্ছে... (বন্ধ করতে Ctrl+C চাপুন){Style.RESET_ALL}\n")

            # লাইভ লগ থ্রেড
            log_thread = threading.Thread(target=live_log_thread, args=(engine,), daemon=True)
            log_thread.start()

            # অটো প্রক্সি রিফ্রেশ শুরু
            engine.proxy_engine.start_auto_refresh(log_callback)

            try:
                engine.start_unlimited(url, threads, target)
            except KeyboardInterrupt:
                engine.stop()
                print(f"\n    {Fore.YELLOW}⛔ বন্ধ করা হয়েছে{Style.RESET_ALL}")

            time.sleep(2)

        # ─────────────────────────────────────────
        # [2] ফ্রি প্রক্সি সংগ্রহ
        # ─────────────────────────────────────────
        elif choice == "2":
            print(f"\n    {Fore.CYAN}🌐 অটো ফ্রি VPN/প্রক্সি সংগ্রহ{Style.RESET_ALL}\n")
            engine.proxy_engine.fetch_all_proxies(log_callback)

            auto_verify = input(f"\n    {Fore.WHITE}এখনই ভেরিফাই করতে চান? (y/n): {Style.RESET_ALL}").strip().lower()
            if auto_verify == 'y':
                engine.proxy_engine.verify_proxies(callback=log_callback)

        # ─────────────────────────────────────────
        # [3] প্রক্সি ভেরিফাই
        # ─────────────────────────────────────────
        elif choice == "3":
            count_input = input(f"    {Fore.WHITE}কতটি চেক করবেন? (ডিফল্ট=500): {Style.RESET_ALL}").strip()
            try:
                max_check = int(count_input) if count_input else 500
            except:
                max_check = 500
            engine.proxy_engine.verify_proxies(max_check=max_check, callback=log_callback)

        # ─────────────────────────────────────────
        # [4] কাস্টম প্রক্সি যোগ
        # ─────────────────────────────────────────
        elif choice == "4":
            print(f"\n    {Fore.CYAN}➕ কাস্টম প্রক্সি/IP যোগ করুন{Style.RESET_ALL}")
            print(f"    {Fore.WHITE}ফরম্যাট: IP:PORT{Style.RESET_ALL}")
            print(f"    {Fore.WHITE}শেষ করতে 'done' লিখুন{Style.RESET_ALL}\n")

            count = 0
            while True:
                proxy = input(f"    {Fore.YELLOW}>> {Style.RESET_ALL}").strip()
                if proxy.lower() == 'done':
                    break
                if engine.proxy_engine.add_custom_proxy(proxy):
                    count += 1
                    print(f"    {Fore.GREEN}✅ যোগ হয়েছে: {proxy}{Style.RESET_ALL}")
                else:
                    print(f"    {Fore.RED}❌ ভুল ফরম্যাট{Style.RESET_ALL}")

            print(f"\n    {Fore.GREEN}মোট {count} টি কাস্টম প্রক্সি যোগ হয়েছে{Style.RESET_ALL}")

        # ─────────────────────────────────────────
        # [5] ফাইল থেকে লোড
        # ─────────────────────────────────────────
        elif choice == "5":
            filepath = input(f"    {Fore.WHITE}ফাইল পাথ (ডিফল্ট=proxies.txt): {Style.RESET_ALL}").strip()
            if not filepath:
                filepath = "proxies.txt"
            count = engine.proxy_engine.load_from_file(filepath)
            print(f"    {Fore.GREEN}📂 {count} টি প্রক্সি লোড হয়েছে{Style.RESET_ALL}")

        # ─────────────────────────────────────────
        # [6] সিস্টেম স্ট্যাটাস
        # ─────────────────────────────────────────
        elif choice == "6":
            stats = engine.proxy_engine.get_stats()
            view_stats = engine.get_stats()
            print(f"""
    {Fore.CYAN}╔═══════════════════════════════════════════╗
    ║         📊 সিস্টেম স্ট্যাটাস              ║
    ╠═══════════════════════════════════════════╣
    ║                                           ║
    ║  {Fore.WHITE}🌐 প্রক্সি পরিসংখ্যান:{Fore.CYAN}                  ║
    ║  {Fore.WHITE}   HTTP:     {stats['http']:>6} টি{Fore.CYAN}                ║
    ║  {Fore.WHITE}   SOCKS4:   {stats['socks4']:>6} টি{Fore.CYAN}                ║
    ║  {Fore.WHITE}   SOCKS5:   {stats['socks5']:>6} টি{Fore.CYAN}                ║
    ║  {Fore.GREEN}   ✅ Working: {stats['working']:>5} টি{Fore.CYAN}               ║
    ║  {Fore.RED}   ❌ Dead:    {stats['dead']:>5} টি{Fore.CYAN}               ║
    ║  {Fore.YELLOW}   📝 Custom:  {stats['custom']:>5} টি{Fore.CYAN}               ║
    ║                                           ║
    ║  {Fore.WHITE}🎬 ভিউ পরিসংখ্যান:{Fore.CYAN}                     ║
    ║  {Fore.GREEN}   ✅ সফল:     {view_stats['success']:>6}{Fore.CYAN}                ║
    ║  {Fore.RED}   ❌ ব্যর্থ:   {view_stats['fail']:>6}{Fore.CYAN}                ║
    ║  {Fore.WHITE}   📊 মোট:     {view_stats['total']:>6}{Fore.CYAN}                ║
    ║                                           ║
    ║  {Fore.WHITE}💻 Optimal Threads: {OPTIMAL_THREADS}{Fore.CYAN}               ║
    ║  {Fore.WHITE}👤 User Agents: {engine.ua_manager.total_agents()}+{Fore.CYAN}                ║
    ║                                           ║
    ╚═══════════════════════════════════════════╝{Style.RESET_ALL}
            """)

        # ─────────────────────────────────────────
        # [7] সব একসাথে (Auto Setup + Run)
        # ─────────────────────────────────────────
        elif choice == "7":
            print(f"\n    {Fore.CYAN}🔄 ওয়ান-ক্লিক অটো সেটআপ{Style.RESET_ALL}\n")

            url = input(f"    {Fore.WHITE}📌 ভিডিও URL: {Style.RESET_ALL}").strip()
            if not url:
                continue
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url

            print(f"\n    {Fore.CYAN}ধাপ ১: প্রক্সি সংগ্রহ...{Style.RESET_ALL}")
            engine.proxy_engine.fetch_all_proxies(log_callback)

            print(f"\n    {Fore.CYAN}ধাপ ২: প্রক্সি ভেরিফাই...{Style.RESET_ALL}")
            engine.proxy_engine.verify_proxies(max_check=300, callback=log_callback)

            working = engine.proxy_engine.get_stats()['working']
            if working == 0:
                print(f"\n    {Fore.RED}❌ কোনো ওয়ার্কিং প্রক্সি পাওয়া যায়নি{Style.RESET_ALL}")
                force = input(f"    {Fore.WHITE}তবুও চালাতে চান? (y/n): {Style.RESET_ALL}").strip().lower()
                if force != 'y':
                    continue

            print(f"\n    {Fore.CYAN}ধাপ ৩: UNLIMITED ভিউ বুস্ট শুরু...{Style.RESET_ALL}")
            print(f"    {Fore.YELLOW}বন্ধ করতে Ctrl+C চাপুন{Style.RESET_ALL}\n")

            log_thread = threading.Thread(target=live_log_thread, args=(engine,), daemon=True)
            log_thread.start()
            engine.proxy_engine.start_auto_refresh(log_callback)

            try:
                engine.start_unlimited(url, OPTIMAL_THREADS, 0)
            except KeyboardInterrupt:
                engine.stop()

            time.sleep(2)

        # ─────────────────────────────────────────
        # [8] ওয়ার্কিং প্রক্সি সেভ
        # ─────────────────────────────────────────
        elif choice == "8":
            count = engine.proxy_engine.save_working()
            print(f"    {Fore.GREEN}💾 {count} টি ওয়ার্কিং প্রক্সি সেভ হয়েছে{Style.RESET_ALL}")

        # ─────────────────────────────────────────
        # [9] সাহায্য
        # ─────────────────────────────────────────
        elif choice == "9":
            print(f"""
    {Fore.CYAN}╔═══════════════════════════════════════════════════════════╗
    ║                    ❓ সাহায্য / Help                      ║
    ╠═══════════════════════════════════════════════════════════╣
    ║                                                           ║
    ║  🔹 সাপোর্টেড প্ল্যাটফর্ম:                               ║
    ║     YouTube, Facebook, Instagram, TikTok,                 ║
    ║     Twitter/X, Dailymotion, Vimeo, Twitch                 ║
    ║                                                           ║
    ║  🔹 দ্রুত শুরু করতে:                                     ║
    ║     অপশন [7] চাপুন → URL দিন → সব অটো হবে               ║
    ║                                                           ║
    ║  🔹 UNLIMITED মোড:                                        ║
    ║     ভিউ সংখ্যায় 0 দিলে থামবে না, ম্যানুয়ালি            ║
    ║     Ctrl+C দিয়ে বন্ধ করতে হবে                            ║
    ║                                                           ║
    ║  🔹 প্রক্সি অটো রিফ্রেশ:                                 ║
    ║     প্রতি ১০ মিনিটে নতুন প্রক্সি সংগ্রহ হয়             ║
    ║                                                           ║
    ║  🔹 কাস্টম প্রক্সি:                                      ║
    ║     proxies.txt ফাইলে রাখুন (প্রতি লাইনে IP:PORT)        ║
    ║     অথবা অপশন [4] দিয়ে ম্যানুয়ালি যোগ করুন            ║
    ║                                                           ║
    ║  🔹 .EXE বানাতে:                                          ║
    ║     build.bat ফাইল ডাবল ক্লিক করুন                       ║
    ║                                                           ║
    ║  ⚠️ শুধুমাত্র শিক্ষামূলক উদ্দেশ্যে                      ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝{Style.RESET_ALL}
            """)

        # ─────────────────────────────────────────
        # [0] বের হন
        # ─────────────────────────────────────────
        elif choice == "0":
            engine.proxy_engine.stop()
            print(f"\n    {Fore.YELLOW}👋 বিদায়! ধন্যবাদ।{Style.RESET_ALL}")
            sys.exit(0)

        else:
            print(f"    {Fore.RED}❌ ভুল পছন্দ!{Style.RESET_ALL}")

        input(f"\n    {Fore.WHITE}⏎ Enter চাপুন...{Style.RESET_ALL}")
        clear()
        banner()


if __name__ == "__main__":
    main()
