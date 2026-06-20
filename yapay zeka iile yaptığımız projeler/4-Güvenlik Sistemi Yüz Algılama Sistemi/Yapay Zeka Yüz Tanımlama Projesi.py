import sys

try:
    import cv2
except ImportError:
    print("opencv-python yüklü değil. Önce şunu çalıştır:")
    print('  .venv/bin/pip install opencv-python')
    print('Sonra programı şöyle başlat:')
    print('  .venv/bin/python "4-Yapay Zeka Yüz Tanımlaam Projesi.py"')
    sys.exit(1)

try:
    import pygame
except ImportError:
    print("pygame yüklü değil. Önce şunu çalıştır:")
    print('  .venv/bin/pip install pygame')
    sys.exit(1)

# --- Ayarlar ---
EKRAN_GENISLIK = 960
EKRAN_YUKSEKLIK = 600
KAMERA_SURESI = 15
GIRIS_ICIN_KARE = 10
FPS = 30

BEYAZ = (255, 255, 255)
SIYAH = (20, 20, 20)
YESIL = (68, 255, 136)
KIRMIZI = (255, 80, 80)
MAVI = (26, 26, 140)


class YuzTanimaEkrani:
    """Kameradan gelen görüntüyü ekranda gösteren yüz tanıma arayüzü."""

    def __init__(self):
        pygame.init()
        self.ekran = pygame.display.set_mode((EKRAN_GENISLIK, EKRAN_YUKSEKLIK))
        pygame.display.set_caption("Yapay Zeka Yüz Tanıma - Giriş Sistemi")
        self.saat = pygame.time.Clock()
        self.font_baslik = pygame.font.SysFont("dejavusans", 28, bold=True)
        self.font_normal = pygame.font.SysFont("dejavusans", 22)
        self.font_kucuk = pygame.font.SysFont("dejavusans", 18)

        yuz_dosyasi = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        self.yuz_algilayici = cv2.CascadeClassifier(yuz_dosyasi)

        self.kamera = cv2.VideoCapture(0)
        self.kamera_ok = self.kamera.isOpened() and not self.yuz_algilayici.empty()

    def _kareyi_pygame_yuzeyine_cevir(self, kare):
        """OpenCV görüntüsünü pygame ekranına yansıtmak için dönüştürür."""
        kare = cv2.cvtColor(kare, cv2.COLOR_BGR2RGB)
        kare = pygame.surfarray.make_surface(kare.swapaxes(0, 1))
        return pygame.transform.scale(kare, (EKRAN_GENISLIK, EKRAN_YUKSEKLIK - 80))

    def _metin_yaz(self, yazi, font, renk, x, y):
        yuzey = font.render(yazi, True, renk)
        self.ekran.blit(yuzey, (x, y))

    def _kutuya_metin(self, yazi, font, renk, arka_plan, x, y, padding=10):
        yuzey = font.render(yazi, True, renk)
        kutu = yuzey.get_rect(topleft=(x, y))
        kutu.inflate_ip(padding * 2, padding * 2)
        pygame.draw.rect(self.ekran, arka_plan, kutu, border_radius=8)
        self.ekran.blit(yuzey, (x + padding, y + padding))

    def _basari_ekrani(self):
        self.ekran.fill(MAVI)
        self._metin_yaz("Giriş Başarılı!", self.font_baslik, YESIL, 330, 250)
        self._metin_yaz("Yüz tanımlandı.", self.font_normal, BEYAZ, 380, 300)
        pygame.display.flip()
        pygame.time.wait(2000)

    def calistir(self):
        if not self.kamera_ok:
            print("Kamera veya yüz tanıma modeli açılamadı.")
            pygame.quit()
            return False

        print("Kamera açıldı. Ekranda canlı görüntü gösteriliyor.")
        print("Alternatif giriş için ekrandayken 'H' tuşuna basın.")

        yuz_sayaci = 0
        baslangic = pygame.time.get_ticks()
        calisiyor = True
        sonuc = False
        kamera_alani = pygame.Rect(0, 80, EKRAN_GENISLIK, EKRAN_YUKSEKLIK - 80)

        while calisiyor:
            for olay in pygame.event.get():
                if olay.type == pygame.QUIT:
                    calisiyor = False
                elif olay.type == pygame.KEYDOWN:
                    if olay.key == pygame.K_h:
                        calisiyor = False
                    elif olay.key == pygame.K_ESCAPE:
                        calisiyor = False

            ok, kare = self.kamera.read()
            if not ok:
                print("Kameradan görüntü alınamadı.")
                break

            # Ayna görüntüsü (kendinizi doğal şekilde görürsünüz)
            kare = cv2.flip(kare, 1)

            gri = cv2.cvtColor(kare, cv2.COLOR_BGR2GRAY)
            yuzler = self.yuz_algilayici.detectMultiScale(
                gri,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(80, 80),
            )

            gecen_sure = (pygame.time.get_ticks() - baslangic) / 1000
            kalan_sure = max(int(KAMERA_SURESI - gecen_sure), 0)
            durum_mesaji = "Yüz aranıyor..."
            durum_renk = KIRMIZI

            if len(yuzler) > 0:
                yuz_sayaci += 1
                durum_mesaji = "Yüz algılandı!"
                durum_renk = YESIL
                for (x, y, w, h) in yuzler:
                    cv2.rectangle(kare, (x, y), (x + w, y + h), (68, 255, 136), 3)

                if yuz_sayaci >= GIRIS_ICIN_KARE:
                    sonuc = True
                    calisiyor = False
                    break
            else:
                yuz_sayaci = 0

            # Üst bilgi çubuğu
            self.ekran.fill(SIYAH)
            self._metin_yaz("Yüz Tanıma Giriş Sistemi", self.font_baslik, BEYAZ, 20, 20)
            self._kutuya_metin(durum_mesaji, self.font_normal, durum_renk, (40, 40, 40), 20, 48)

            # Kamera görüntüsünü ekrana yansıt
            kamera_yuzey = self._kareyi_pygame_yuzeyine_cevir(kare)
            self.ekran.blit(kamera_yuzey, kamera_alani.topleft)
            pygame.draw.rect(self.ekran, BEYAZ, kamera_alani, 2)

            # Alt bilgi
            bilgi = f"Kalan süre: {kalan_sure} sn  |  H: Alternatif giriş  |  ESC: Çık"
            self._metin_yaz(bilgi, self.font_kucuk, BEYAZ, 20, EKRAN_YUKSEKLIK - 35)

            pygame.display.flip()
            self.saat.tick(FPS)

            if gecen_sure >= KAMERA_SURESI:
                break

        self.kamera.release()

        if sonuc:
            self._basari_ekrani()

        pygame.quit()
        return sonuc


def alternatif_giris():
    """Yüz tanınamazsa kullanıcı adı ve şifre ile giriş yapılır."""
    print("Yüzünüz Tanımlamadığı İçin Alternatif Oturum Açma İşlemi Uygulanıyor.")
    kullanici_adi = input("Lütfen Kullanıcı Adınızı Giriniz: ")
    sifre = input("Şifrenizi Giriniz: ")

    if kullanici_adi == "admin" and sifre == "123":
        print("Giriş Başarılı")
    else:
        print("Giriş Başarılı Değil")


def main():
    print("=== Yapay Zeka Yüz Tanıma Giriş Sistemi ===")

    uygulama = YuzTanimaEkrani()
    yuz_tanimlandi = uygulama.calistir()

    if yuz_tanimlandi:
        print("Giriş Başarılı")
    else:
        alternatif_giris()


if __name__ == "__main__":
    main()
