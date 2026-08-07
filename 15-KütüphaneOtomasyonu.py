kutuphane_veritabani={
    "uyeler":[
        {
            "kullanici_adi":"ahmet",
            "sifre":"123",
            "ad_soyad":"Ahmet Yılmaz",
            "odunc_kitaplar":[]
        },        
        {
            "kullanici_adi":"besse",
            "sifre":"123",
            "ad_soyad":"Besse Tuğtekin",
            "odunc_kitaplar":[]
        },
        {
            "kullanici_adi":"ali",
            "sifre":"123",
            "ad_soyad":"Ali Yülkebir Güneş",
            "odunc_kitaplar":[]
        },


    ],
    "kitaplar":[

        {
            "id":1,
            "ad":"Yapay Zekayaya Giriş",
            "stok":3
        },
        {
            "id":2,
            "ad":"Python ile Progralama",
            "stok":0
        },
        {
            "id":3,
            "ad":"Hasterinden Prangalar Eskittim",
            "stok":5
        }
    ]

}

def uye_giris(kullaniciAdi,sifre):

    for uye in kutuphane_veritabani["uyeler"]:
        if uye["kullanici_adi"]==kullaniciAdi and uye["sifre"]==sifre:
            return uye

    return None


def kitaplari_listele():
    print("Mevcut Kitap Listesi")
    for kitap in kutuphane_veritabani["kitaplar"]:
        durum=f"Stok Var {kitap["stok"]} adet" if kitap["stok"]>0 else "stok yok"


        print(f"{kitap["id"]} - {kitap["ad"]} -> {durum}")



def kitap_odunc_al(uye,kitap_id):
    for kitap in kutuphane_veritabani["kitaplar"]:
        if kitap["id"]==kitap_id:
            if kitap["stok"]>0:
                kitap["stok"]-=1
                uye["odunc_kitaplar"].append(kitap["ad"])
                print("Kitap Başarılı bir şekilde ödünç verildi")

                return True

            else:
                print(f"Üzgünüz {kitap["ad"]} kitabı tükendi.")
                return False
    print("Geçersiz ID")
    return False


def aldigim_kitaplar(uye):
    print(f"Sayın {uye["ad_soyad"]} Almış Olduğunuz Kitaplar:")
    if not uye["odunc_kitaplar"]:
        print("Henüz ödünç kitap almadınız")

    else:
        for kitap in uye["odunc_kitaplar"]:
            print(f"- {kitap}")



while True:
    username=input("Üye Kullanıcı Adı:").strip()
    password=input("Şifre:").strip()

    aktif_uye=uye_giris(username,password)

    if aktif_uye:
        print(f"Giriş Baralı Hoşgeldin {aktif_uye["ad_soyad"]}")
        break

    else:
        print("Hatalı Kullanıcı adı veya şifre!")


while True:
    print("""
    (1) Kitap Listele
    (2) Kitap Ödünç Al
    (3) Aldığım Kitaplar
    (4) Çıkış
    
    """)
    secim=input("İşleminizi Seçiniz (1-4): ").strip()

    if secim=="1":
        kitaplari_listele()

    elif secim=="2":
        kitaplari_listele()
        kitap_id=int(input("Ödünç Almak İstediğiniz Kitap ID'sini giriniz:"))

        kitap_odunc_al(aktif_uye,kitap_id)

    elif secim=="3":
        aldigim_kitaplar(aktif_uye)

    elif secim=="4":
        print("Çıkış Yapıldı İyi Okumalar")
        break
    else:
        print("Geçersiz Seçim")
