yangin_alarmi_aktif=False
evde_insan_var_mi=True
oda_sicakliği=35


if yangin_alarmi_aktif:
    print("Yangın alarmı aktif. Fıskiyeler çalıştırılıyor. İtafayeye Haber Veriliyor.")

else:
    
    if evde_insan_var_mi:
        if oda_sicakliği>25:
            print("Klimalar Çalıştırılıyor.")
        elif oda_sicakliği<18:
            print("Kombi Çalıştırılıyor.")
        else:
            print("Konfor mod çalıştırıldı (Klima ve Kombi Açık Değil)")

    else:
        print("Eko Mod açıldı (Enerji Modu Aktif)")

