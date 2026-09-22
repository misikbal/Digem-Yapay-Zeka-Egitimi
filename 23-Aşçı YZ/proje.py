import os
import base64
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

# ==========================================
# 1. API ANAHTARLARI VE AYARLAR
# ==========================================
# DİKKAT: Aşağıdaki iki tırnak içini kendi bilgilerinizle doldurun!
TELEGRAM_TOKEN = "xxx"
OPENAI_API_KEY = "xxx"

# OpenAI istemcisini (client) başlatıyoruz
client = OpenAI(api_key=OPENAI_API_KEY)

# ==========================================
# 2. GÖRSEL İŞLEME (YARDIMCI FONKSİYON)
# ==========================================
def fotografi_base64_yap(dosya_yolu):
    """
    Telegram'dan inen fotoğrafı, yapay zekanın anlayabilmesi için 
    Base64 (uzun bir metin şifrelemesi) formatına dönüştürür.
    """
    with open(dosya_yolu, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# ==========================================
# 3. TELEGRAM BOT KOMUTLARI VE TEPKİLERİ
# ==========================================
async def baslangic_mesaji(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kullanıcı bota ilk kez /start yazdığında çalışır."""
    mesaj = (
        "🍳 Merhaba! Ben DİGEM Görsel Mutfak Şefi.\n\n"
        "Ne pişireceğini bilmiyor musun? Bana buzdolabının içini, "
        "mutfak tezgahını veya elindeki malzemelerin fotoğrafını gönder, "
        "sana 15 dakikada hazırlayabileceğin harika tarifler çıkarayım!"
    )
    await update.message.reply_text(mesaj)


async def fotograf_alindi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kullanıcı bota herhangi bir fotoğraf gönderdiğinde tetiklenir."""
    
    # Adım 1: Kullanıcıyı bekletme mesajı at (AI süreci birkaç saniye sürebilir)
    mesaj_kutusu = await update.message.reply_text("👀 Hımm, fotoğrafa bakıyorum... Malzemeleri inceliyorum, bekle lütfen ⏳")
    
    try:
        # Adım 2: Telegram'daki fotoğrafı bilgisayara indirme ([-1] en yüksek kalite demektir)
        fotograf_dosyasi = await update.message.photo[-1].get_file()
        gecici_dosya_adi = "gecici_malzemeler.jpg"
        
        await fotograf_dosyasi.download_to_drive(gecici_dosya_adi)
        
        # Adım 3: İndirilen fotoğrafı Base64 şifreli metne çevirme
        base64_gorsel = fotografi_base64_yap(gecici_dosya_adi)
        
        # Adım 4: Yapay Zekaya (GPT-4o Vision) istek gönderme
        response = client.chat.completions.create(
            model="gpt-4o",  # Görsel anlayabilen ana model
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Sen usta, enerjik ve pratik bir mutfak şefisin. "
                        "Kullanıcının gönderdiği fotoğraftaki yiyecek ve malzemeleri tespit et. "
                        "SADECE o fotoğrafta bulunan malzemeleri (ve evde bulunabilecek yağ, tuz, su gibi temel şeyleri) "
                        "kullanarak yapılabilecek en iyi 2 pratik tarifi adım adım yaz. "
                        "Eğer fotoğrafta yiyecek yoksa esprili bir şekilde 'Ben şefim, bu yenmez!' diyerek reddet."
                    )
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Bu fotoğrafta hangi malzemeler var ve bunlarla ne yemek yapabilirim?"},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_gorsel}"}
                        }
                    ]
                }
            ],
            max_tokens=800, # Tarif uzun olabileceği için kelime limitini yüksek tuttuk
            temperature=0.6 # Biraz yaratıcılık katması için ayar
        )
        
        # Adım 5: Yapay Zekadan dönen metni yakalama
        ai_cevabi = response.choices[0].message.content
        
        # Adım 6: Daha önce attığımız "bekle lütfen" mesajını düzenleyip sonucu basma
        await mesaj_kutusu.edit_text(f"👨‍🍳 ŞEFİN TAVSİYESİ:\n\n{ai_cevabi}")
        
        # Adım 7: İşlem bitince bilgisayarda yer kaplamaması için inen resmi silme
        if os.path.exists(gecici_dosya_adi):
            os.remove(gecici_dosya_adi)

    except Exception as e:
        # Kod çökerse veya internet koparsa Telegram'da hata mesajı ver
        await mesaj_kutusu.edit_text(f"❌ Eyvah, mutfakta bir kaza oldu! Hata detayı: {e}")


async def metin_mesaji_alindi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kullanıcı fotoğraf yerine yazı yazarsa uyar."""
    await update.message.reply_text("😅 Ben sadece fotoğraflardan anlıyorum. Lütfen bana malzemelerin fotoğrafını gönder!")


# ==========================================
# 4. BOTU ÇALIŞTIRMA (ANA MOTOR - MAIN)
# ==========================================
if __name__ == '__main__':
    print("==================================================")
    print("🚀 DİGEM ŞEF BOTU BAŞLATILIYOR (Lütfen bekleyin...)")
    print("📱 Artık Telegram üzerinden bota mesaj ve fotoğraf atabilirsiniz.")
    print("🚨 Kodu durdurmak için terminalde CTRL+C tuşlarına basabilirsiniz.")
    print("==================================================")
    
    # Uygulamayı Token ile inşa etme
    uygulama = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Olay dinleyicilerini (Handlers) ekleme
    uygulama.add_handler(CommandHandler("start", baslangic_mesaji)) # /start komutu gelirse
    uygulama.add_handler(MessageHandler(filters.PHOTO, fotograf_alindi)) # Fotoğraf gelirse
    uygulama.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, metin_mesaji_alindi)) # Yazı gelirse
    
    # Botu uyandırma ve sürekli mesaj bekleme döngüsüne (Polling) sokma
    uygulama.run_polling()