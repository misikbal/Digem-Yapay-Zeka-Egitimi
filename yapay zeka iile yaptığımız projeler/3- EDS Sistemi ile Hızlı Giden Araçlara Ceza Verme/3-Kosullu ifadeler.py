import sys

try:
    import pygame
except ImportError:
    print("pygame yüklü değil. Önce şunu çalıştır:")
    print('  /usr/bin/python3 -m venv .venv && .venv/bin/pip install pygame')
    print('Sonra oyunu şöyle başlat:')
    print('  .venv/bin/python "3-Kosullu ifadeler.py"')
    sys.exit(1)

# --- Oyun ayarları ---
GENISLIK = 800
YUKSEKLIK = 600
FPS = 60
HIZ_SINIRI = 50
MAKS_HIZ = 120
HIZLANMA = 0.35
YAVASLAMA = 0.2
YOL_HIZ_CARPANI = 0.08

BEYAZ = (255, 255, 255)
SIYAH = (0, 0, 0)
KIRMIZI = (230, 57, 70)
YESIL = (45, 90, 39)
YOL_RENGI = (51, 51, 51)
SARI = (255, 204, 0)
MAVI = (26, 26, 140)
ACIK_YESIL = (68, 255, 136)
ACIK_KIRMIZI = (255, 68, 68)


