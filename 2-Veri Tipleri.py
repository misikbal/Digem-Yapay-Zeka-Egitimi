surucu_adi=input("Sürücü adınızı giriniz: ")  # Kullanıcıdan sürücü adını alır ve metin olarak saklar
mesafe=input("Mesafe giriniz: ")  # Kullanıcıdan mesafeyi alır (metin olarak kalır, sayıya çevrilmez)
yakit_fiyati=int(input("Yakıt fiyatı giriniz: "))  # Kullanıcıdan yakıt fiyatını alır ve tam sayıya (int) çevirir
klima_modu=input("Klima modunu giriniz: ")  # Kullanıcıdan klima modunu alır ve metin olarak saklar
print(type(yakit_fiyati))  # yakit_fiyati değişkeninin veri tipini ekrana yazdırır (<class 'int'>)
dolar_fiyati=46.16  # 1 doların TL karşılığını ondalıklı sayı olarak bir değişkene atar
print("Hoşgeldiniz", surucu_adi)  # Sürücüye hoşgeldin mesajı ve adını ekrana yazdırır
print("Şuana kadar gittiğiniz mesafe:", mesafe, "km")  # Gidilen mesafeyi ekrana yazdırır
print("Yakıt fiyatı:", yakit_fiyati, "TL")  # Yakıt fiyatını TL cinsinden ekrana yazdırır
hesaplama= yakit_fiyati/dolar_fiyati  # Yakıt fiyatını TL'den dolara çevirir (bölme işlemi)
print("Yakıt Fiyatı (USD)",round(hesaplama,2) ," USD")  # USD fiyatını 2 ondalık basamağa yuvarlayıp ekrana yazdırır
print("Klima modu:", klima_modu)  # Klima modu bilgisini ekrana yazdırır
