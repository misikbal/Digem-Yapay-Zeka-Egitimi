yuz_tanimlama=input("Yüz Tanımlandı mı? ")
if yuz_tanimlama=="evet":
    print("Giriş Başarılı")

elif yuz_tanimlama=="hayır":
    print("Yüzünüz Tanımlamadığı İçin Alteratif Oturum Açma İşlemi Uygulanıyor.")
    kullanici_adi=input("Lütfen Kullanıcı Adınızı Giriniz:")
    sifre=input("Şifrenizi Giriniz:")
    
    if kullanici_adi=="admin" and  sifre=="123":
        print("Giriş Başarılı")
    else:
        print("Giriş Başarılı Değil")

# Karşılaştırma operatörleri (koşullu ifadelerde kullanılır):
# ==  eşittir           örnek: yuz_tanımlama == True
# !=  eşit değildir     örnek: kullanici_adi != "admin"
# >   büyüktür          örnek: arac_hizi > 50
# <   küçüktür          örnek: sicaklik < 0
# >=  büyük eşittir     örnek: puan >= 50
# <=  küçük eşittir     örnek: yas <= 18

# Mantıksal operatörler (birden fazla koşulu birleştirir):
# and  her iki koşul da doğru olmalı    örnek: yas >= 18 and kimlik_var == True
# or   koşullardan en az biri doğru     örnek: vip == True or puan >= 100
# not  koşulun tersini alır              örnek: not yuz_tanımlamaGir