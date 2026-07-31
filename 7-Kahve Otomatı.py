print("""
Otomatımıza Hoşgeldiniz

(1) Ekspreso
(2) Latte
(3) Mocha
(4) Çay
""")
fiyat=0
secim=input("Lütfen Seçimizi Yapınız:")

if secim=="1":
    secilen_urun="Ekspreso"
    fiyat=40

elif secim=="2":
    secilen_urun="Latte"
    fiyat=50

elif secim=="3":
    secilen_urun="Mocha"
    fiyat=60

elif secim=="4":
    secilen_urun="Çay"
    fiyat=10

else:
    secilen_urun="Geçersiz"
    fiyat=0
    print("Hatalı Tuşlama Yaptınız")


if secilen_urun=="Geçersiz":
    print("Program Sonlandırılıyor")

else:
    print(f"Seçilen: {secilen_urun} Ödemeniz Gereken Tutar {fiyat} TL.")
    atilan_para=int(input("Lütfen otomata para yükleyiniz (TL): "))

    if atilan_para>=fiyat:
        para_ustu=atilan_para-fiyat
        print(f"{secilen_urun} hazılanıyor... Lütfen Bekleyiniz.")
        print(f"İşlem Tamamlandı Para üstünüz {para_ustu} TL. Afiyet Olsun")
    else:
        eksik=fiyat-atilan_para
        print(f"Yetersiz Bakiye!!! {secilen_urun} için {eksik} TL daha yüklemeniz gerek")
