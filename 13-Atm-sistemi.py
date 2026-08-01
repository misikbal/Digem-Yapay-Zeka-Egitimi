banka_kullanicilari=[
    {
        "musteri_id":101,
        "kullanci_id":"ahmet",
        "pin":"1234",
        "hesap":{
            "ad_soyad":"Ahmet Yılmaz",
            "bakiye":4500,
            "para_birimi":"TL"
        },
        "gecmis_islemler":["+500 TL Havala","-150 TL Market"]
    },

    {
        "musteri_id":102,
        "kullanci_id":"ayşe",
        "pin":"1234",
        "hesap":{
            "ad_soyad":"Ayşe Çınar",
            "bakiye":1500,
            "para_birimi":"TL"
        },
        "gecmis_islemler":["+100 TL Havala","-5650 TL Market"]
    },

    {
        "musteri_id":103,
        "kullanci_id":"mehmet",
        "pin":"1234",
        "hesap":{
            "ad_soyad":"Mehmet Yılmaz",
            "bakiye":12400,
            "para_birimi":"TL"
        },
        "gecmis_islemler":[]
    }
]


print("===================================")
print("Akıllı Banka ATM'si")
print("===================================")


aktif_musteri=None

while True:
    girilen_kullanici=input("Kullanıcı Adı: ").strip()
    girilen_sifre=input("Pin Numaranız:").strip()

    for musteri in banka_kullanicilari:
        if girilen_kullanici==musteri["kullanci_id"] and girilen_sifre==musteri["pin"]:
            aktif_musteri=musteri
            break

    if aktif_musteri:
        print(f"Giriş Başarılı Hoşgeldiniz {aktif_musteri["hesap"]["ad_soyad"]}")
        break
    else:
        print("İşlem Başarısız Bilgilerinizi Kontrol ediniz")

while True:
    print("---------------------------------------")
    print("(1) Bakiye Sogulama")
    print("(2) İşlem Geçmişini Listele")
    print("(3) Para Yatır")
    print("(4) Para Çekme")
    print("(5) Kart İade/Çıkış")


    secim=input("Yapmak istediğiniz işlemi seçiniz (1-5):").strip()


    if secim=="1":
        bakiye=aktif_musteri["hesap"]["bakiye"]
        birim=aktif_musteri["hesap"]["para_birimi"]
        print(f" \n \n \n Güncel Bakiyeniz: {bakiye} {birim}\n \n \n")

    elif secim=="2":
        print(f"\n \n \n{aktif_musteri["hesap"]["ad_soyad"]} - İşlem Geçmişi")

        for islem in aktif_musteri["gecmis_islemler"]:
            print(islem)

    elif secim=="3":
        miktar=int(input("\n \n Yatıralacak Tutar (TL):"))

        if miktar>0:
            aktif_musteri["hesap"]["bakiye"]+= miktar
            yeni_islem=f"+{miktar} TL Para Yatırıldı"

            aktif_musteri["gecmis_islemler"].append(yeni_islem)
            print("İşlem Başarılı \n \n")

        else:
            print("Geçersiz İşlem")


    elif secim=="4":
        miktar=int(input("\n Çekilecek Miktar:"))
        mevcut_bakiye=aktif_musteri["hesap"]["bakiye"]

        if miktar>mevcut_bakiye:
            print("Yetersiz Bakiye")
        elif miktar<=0:
            print("Geçersiz Tutar")
        else:
            aktif_musteri["hesap"]["bakiye"]-=miktar

            yeni_islem=f"-{miktar}  TL Para Çekme"

            aktif_musteri["gecmis_islemler"].append(yeni_islem)

    elif secim=="5":
        print("Kartınız İade Ediliyor...")
        break

    else:
        print("Geçersiz Seçim!")



    




