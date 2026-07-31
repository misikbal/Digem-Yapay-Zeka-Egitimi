kullanici_bilgileri=[
    {
        "kullanci_adi":"zeynep",
        "sifre":"123",
        "kullanici_detay_bilgileri":{
            "adsoyad":"Zeynep Özkan",
            "telefon":"05555555555",
            "tc":"11111111111",
            "rol":"öğrenci"
        },
        "aktif_mi":True
    },
    {
        "kullanci_adi":"esma",
        "sifre":"123",
        "kullanici_detay_bilgileri":{
            "adsoyad":"Esma Akbulut",
            "telefon":"05555555551",
            "tc":"11111111112",
            "rol":"öğrenci"
        },
        "aktif_mi":True

    },
    {
        "kullanci_adi":"admin",
        "sifre":"123",
        "kullanici_detay_bilgileri":{
            "adsoyad":"Besse Tuğtekin",
            "telefon":"05555555552",
            "tc":"11111111113",
            "rol":"yönetici"
        },
        "aktif_mi":True
    }
]

print("------------------------------------------------------")
print("Giriş Otomasyonu")
print("------------------------------------------------------")

hak=3
giris_yapan_kullanici=None

while hak>0:
    girilen_kullanci=input("Kullanıcı adınızı yazınız:").strip()
    girilen_parola=input("Parolanızı giriniz:").strip()

    print("Doğrulanıyor...")

    bulundu_mu=False

    for kullanici in kullanici_bilgileri:
        if girilen_kullanci==kullanici["kullanci_adi"] and girilen_parola==kullanici["sifre"]:
            bulundu_mu=True

            if not kullanici["aktif_mi"]:
                print("Hata! Hesabınız Dondurulmuştur. (Hesap Engellendi)")
                break
            
            giris_yapan_kullanici=kullanici
            break

    if giris_yapan_kullanici:
        print("Giriş Başarılı ")

        print(f"Hoşgeldiniz:      {giris_yapan_kullanici["kullanici_detay_bilgileri"]["adsoyad"]}")
        print(f"Telefon Bilginiz: {giris_yapan_kullanici["kullanici_detay_bilgileri"]["telefon"]}")
        print(f"Yetkili Rolü:     {giris_yapan_kullanici["kullanici_detay_bilgileri"]["rol"]}")


        break

    if not bulundu_mu:
        hak=hak-1
        print(f"Hata Kullancı adı veya şifre yanlış. {hak} Hakkınız Kaldı")

if hak==0:
    print("3 Defa Hatalı Giriş yaptığınız için hesap güvenlik nedeniyle kitlendi.")





