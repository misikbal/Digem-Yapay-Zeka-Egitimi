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
        {"id":1,"ad":"Zamanın Kısa Tarihi","yazar":"Stephen Hawking","stok":3},
        {"id":2,"ad":"Kozmos","yazar":"Carl Sagan","stok":4},
        {"id":3,"ad":"Gen Bencil midir?","yazar":"Richard Dawkins","stok":2},
        {"id":4,"ad":"Türlerin Kökeni","yazar":"Charles Darwin","stok":5},
        {"id":5,"ad":"Sapiens","yazar":"Yuval Noah Harari","stok":6},
        {"id":6,"ad":"Gen","yazar":"Siddhartha Mukherjee","stok":3},
        {"id":7,"ad":"Acelecilere Astrofizik","yazar":"Neil deGrasse Tyson","stok":4},
        {"id":8,"ad":"Zarif Evren","yazar":"Brian Greene","stok":2},
        {"id":9,"ad":"Sessiz Bahar","yazar":"Rachel Carson","stok":1},
        {"id":10,"ad":"Henrietta Lacks'in Ölümsüz Yaşamı","yazar":"Rebecca Skloot","stok":3},
        {"id":11,"ad":"Hızlı ve Yavaş Düşünme","yazar":"Daniel Kahneman","stok":0},
        {"id":12,"ad":"Karanlık Bir Dünyada Bilimin Mum Işığı","yazar":"Carl Sagan","stok":2},
        {"id":13,"ad":"Tüfek, Mikrop ve Çelik","yazar":"Jared Diamond","stok":4},
        {"id":14,"ad":"İkili Sarmal","yazar":"James D. Watson","stok":3},
        {"id":15,"ad":"Neden Uyuruz?","yazar":"Matthew Walker","stok":5},
        {"id":16,"ad":"Ağaçların Gizli Yaşamı","yazar":"Peter Wohlleben","stok":4},
        {"id":17,"ad":"Kaos","yazar":"James Gleick","stok":0},
        {"id":18,"ad":"Evrenin Dokusu","yazar":"Brian Greene","stok":2},
        {"id":19,"ad":"Homo Deus","yazar":"Yuval Noah Harari","stok":3},
        {"id":20,"ad":"Altıncı Yok Oluş","yazar":"Elizabeth Kolbert","stok":4},
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