class AracOyunu:
    def __init__(self):
        pygame.init()
        self.ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
        pygame.display.set_caption("Koşullu İfadeler - EDS Oyunu")
        self.saat = pygame.time.Clock()
        self.font_kucuk = pygame.font.SysFont("dejavusans", 18)
        self.font_orta = pygame.font.SysFont("dejavusans", 24)
        self.font_buyuk = pygame.font.SysFont("dejavusans", 36, bold=True)

        self.w_basili = False
        self.arac_hizi = 0.0
        self.yol_kayma = 0.0
        self.toplam_mesafe = 0.0
        self.ceza_sayisi = 0
        self.ceza_mesaji = ""
        self.ceza_alt_mesaj = ""
        self.ceza_suresi = 0
        self.gecilen_eds = set()
        self.eds_noktalari = [800, 1600, 2400, 3200, 4000]
        self.calisyor = True
        self.arac_sprite = self._arac_sprite_olustur()

    def _arac_sprite_olustur(self):
        """Yukari bakan (ileri giden) araba goruntusu."""
        sprite = pygame.Surface((52, 76), pygame.SRCALPHA)

        # Golge
        pygame.draw.ellipse(sprite, (0, 0, 0, 60), (6, 62, 40, 12))

        # Tekerlekler
        tekerlek_renk = (25, 25, 25)
        pygame.draw.rect(sprite, tekerlek_renk, (0, 18, 10, 20), border_radius=3)
        pygame.draw.rect(sprite, tekerlek_renk, (42, 18, 10, 20), border_radius=3)
        pygame.draw.rect(sprite, tekerlek_renk, (0, 46, 10, 20), border_radius=3)
        pygame.draw.rect(sprite, tekerlek_renk, (42, 46, 10, 20), border_radius=3)

        # Govde
        pygame.draw.rect(sprite, (220, 50, 50), (8, 14, 36, 48), border_radius=8)
        pygame.draw.rect(sprite, (180, 35, 35), (8, 48, 36, 14), border_radius=6)

        # Cam / tavan
        pygame.draw.rect(sprite, (120, 200, 255), (12, 24, 28, 22), border_radius=5)
        pygame.draw.rect(sprite, (90, 170, 230), (12, 10, 28, 14), border_radius=4)

        # Farlar
        pygame.draw.circle(sprite, (255, 255, 180), (14, 8), 4)
        pygame.draw.circle(sprite, (255, 255, 180), (38, 8), 4)

        # Stop lambalari
        pygame.draw.circle(sprite, (255, 40, 40), (14, 58), 3)
        pygame.draw.circle(sprite, (255, 40, 40), (38, 58), 3)

        return sprite

    def _eds_kontrol(self):
        for eds_mesafe in self.eds_noktalari:
            if eds_mesafe in self.gecilen_eds:
                continue
            if self.toplam_mesafe >= eds_mesafe:
                self.gecilen_eds.add(eds_mesafe)
                if self.arac_hizi > HIZ_SINIRI:
                    self.ceza_sayisi += 1
                    self.ceza_mesaji = (
                        "Geçmiş Olsun Hız Sınırını Aştığınız İçin Ceza Yediniz."
                    )
                    self.ceza_alt_mesaj = "Afiyet Olsun :)"
                    self.ceza_suresi = 180
                else:
                    self.ceza_mesaji = "Ceza Yemediniz İyi Yolculuklar"
                    self.ceza_alt_mesaj = ""
                    self.ceza_suresi = 90

    def _guncelle(self):
        if self.w_basili:
            self.arac_hizi = min(self.arac_hizi + HIZLANMA, MAKS_HIZ)
        else:
            self.arac_hizi = max(self.arac_hizi - YAVASLAMA, 0)

        hareket = self.arac_hizi * YOL_HIZ_CARPANI
        self.yol_kayma = (self.yol_kayma + hareket) % 80
        self.toplam_mesafe += hareket

        if self.ceza_suresi > 0:
            self.ceza_suresi -= 1

        self._eds_kontrol()

    def _yol_ciz(self):
        yol_sol = GENISLIK // 2 - 120
        yol_sag = GENISLIK // 2 + 120
        pygame.draw.rect(self.ekran, YOL_RENGI, (yol_sol, 0, 240, YUKSEKLIK))

        for i in range(-2, 14):
            y = int((i * 80 + self.yol_kayma) % (YUKSEKLIK + 80)) - 80
            pygame.draw.rect(self.ekran, SARI, (GENISLIK // 2 - 4, y, 8, 40))

        pygame.draw.line(self.ekran, BEYAZ, (yol_sol, 0), (yol_sol, YUKSEKLIK), 3)
        pygame.draw.line(self.ekran, BEYAZ, (yol_sag, 0), (yol_sag, YUKSEKLIK), 3)

    def _eds_tabelalari_ciz(self):
        yol_sol = GENISLIK // 2 - 120
        yol_sag = GENISLIK // 2 + 120

        for eds_mesafe in self.eds_noktalari:
            mesafe_kaldi = eds_mesafe - self.toplam_mesafe
            if mesafe_kaldi <= 0 or mesafe_kaldi > 650:
                continue

            # EDS ileride (ustte), araca yaklastikca asagi iner
            ekran_y = int(120 + (650 - mesafe_kaldi) * 0.65)

            pygame.draw.rect(self.ekran, MAVI, (yol_sol - 70, ekran_y - 25, 60, 50))
            pygame.draw.rect(self.ekran, BEYAZ, (yol_sol - 70, ekran_y - 25, 60, 50), 2)
            pygame.draw.rect(self.ekran, MAVI, (yol_sag + 10, ekran_y - 25, 60, 50))
            pygame.draw.rect(self.ekran, BEYAZ, (yol_sag + 10, ekran_y - 25, 60, 50), 2)

            for x_ofset in (yol_sol - 55, yol_sag + 25):
                eds_yazi = self.font_kucuk.render("EDS", True, BEYAZ)
                sinir_yazi = self.font_kucuk.render(str(HIZ_SINIRI), True, ACIK_KIRMIZI)
                self.ekran.blit(eds_yazi, (x_ofset, ekran_y - 18))
                self.ekran.blit(sinir_yazi, (x_ofset + 7, ekran_y + 2))

            # Yol ustu kirmizi EDS cizgisi
            pygame.draw.line(
                self.ekran, ACIK_KIRMIZI,
                (yol_sol, ekran_y + 30), (yol_sag, ekran_y + 30), 4
            )

    def _arac_ciz(self):
        cx = GENISLIK // 2
        cy = YUKSEKLIK - 110
        sprite_rect = self.arac_sprite.get_rect(center=(cx, cy))
        self.ekran.blit(self.arac_sprite, sprite_rect)

    def _polis_cezasi_ciz(self):
        if self.ceza_suresi <= 0 or not self.ceza_mesaji:
            return

        pygame.draw.rect(self.ekran, (26, 26, 46), (120, 180, GENISLIK - 240, 140))
        pygame.draw.rect(self.ekran, KIRMIZI, (120, 180, GENISLIK - 240, 140), 4)

        baslik = self.font_orta.render("POLIS CEZASI", True, ACIK_KIRMIZI)
        mesaj = self.font_kucuk.render(self.ceza_mesaji, True, BEYAZ)
        self.ekran.blit(baslik, baslik.get_rect(center=(GENISLIK // 2, 210)))
        self.ekran.blit(mesaj, mesaj.get_rect(center=(GENISLIK // 2, 250)))

        if self.ceza_alt_mesaj:
            alt = self.font_kucuk.render(self.ceza_alt_mesaj, True, BEYAZ)
            self.ekran.blit(alt, alt.get_rect(center=(GENISLIK // 2, 280)))

    def _hud_ciz(self):
        hiz_renk = ACIK_KIRMIZI if self.arac_hizi > HIZ_SINIRI else ACIK_YESIL

        pygame.draw.rect(self.ekran, SIYAH, (10, 10, 210, 90))
        pygame.draw.rect(self.ekran, BEYAZ, (10, 10, 210, 90), 2)
        self.ekran.blit(self.font_kucuk.render("HIZ (km/s)", True, (170, 170, 170)), (20, 18))
        self.ekran.blit(self.font_buyuk.render(str(int(self.arac_hizi)), True, hiz_renk), (20, 38))
        self.ekran.blit(
            self.font_kucuk.render(f"EDS Siniri: {HIZ_SINIRI} km/s", True, SARI), (20, 78)
        )

        pygame.draw.rect(self.ekran, SIYAH, (GENISLIK - 220, 10, 210, 90))
        pygame.draw.rect(self.ekran, BEYAZ, (GENISLIK - 220, 10, 210, 90), 2)
        self.ekran.blit(self.font_kucuk.render("CEZA SAYISI", True, (170, 170, 170)), (GENISLIK - 210, 18))
        self.ekran.blit(self.font_buyuk.render(str(self.ceza_sayisi), True, ACIK_KIRMIZI), (GENISLIK - 210, 38))

        bilgi = self.font_kucuk.render(
            "W basili tut = hizlan | EDS'de 50 km/s uzeri = ceza | ESC = cikis", True, BEYAZ
        )
        self.ekran.blit(bilgi, bilgi.get_rect(center=(GENISLIK // 2, YUKSEKLIK - 20)))

    def _ciz(self):
        self.ekran.fill(YESIL)
        self._yol_ciz()
        self._eds_tabelalari_ciz()
        self._arac_ciz()
        self._hud_ciz()
        self._polis_cezasi_ciz()
        pygame.display.flip()

    def _olaylari_isle(self):
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                self.calisyor = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_w:
                    self.w_basili = True
                elif olay.key == pygame.K_ESCAPE:
                    self.calisyor = False
            elif olay.type == pygame.KEYUP:
                if olay.key == pygame.K_w:
                    self.w_basili = False

    def baslat(self):
        while self.calisyor:
            self._olaylari_isle()
            self._guncelle()
            self._ciz()
            self.saat.tick(FPS)
        pygame.quit()


if __name__ == "__main__":
    oyun = AracOyunu()
    oyun.baslat()
