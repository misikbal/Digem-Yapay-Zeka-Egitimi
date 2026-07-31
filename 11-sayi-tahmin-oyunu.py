from random import randint

rastgele_sayi=randint(1,10)

hak=3
print("Sayı Tahmin Oyununa Hoşgeldiniz")
while hak>0:

    print(f"{hak} Hakkınız Kaldı")
    tahmin=int(input("Bir Sayı Giriniz:"))

    if tahmin==rastgele_sayi:
        print("Tebrikler Oyunu Kazandınız")
        break
    elif tahmin>rastgele_sayi:
        print("Daha küçük bir sayı giriniz")
        hak-=1

    elif tahmin<rastgele_sayi:
        print("Daha büyük bir sayı giriniz")
        hak-=1

    

