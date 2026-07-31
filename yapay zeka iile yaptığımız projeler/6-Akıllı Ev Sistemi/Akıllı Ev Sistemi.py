import tkinter as tk
from tkinter import font as tkfont


# --- Renkler ---
ARKA_PLAN = "#0b1020"
KART = "#161e34"
KENARLIK = "#2a3550"
YAZI = "#eef2ff"
YAZI_SOLUK = "#94a3b8"
VURGU = "#38bdf8"
BASARI = "#34d399"
UYARI = "#fbbf24"
TEHLIKE = "#f87171"
BASLIK_CUBUGU = "#121a2e"


class AkilliEvSistemi:
    """6-Akıllı Ev Sistemi.py mantığını masaüstü arayüzünde çalıştırır."""

    def __init__(self):
        self.pencere = tk.Tk()
        self.yangin_alarmi_aktif = tk.BooleanVar(self.pencere, value=False)
        self.evde_insan_var_mi = tk.BooleanVar(self.pencere, value=True)
        self.oda_sicakligi = tk.IntVar(self.pencere, value=35)

        self.pencere.title("Akıllı Ev Sistemi")
        self.pencere.configure(bg=ARKA_PLAN)
        self.pencere.geometry("720x680")
        self.pencere.minsize(600, 600)

        self._fontlari_ayarla()
        self._arayuz_olustur()
        self._pencereyi_ortala()
        self._saati_guncelle()
        self.guncelle_sistem()

    def _fontlari_ayarla(self):
        self.baslik_font = tkfont.Font(family="Segoe UI", size=20, weight="bold")
        self.alt_baslik_font = tkfont.Font(family="Segoe UI", size=10)
        self.kart_baslik_font = tkfont.Font(family="Segoe UI", size=12, weight="bold")
        self.normal_font = tkfont.Font(family="Segoe UI", size=11)
        self.kucuk_font = tkfont.Font(family="Segoe UI", size=9)
        self.durum_font = tkfont.Font(family="Segoe UI", size=13, weight="bold")
        self.sicaklik_font = tkfont.Font(family="Segoe UI", size=36, weight="bold")
        self.cihaz_font = tkfont.Font(family="Segoe UI", size=11, weight="bold")

    def _pencereyi_ortala(self):
        self.pencere.update_idletasks()
        genislik = self.pencere.winfo_width()
        yukseklik = self.pencere.winfo_height()
        x = (self.pencere.winfo_screenwidth() - genislik) // 2
        y = (self.pencere.winfo_screenheight() - yukseklik) // 2
        self.pencere.geometry(f"{genislik}x{yukseklik}+{x}+{y}")

    def _kart(self, ust, baslik, emoji):
        cerceve = tk.Frame(ust, bg=KART, highlightbackground=KENARLIK, highlightthickness=1)
        baslik_cerceve = tk.Frame(cerceve, bg=KART)
        baslik_cerceve.pack(fill="x", padx=16, pady=(14, 4))
        tk.Label(
            baslik_cerceve,
            text=emoji,
            font=self.kart_baslik_font,
            fg=YAZI,
            bg=KART,
        ).pack(side="left", padx=(0, 8))
        tk.Label(
            baslik_cerceve,
            text=baslik,
            font=self.kart_baslik_font,
            fg=YAZI,
            bg=KART,
        ).pack(side="left")
        return cerceve

    def _anahtar(self, ust, metin, degisken, komut):
        satir = tk.Frame(ust, bg=KART)
        satir.pack(fill="x", padx=16, pady=(8, 14))
        tk.Checkbutton(
            satir,
            text=metin,
            variable=degisken,
            font=self.normal_font,
            fg=YAZI,
            bg=KART,
            activebackground=KART,
            activeforeground=YAZI,
            selectcolor=KENARLIK,
            highlightthickness=0,
            command=komut,
        ).pack(anchor="w")

    def _arayuz_olustur(self):
        # --- Üst başlık ---
        ust = tk.Frame(self.pencere, bg=BASLIK_CUBUGU, padx=20, pady=16)
        ust.pack(fill="x")

        sol = tk.Frame(ust, bg=BASLIK_CUBUGU)
        sol.pack(side="left", fill="x", expand=True)

        tk.Label(sol, text="🏠", font=self.baslik_font, fg=YAZI, bg=BASLIK_CUBUGU).pack(
            side="left", padx=(0, 12)
        )
        baslik_metin = tk.Frame(sol, bg=BASLIK_CUBUGU)
        baslik_metin.pack(side="left")
        tk.Label(
            baslik_metin,
            text="Akıllı Ev Sistemi",
            font=self.baslik_font,
            fg=YAZI,
            bg=BASLIK_CUBUGU,
        ).pack(anchor="w")
        tk.Label(
            baslik_metin,
            text="Otomasyon kontrol paneli",
            font=self.alt_baslik_font,
            fg=YAZI_SOLUK,
            bg=BASLIK_CUBUGU,
        ).pack(anchor="w")

        sag = tk.Frame(ust, bg=BASLIK_CUBUGU)
        sag.pack(side="right")
        self.sistem_etiket = tk.Label(
            sag,
            text="● Sistem Aktif",
            font=self.kucuk_font,
            fg=BASARI,
            bg=BASLIK_CUBUGU,
        )
        self.sistem_etiket.pack(anchor="e")
        self.saat_etiket = tk.Label(
            sag,
            text="--:--",
            font=self.normal_font,
            fg=YAZI_SOLUK,
            bg=BASLIK_CUBUGU,
        )
        self.saat_etiket.pack(anchor="e")

        icerik = tk.Frame(self.pencere, bg=ARKA_PLAN, padx=20, pady=16)
        icerik.pack(fill="both", expand=True)

        # --- Durum paneli ---
        self.durum_panel = tk.Frame(icerik, bg="#1a3d32", highlightbackground=BASARI, highlightthickness=1)
        self.durum_panel.pack(fill="x", pady=(0, 16))

        durum_icerik = tk.Frame(self.durum_panel, bg="#1a3d32")
        durum_icerik.pack(fill="x", padx=16, pady=14)

        self.durum_ikon = tk.Label(
            durum_icerik,
            text="✓",
            font=self.durum_font,
            fg=YAZI,
            bg="#1a3d32",
            width=3,
        )
        self.durum_ikon.pack(side="left", padx=(0, 12))

        durum_metin = tk.Frame(durum_icerik, bg="#1a3d32")
        durum_metin.pack(side="left", fill="x", expand=True)
        tk.Label(
            durum_metin,
            text="SİSTEM DURUMU",
            font=self.kucuk_font,
            fg=YAZI_SOLUK,
            bg="#1a3d32",
        ).pack(anchor="w")
        self.durum_mesaj = tk.Label(
            durum_metin,
            text="",
            font=self.durum_font,
            fg=YAZI,
            bg="#1a3d32",
            wraplength=520,
            justify="left",
        )
        self.durum_mesaj.pack(anchor="w")

        # --- Kontroller ---
        kontrol_satir = tk.Frame(icerik, bg=ARKA_PLAN)
        kontrol_satir.pack(fill="x", pady=(0, 16))
        kontrol_satir.grid_columnconfigure(0, weight=1)
        kontrol_satir.grid_columnconfigure(1, weight=1)

        alarm_kart = self._kart(kontrol_satir, "Yangın Alarmı", "🔥")
        alarm_kart.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        tk.Label(
            alarm_kart,
            text="Alarm aktif olduğunda fıskiyeler devreye girer ve itfaiye bilgilendirilir.",
            font=self.kucuk_font,
            fg=YAZI_SOLUK,
            bg=KART,
            wraplength=260,
            justify="left",
        ).pack(anchor="w", padx=16, pady=(0, 4))
        self._anahtar(
            alarm_kart,
            "Yangın alarmını aç",
            self.yangin_alarmi_aktif,
            self.guncelle_sistem,
        )

        insan_kart = self._kart(kontrol_satir, "Evde Kimse Var mı?", "👤")
        insan_kart.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        tk.Label(
            insan_kart,
            text="Ev boşken enerji tasarrufu için eko mod devreye girer.",
            font=self.kucuk_font,
            fg=YAZI_SOLUK,
            bg=KART,
            wraplength=260,
            justify="left",
        ).pack(anchor="w", padx=16, pady=(0, 4))
        self._anahtar(
            insan_kart,
            "Evde insan var",
            self.evde_insan_var_mi,
            self.guncelle_sistem,
        )

        sicaklik_kart = self._kart(icerik, "Oda Sıcaklığı", "🌡️")
        sicaklik_kart.pack(fill="x", pady=(0, 16))

        sicaklik_goster = tk.Frame(sicaklik_kart, bg=KART)
        sicaklik_goster.pack(pady=(4, 8))
        self.sicaklik_etiket = tk.Label(
            sicaklik_goster,
            text="35",
            font=self.sicaklik_font,
            fg=UYARI,
            bg=KART,
        )
        self.sicaklik_etiket.pack(side="left")
        tk.Label(
            sicaklik_goster,
            text="°C",
            font=self.kart_baslik_font,
            fg=YAZI_SOLUK,
            bg=KART,
        ).pack(side="left", padx=(4, 0), pady=(12, 0))

        tk.Scale(
            sicaklik_kart,
            from_=10,
            to=45,
            orient="horizontal",
            variable=self.oda_sicakligi,
            font=self.normal_font,
            fg=YAZI,
            bg=KART,
            troughcolor=KENARLIK,
            activebackground=VURGU,
            highlightthickness=0,
            sliderlength=22,
            length=620,
            command=lambda _: self.guncelle_sistem(),
        ).pack(padx=16, pady=(0, 4))

        sicaklik_etiketler = tk.Frame(sicaklik_kart, bg=KART)
        sicaklik_etiketler.pack(fill="x", padx=16, pady=(0, 14))
        tk.Label(sicaklik_etiketler, text="10°C", font=self.kucuk_font, fg=YAZI_SOLUK, bg=KART).pack(
            side="left"
        )
        tk.Label(
            sicaklik_etiketler,
            text="Konfor: 18–25°C",
            font=self.kucuk_font,
            fg=BASARI,
            bg=KART,
        ).pack(side="left", expand=True)
        tk.Label(sicaklik_etiketler, text="45°C", font=self.kucuk_font, fg=YAZI_SOLUK, bg=KART).pack(
            side="right"
        )

        # --- Cihazlar ---
        tk.Label(
            icerik,
            text="CİHAZ DURUMLARI",
            font=self.kucuk_font,
            fg=YAZI_SOLUK,
            bg=ARKA_PLAN,
        ).pack(anchor="w", pady=(0, 8))

        cihaz_grid = tk.Frame(icerik, bg=ARKA_PLAN)
        cihaz_grid.pack(fill="x")
        for i in range(4):
            cihaz_grid.grid_columnconfigure(i, weight=1)

        self.cihazlar = {}
        cihaz_listesi = [
            ("klima", "❄️", "Klima"),
            ("kombi", "♨️", "Kombi"),
            ("fiskiye", "💧", "Fıskiyeler"),
            ("eko", "🌿", "Eko Mod"),
        ]

        for index, (anahtar, emoji, ad) in enumerate(cihaz_listesi):
            kart = tk.Frame(cihaz_grid, bg=KART, highlightbackground=KENARLIK, highlightthickness=1)
            kart.grid(row=0, column=index, sticky="nsew", padx=(0 if index == 0 else 4, 0), pady=2)

            tk.Label(kart, text=emoji, font=self.baslik_font, fg=YAZI_SOLUK, bg=KART).pack(pady=(12, 2))
            tk.Label(kart, text=ad, font=self.cihaz_font, fg=YAZI_SOLUK, bg=KART).pack()
            durum = tk.Label(kart, text="Kapalı", font=self.kucuk_font, fg=YAZI_SOLUK, bg=KART)
            durum.pack(pady=(2, 12))
            self.cihazlar[anahtar] = {"kart": kart, "durum": durum}

        tk.Label(
            self.pencere,
            text="Yapay Zeka Eğitimi — Akıllı Ev Sistemi Projesi",
            font=self.kucuk_font,
            fg=YAZI_SOLUK,
            bg=ARKA_PLAN,
            pady=10,
        ).pack(side="bottom")

    def _cihaz_guncelle(self, ad, aktif):
        bilgi = self.cihazlar[ad]
        if aktif:
            bilgi["kart"].configure(highlightbackground=VURGU)
            bilgi["durum"].configure(text="Açık", fg=BASARI)
            for etiket in bilgi["kart"].winfo_children():
                if isinstance(etiket, tk.Label):
                    etiket.configure(fg=YAZI)
        else:
            bilgi["kart"].configure(highlightbackground=KENARLIK)
            bilgi["durum"].configure(text="Kapalı", fg=YAZI_SOLUK)
            for etiket in bilgi["kart"].winfo_children():
                if isinstance(etiket, tk.Label):
                    etiket.configure(fg=YAZI_SOLUK)

    def _durum_paneli_ayarla(self, mod):
        renkler = {
            "basari": ("#1a3d32", BASARI),
            "uyari": ("#3d3418", UYARI),
            "tehlike": ("#3d1f1f", TEHLIKE),
        }
        arka_plan, kenarlik = renkler[mod]

        self.durum_panel.configure(bg=arka_plan, highlightbackground=kenarlik)
        for cerceve in self.durum_panel.winfo_children():
            cerceve.configure(bg=arka_plan)
            for cocuk in cerceve.winfo_children():
                if isinstance(cocuk, tk.Frame):
                    cocuk.configure(bg=arka_plan)
                    for torun in cocuk.winfo_children():
                        if isinstance(torun, tk.Label) and torun is not self.durum_ikon:
                            torun.configure(bg=arka_plan)
                elif isinstance(cocuk, tk.Label) and cocuk is not self.durum_ikon:
                    cocuk.configure(bg=arka_plan)
        self.durum_ikon.configure(bg=arka_plan)

    def _sicaklik_rengi(self, sicaklik):
        if sicaklik > 25:
            return UYARI
        if sicaklik < 18:
            return VURGU
        return BASARI

    def guncelle_sistem(self):
        yangin_alarmi_aktif = self.yangin_alarmi_aktif.get()
        evde_insan_var_mi = self.evde_insan_var_mi.get()
        oda_sicakligi = self.oda_sicakligi.get()

        self.sicaklik_etiket.configure(
            text=str(oda_sicakligi),
            fg=self._sicaklik_rengi(oda_sicakligi),
        )

        for ad in self.cihazlar:
            self._cihaz_guncelle(ad, False)

        if yangin_alarmi_aktif:
            self._durum_paneli_ayarla("tehlike")
            self.durum_ikon.configure(text="🚨")
            self.durum_mesaj.configure(
                text="Yangın alarmı aktif. Fıskiyeler çalıştırılıyor. İtfaiyeye haber veriliyor."
            )
            self._cihaz_guncelle("fiskiye", True)
            return

        if not evde_insan_var_mi:
            self._durum_paneli_ayarla("uyari")
            self.durum_ikon.configure(text="🌿")
            self.durum_mesaj.configure(text="Eko Mod açıldı (Enerji Modu Aktif)")
            self._cihaz_guncelle("eko", True)
            return

        if oda_sicakligi > 25:
            self._durum_paneli_ayarla("uyari")
            self.durum_ikon.configure(text="❄️")
            self.durum_mesaj.configure(text="Klimalar çalıştırılıyor.")
            self._cihaz_guncelle("klima", True)
        elif oda_sicakligi < 18:
            self._durum_paneli_ayarla("uyari")
            self.durum_ikon.configure(text="♨️")
            self.durum_mesaj.configure(text="Kombi çalıştırılıyor.")
            self._cihaz_guncelle("kombi", True)
        else:
            self._durum_paneli_ayarla("basari")
            self.durum_ikon.configure(text="✓")
            self.durum_mesaj.configure(
                text="Konfor mod çalıştırıldı (Klima ve Kombi Açık Değil)"
            )

    def _saati_guncelle(self):
        from datetime import datetime

        self.saat_etiket.configure(text=datetime.now().strftime("%H:%M"))
        self.pencere.after(1000, self._saati_guncelle)

    def calistir(self):
        self.pencere.mainloop()


if __name__ == "__main__":
    uygulama = AkilliEvSistemi()
    uygulama.calistir()
