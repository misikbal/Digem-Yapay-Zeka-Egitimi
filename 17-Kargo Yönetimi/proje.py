import json


dosya_adi="data.json"


def verileri_yukle():

    try:
        with open(dosya_adi, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("data.json dosyası bulunamadı. Yeni bir veritabanı dosyası oluşturuluyor")
        varsayilan_veri={"kargolar":{}}
        verileri_kaydet(varsayilan_veri)
        return varsayilan_veri

    except json.JSONDecodeError:
        print("Json dosyasında bir bozuluklu var Sistem varsayılan ayarlarda çalıştırılıyor")
        return {"kargolar":{}}


def verileri_kaydet(yeni_veri):
    try:
        with open(dosya_adi,"w",encoding="utf-8") as var_olan_veriler:
            json.dump(yeni_veri, var_olan_veriler, indent=4, ensure_ascii=False)

    except Exception as error:
        print(f"Dosya yazım hatası oluştu Hata Kodu:{error}")

def kargo_sorgula(kargo_veri):
    kod=input("Takip Numarsını Giriniz: (Örn:TR101)").strip().upper()

    try:
        bilgi=kargo_veri["kargolar"][kod]
        print(f"""
        Kargo Bilgisi {kod}

        Alıcı: {bilgi["alici"]}

        Ürün: {bilgi["urun"]}

        Durum: {bilgi["durum"]}

        Ağırlık: {bilgi["agirilik_kg"]}
        
        
        """)

    except KeyError:

        print(f" Hata: {kod} numaralı bir kargo kaydı sistemde bulunamadı")
        
def yeni_kargo_ekle(kargo_veri):

    print("Yeni Kargo Girişi")
    kod=input("Takip Bumarası Belirleyin (Örn TR103)").strip().upper()
    
    if kod in kargo_veri["kargolar"]:
        print("Bu takip numarası zaten sistemde kayıtlı")
        return

    alici=input("Alıcı Ad Soyad").strip()
    urun=input("Ürün Açıklaması").strip()
    

    while True:
        try:
            agirilik=float(input("Kargo Ağırlığını Giriniz KG: Örn:1.5):"))

            if agirilik<=0:
                print("Ağırlık 0 veya negatif olamaz Tekrar Deneyiniz")
                continue
            break

        except ValueError:
            print("Hata: Lütfen ağırlığı sadece sayı/ondalıklı olarak giriniz (Örn 1.5)")

    kargo_veri["kargolar"][kod]={
        "alici":alici,
        "urun":urun,
        "durum":"Kargo Alındı",
        "agirilik_kg":agirilik
    }

    verileri_kaydet(kargo_veri)
    print(f"{kod} takip numaralı kargo başarılı bir şekilde oluşturuldu.")


verileri_yukle()