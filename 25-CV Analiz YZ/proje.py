from openai import OpenAI
import sqlite3
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

OPENAI_API_KEY = "sk-proj-xxx"

client=OpenAI(api_key=OPENAI_API_KEY)


DB_NAME = "cv_analyzer.db"


def veritabani_olustur():
    connection=sqlite3.connect(DB_NAME)
    cursor=connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analyses(

    
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cv_text TEXT NOT NULL,
        job_description TEXT NOT NULL,
        match_score INTEGER,
        analysis TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    
    """)

    connection.commit()
    connection.close()



def cv_analiz(cv_metni, is_ilani):

    prompt=f"""
    Sen deneyimli bir teknik işe alım uzmanısın.
    Aşağıdaki CV ile iş ilanını karşılaştır.
    CV:
    ----------------
    {cv_metni}


    İŞ İLANI:
    ----------------
    {is_ilani}
    ----------------


    Aşağıdaki başlıklarda analiz yap:

    1. GÜÇLÜ YÖNLER
    2. EKSİK YETKİNLİKLER
    3. GELİŞTİRİLMESİ GEREKEN NOKTALAR
    4. UYGUNLUK PUANI
    5. GELİŞTİRİLMİŞ CV ÖZETİ


    Uygunluk puanını ayrıca şu formatta yaz:

    PUAN: 75

    Puan 0 ile 100 arasında olsun.

    """


    response=client.responses.create(

        model="gpt-6-luna",

        input=prompt
    )

    return response.output_text



def puani_bul(analiz):
    try:
         satirlar = analiz.split("\n")

         for satir in satirlar:
            if "PUAN:" in satir.upper():
                puan_metni=satir.split(":")[1].strip()
                puan = int (puan_metni)
                return puan

    except:
        pass

    return 0

def analiz_kaydet(cv_metni, is_ilani,puan,analiz):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO analyses(
        cv_text,
        job_description,
        match_score,
        analysis

    
    )
    VALUES(?,?,?,?)
    
    """,(
        cv_metni,
        is_ilani,
        puan,
        analiz
    ))

    connection.commit()
    connection.close()

    print("ANaliz Veritabanına Kaydedildi")

