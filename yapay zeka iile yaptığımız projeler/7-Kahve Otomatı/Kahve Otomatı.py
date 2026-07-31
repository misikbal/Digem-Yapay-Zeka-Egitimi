"""
7-Kahve Otomatı.py — Kahve otomatı simülasyonu.

Web arayüzünü tarayıcıda açmak için bu dosyayı çalıştırın:
    python "Kahve Otomatı.py"
"""

import http.server
import socketserver
import webbrowser
from pathlib import Path

PORT = 8765
PROJE_KLASORU = Path(__file__).resolve().parent


class StatikSunucu(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PROJE_KLASORU), **kwargs)


def main():
    url = f"http://localhost:{PORT}/index.html"
    print(f"Kahve Otomatı arayüzü başlatılıyor: {url}")
    print("Durdurmak için Ctrl+C")

    with socketserver.TCPServer(("", PORT), StatikSunucu) as httpd:
        webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nSunucu kapatıldı.")


if __name__ == "__main__":
    main()
