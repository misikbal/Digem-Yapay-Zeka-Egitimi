# Sayı Tahmin Oyunu — Modern Arayüz (tkinter)
# Ders dosyası: 11-sayi-tahmin-oyunu.py (terminal sürümü)
# Çalıştırmak için: python3 "Sayı Tahmin Oyunu.py"

import tkinter as tk
from tkinter import font as tkfont
from random import randint

# --- Renk paleti ---
ZEMIN = "#0e1024"
KART = "#181b36"
KART_ACIK = "#20244a"
MOR = "#6c5ce7"
MOR_HOVER = "#8577f0"
YESIL = "#00d2a0"
KIRMIZI = "#ff5c7a"
SARI = "#ffc857"
MAVI = "#4aa8ff"
YAZI = "#eef0ff"
SOLUK = "#8b90bd"

ZORLUKLAR = {
    "Kolay": {"alt": 1, "ust": 10, "hak": 4},
    "Orta": {"alt": 1, "ust": 50, "hak": 6},
    "Zor": {"alt": 1, "ust": 100, "hak": 8},
}


def yuvarlak_dikdortgen(tuval, x1, y1, x2, y2, yaricap=16, **ayarlar):
    """Canvas üzerinde yuvarlak köşeli dikdörtgen çizer."""
    noktalar = [
        x1 + yaricap, y1,
        x2 - yaricap, y1, x2, y1,
        x2, y1 + yaricap,
        x2, y2 - yaricap, x2, y2,
        x2 - yaricap, y2,
        x1 + yaricap, y2, x1, y2,
        x1, y2 - yaricap,
        x1, y1 + yaricap, x1, y1,
    ]
    return tuval.create_polygon(noktalar, smooth=True, **ayarlar)


def renk_karistir(renk1, renk2, oran):
    """İki hex rengi arasında geçiş rengi üretir (oran: 0.0 - 1.0)."""
    r1, g1, b1 = (int(renk1[i:i + 2], 16) for i in (1, 3, 5))
    r2, g2, b2 = (int(renk2[i:i + 2], 16) for i in (1, 3, 5))
    r = round(r1 + (r2 - r1) * oran)
    g = round(g1 + (g2 - g1) * oran)
    b = round(b1 + (b2 - b1) * oran)
    return f"#{r:02x}{g:02x}{b:02x}"


def uygun_font(*adaylar):
    mevcut = {ad.lower() for ad in tkfont.families()}
    for ad in adaylar:
        if ad.lower() in mevcut:
            return ad
    return "TkDefaultFont"


class YuvarlakButon(tk.Canvas):
    def __init__(self, ebeveyn, metin, komut, genislik=150, yukseklik=48,
                 dolgu=MOR, dolgu_hover=MOR_HOVER, yazi_rengi=YAZI,
                 kenar=None, yaricap=16, font=None):
        super().__init__(ebeveyn, width=genislik, height=yukseklik,
                         bg=ebeveyn["bg"], highlightthickness=0, bd=0)
        self.komut = komut
        self.dolgu = dolgu
        self.dolgu_hover = dolgu_hover
        self.aktif = True

        self.sekil = yuvarlak_dikdortgen(
            self, 2, 2, genislik - 2, yukseklik - 2, yaricap,
            fill=dolgu, outline=kenar or dolgu, width=2,
        )
        self.yazi = self.create_text(genislik / 2, yukseklik / 2,
                                     text=metin, fill=yazi_rengi, font=font)

        self.bind("<Enter>", self._uzerine_gelince)
        self.bind("<Leave>", self._ayrilinca)
        self.bind("<Button-1>", self._tiklaninca)

    def _uzerine_gelince(self, _=None):
        if self.aktif:
            self.itemconfig(self.sekil, fill=self.dolgu_hover)
            self.configure(cursor="hand2")

    def _ayrilinca(self, _=None):
        self.itemconfig(self.sekil, fill=self.dolgu)
        self.configure(cursor="")

    def _tiklaninca(self, _=None):
        if self.aktif and self.komut:
            self.komut()

    def gorunum_ayarla(self, dolgu, dolgu_hover, yazi_rengi, kenar=None):
        self.dolgu = dolgu
        self.dolgu_hover = dolgu_hover
        self.itemconfig(self.sekil, fill=dolgu, outline=kenar or dolgu)
        self.itemconfig(self.yazi, fill=yazi_rengi)

    def durum_ayarla(self, aktif):
        self.aktif = aktif
        self.itemconfig(self.yazi, fill=YAZI if aktif else SOLUK)


