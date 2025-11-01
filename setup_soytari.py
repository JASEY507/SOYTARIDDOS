import os
print("""
\033[38;2;180;0;255m╔═╗╔═╗ ╦ ╦ ╦╦╔═╗ ╦╔╦╗╔╦╗╔╦╗╔═╗╔═╗
\033[38;2;180;0;255m╚═╗╠═╝ ║ ║ ║║║╣  ║ ║  ║  ║ ╠═╣╠═╝
\033[38;2;180;0;255m╚═╝╩   ╚═╝╚╝╚═╝ ╩ ╩  ╩  ╩ ╩ ╩╩  
    \033[38;2;255;0;100m> SOYTARIDDOS KURULUM\033[0m
""")
print("[0] pip\n[1] pip3")
c = input(">>> ")
cmd = "pip" if c == "0" else "pip3"
os.system(f"{cmd} install cloudscraper socks pysocks colorama undetected-chromedriver httpx")
if os.name != "nt":
    os.system("wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb")
    os.system("dpkg -i google-chrome-stable_current_amd64.deb || apt-get install -f -y")
print("\033[38;2;0;255;0mKurulum tamamlandı. 'python3 soytariddos.py' ile başlat.")
