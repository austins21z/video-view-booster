"""
কনফিগারেশন - Windows Optimized
"""
import os
import sys

# ============================================
# মূল সেটিংস
# ============================================

# ভিউ লিমিট - 0 মানে UNLIMITED
VIEW_LIMIT = 0

# একসাথে কতটি থ্রেড (Windows এর জন্য অপটিমাইজড)
# RAM অনুযায়ী অটো সেট হবে
MAX_THREADS = 20

# প্রতিটি ভিউয়ের মধ্যে ডিলে (সেকেন্ড)
MIN_DELAY = 1
MAX_DELAY = 3

# প্রক্সি টাইমআউট
PROXY_TIMEOUT = 10
REQUEST_TIMEOUT = 25

# প্রক্সি অটো রিফ্রেশ (মিনিটে)
PROXY_REFRESH_INTERVAL = 10

# ============================================
# ফ্রি প্রক্সি সোর্স (অটো VPN এর বিকল্প)
# ============================================
PROXY_SOURCES = [
    # HTTP প্রক্সি
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
    "https://raw.githubusercontent.com/UserR3X/proxy-list/main/online/http.txt",
    "https://raw.githubusercontent.com/ErcinDedeworken/proxies/main/proxies",
    "https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-Repo/master/proxy_list.txt",
    "https://raw.githubusercontent.com/almroot/proxylist/master/list.txt",
    "https://raw.githubusercontent.com/aslisk/proxyhttps/main/https.txt",
    "https://raw.githubusercontent.com/saisuiu/Lionkings-Http-Proxys-Len/main/cnfree.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXY_LIST/master/http.txt",
    "https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/FLAVOR-FLAVIUS/proxy/main/httpproxy.txt",

    # SOCKS4 প্রক্সি
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",

    # SOCKS5 প্রক্সি
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
]

# ============================================
# সাপোর্টেড প্ল্যাটফর্ম
# ============================================
SUPPORTED_PLATFORMS = {
    "youtube": ["youtube.com", "youtu.be"],
    "facebook": ["facebook.com", "fb.watch", "fb.com"],
    "instagram": ["instagram.com"],
    "tiktok": ["tiktok.com", "vm.tiktok.com"],
    "twitter": ["twitter.com", "x.com"],
    "dailymotion": ["dailymotion.com"],
    "vimeo": ["vimeo.com"],
    "twitch": ["twitch.tv"],
    "reddit": ["reddit.com"],
    "linkedin": ["linkedin.com"],
}

# ============================================
# Windows অপটিমাইজেশন
# ============================================
def get_optimal_threads():
    """সিস্টেম অনুযায়ী অপটিমাল থ্রেড সংখ্যা"""
    try:
        import psutil
        ram_gb = psutil.virtual_memory().total / (1024**3)
        cpu_count = os.cpu_count() or 4

        if ram_gb >= 16:
            return min(50, cpu_count * 8)
        elif ram_gb >= 8:
            return min(30, cpu_count * 5)
        elif ram_gb >= 4:
            return min(20, cpu_count * 3)
        else:
            return min(10, cpu_count * 2)
    except ImportError:
        return MAX_THREADS

# অটো ডিটেক্ট
try:
    OPTIMAL_THREADS = get_optimal_threads()
except:
    OPTIMAL_THREADS = MAX_THREADS

# ============================================
# পাথ সেটিংস
# ============================================
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_FILE = os.path.join(BASE_DIR, "view_log.txt")
PROXY_FILE = os.path.join(BASE_DIR, "proxies.txt")
WORKING_PROXY_FILE = os.path.join(BASE_DIR, "working_proxies.txt")