class SicaklikCubugu(tk.Canvas):
    """Tahminin sayıya ne kadar yakın olduğunu gösteren çubuk."""

    def __init__(self, ebeveyn, genislik=340, yukseklik=12):
        super().__init__(ebeveyn, width=genislik, height=yukseklik,
                         bg=ebeveyn["bg"], highlightthickness=0, bd=0)
        self.genislik = genislik
        self.yukseklik = yukseklik
        self.oran = 0.0
        self.hedef_oran = 0.0
        self._animasyon = None
        self._ciz()

    def _ciz(self):
        self.delete("all")
        yuvarlak_dikdortgen(self, 0, 0, self.genislik, self.yukseklik,
                            self.yukseklik / 2, fill=KART_ACIK, outline=KART_ACIK)
        dolu = self.oran * self.genislik
        if dolu > self.yukseklik:
            renk = renk_karistir(MAVI, KIRMIZI, self.oran)
            yuvarlak_dikdortgen(self, 0, 0, dolu, self.yukseklik,
                                self.yukseklik / 2, fill=renk, outline=renk)

    def ayarla(self, hedef_oran):
        self.hedef_oran = max(0.0, min(1.0, hedef_oran))
        if self._animasyon:
            self.after_cancel(self._animasyon)
        self._adim()

    def _adim(self):
        fark = self.hedef_oran - self.oran
        if abs(fark) < 0.01:
            self.oran = self.hedef_oran
            self._ciz()
            self._animasyon = None
            return
        self.oran += fark * 0.25
        self._ciz()
        self._animasyon = self.after(16, self._adim)


