sayi1=int(input("1.Sayınızı Giriniz:"))
sayi2=int(input("2.Sayınızı Giriniz:"))
islem=input("Hangi İşlemi Yapmak İstiyorsunuz (+ - * /):")


if islem=="+":
    print("Toplama İşleminin Sonucu:",sayi1+sayi2)

elif islem=="-":
    print("Çıkarma İşleminin Sonucu:",sayi1-sayi2)

elif islem=="*":
    print("Çarpma İşleminin Sonucu:",sayi1*sayi2)

elif islem=="/":
    if sayi2!=0:
        print("Bölme İşleminin Sonucu:",sayi1/sayi2)
    else:
        print("Bir sayı sıfıra bölünemez")

else:
    print("Hatalı Bir İşlem Girdiniz")
