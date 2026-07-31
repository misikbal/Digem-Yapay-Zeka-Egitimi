import math
import tkinter as tk
from tkinter import font as tkfont


# --- Renkler (Windows Hesap Makinesi tarzı) ---
ARKA_PLAN = "#171717"
BASLIK_CUBUGU = "#1f1f1f"
EKRAN_RENK = "#1f1f1f"
AYIRICI = "#2f2f2f"
BUTON_RENK = "#505050"
BUTON_BASILI = "#666666"
ESIT_RENK = "#ff9500"
ESIT_BASILI = "#ffb04d"
YAZI = "#ffffff"
YAZI_SOLUK = "#cccccc"


class GelismisHesapMakinesi:
    """5-Hesap_Makinesi.py mantığını modern arayüzle çalıştırır."""

    def __init__(self):
        self.pencere = tk.Tk()
        self.pencere.overrideredirect(True)
        self.pencere.configure(bg=ARKA_PLAN)
        self.pencere.geometry("340x520")

        self.sayi1 = None
        self.islem = None
        self.yeni_giris = True
        self.geri_al_yigini = []

        self._pencereyi_ortala()
        self._arayuz_olustur()
        self._surukleme_ayarla()
        self._ekran_guncelle()

    def _pencereyi_ortala(self):
        self.pencere.update_idletasks()
        genislik = self.pencere.winfo_width()
        yukseklik = self.pencere.winfo_height()
        x = (self.pencere.winfo_screenwidth() - genislik) // 2
        y = (self.pencere.winfo_screenheight() - yukseklik) // 2
        self.pencere.geometry(f"{genislik}x{yukseklik}+{x}+{y}")

    def _surukleme_ayarla(self):
        self._surukle_x = 0
        self._surukle_y = 0

        def basla(olay):
            self._surukle_x = olay.x
            self._surukle_y = olay.y

        def surukle(olay):
            x = self.pencere.winfo_x() + olay.x - self._surukle_x
            y = self.pencere.winfo_y() + olay.y - self._surukle_y
            self.pencere.geometry(f"+{x}+{y}")

        self.baslik_cubugu.bind("<Button-1>", basla)
        self.baslik_cubugu.bind("<B1-Motion>", surukle)
        self.mod_etiket.bind("<Button-1>", basla)
        self.mod_etiket.bind("<B1-Motion>", surukle)

    def _buton(self, ust, metin, komut, renk=BUTON_RENK, kalin=False, rowspan=1, colspan=1):
        font = self.buton_font_kalin if kalin else self.buton_font
        btn = tk.Button(
            ust,
            text=metin,
            font=font,
            fg=YAZI,
            bg=renk,
            activebackground=BUTON_BASILI if renk == BUTON_RENK else ESIT_BASILI,
            activeforeground=YAZI,
            relief="flat",
            bd=0,
            highlightthickness=0,
            cursor="hand2",
            command=komut,
        )
        return btn

    def _arayuz_olustur(self):
        self.buton_font = tkfont.Font(family="Segoe UI", size=14)
        self.buton_font_kalin = tkfont.Font(family="Segoe UI", size=14, weight="bold")
        self.ifade_font = tkfont.Font(family="Segoe UI", size=22)
        self.sonuc_font = tkfont.Font(family="Segoe UI", size=28, weight="bold")
        self.baslik_font = tkfont.Font(family="Segoe UI", size=11)
        self.kucuk_font = tkfont.Font(family="Segoe UI", size=10)

        # --- Başlık çubuğu ---
        self.baslik_cubugu = tk.Frame(self.pencere, bg=BASLIK_CUBUGU, height=36)
        self.baslik_cubugu.pack(fill="x")
        self.baslik_cubugu.pack_propagate(False)

        sol_baslik = tk.Frame(self.baslik_cubugu, bg=BASLIK_CUBUGU)
        sol_baslik.pack(side="left", padx=4)

        tk.Button(
            sol_baslik,
            text="↶",
            font=self.baslik_font,
            fg=YAZI,
            bg=BASLIK_CUBUGU,
            activebackground=AYIRICI,
            activeforeground=YAZI,
            relief="flat",
            bd=0,
            padx=8,
            pady=4,
            cursor="hand2",
            command=self.geri_al,
        ).pack(side="left")

        self.mod_etiket = tk.Label(
            self.baslik_cubugu,
            text="Basic  ▾",
            font=self.baslik_font,
            fg=YAZI,
            bg=BASLIK_CUBUGU,
            padx=8,
        )
        self.mod_etiket.place(relx=0.5, rely=0.5, anchor="center")

        sag_baslik = tk.Frame(self.baslik_cubugu, bg=BASLIK_CUBUGU)
        sag_baslik.pack(side="right", padx=2)

        for metin, komut in [
            ("☰", lambda: None),
            ("─", self.pencere.iconify),
            ("□", self._buyut_kucult),
            ("✕", self.pencere.destroy),
        ]:
            tk.Button(
                sag_baslik,
                text=metin,
                font=self.baslik_font,
                fg=YAZI,
                bg=BASLIK_CUBUGU,
                activebackground=AYIRICI,
                activeforeground=YAZI,
                relief="flat",
                bd=0,
                width=3,
                cursor="hand2",
                command=komut,
            ).pack(side="left")

        # --- Ekran alanı ---
        ekran_cerceve = tk.Frame(self.pencere, bg=EKRAN_RENK, height=120)
        ekran_cerceve.pack(fill="x")
        ekran_cerceve.pack_propagate(False)

        alt_ekran = tk.Frame(ekran_cerceve, bg=EKRAN_RENK)
        alt_ekran.pack(side="bottom", fill="x", padx=16, pady=(0, 14))

        self.ifade_etiket = tk.Label(
            alt_ekran,
            text="0",
            font=self.ifade_font,
            fg=YAZI_SOLUK,
            bg=EKRAN_RENK,
            anchor="w",
        )
        self.ifade_etiket.pack(side="left", fill="x", expand=True)

        sonuc_cerceve = tk.Frame(alt_ekran, bg=EKRAN_RENK)
        sonuc_cerceve.pack(side="right")

        tk.Label(
            sonuc_cerceve,
            text="=",
            font=self.ifade_font,
            fg=YAZI_SOLUK,
            bg=EKRAN_RENK,
        ).pack(side="left", padx=(8, 6))

        self.sonuc_etiket = tk.Label(
            sonuc_cerceve,
            text="0",
            font=self.sonuc_font,
            fg=YAZI,
            bg=EKRAN_RENK,
        )
        self.sonuc_etiket.pack(side="right")

        tk.Frame(self.pencere, bg=AYIRICI, height=1).pack(fill="x")

        # --- Tuş takımı ---
        tus_cerceve = tk.Frame(self.pencere, bg=ARKA_PLAN, padx=6, pady=6)
        tus_cerceve.pack(fill="both", expand=True)

        for i in range(5):
            tus_cerceve.grid_columnconfigure(i, weight=1, uniform="tus")
            tus_cerceve.grid_rowconfigure(i, weight=1, uniform="tus")

        tuslar = [
            ("C", 0, 0, self.temizle, True),
            ("(", 0, 1, lambda: None),
            (")", 0, 2, lambda: None),
            ("mod", 0, 3, lambda: self.islem_sec("%")),
            ("π", 0, 4, self.pi_ekle),
            ("7", 1, 0, lambda: self.rakam_ekle("7")),
            ("8", 1, 1, lambda: self.rakam_ekle("8")),
            ("9", 1, 2, lambda: self.rakam_ekle("9")),
            ("÷", 1, 3, lambda: self.islem_sec("/")),
            ("√", 1, 4, self.karekok),
            ("4", 2, 0, lambda: self.rakam_ekle("4")),
            ("5", 2, 1, lambda: self.rakam_ekle("5")),
            ("6", 2, 2, lambda: self.rakam_ekle("6")),
            ("×", 2, 3, lambda: self.islem_sec("*")),
            ("x²", 2, 4, self.kare_al),
            ("1", 3, 0, lambda: self.rakam_ekle("1")),
            ("2", 3, 1, lambda: self.rakam_ekle("2")),
            ("3", 3, 2, lambda: self.rakam_ekle("3")),
            ("−", 3, 3, lambda: self.islem_sec("-")),
            ("0", 4, 0, lambda: self.rakam_ekle("0")),
            (",", 4, 1, lambda: self.rakam_ekle(",")),
            ("%", 4, 2, self.yuzde),
            ("+", 4, 3, lambda: self.islem_sec("+")),
        ]

        for metin, satir, sutun, komut, *ekstra in tuslar:
            kalin = ekstra[0] if ekstra else False
            btn = self._buton(tus_cerceve, metin, komut, kalin=kalin)
            btn.grid(row=satir, column=sutun, padx=3, pady=3, sticky="nsew")

        esit_btn = self._buton(tus_cerceve, "=", self.hesapla, renk=ESIT_RENK)
        esit_btn.grid(row=3, column=4, rowspan=2, padx=3, pady=3, sticky="nsew")

        self.pencere.bind("<Key>", self.klavye_tus)
        self._buyuk_mu = False

    def _buyut_kucult(self):
        if self._buyuk_mu:
            self.pencere.geometry("340x520")
            self._buyuk_mu = False
        else:
            self.pencere.geometry("420x640")
            self._buyuk_mu = True
        self._pencereyi_ortala()

    def _durum_kaydet(self):
        self.geri_al_yigini.append(
            (self.sayi1, self.islem, self.yeni_giris, self.girdi_metni())
        )

    def geri_al(self):
        if not self.geri_al_yigini:
            return
        self.sayi1, self.islem, self.yeni_giris, girdi = self.geri_al_yigini.pop()
        self._girdi_yaz(girdi)
        self._ekran_guncelle()

    def girdi_metni(self):
        return self._girdi_deger().replace(".", ",")

    def _girdi_yaz(self, metin):
        self._aktif_girdi = metin.replace(",", ".")

    def _girdi_deger(self):
        if not hasattr(self, "_aktif_girdi"):
            self._aktif_girdi = "0"
        return self._aktif_girdi

    def _mevcut_sayi(self):
        metin = self._girdi_deger().strip()
        if metin in ("", "-", ".", "-."):
            return None
        try:
            return float(metin)
        except ValueError:
            return None

    def _sayi_goster(self, sayi):
        if sayi is None:
            return "0"
        if isinstance(sayi, float) and sayi.is_integer():
            return str(int(sayi)).replace(".", ",")
        metin = f"{sayi:.10g}".replace(".", ",")
        return metin

    def _islem_goster(self, islem):
        return {"+": "+", "-": "−", "*": "×", "/": "÷", "%": "mod"}.get(islem, islem)

    def _onizleme_sonuc(self):
        if self.sayi1 is None or not self.islem:
            return self._mevcut_sayi()

        sayi2 = self._mevcut_sayi()
        if sayi2 is None and self.yeni_giris:
            return self.sayi1
        if sayi2 is None:
            return None

        try:
            return self._islem_yap(self.sayi1, sayi2, self.islem)
        except (ZeroDivisionError, ValueError):
            return None

    def _islem_yap(self, sayi1, sayi2, islem):
        if islem == "+":
            return sayi1 + sayi2
        if islem == "-":
            return sayi1 - sayi2
        if islem == "*":
            return sayi1 * sayi2
        if islem == "/":
            if sayi2 == 0:
                raise ZeroDivisionError
            return sayi1 / sayi2
        if islem == "%":
            if sayi2 == 0:
                raise ZeroDivisionError
            return sayi1 % sayi2
        raise ValueError("Hatalı işlem")

    def _ekran_guncelle(self):
        girdi = self.girdi_metni()

        if self.sayi1 is not None and self.islem:
            if self.yeni_giris:
                ifade = f"{self._sayi_goster(self.sayi1)} {self._islem_goster(self.islem)}"
            else:
                ifade = (
                    f"{self._sayi_goster(self.sayi1)} {self._islem_goster(self.islem)} "
                    f"{girdi}"
                )
        else:
            ifade = girdi

        onizleme = self._onizleme_sonuc()
        self.ifade_etiket.config(text=ifade)
        self.sonuc_etiket.config(
            text=self._sayi_goster(onizleme) if onizleme is not None else girdi
        )

    def temizle(self):
        self._durum_kaydet()
        self.sayi1 = None
        self.islem = None
        self.yeni_giris = True
        self._aktif_girdi = "0"
        self._ekran_guncelle()

    def rakam_ekle(self, rakam):
        self._durum_kaydet()
        rakam = "," if rakam == "," else rakam
        mevcut = self._girdi_deger()

        if self.yeni_giris:
            if rakam == ",":
                self._aktif_girdi = "0."
            else:
                self._aktif_girdi = rakam
            self.yeni_giris = False
        else:
            if rakam == "," and "." in mevcut:
                return
            if mevcut == "0" and rakam != ",":
                self._aktif_girdi = rakam
            else:
                self._aktif_girdi = mevcut + ("." if rakam == "," else rakam)

        self._ekran_guncelle()

    def islem_sec(self, islem):
        deger = self._mevcut_sayi()
        if deger is None:
            return

        self._durum_kaydet()

        if self.sayi1 is not None and self.islem and not self.yeni_giris:
            try:
                sonuc = self._islem_yap(self.sayi1, deger, self.islem)
                self.sayi1 = sonuc
                self._aktif_girdi = str(sonuc)
            except ZeroDivisionError:
                self.sayi1 = None
                self.islem = None
                self._aktif_girdi = "0"
                self._ekran_guncelle()
                return

        self.sayi1 = self._mevcut_sayi() if self.sayi1 is None else self.sayi1
        if self.sayi1 is None:
            return

        self.islem = islem
        self.yeni_giris = True
        self._ekran_guncelle()

    def hesapla(self):
        if self.sayi1 is None or not self.islem:
            return

        sayi2 = self._mevcut_sayi()
        if sayi2 is None:
            return

        self._durum_kaydet()

        try:
            sonuc = self._islem_yap(self.sayi1, sayi2, self.islem)
        except ZeroDivisionError:
            self._aktif_girdi = "0"
            self.sayi1 = None
            self.islem = None
            self.yeni_giris = True
            self._ekran_guncelle()
            return
        except ValueError:
            return

        self._aktif_girdi = f"{sonuc:.10g}"
        self.sayi1 = sonuc
        self.islem = None
        self.yeni_giris = True
        self._ekran_guncelle()

    def pi_ekle(self):
        self._durum_kaydet()
        self._aktif_girdi = f"{math.pi:.10g}"
        self.yeni_giris = False
        self._ekran_guncelle()

    def karekok(self):
        deger = self._mevcut_sayi()
        if deger is None or deger < 0:
            return
        self._durum_kaydet()
        self._aktif_girdi = f"{math.sqrt(deger):.10g}"
        self.yeni_giris = False
        self._ekran_guncelle()

    def kare_al(self):
        deger = self._mevcut_sayi()
        if deger is None:
            return
        self._durum_kaydet()
        self._aktif_girdi = f"{deger ** 2:.10g}"
        self.yeni_giris = False
        self._ekran_guncelle()

    def yuzde(self):
        deger = self._mevcut_sayi()
        if deger is None:
            return
        self._durum_kaydet()
        self._aktif_girdi = f"{deger / 100:.10g}"
        self.yeni_giris = False
        self._ekran_guncelle()

    def klavye_tus(self, olay):
        tus = olay.char

        if tus in "0123456789":
            self.rakam_ekle(tus)
        elif tus in ".,":
            self.rakam_ekle(",")
        elif tus in "+-*/":
            self.islem_sec(tus)
        elif tus in ("\r", "\n"):
            self.hesapla()
        elif olay.keysym == "Escape":
            self.temizle()

    def calistir(self):
        self.pencere.mainloop()


if __name__ == "__main__":
    uygulama = GelismisHesapMakinesi()
    uygulama.calistir()
