import json

dosya_yolu="data.json"


def verileri_oku():
    with open(dosya_yolu, "r", encoding="utf-8") as dosya:
        return json.load(dosya)

def verileri_kaydet(data):
    with open(dosya_yolu,"w",encoding="utf-8") as dosya:

        json.dump(data, dosya, indent=4, ensure_ascii=False)
    print("Değişiklikler data.json' a kaydoldu.")

def giris_yap(username, password, veriler):
    for kullanici in veriler["kullanicilar"]:
        if kullanici["kullanici_adi"]==username and kullanici["sifre"]==password:
            return kullanici

    return None

def etkinlikleri_listele(veriler):
    print("Güncel Etkinlik ve Konser Listesi:")
    for e in veriler["etkinlikler"]:
        durum=f"Bilet Var {e["kontenjan"]} Adet" if e["kontenjan"]>0 else "X Tükendi"
        print(f"{e["id"]} - {e["ad"]} | Fiyat: {e["fiyat"]} | Durum: {durum}")

def bilet_satin_al(aktif_kullanici, etkinlik_id, adet, veriler):
    for e in veriler["etkinlikler"]:
        if e["id"]==etkinlik_id:
            if e["kontenjan"]>=adet:
                toplam_tutar=e["fiyat"]*adet

                e["kontenjan"]-=adet

                bilet_kaydi=f"{e["ad"]}  {adet} Bilet - Toplam: {toplam_tutar}"
                aktif_kullanici["biletlerim"].append(bilet_kaydi)

                verileri_kaydet(veriler)
                print("İşlem Başarılı")
                print(bilet_kaydi)

                return True

            else:
                print("Üzgünüz Yetersiz Kontenjan. ")
                return False

    print("Geçersiz Etkinlik ID")
    return False


sistem_verileri=verileri_oku()
aktif_kullanici=None


while True:
    print("Lütfen Hesabınıza Giriş Yapın")
    username=input("Kullanıcı Adınız:").strip()
    password=input("Şifre").strip()

    aktif_kullanici=giris_yap(username,password,sistem_verileri)

    if aktif_kullanici:
        print("Giriş Başarılı")
        break
    else:
        print("Kulanıcı adı veya şifre yanlış")


while True:
    print("""
    (1) Etkinlikleri Listele
    (2) Bilet Satın Al
    (3) Biletlerimi Göster
    (4) Çıkış    
    """)
    secim=input("Lütfen Seçiminizi Yapınız (1-4):")

    if secim=="1":
        etkinlikleri_listele(sistem_verileri)

    elif secim=="2":
        etkinlikleri_listele(sistem_verileri)
        etkinlik_id=int(input("Lütfen satın almak istediğiniz etkinliğin id bilgisini giriniz:"))
        bilet_adet=int(input("Kaç adet bilet almak istiyorsunuz"))
        if bilet_adet>0:
            bilet_satin_al(aktif_kullanici, etkinlik_id, bilet_adet, sistem_verileri)

        else:
            print("Bilet adeti en az 1 olmalıdır!")

    elif secim=="3":

        print(f"{aktif_kullanici["ad_soyad"]} - Satın alınan biletler")
        if not aktif_kullanici["biletlerim"]:
            print("Henüz satın alınmış biletinz yoktur")

        
        else:
            for bilet in aktif_kullanici["biletlerim"]:
                print(bilet)

    elif secim=="4":
        print("Çıkış yapılıyor")
        break