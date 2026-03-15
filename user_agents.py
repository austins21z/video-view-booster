"""
User Agent Manager - 200+ Unique User Agents
Windows Optimized - Memory Efficient
"""

import random
import hashlib
import time


class UserAgentManager:
    def __init__(self):
        self._agents = self._build_agents()
        self._referers = self._build_referers()
        self._languages = self._build_languages()
        self._platforms = self._build_platform_hints()

    def _build_agents(self):
        """200+ ইউজার এজেন্ট"""
        agents = []
        
        # Chrome versions (Windows)
        chrome_versions = list(range(100, 122))
        for v in chrome_versions:
            agents.append(f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v}.0.0.0 Safari/537.36")
            agents.append(f"Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v}.0.0.0 Safari/537.36")

        # Chrome (Mac)
        for v in chrome_versions[-15:]:
            agents.append(f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v}.0.0.0 Safari/537.36")

        # Chrome (Linux)
        for v in chrome_versions[-10:]:
            agents.append(f"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v}.0.0.0 Safari/537.36")

        # Firefox versions
        for v in range(100, 122):
            agents.append(f"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:{v}.0) Gecko/20100101 Firefox/{v}.0")
            if v > 110:
                agents.append(f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:{v}.0) Gecko/20100101 Firefox/{v}.0")
                agents.append(f"Mozilla/5.0 (X11; Linux x86_64; rv:{v}.0) Gecko/20100101 Firefox/{v}.0")

        # Edge
        for v in range(100, 122):
            agents.append(f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v}.0.0.0 Safari/537.36 Edg/{v}.0.0.0")

        # Safari
        safari_versions = ["16.4", "16.5", "16.6", "17.0", "17.1", "17.2"]
        for sv in safari_versions:
            agents.append(f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{sv} Safari/605.1.15")

        # Mobile - Android
        android_devices = [
            "SM-S918B", "SM-S911B", "SM-G998B", "SM-A546B", "SM-A536B",
            "Pixel 8 Pro", "Pixel 7a", "Pixel 8", "Pixel 7",
            "OnePlus 12", "OnePlus 11", "OnePlus Nord",
            "Redmi Note 12 Pro", "Redmi Note 13", "POCO X5 Pro",
            "M2101K6G", "RMX3630", "V2227", "CPH2451",
        ]
        for device in android_devices:
            for av in [12, 13, 14]:
                for cv in [118, 119, 120, 121]:
                    agents.append(f"Mozilla/5.0 (Linux; Android {av}; {device}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{cv}.0.6099.144 Mobile Safari/537.36")

        # Mobile - iPhone
        ios_versions = [
            ("16_6", "16.6"), ("16_7", "16.7"), 
            ("17_0", "17.0"), ("17_1", "17.1"), ("17_2", "17.2")
        ]
        for ios_v, saf_v in ios_versions:
            agents.append(f"Mozilla/5.0 (iPhone; CPU iPhone OS {ios_v} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{saf_v} Mobile/15E148 Safari/604.1")
            agents.append(f"Mozilla/5.0 (iPhone; CPU iPhone OS {ios_v} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/120.0.6099.119 Mobile/15E148 Safari/604.1")

        # Opera
        for v in [104, 105, 106]:
            agents.append(f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/{v}.0.0.0")

        # Brave
        agents.append("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Brave/120")
        agents.append("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Brave/119")

        # Samsung Browser
        agents.append("Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/23.0 Chrome/115.0.0.0 Mobile Safari/537.36")
        agents.append("Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/22.0 Chrome/111.0.0.0 Mobile Safari/537.36")

        return agents

    def _build_referers(self):
        return [
            "https://www.google.com/",
            "https://www.google.co.in/",
            "https://www.google.co.uk/",
            "https://www.google.com.bd/",
            "https://www.google.de/",
            "https://www.google.fr/",
            "https://www.google.es/",
            "https://www.google.com.br/",
            "https://www.google.co.jp/",
            "https://www.bing.com/",
            "https://search.yahoo.com/",
            "https://duckduckgo.com/",
            "https://www.facebook.com/",
            "https://twitter.com/",
            "https://www.reddit.com/",
            "https://t.co/",
            "https://www.instagram.com/",
            "https://www.linkedin.com/",
            "https://www.pinterest.com/",
            "https://web.whatsapp.com/",
            "https://telegram.org/",
            "https://www.tiktok.com/",
            "",
        ]

    def _build_languages(self):
        return [
            "en-US,en;q=0.9",
            "en-GB,en;q=0.9",
            "en-US,en;q=0.9,bn;q=0.8",
            "bn-BD,bn;q=0.9,en-US;q=0.8,en;q=0.7",
            "hi-IN,hi;q=0.9,en-US;q=0.8",
            "es-ES,es;q=0.9,en;q=0.8",
            "fr-FR,fr;q=0.9,en;q=0.8",
            "de-DE,de;q=0.9,en;q=0.8",
            "pt-BR,pt;q=0.9,en;q=0.8",
            "ja-JP,ja;q=0.9,en;q=0.8",
            "ko-KR,ko;q=0.9,en;q=0.8",
            "zh-CN,zh;q=0.9,en;q=0.8",
            "ar-SA,ar;q=0.9,en;q=0.8",
            "ru-RU,ru;q=0.9,en;q=0.8",
            "it-IT,it;q=0.9,en;q=0.8",
            "tr-TR,tr;q=0.9,en;q=0.8",
            "id-ID,id;q=0.9,en;q=0.8",
            "th-TH,th;q=0.9,en;q=0.8",
            "vi-VN,vi;q=0.9,en;q=0.8",
            "nl-NL,nl;q=0.9,en;q=0.8",
        ]

    def _build_platform_hints(self):
        return [
            '"Windows"', '"macOS"', '"Linux"',
            '"Android"', '"iOS"', '"Chrome OS"',
        ]

    def get_random_headers(self):
        """সম্পূর্ণ র্যান্ডম ইউনিক হেডার"""
        ua = random.choice(self._agents)
        ref = random.choice(self._referers)

        headers = {
            "User-Agent": ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": random.choice(self._languages),
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": random.choice(["none", "cross-site", "same-origin", "same-site"]),
            "Sec-Fetch-User": "?1",
            "Cache-Control": random.choice(["max-age=0", "no-cache", ""]),
            "DNT": random.choice(["1", "0"]),
            "Sec-Ch-Ua-Platform": random.choice(self._platforms),
        }

        if ref:
            headers["Referer"] = ref

        # ইউনিক ফিঙ্গারপ্রিন্ট
        unique_seed = f"{ua}{time.time()}{random.random()}"
        fp = hashlib.md5(unique_seed.encode()).hexdigest()[:16]

        return headers, fp

    def total_agents(self):
        return len(self._agents)
