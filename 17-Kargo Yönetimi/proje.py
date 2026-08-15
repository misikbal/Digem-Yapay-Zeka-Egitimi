import json
import os
import smtplib
from email.message import EmailMessage
from pathlib import Path


dosya_adi = "data.json"
ENV_DOSYASI = Path(__file__).resolve().parent / ".env"


def env_yukle():
    """Basit .env okuyucu (ek paket gerekmez)."""
    if not ENV_DOSYASI.exists():
        return
    with open(ENV_DOSYASI, "r", encoding="utf-8") as file:
        for satir in file:
            satir = satir.strip()
            if not satir or satir.startswith("#") or "=" not in satir:
                continue
            anahtar, deger = satir.split("=", 1)
            os.environ.setdefault(anahtar.strip(), deger.strip())


def verileri_yukle():

    try:
        with open("data.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("data.json dosyası bulunamadı. Yeni bir veritabanı dosyası oluşturuluyor")
        varsayilan_veri = {"kargolar": {}}
        verileri_kaydet(varsayilan_veri)
        return varsayilan_veri

    except json.JSONDecodeError:
        print("Json dosyasında bir bozuluklu var Sistem varsayılan ayarlarda çalıştırılıyor")
        return {"kargolar": {}}


def verileri_kaydet(yeni_veri):
    try:
        with open("data.json", "w", encoding="utf-8") as var_olan_veriler:
            json.dump(yeni_veri, var_olan_veriler, indent=4, ensure_ascii=False)

    except Exception as error:
        print(f"Dosya yazım hatası oluştu Hata Kodu:{error}")


def durum_mail_gonder(kod, kargo):
    """Kargo durumu değişince alıcının mail adresine bildirim gönderir."""
    alici_mail = kargo.get("mail", "").strip()
    if not alici_mail:
        print("Bu kargo için mail adresi kayıtlı değil; bildirim gönderilmedi.")
        return

    host = os.environ.get("SMTP_HOST", "mail.kodmis.com")
    port = int(os.environ.get("SMTP_PORT", "465"))
    kullanici = os.environ.get("SMTP_USER", "")
    sifre = os.environ.get("SMTP_PASSWORD", "")
    gonderen = os.environ.get("SMTP_FROM", kullanici)

    if not kullanici or not sifre:
        print("SMTP bilgileri eksik (.env dosyasını kontrol edin); mail gönderilemedi.")
        return

    mesaj = EmailMessage()
    mesaj["From"] = gonderen
    mesaj["To"] = alici_mail
    mesaj["Subject"] = f"Kargo Durum Güncellemesi - {kod}"
    mesaj.set_content(
        f"""Sayın {kargo["alici"]},

{kod} takip numaralı kargonuzun durumu güncellendi.

Ürün: {kargo["urun"]}
Yeni Durum: {kargo["durum"]}
Ağırlık: {kargo["agirilik_kg"]} kg

İyi günler dileriz.
"""
    )

    try:
        with smtplib.SMTP_SSL(host, port) as smtp:
            smtp.login(kullanici, sifre)
            smtp.send_message(mesaj)
        print(f"Durum bildirimi {alici_mail} adresine gönderildi.")
    except Exception as error:
        print(f"Mail gönderilemedi: {error}")


def kargo_sorgula(kargo_veri):
    kod = input("Takip Numarsını Giriniz: (Örn:TR101)").strip().upper()

    try:
        bilgi = kargo_veri["kargolar"][kod]
        print(f"""
        Kargo Bilgisi {kod}

        Alıcı: {bilgi["alici"]}

        Mail: {bilgi.get("mail", "-")}

        Ürün: {bilgi["urun"]}

        Durum: {bilgi["durum"]}

        Ağırlık: {bilgi["agirilik_kg"]}
        
        
        """)

    except KeyError:

        print(f" Hata: {kod} numaralı bir kargo kaydı sistemde bulunamadı")


def yeni_kargo_ekle(kargo_veri):

    print("Yeni Kargo Girişi")
    kod = input("Takip Bumarası Belirleyin (Örn TR103):").strip().upper()

    if kod in kargo_veri["kargolar"]:
        print("Bu takip numarası zaten sistemde kayıtlı")
        return

    alici = input("Alıcı Ad Soyad:").strip()
    mail = input("Alıcı Mail Adresi:").strip()
    urun = input("Ürün Açıklaması:").strip()

    while True:
        try:
            agirilik = float(input("Kargo Ağırlığını Giriniz KG: Örn:1.5):"))

            if agirilik <= 0:
                print("Ağırlık 0 veya negatif olamaz Tekrar Deneyiniz")
                continue
            break

        except ValueError:
            print("Hata: Lütfen ağırlığı sadece sayı/ondalıklı olarak giriniz (Örn 1.5)")

    kargo_veri["kargolar"][kod] = {
        "alici": alici,
        "mail": mail,
        "urun": urun,
        "durum": "Kargo Alındı",
        "agirilik_kg": agirilik,
    }

    verileri_kaydet(kargo_veri)
    print(f"{kod} takip numaralı kargo başarılı bir şekilde oluşturuldu.")


def durum_guncelle(kargo_veri):

    kod = input("Durumu güncellenecek Kargo Kodu:").strip().upper()

    try:
        secili_kargo = kargo_veri["kargolar"][kod]

        print(f"Mevcut Durum: {secili_kargo['durum']}")

        print("""
        (1) Dağıtımda
        (2) Teslim Edildi
        (3) İade Edildi
        """)

        secim = input("Yeni Durumu Seçin  (1-3):").strip()

        durumlar = {"1": "Dağıtımda", "2": "Teslim Edildi", "3": "İade Edildi"}

        if secim not in durumlar:
            print("Hatalı durum seçimi")
            return

        secili_kargo["durum"] = durumlar[secim]
        verileri_kaydet(kargo_veri)
        print(f"{kod} numaralı kargo durumu {secili_kargo['durum']} olarak güncelledin")
        durum_mail_gonder(kod, secili_kargo)

    except KeyError:
        print("Böyle bir takip numarası sistemde mevcut değildir")


env_yukle()
gelen_veriler = verileri_yukle()

while True:
    print("""
    (1) Kargo Sorgula
    (2) Yeni Kargo Gönder
    (3) Durum Güncelle
    (4) Çıkış
    
    """)

    secim = input("Yapmak İstediğiniz işlemi seçin (1-4)").strip()
    if secim == "1":
        kargo_sorgula(gelen_veriler)

    elif secim == "2":
        yeni_kargo_ekle(gelen_veriler)

    elif secim == "3":
        durum_guncelle(gelen_veriler)

    elif secim == "4":
        print("Çıkış Yapılıyor")
        break

    else:
        print("Hatalı Menü Seçimi")
