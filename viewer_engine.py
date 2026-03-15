"""
Viewer Engine - Unlimited View Booster
Windows Optimized - No Memory Leak
"""

import requests
import time
import random
import threading
import queue
from datetime import datetime
from user_agents import UserAgentManager
from proxy_engine import ProxyEngine
from config import MIN_DELAY, MAX_DELAY, REQUEST_TIMEOUT, SUPPORTED_PLATFORMS


class ViewerEngine:
    def __init__(self):
        self.ua_manager = UserAgentManager()
        self.proxy_engine = ProxyEngine()

        # কাউন্টার
        self.success_count = 0
        self.fail_count = 0
        self.total_attempts = 0
        self.views_per_minute = 0

        # কন্ট্রোল
        self._running = False
        self._paused = False
        self._lock = threading.Lock()
        self._start_time = None
        self._minute_counter = 0
        self._last_minute_check = 0

        # লগ কিউ
        self.log_queue = queue.Queue(maxsize=1000)

    def detect_platform(self, url):
        """প্ল্যাটফর্ম ডিটেক্ট"""
        url_lower = url.lower()
        for platform, domains in SUPPORTED_PLATFORMS.items():
            for domain in domains:
                if domain in url_lower:
                    return platform
        return "unknown"

    def _send_single_view(self, url, view_num):
        """একটি ভিউ পাঠায় - Memory Efficient"""
        if not self._running or self._paused:
            return False

        headers, fingerprint = self.ua_manager.get_random_headers()
        proxy_dict, proxy_str = self.proxy_engine.get_random_proxy()

        try:
            session = requests.Session()
            session.headers.update(headers)

            kwargs = {
                "timeout": REQUEST_TIMEOUT,
                "allow_redirects": True,
                "stream": False,
            }

            if proxy_dict:
                kwargs["proxies"] = proxy_dict

            response = session.get(url, **kwargs)

            # সেশন বন্ধ করি (মেমরি ফ্রি)
            session.close()

            if response.status_code in [200, 301, 302, 303]:
                with self._lock:
                    self.success_count += 1
                    self.total_attempts += 1
                    self._minute_counter += 1

                if proxy_str:
                    self.proxy_engine.mark_proxy_good(proxy_str)

                log_msg = (
                    f"✅ #{view_num} | "
                    f"Status: {response.status_code} | "
                    f"IP: {(proxy_str or 'Direct')[:25]} | "
                    f"UA: {headers['User-Agent'][:40]}..."
                )
                self._add_log("success", log_msg)
                return True
            else:
                with self._lock:
                    self.fail_count += 1
                    self.total_attempts += 1

                self._add_log("fail", f"❌ #{view_num} | Status: {response.status_code}")
                return False

        except requests.exceptions.ProxyError:
            with self._lock:
                self.fail_count += 1
                self.total_attempts += 1
            if proxy_str:
                self.proxy_engine.mark_proxy_dead(proxy_str)
            self._add_log("warn", f"⚠️ #{view_num} | প্রক্সি ডেড: {(proxy_str or '')[:25]}")
            return False

        except requests.exceptions.Timeout:
            with self._lock:
                self.fail_count += 1
                self.total_attempts += 1
            self._add_log("warn", f"⏱️ #{view_num} | টাইমআউট")
            return False

        except requests.exceptions.ConnectionError:
            with self._lock:
                self.fail_count += 1
                self.total_attempts += 1
            if proxy_str:
                self.proxy_engine.mark_proxy_dead(proxy_str)
            return False

        except Exception as e:
            with self._lock:
                self.fail_count += 1
                self.total_attempts += 1
            self._add_log("error", f"❌ #{view_num} | Error: {str(e)[:40]}")
            return False

    def start_unlimited(self, url, thread_count=20, target_views=0, callback=None):
        """
        আনলিমিটেড ভিউ বুস্টার
        target_views=0 মানে আনলিমিটেড
        """
        self._running = True
        self._paused = False
        self.success_count = 0
        self.fail_count = 0
        self.total_attempts = 0
        self._start_time = time.time()
        self._minute_counter = 0
        self._last_minute_check = time.time()

        platform = self.detect_platform(url)

        self._add_log("info", f"🎬 শুরু হচ্ছে...")
        self._add_log("info", f"📌 URL: {url}")
        self._add_log("info", f"🌐 Platform: {platform.upper()}")
        self._add_log("info", f"🎯 Target: {'UNLIMITED ∞' if target_views == 0 else target_views}")
        self._add_log("info", f"🧵 Threads: {thread_count}")
        self._add_log("info", f"👤 User Agents: {self.ua_manager.total_agents()}+")
        self._add_log("info", "")

        view_number = 0
        active_threads = []

        try:
            while self._running:
                # টার্গেট চেক (0 = unlimited)
                if target_views > 0 and view_number >= target_views:
                    self._add_log("info", f"🎯 টার্গেট {target_views} ভিউ পূরণ হয়েছে!")
                    break

                # পজ চেক
                if self._paused:
                    time.sleep(0.5)
                    continue

                # ডেড থ্রেড পরিষ্কার
                active_threads = [t for t in active_threads if t.is_alive()]

                # নতুন থ্রেড শুরু
                while len(active_threads) < thread_count and self._running:
                    if target_views > 0 and view_number >= target_views:
                        break

                    view_number += 1

                    t = threading.Thread(
                        target=self._send_single_view,
                        args=(url, view_number),
                        daemon=True
                    )
                    t.start()
                    active_threads.append(t)

                    # ডিলে
                    time.sleep(random.uniform(MIN_DELAY, MAX_DELAY) / thread_count)

                # প্রতি মিনিটে স্ট্যাটাস
                now = time.time()
                if now - self._last_minute_check >= 60:
                    self.views_per_minute = self._minute_counter
                    self._minute_counter = 0
                    self._last_minute_check = now
                    elapsed = now - self._start_time
                    self._add_log("info",
                        f"📊 স্ট্যাটাস: ✅{self.success_count} "
                        f"❌{self.fail_count} "
                        f"⚡{self.views_per_minute}/min "
                        f"⏱️{elapsed/60:.1f}min"
                    )

                # কলব্যাক
                if callback:
                    callback(self.get_stats())

                time.sleep(0.1)

        except KeyboardInterrupt:
            self._add_log("warn", "⛔ ব্যবহারকারী দ্বারা বন্ধ করা হয়েছে")

        # সব থ্রেড শেষ হওয়া পর্যন্ত অপেক্ষা
        self._running = False
        for t in active_threads:
            t.join(timeout=5)

        self._show_final_stats()

    def _show_final_stats(self):
        """ফাইনাল স্ট্যাটাস"""
        elapsed = time.time() - self._start_time if self._start_time else 0
        rate = self.success_count / (elapsed / 60) if elapsed > 60 else self.success_count

        self._add_log("info", "")
        self._add_log("info", "═" * 50)
        self._add_log("info", "📊 ফাইনাল রিপোর্ট")
        self._add_log("info", "═" * 50)
        self._add_log("info", f"✅ সফল ভিউ: {self.success_count}")
        self._add_log("info", f"❌ ব্যর্থ: {self.fail_count}")
        self._add_log("info", f"📊 মোট প্রচেষ্টা: {self.total_attempts}")
        if self.total_attempts > 0:
            self._add_log("info", f"📈 সাফল্যের হার: {(self.success_count/self.total_attempts)*100:.1f}%")
        self._add_log("info", f"⚡ গড় রেট: {rate:.1f} views/min")
        self._add_log("info", f"⏱️ মোট সময়: {elapsed/60:.1f} মিনিট")
        self._add_log("info", "═" * 50)

    def _add_log(self, level, message):
        """লগ যোগ করে"""
        try:
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.log_queue.put_nowait((level, timestamp, message))
        except queue.Full:
            try:
                self.log_queue.get_nowait()
                self.log_queue.put_nowait((level, timestamp, message))
            except:
                pass

    def get_stats(self):
        """বর্তমান পরিসংখ্যান"""
        elapsed = time.time() - self._start_time if self._start_time else 0
        return {
            "success": self.success_count,
            "fail": self.fail_count,
            "total": self.total_attempts,
            "elapsed": elapsed,
            "rate": self.success_count / (elapsed / 60) if elapsed > 60 else self.success_count,
            "running": self._running,
            "paused": self._paused,
        }

    def pause(self):
        """পজ করে"""
        self._paused = True
        self._add_log("warn", "⏸️ পজ করা হয়েছে")

    def resume(self):
        """রিজিউম করে"""
        self._paused = False
        self._add_log("info", "▶️ রিজিউম হয়েছে")

    def stop(self):
        """বন্ধ করে"""
        self._running = False
        self._add_log("warn", "⛔ বন্ধ করা হচ্ছে...")

    def is_running(self):
        return self._running
