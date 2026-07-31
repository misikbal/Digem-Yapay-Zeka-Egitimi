# Alışveriş Sepeti — Liste işlemleri + fiyat / kargo
# Web arayüzü: index.html
# Kural: sepet tutarı 1000 TL'den fazla ise kargo ücretsiz

KARGO_UCRETI = 99
UCRETSIZ_KARGO_LIMITI = 1000

sepet = [
    {"ad": "Telefon", "fiyat": 18500},
    {"ad": "Kulaklık", "fiyat": 1299},
]

print("Mevcut Sepetiniz:", sepet)

yeni_urun = input("Sepete Eklemek İstediğiniz Ürünü Giriniz: ")
yeni_fiyat = int(input("Ürün Fiyatını Giriniz (TL): "))
sepet.append({"ad": yeni_urun, "fiyat": yeni_fiyat})
print("Sepetiniz:", sepet)
print("Sepetinizdeki Ürün Sayısı:", len(sepet))

silinecek_urun = input("Silmek İstediğiniz Ürünü Giriniz: ")
bulundu = False
for urun in sepet:
    if urun["ad"] == silinecek_urun:
        sepet.remove(urun)
        bulundu = True
        break

if bulundu:
    print(sepet)
else:
    print("Ürün Bulunamadı")

ara_toplam = sum(urun["fiyat"] for urun in sepet)
kargo = 0 if ara_toplam > UCRETSIZ_KARGO_LIMITI else KARGO_UCRETI
genel_toplam = ara_toplam + kargo

print("Ara Toplam:", ara_toplam, "TL")
print("Kargo:", "Ücretsiz" if kargo == 0 else f"{kargo} TL")
print("Genel Toplam:", genel_toplam, "TL")
