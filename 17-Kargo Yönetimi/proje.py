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


def verileri_kaydet(data):
    pass


verileri_yukle()