class SayiTahminOyunu:
    def __init__(self, kok):
        self.kok = kok
        self.zorluk = "Orta"
        self.zorluk_butonlari = {}
        self.gecmis = []

        baslik_font = uygun_font("Segoe UI Semibold", "Ubuntu", "DejaVu Sans", "Arial")
        govde_font = uygun_font("Segoe UI", "Ubuntu", "DejaVu Sans", "Arial")

        self.f_baslik = (baslik_font, 24, "bold")
        self.f_alt_baslik = (govde_font, 11)
        self.f_etiket = (govde_font, 10, "bold")
        self.f_mesaj = (govde_font, 14, "bold")
        self.f_ipucu = (govde_font, 11)
        self.f_giris = (govde_font, 28, "bold")
        self.f_buton = (govde_font, 12, "bold")
        self.f_kalp = (govde_font, 18)
        self.f_cip = (govde_font, 11, "bold")

        self._pencere_kur()
        self._arayuz_kur()
        self.yeni_oyun()

    # --- Arayüz kurulumu ---

    def _pencere_kur(self):
        self.kok.title("Sayı Tahmin Oyunu")
        self.kok.configure(bg=ZEMIN)
        self.kok.resizable(False, False)
        genislik, yukseklik = 460, 700
        x = (self.kok.winfo_screenwidth() - genislik) // 2
        y = max(0, (self.kok.winfo_screenheight() - yukseklik) // 2 - 20)
        self.kok.geometry(f"{genislik}x{yukseklik}+{x}+{y}")
        self.kok.bind("<Return>", lambda _: self.tahmin_et())
        self.kok.bind("<Escape>", lambda _: self.yeni_oyun())

    def _arayuz_kur(self):
        kabuk = tk.Frame(self.kok, bg=ZEMIN)
        kabuk.pack(fill="both", expand=True, padx=28, pady=24)

        tk.Label(kabuk, text="Sayı Tahmin Oyunu", bg=ZEMIN, fg=YAZI,
                 font=self.f_baslik).pack(anchor="w")
        tk.Label(kabuk, text="Tuttuğum sayıyı hakkın bitmeden bulabilir misin?",
                 bg=ZEMIN, fg=SOLUK, font=self.f_alt_baslik).pack(anchor="w", pady=(4, 18))

        self._zorluk_kur(kabuk)
        self._durum_karti_kur(kabuk)
        self._giris_kur(kabuk)
        self._gecmis_kur(kabuk)

    def _zorluk_kur(self, ebeveyn):
        tk.Label(ebeveyn, text="ZORLUK", bg=ZEMIN, fg=SOLUK,
                 font=self.f_etiket).pack(anchor="w")
        satir = tk.Frame(ebeveyn, bg=ZEMIN)
        satir.pack(fill="x", pady=(8, 18))

        for ad in ZORLUKLAR:
            buton = YuvarlakButon(
                satir, ad, lambda a=ad: self.zorluk_sec(a),
                genislik=126, yukseklik=44, dolgu=KART, dolgu_hover=KART_ACIK,
                kenar=KART_ACIK, font=self.f_buton,
            )
            buton.pack(side="left", padx=(0, 9))
            self.zorluk_butonlari[ad] = buton

    def _durum_karti_kur(self, ebeveyn):
        kart = tk.Frame(ebeveyn, bg=KART)
        kart.pack(fill="x")
        ic = tk.Frame(kart, bg=KART)
        ic.pack(fill="x", padx=20, pady=20)

        self.aralik_etiketi = tk.Label(ic, text="", bg=KART, fg=SOLUK,
                                       font=self.f_etiket)
        self.aralik_etiketi.pack(anchor="w")

        self.kalpler = tk.Label(ic, text="", bg=KART, fg=KIRMIZI,
                                font=self.f_kalp)
        self.kalpler.pack(anchor="w", pady=(6, 12))

        self.mesaj = tk.Label(ic, text="", bg=KART, fg=YAZI,
                              font=self.f_mesaj, wraplength=340, justify="left")
        self.mesaj.pack(anchor="w")

        self.ipucu = tk.Label(ic, text="", bg=KART, fg=SOLUK,
                              font=self.f_ipucu, wraplength=340, justify="left")
        self.ipucu.pack(anchor="w", pady=(4, 14))

        self.sicaklik = SicaklikCubugu(ic, genislik=340)
        self.sicaklik.pack(anchor="w")

    def _giris_kur(self, ebeveyn):
        cerceve = tk.Frame(ebeveyn, bg=ZEMIN)
        cerceve.pack(fill="x", pady=(18, 0))

        kenarlik = tk.Frame(cerceve, bg=KART_ACIK)
        kenarlik.pack(fill="x")
        self.giris = tk.Entry(kenarlik, font=self.f_giris, justify="center",
                              bg=KART, fg=YAZI, insertbackground=MOR,
                              disabledbackground=KART, disabledforeground=SOLUK,
                              relief="flat", bd=0)
        self.giris.pack(fill="x", padx=2, pady=2, ipady=10)
        self.giris.bind("<FocusIn>", lambda _: kenarlik.configure(bg=MOR))
        self.giris.bind("<FocusOut>", lambda _: kenarlik.configure(bg=KART_ACIK))

        butonlar = tk.Frame(cerceve, bg=ZEMIN)
        butonlar.pack(fill="x", pady=(14, 0))

        self.tahmin_butonu = YuvarlakButon(
            butonlar, "Tahmin Et", self.tahmin_et,
            genislik=250, yukseklik=52, font=self.f_buton,
        )
        self.tahmin_butonu.pack(side="left")

        YuvarlakButon(
            butonlar, "Yeni Oyun", self.yeni_oyun,
            genislik=140, yukseklik=52, dolgu=KART, dolgu_hover=KART_ACIK,
            kenar=KART_ACIK, font=self.f_buton,
        ).pack(side="left", padx=(12, 0))

    def _gecmis_kur(self, ebeveyn):
        tk.Label(ebeveyn, text="TAHMİNLERİN", bg=ZEMIN, fg=SOLUK,
                 font=self.f_etiket).pack(anchor="w", pady=(22, 8))
        self.gecmis_alani = tk.Frame(ebeveyn, bg=ZEMIN, height=70)
        self.gecmis_alani.pack(fill="both", expand=True)

    # --- Oyun akışı ---

    def zorluk_sec(self, ad):
        self.zorluk = ad
        self.yeni_oyun()

    def yeni_oyun(self):
        ayar = ZORLUKLAR[self.zorluk]
        self.alt, self.ust = ayar["alt"], ayar["ust"]
        self.rastgele_sayi = randint(self.alt, self.ust)
        self.hak = ayar["hak"]
        self.oyun_bitti = False
        self.gecmis.clear()

        for ad, buton in self.zorluk_butonlari.items():
            if ad == self.zorluk:
                buton.gorunum_ayarla(MOR, MOR_HOVER, YAZI)
            else:
                buton.gorunum_ayarla(KART, KART_ACIK, SOLUK, kenar=KART_ACIK)

        self.aralik_etiketi.configure(text=f"{self.alt} - {self.ust} ARASINDA BİR SAYI")
        self.mesaj.configure(text="Hadi başlayalım!", fg=YAZI)
        self.ipucu.configure(text="Bir sayı yaz ve Enter'a bas.")
        self.sicaklik.ayarla(0)
        self.tahmin_butonu.durum_ayarla(True)
        self.tahmin_butonu.itemconfig(self.tahmin_butonu.yazi, text="Tahmin Et")
        self.giris.configure(state="normal")
        self.giris.delete(0, "end")
        self.giris.focus_set()
        self._kalpleri_ciz()
        self._gecmisi_ciz()

    def tahmin_et(self):
        if self.oyun_bitti:
            self.yeni_oyun()
            return

        metin = self.giris.get().strip()
        self.giris.delete(0, "end")

        if not metin.lstrip("-").isdigit():
            self._uyar("Lütfen sadece sayı gir.")
            return

        tahmin = int(metin)
        if not self.alt <= tahmin <= self.ust:
            self._uyar(f"Sayı {self.alt} ile {self.ust} arasında olmalı.")
            return

        if tahmin in [t for t, _ in self.gecmis]:
            self._uyar(f"{tahmin} sayısını daha önce denedin.")
            return

        uzaklik = abs(tahmin - self.rastgele_sayi)
        self.sicaklik.ayarla(1 - uzaklik / (self.ust - self.alt))

        if tahmin == self.rastgele_sayi:
            self.gecmis.append((tahmin, "dogru"))
            self._kazandi()
        else:
            yon = "kucuk" if tahmin > self.rastgele_sayi else "buyuk"
            self.gecmis.append((tahmin, yon))
            self.hak -= 1
            self._kalpleri_ciz()
            if self.hak == 0:
                self._kaybetti()
            else:
                if yon == "kucuk":
                    self.mesaj.configure(text="Daha küçük bir sayı gir", fg=MAVI)
                else:
                    self.mesaj.configure(text="Daha büyük bir sayı gir", fg=SARI)
                self.ipucu.configure(text=self._yakinlik_ipucu(uzaklik))
                self._salla()

        self._gecmisi_ciz()

    def _yakinlik_ipucu(self, uzaklik):
        oran = uzaklik / (self.ust - self.alt)
        if oran <= 0.05:
            return "Yanıyorsun, çok yakınsın!"
        if oran <= 0.15:
            return "Sıcak, doğru yoldasın."
        if oran <= 0.35:
            return "Ilık, biraz daha yaklaş."
        return "Buz gibi, sayıdan uzaktasın."

    def _uyar(self, metin):
        self.mesaj.configure(text=metin, fg=SARI)
        self.ipucu.configure(text="Bu deneme hakkından düşmedi.")
        self._salla()

    def _kazandi(self):
        self.oyun_bitti = True
        deneme = len(self.gecmis)
        self.mesaj.configure(text=f"Tebrikler, kazandın! Sayı {self.rastgele_sayi}",
                             fg=YESIL)
        self.ipucu.configure(text=f"{deneme} denemede buldun. Yeni oyun için Enter'a bas.")
        self.sicaklik.ayarla(1)
        self._oyunu_kapat()

    def _kaybetti(self):
        self.oyun_bitti = True
        self.mesaj.configure(text=f"Hakların bitti! Sayı {self.rastgele_sayi} idi",
                             fg=KIRMIZI)
        self.ipucu.configure(text="Yeni oyun için Enter'a bas.")
        self._oyunu_kapat()
        self._salla()

    def _oyunu_kapat(self):
        self.giris.configure(state="disabled")
        self.tahmin_butonu.itemconfig(self.tahmin_butonu.yazi, text="Tekrar Oyna")

    # --- Görsel yardımcılar ---

    def _kalpleri_ciz(self):
        toplam = ZORLUKLAR[self.zorluk]["hak"]
        dolu = "\u2665 " * self.hak
        bos = "\u2661 " * (toplam - self.hak)
        self.kalpler.configure(text=(dolu + bos).strip())

    def _gecmisi_ciz(self):
        for cocuk in self.gecmis_alani.winfo_children():
            cocuk.destroy()

        satir = tk.Frame(self.gecmis_alani, bg=ZEMIN)
        satir.pack(anchor="w")
        for sira, (tahmin, yon) in enumerate(self.gecmis):
            if sira and sira % 5 == 0:
                satir = tk.Frame(self.gecmis_alani, bg=ZEMIN)
                satir.pack(anchor="w", pady=(8, 0))

            if yon == "dogru":
                renk, isaret = YESIL, "\u2713"
            elif yon == "kucuk":
                renk, isaret = MAVI, "\u2193"
            else:
                renk, isaret = SARI, "\u2191"

            cip = tk.Canvas(satir, width=68, height=34, bg=ZEMIN,
                            highlightthickness=0, bd=0)
            cip.pack(side="left", padx=(0, 8))
            yuvarlak_dikdortgen(cip, 1, 1, 67, 33, 12, fill=KART, outline=renk)
            cip.create_text(34, 17, text=f"{tahmin} {isaret}", fill=renk,
                            font=self.f_cip)

    def _salla(self, adim=0):
        """Hatalı tahminde pencereyi kısa süre titretir."""
        if adim == 0:
            self._asil_x = self.kok.winfo_x()
            self._asil_y = self.kok.winfo_y()
        if adim >= 6:
            self.kok.geometry(f"+{self._asil_x}+{self._asil_y}")
            return
        kayma = 8 if adim % 2 == 0 else -8
        self.kok.geometry(f"+{self._asil_x + kayma}+{self._asil_y}")
        self.kok.after(30, lambda: self._salla(adim + 1))


if __name__ == "__main__":
    kok = tk.Tk()
    SayiTahminOyunu(kok)
    kok.mainloop()
