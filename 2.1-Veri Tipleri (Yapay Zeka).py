while True:  # Geçerli bir sürücü adı girilene kadar döngüyü tekrarlar
    surucu_adi = input("Sürücü adınızı giriniz: ").strip()  # Kullanıcıdan ad alır, baş/son boşlukları temizler
    if surucu_adi:  # Ad boş değilse (en az bir karakter varsa) koşul sağlanır
        break  # Döngüden çıkar, bir sonraki adıma geçer
    print("Hata: Sürücü adı boş olamaz.")  # Ad boşsa kullanıcıya hata mesajı gösterir

while True:  # Geçerli bir mesafe girilene kadar döngüyü tekrarlar
    try:  # Hata oluşabilecek kodu dene
        mesafe = int(input("Mesafe giriniz: "))  # Kullanıcıdan mesafeyi alır ve tam sayıya çevirir
        if mesafe <= 0:  # Mesafe 0 veya negatifse koşul sağlanır
            print("Hata: Mesafe 0'dan büyük bir sayı olmalıdır.")  # Kullanıcıya uyarı mesajı gösterir
            continue  # Döngünün başına döner, tekrar sorar
        break  # Geçerli mesafe girildiyse döngüden çıkar
    except ValueError:  # Sayıya çevrilemezse (örn. "elma") bu bloğa girer
        print("Hata: Lütfen sadece sayı girin (örnek: 450)")  # Kullanıcıya hata mesajı gösterir

while True:  # Geçerli bir yakıt fiyatı girilene kadar döngüyü tekrarlar
    try:  # Hata oluşabilecek kodu dene
        yakit_fiyati = int(input("Yakıt fiyatı giriniz: "))  # Kullanıcıdan fiyatı alır ve tam sayıya çevirir
        if yakit_fiyati <= 0:  # Fiyat 0 veya negatifse koşul sağlanır
            print("Hata: Yakıt fiyatı 0'dan büyük bir sayı olmalıdır.")  # Kullanıcıya uyarı mesajı gösterir
            continue  # Döngünün başına döner, tekrar sorar
        break  # Geçerli fiyat girildiyse döngüden çıkar
    except ValueError:  # Sayıya çevrilemezse bu bloğa girer
        print("Hata: Lütfen sadece sayı girin (örnek: 67)")  # Kullanıcıya hata mesajı gösterir

while True:  # Geçerli bir klima modu girilene kadar döngüyü tekrarlar
    klima_modu = input("Klima modunu giriniz (true/false): ").strip().lower()  # Girdiyi alır, boşlukları temizler, küçük harfe çevirir
    if klima_modu in ("true", "false", "evet", "hayır", "hayir"):  # Girdi kabul edilen değerlerden biriyse koşul sağlanır
        break  # Döngüden çıkar
    print("Hata: Lütfen true, false, evet veya hayır girin.")  # Geçersiz girişte kullanıcıya hata mesajı gösterir

dolar_fiyati = 46.16  # 1 doların TL karşılığını ondalıklı sayı olarak bir değişkene atar
print("Hoşgeldiniz", surucu_adi)  # Sürücüye hoşgeldin mesajı ve adını ekrana yazdırır
print("Şuana kadar gittiğiniz mesafe:", mesafe, "km")  # Gidilen mesafeyi ekrana yazdırır
print("Yakıt fiyatı:", yakit_fiyati, "TL")  # Yakıt fiyatını TL cinsinden ekrana yazdırır
hesaplama = yakit_fiyati / dolar_fiyati  # Yakıt fiyatını TL'den dolara çevirir (bölme işlemi)
print("Yakıt Fiyatı (USD)", round(hesaplama, 2), " USD")  # USD fiyatını 2 ondalık basamağa yuvarlayıp ekrana yazdırır
print("Klima modu:", klima_modu)  # Klima modu bilgisini ekrana yazdırır
