"""
Proxy Engine - Auto Free VPN/Proxy System
Windows Optimized - No Lag
"""

import requests
import random
import time
import threading
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import deque
from config import PROXY_SOURCES, PROXY_TIMEOUT, PROXY_REFRESH_INTERVAL


class ProxyEngine:
    def __init__(self):
        self._all_proxies = {
            "http": set(),
            "socks4": set(),
            "socks5": set(),
        }
        self._working_proxies = deque(maxlen=5000)
        self._dead_proxies = set()
        self._custom_proxies = set()
        self._lock = threading.Lock()
        self._is_fetching = False
        self._last_fetch_time = 0
        self._auto_refresh_thread = None
        self._running = True

        # পারফরম্যান্স ট্র্যাকিং
        self._proxy_scores = {}
        self._total_fetched = 0
        self._total_verified = 0

    def fetch_all_proxies(self, callback=None):
        """সব সোর্স থেকে প্রক্সি সংগ্রহ"""
        if self._is_fetching:
            return

        self._is_fetching = True
        total_new = 0

        def fetch_single(url):
            nonlocal total_new
            try:
                resp = requests.get(url, timeout=15, headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"
                })
                if resp.status_code == 200:
                    proxies = resp.text.strip().split('\n')
                    count = 0
                    for p in proxies:
                        p = p.strip().replace('\r', '')
                        if p and ':' in p and len(p) < 50:
                            # টাইপ ডিটেক্ট
                            if 'socks5' in url.lower():
                                proxy_type = 'socks5'
                            elif 'socks4' in url.lower():
                                proxy_type = 'socks4'
                            else:
                                proxy_type = 'http'

                            with self._lock:
                                if p not in self._dead_proxies:
                                    self._all_proxies[proxy_type].add(p)
                                    count += 1
                    total_new += count
                    return url[:50], count, True
            except:
                pass
            return url[:50], 0, False

        if callback:
            callback("status", "🌐 ফ্রি প্রক্সি/VPN সংগ্রহ শুরু...")

        # মাল্টিথ্রেডে দ্রুত ফেচ
        with ThreadPoolExecutor(max_workers=15) as executor:
            futures = {executor.submit(fetch_single, url): url for url in PROXY_SOURCES}

            completed = 0
            for future in as_completed(futures):
                completed += 1
                try:
                    source, count, success = future.result()
                    if callback and success and count > 0:
                        callback("progress", f"  ✅ {source}... → {count} টি প্রক্সি")
                except:
                    pass

        total = sum(len(v) for v in self._all_proxies.values())
        self._total_fetched = total
        self._last_fetch_time = time.time()
        self._is_fetching = False

        if callback:
            callback("done", f"\n📊 মোট সংগ্রহ: {total} টি প্রক্সি "
                            f"(HTTP: {len(self._all_proxies['http'])} | "
                            f"SOCKS4: {len(self._all_proxies['socks4'])} | "
                            f"SOCKS5: {len(self._all_proxies['socks5'])})")

        return total

    def verify_proxies(self, max_workers=80, max_check=500, callback=None):
        """প্রক্সি ভেরিফাই - Windows Optimized"""
        all_list = []
        for ptype, proxies in self._all_proxies.items():
            for p in proxies:
                if p not in self._dead_proxies:
                    all_list.append((p, ptype))

        # শুধু র্যান্ডম max_check টি ভেরিফাই করি (দ্রুত)
        if len(all_list) > max_check:
            random.shuffle(all_list)
            all_list = all_list[:max_check]

        if not all_list:
            if callback:
                callback("error", "❌ কোনো প্রক্সি নেই ভেরিফাই করার জন্য")
            return 0

        if callback:
            callback("status", f"🔍 {len(all_list)} টি প্রক্সি ভেরিফাই হচ্ছে...")

        verified = 0
        checked = 0
        total = len(all_list)

        def check_one(proxy_data):
            nonlocal verified, checked
            proxy, ptype = proxy_data
            is_working = self._test_single_proxy(proxy, ptype)

            with self._lock:
                checked += 1
                if is_working:
                    self._working_proxies.append((proxy, ptype))
                    self._proxy_scores[proxy] = 100
                    verified += 1
                else:
                    self._dead_proxies.add(proxy)

            if callback and checked % 20 == 0:
                callback("progress", f"  📊 {checked}/{total} চেক হয়েছে | ✅ {verified} টি ওয়ার্কিং")

            return is_working

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(check_one, all_list)

        self._total_verified = verified

        if callback:
            callback("done", f"\n✅ ভেরিফাই সম্পন্ন: {verified} টি ওয়ার্কিং / {total} টি চেক")

        return verified

    def _test_single_proxy(self, proxy, ptype="http"):
        """একটি প্রক্সি টেস্ট"""
        if ptype == "http":
            proxy_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
        elif ptype == "socks4":
            proxy_dict = {"http": f"socks4://{proxy}", "https": f"socks4://{proxy}"}
        elif ptype == "socks5":
            proxy_dict = {"http": f"socks5://{proxy}", "https": f"socks5://{proxy}"}
        else:
            proxy_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"}

        test_urls = [
            "http://httpbin.org/ip",
            "http://ip-api.com/json",
            "https://api.ipify.org?format=json",
            "http://ifconfig.me/ip",
        ]

        try:
            resp = requests.get(
                random.choice(test_urls),
                proxies=proxy_dict,
                timeout=PROXY_TIMEOUT,
                headers={"User-Agent": "Mozilla/5.0"}
            )
            return resp.status_code == 200
        except:
            return False

    def get_random_proxy(self):
        """র্যান্ডম ওয়ার্কিং প্রক্সি দেয়"""
        # প্রথমে ওয়ার্কিং লিস্ট থেকে
        if self._working_proxies:
            proxy, ptype = random.choice(list(self._working_proxies))
            return self._format_proxy(proxy, ptype), proxy

        # কাস্টম প্রক্সি
        if self._custom_proxies:
            proxy = random.choice(list(self._custom_proxies))
            return {"http": f"http://{proxy}", "https": f"http://{proxy}"}, proxy

        # আনভেরিফাইড থেকে
        for ptype in ["http", "socks5", "socks4"]:
            if self._all_proxies[ptype]:
                proxy = random.choice(list(self._all_proxies[ptype]))
                return self._format_proxy(proxy, ptype), proxy

        return None, None

    def _format_proxy(self, proxy, ptype):
        """প্রক্সি ফরম্যাট করে"""
        if ptype == "socks5":
            return {"http": f"socks5://{proxy}", "https": f"socks5://{proxy}"}
        elif ptype == "socks4":
            return {"http": f"socks4://{proxy}", "https": f"socks4://{proxy}"}
        else:
            return {"http": f"http://{proxy}", "https": f"http://{proxy}"}

    def mark_proxy_dead(self, proxy_str):
        """একটি প্রক্সি ডেড হিসেবে মার্ক"""
        with self._lock:
            self._dead_proxies.add(proxy_str)
            # ওয়ার্কিং লিস্ট থেকে সরান
            self._working_proxies = deque(
                [(p, t) for p, t in self._working_proxies if p != proxy_str],
                maxlen=5000
            )

    def mark_proxy_good(self, proxy_str):
        """ভালো প্রক্সির স্কোর বাড়ান"""
        with self._lock:
            self._proxy_scores[proxy_str] = self._proxy_scores.get(proxy_str, 50) + 10

    def add_custom_proxy(self, proxy):
        """কাস্টম প্রক্সি যোগ"""
        proxy = proxy.strip()
        if proxy and ':' in proxy:
            self._custom_proxies.add(proxy)
            return True
        return False

    def load_from_file(self, filepath="proxies.txt"):
        """ফাইল থেকে প্রক্সি লোড"""
        count = 0
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and ':' in line and not line.startswith('#'):
                        self._custom_proxies.add(line)
                        count += 1
        return count

    def save_working(self, filepath="working_proxies.txt"):
        """ওয়ার্কিং প্রক্সি সেভ"""
        with open(filepath, 'w') as f:
            for proxy, ptype in self._working_proxies:
                f.write(f"{proxy} # {ptype}\n")
        return len(self._working_proxies)

    def start_auto_refresh(self, callback=None):
        """অটো রিফ্রেশ থ্রেড শুরু"""
        def refresh_loop():
            while self._running:
                time.sleep(PROXY_REFRESH_INTERVAL * 60)
                if self._running:
                    if callback:
                        callback("status", "🔄 প্রক্সি অটো রিফ্রেশ হচ্ছে...")
                    self.fetch_all_proxies(callback)
                    self.verify_proxies(max_check=200, callback=callback)

        self._auto_refresh_thread = threading.Thread(target=refresh_loop, daemon=True)
        self._auto_refresh_thread.start()

    def stop(self):
        """ইঞ্জিন বন্ধ"""
        self._running = False

    def get_stats(self):
        """পরিসংখ্যান"""
        return {
            "total_fetched": sum(len(v) for v in self._all_proxies.values()),
            "http": len(self._all_proxies["http"]),
            "socks4": len(self._all_proxies["socks4"]),
            "socks5": len(self._all_proxies["socks5"]),
            "working": len(self._working_proxies),
            "dead": len(self._dead_proxies),
            "custom": len(self._custom_proxies),
        }
