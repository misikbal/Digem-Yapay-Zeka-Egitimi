"""
18. DERS - SQLite ile Veritabani

SQLite nedir?
- Python ile birlikte gelen (ek kurulum gerekmez) hafif bir veritabanidir.
- Veriler tek bir .db dosyasinda saklanir (ornegin: okul.db).
- JSON dosyasi gibi calisir ama verileri tablo halinde duzenli tutar.

Temel adimlar:
1) Baglanti ac  -> sqlite3.connect("dosya.db")
2) Tablo olustur -> CREATE TABLE ...
3) Veri ekle     -> INSERT INTO ...
4) Veri oku      -> SELECT ...
5) Veri guncelle -> UPDATE ...
6) Veri sil      -> DELETE ...
7) Baglantiyi kapat -> conn.close()
"""

import sqlite3
from pathlib import Path

# Veritabani dosyasi bu klasorde olusacak
VERITABANI = Path(__file__).resolve().parent / "okul.db"


def ayirici(baslik):
    print("\n" + "=" * 50)
    print(baslik)
    print("=" * 50)


# ---------------------------------------------------------
# ORNEK 1: Baglanti ve tablo olusturma
# ---------------------------------------------------------
def ornek_1_tablo_olustur():
    ayirici("ORNEK 1 - Tablo Olusturma")

    conn = sqlite3.connect(VERITABANI)
    cursor = conn.cursor()

    # ogrenciler adinda bir tablo olusturuyoruz
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ogrenciler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad TEXT NOT NULL,
            sinif INTEGER,
            not_ortalamasi REAL
        )
    """)

    conn.commit()
    conn.close()
    print("Tablo hazir: ogrenciler")


# ---------------------------------------------------------
# ORNEK 2: Veri ekleme (INSERT)
# ---------------------------------------------------------
def ornek_2_veri_ekle():
    ayirici("ORNEK 2 - Veri Ekleme")

    conn = sqlite3.connect(VERITABANI)
    cursor = conn.cursor()

    ogrenciler = [
        ("Ahmet", 10, 85.5),
        ("Ayse", 10, 92.0),
        ("Mehmet", 11, 78.3),
        ("Zeynep", 11, 88.7),
    ]

    cursor.executemany(
        "INSERT INTO ogrenciler (ad, sinif, not_ortalamasi) VALUES (?, ?, ?)",
        ogrenciler,
    )

    conn.commit()
    conn.close()
    print(f"{len(ogrenciler)} ogrenci eklendi.")


# ---------------------------------------------------------
# ORNEK 3: Veri okuma (SELECT)
# ---------------------------------------------------------
def ornek_3_veri_oku():
    ayirici("ORNEK 3 - Veri Okuma")

    conn = sqlite3.connect(VERITABANI)
    cursor = conn.cursor()

    # Tum ogrencileri getir
    cursor.execute("SELECT id, ad, sinif, not_ortalamasi FROM ogrenciler")
    tum_kayitlar = cursor.fetchall()

    print("Tum ogrenciler:")
    for kayit in tum_kayitlar:
        print(f"  ID:{kayit[0]} | {kayit[1]} | Sinif:{kayit[2]} | Not:{kayit[3]}")

    # Sadece 10. sinif ogrencileri
    cursor.execute(
        "SELECT ad, not_ortalamasi FROM ogrenciler WHERE sinif = ?",
        (10,),
    )
    onuncu_sinif = cursor.fetchall()

    print("\n10. sinif ogrencileri:")
    for ad, not_ort in onuncu_sinif:
        print(f"  {ad} -> {not_ort}")

    conn.close()


# ---------------------------------------------------------
# ORNEK 4: Veri guncelleme (UPDATE)
# ---------------------------------------------------------
def ornek_4_veri_guncelle():
    ayirici("ORNEK 4 - Veri Guncelleme")

    conn = sqlite3.connect(VERITABANI)
    cursor = conn.cursor()

    # Ahmet'in notunu guncelle
    cursor.execute(
        "UPDATE ogrenciler SET not_ortalamasi = ? WHERE ad = ?",
        (90.0, "Ahmet"),
    )

    conn.commit()

    cursor.execute("SELECT ad, not_ortalamasi FROM ogrenciler WHERE ad = 'Ahmet'")
    guncel = cursor.fetchone()
    print(f"Guncellenen kayit: {guncel[0]} -> yeni not: {guncel[1]}")

    conn.close()


# ---------------------------------------------------------
# ORNEK 5: Veri silme (DELETE)
# ---------------------------------------------------------
def ornek_5_veri_sil():
    ayirici("ORNEK 5 - Veri Silme")

    conn = sqlite3.connect(VERITABANI)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM ogrenciler WHERE ad = ?", ("Mehmet",))
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM ogrenciler")
    kalan = cursor.fetchone()[0]
    print(f"Mehmet silindi. Kalan ogrenci sayisi: {kalan}")

    conn.close()


# ---------------------------------------------------------
# ORNEK 6: Basit arama fonksiyonu (gercek hayat kullanimi)
# ---------------------------------------------------------
def ogrenci_ara(ad):
    """Isme gore ogrenci arar. Bulamazsa None doner."""
    conn = sqlite3.connect(VERITABANI)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, ad, sinif, not_ortalamasi FROM ogrenciler WHERE ad = ?",
        (ad,),
    )
    sonuc = cursor.fetchone()
    conn.close()
    return sonuc


def ornek_6_arama():
    ayirici("ORNEK 6 - Fonksiyon ile Arama")

    bulunan = ogrenci_ara("Ayse")
    if bulunan:
        print(f"Bulundu: ID={bulunan[0]}, Ad={bulunan[1]}, Sinif={bulunan[2]}, Not={bulunan[3]}")
    else:
        print("Ogrenci bulunamadi.")


# ---------------------------------------------------------
# ORNEK 7: Ikinci tablo ile iliski (basit)
# ---------------------------------------------------------
def ornek_7_ikinci_tablo():
    ayirici("ORNEK 7 - Iki Tablo (Ders Notlari)")

    conn = sqlite3.connect(VERITABANI)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ders_notlari (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ogrenci_id INTEGER,
            ders TEXT,
            puan INTEGER,
            FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler(id)
        )
    """)

    # Ayse'nin id'sini bul
    cursor.execute("SELECT id FROM ogrenciler WHERE ad = 'Ayse'")
    ayse_id = cursor.fetchone()[0]

    cursor.executemany(
        "INSERT INTO ders_notlari (ogrenci_id, ders, puan) VALUES (?, ?, ?)",
        [
            (ayse_id, "Matematik", 95),
            (ayse_id, "Fizik", 88),
            (ayse_id, "Kimya", 92),
        ],
    )
    conn.commit()

    # JOIN ile ogrenci adi + ders notlarini birlikte oku
    cursor.execute("""
        SELECT o.ad, d.ders, d.puan
        FROM ogrenciler o
        JOIN ders_notlari d ON o.id = d.ogrenci_id
        WHERE o.ad = 'Ayse'
    """)

    print("Ayse'nin ders notlari:")
    for satir in cursor.fetchall():
        print(f"  {satir[1]}: {satir[2]}")

    conn.close()


# ---------------------------------------------------------
# Calistir
# ---------------------------------------------------------
if __name__ == "__main__":
    print("SQLite Ders Ornekleri Basliyor...")
    print(f"Veritabani dosyasi: {VERITABANI}")

    # Her calistirmada temiz baslangic icin eski db'yi silebilirsiniz
    # (ilk ogrenme icin kolaylik saglar)
    if VERITABANI.exists():
        VERITABANI.unlink()
        print("Eski veritabani silindi, sifirdan basliyoruz.")

    ornek_1_tablo_olustur()
    ornek_2_veri_ekle()
    ornek_3_veri_oku()
    ornek_4_veri_guncelle()
    ornek_5_veri_sil()
    ornek_6_arama()
    ornek_7_ikinci_tablo()

    print("\nTum ornekler tamamlandi!")
