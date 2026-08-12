import urllib.request, re, os

req = urllib.request.Request(
    "https://sites.google.com/view/wallenvy",
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0"}
)
with urllib.request.urlopen(req, timeout=20) as r:
    html = r.read().decode("utf-8", errors="ignore")

urls = re.findall(r'https://lh3\.googleusercontent\.com/sitesv/[^"\'&\s<>]+', html)
print(f"Found {len(urls)} image URLs")
for i, u in enumerate(urls[:6]):
    print(f"[{i}] {u[:120]}...")

# Try downloading each as potential banner
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for i, url in enumerate(urls[:6]):
    try:
        req2 = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req2, timeout=15) as r:
            data = r.read()
        dest = os.path.join(ROOT, "assets", "images", f"candidate-{i}.jpg")
        with open(dest, "wb") as f:
            f.write(data)
        print(f"  -> Downloaded candidate-{i}.jpg ({len(data)//1024}KB)")
    except Exception as e:
        print(f"  -> FAIL candidate-{i}: {e}")