def analizleri_listele():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
    SELECT id, match_score, created_at
    FROM analyses
    ORDER BY id DESC
    """)

    analizler=cursor.fetchall()

    connection.close()

    if len(analizler) == 0:
        print("\nHenüz kayıtlı analiz bulunmuyor.")
        return

    print("\n" + "=" * 50)
    print("GEÇMİŞ ANALİZLER")
    print("=" * 50)


    for analiz in analizler:

        print(f"""
            ID: {analiz[0]}
            Puan: {analiz[1]}
            Tarih: {analiz[2]}
            -----------------------------
        """)



def analiz_detayi_goster():


    analiz_id=input("Görüntülemek istediğiniz analiz ID'sini giriniz:")


    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()


    cursor.execute("""
    SELECT * FROM analyses WHERE id=?   
    
    """,(analiz_id,))

    analiz=cursor.fetchone()


    connection.close()

    if analiz is None:
        print("Analiz Bulunmadı")
        return


    print("\n" + "=" * 60)
    print("ANALİZ DETAYI")
    print("=" * 60)


    print(f"""
    ID:
    {analiz[0]}

    TARİH:
    {analiz[5]}

    UYGUNLUK PUANI:
    {analiz[3]}

    CV:
    {analiz[1]}

    İŞ İLANI:
    {analiz[2]}

    AI ANALİZİ:
    {analiz[4]}
    """)



def yeni_analiz():
    print("\n" + "=" * 50)
    print("YENİ CV ANALİZİ")
    print("=" * 50)


    cv_metni = input("\nCV metninizi giriniz:\n\n")

    is_ilani = input("\nİş ilanını giriniz:\n\n")

    print("\nCV analiz ediliyor...\n")



    try:

        sonuc=cv_analiz(
            cv_metni,
            is_ilani
        )


        puan=puani_bul(sonuc)
        

        print("ANALİZ SONUC:")
        print(sonuc)

        analiz_kaydet(
            cv_metni,
            is_ilani,
            puan,
            sonuc
        )



    except Exception as hata:
        print("Bir hata oluştu:",hata)





def menu():
    while True:
        print("""
        =================================
                AI CV ANALİZ BOTU
        =================================

        1 - Yeni CV Analizi
        2 - Geçmiş Analizleri Listele
        3 - Analiz Detayı Göster
        4 - Çıkış
        """)

        secim=input("Seçiminiz:")

        if secim=="1":
            yeni_analiz()

        elif secim=="2":
            analizleri_listele()

        elif secim=="3":
            analiz_detayi_goster()
        elif secim=="4":
            print("Çıkış yapılıyor")
            break

        else:
            print("Geçersiz tuşlama yaptınız")



def arayuz():
    pencere = tk.Tk()
    pencere.title("AI CV Analiz Botu")
    pencere.geometry("1100x750")

    sekmeler = ttk.Notebook(pencere)
    sekmeler.pack(fill="both", expand=True, padx=10, pady=10)


    # ---------- YENİ ANALİZ SEKMESİ ----------
    analiz_sekmesi = ttk.Frame(sekmeler)
    sekmeler.add(analiz_sekmesi, text="Yeni CV Analizi")

    analiz_sekmesi.columnconfigure(0, weight=1)
    analiz_sekmesi.columnconfigure(1, weight=1)
    analiz_sekmesi.rowconfigure(1, weight=1)
    analiz_sekmesi.rowconfigure(4, weight=1)

    ttk.Label(analiz_sekmesi, text="CV Metni:").grid(row=0, column=0, sticky="w", padx=5, pady=(5, 0))
    ttk.Label(analiz_sekmesi, text="İş İlanı:").grid(row=0, column=1, sticky="w", padx=5, pady=(5, 0))

    cv_kutusu = scrolledtext.ScrolledText(analiz_sekmesi, wrap="word", undo=True)
    cv_kutusu.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

    ilan_kutusu = scrolledtext.ScrolledText(analiz_sekmesi, wrap="word", undo=True)
    ilan_kutusu.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

    alt_cubuk = ttk.Frame(analiz_sekmesi)
    alt_cubuk.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

    analiz_butonu = ttk.Button(alt_cubuk, text="Analiz Et")
    analiz_butonu.pack(side="left")

    temizle_butonu = ttk.Button(alt_cubuk, text="Temizle")
    temizle_butonu.pack(side="left", padx=5)

    durum_yazisi = ttk.Label(alt_cubuk, text="")
    durum_yazisi.pack(side="left", padx=10)

    ttk.Label(analiz_sekmesi, text="Analiz Sonucu:").grid(row=3, column=0, sticky="w", padx=5)

    sonuc_kutusu = scrolledtext.ScrolledText(analiz_sekmesi, wrap="word", state="disabled")
    sonuc_kutusu.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)


    def sonucu_yaz(kutu, metin):
        kutu.config(state="normal")
        kutu.delete("1.0", "end")
        kutu.insert("1.0", metin)
        kutu.config(state="disabled")


    def analiz_bitti(sonuc, puan, hata):
        analiz_butonu.config(state="normal")

        if hata:
            durum_yazisi.config(text="")
            messagebox.showerror("Hata", f"Bir hata oluştu:\n{hata}")
            return

        durum_yazisi.config(text=f"Uygunluk Puanı: {puan}  (Veritabanına kaydedildi)")
        sonucu_yaz(sonuc_kutusu, sonuc)
        gecmisi_yenile()


    def analiz_et():
        cv_metni = cv_kutusu.get("1.0", "end").strip()
        is_ilani = ilan_kutusu.get("1.0", "end").strip()

        if not cv_metni or not is_ilani:
            messagebox.showwarning("Eksik Bilgi", "Lütfen CV metnini ve iş ilanını giriniz.")
            return

        analiz_butonu.config(state="disabled")
        durum_yazisi.config(text="CV analiz ediliyor, lütfen bekleyin...")
        sonucu_yaz(sonuc_kutusu, "")

        def arka_planda():
            try:
                sonuc = cv_analiz(cv_metni, is_ilani)
                puan = puani_bul(sonuc)
                analiz_kaydet(cv_metni, is_ilani, puan, sonuc)
                pencere.after(0, analiz_bitti, sonuc, puan, None)
            except Exception as hata:
                pencere.after(0, analiz_bitti, None, None, hata)

        threading.Thread(target=arka_planda, daemon=True).start()


    def temizle():
        cv_kutusu.delete("1.0", "end")
        ilan_kutusu.delete("1.0", "end")
        sonucu_yaz(sonuc_kutusu, "")
        durum_yazisi.config(text="")


    analiz_butonu.config(command=analiz_et)
    temizle_butonu.config(command=temizle)


    # ---------- GEÇMİŞ ANALİZLER SEKMESİ ----------
    gecmis_sekmesi = ttk.Frame(sekmeler)
    sekmeler.add(gecmis_sekmesi, text="Geçmiş Analizler")

    gecmis_sekmesi.columnconfigure(1, weight=1)
    gecmis_sekmesi.rowconfigure(0, weight=1)

    tablo = ttk.Treeview(gecmis_sekmesi, columns=("id", "puan", "tarih"), show="headings", selectmode="browse")
    tablo.heading("id", text="ID")
    tablo.heading("puan", text="Puan")
    tablo.heading("tarih", text="Tarih")
    tablo.column("id", width=50, anchor="center")
    tablo.column("puan", width=60, anchor="center")
    tablo.column("tarih", width=160, anchor="center")
    tablo.grid(row=0, column=0, sticky="ns", padx=5, pady=5)

    detay_kutusu = scrolledtext.ScrolledText(gecmis_sekmesi, wrap="word", state="disabled")
    detay_kutusu.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)


    def gecmisi_yenile():
        tablo.delete(*tablo.get_children())

        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        cursor.execute("SELECT id, match_score, created_at FROM analyses ORDER BY id DESC")
        analizler = cursor.fetchall()
        connection.close()

        for analiz in analizler:
            tablo.insert("", "end", values=analiz)


    def detay_goster(event):
        secili = tablo.selection()
        if not secili:
            return

        analiz_id = tablo.item(secili[0], "values")[0]

        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM analyses WHERE id=?", (analiz_id,))
        analiz = cursor.fetchone()
        connection.close()

        if analiz is None:
            return

        metin = (
            f"ID: {analiz[0]}\n"
            f"TARİH: {analiz[5]}\n"
            f"UYGUNLUK PUANI: {analiz[3]}\n\n"
            f"===== CV =====\n{analiz[1]}\n\n"
            f"===== İŞ İLANI =====\n{analiz[2]}\n\n"
            f"===== AI ANALİZİ =====\n{analiz[4]}\n"
        )
        sonucu_yaz(detay_kutusu, metin)


    tablo.bind("<<TreeviewSelect>>", detay_goster)
    gecmisi_yenile()

    pencere.mainloop()



veritabani_olustur()
arayuz()