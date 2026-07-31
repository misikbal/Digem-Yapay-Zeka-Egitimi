sepet=["Telefon","Kulaklık"]
print("Mevcut Sepetiniz:",sepet)

yeni_urun=input("Sepete Eklemeke İstediğiniz Ürünü Giriniz:")
sepet.append(yeni_urun)
print("Sepetiniz:",sepet)
print("Sepetinizdeki Ürün Sayısı:",len(sepet))

silinecek_urun=input("Silmek İstediğiniz Ürünü Giriniz:")
if silinecek_urun in sepet:
    sepet.remove(silinecek_urun)
    print(sepet)

else:
    print("Ürün Bulunamadı")
