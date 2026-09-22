import os
import base64
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

telegram_token="xxxx"
openai_api_key="xxxx"


client=OpenAI(api_key=openai_api_key)


def photo_to_base64(file_path):
    with open(file_path,"rb") as image_files:
        return base64.b64encode(image_files.read()).decode("utf-8")


async def baslangic_mesaji(update:Update, context:ContextTypes.DEFAULT_TYPE):
    mesaj = (
        "🍳 Merhaba! Ben DİGEM Görsel Mutfak Şefi.\n\n"
        "Ne pişireceğini bilmiyor musun? Bana buzdolabının içini, "
        "mutfak tezgahını veya elindeki malzemelerin fotoğrafını gönder, "
        "sana 15 dakikada hazırlayabileceğin harika tarifler çıkarayım!"
    )
    await update.message.reply_text(mesaj)


async def fotograf_alindi(update:Update, context:ContextTypes.DEFAULT_TYPE):
    mesaj_kutusu=await update.message.reply_text("👀 Hımm fotoğrafa bakıyorum...")
    try:
        fotograf_dosyasi=await update.message.photo[-1].get_file()
        gecici_dosya_adi="gecici_malzemler.jpg"
        await fotograf_dosyasi.download_to_drive(gecici_dosya_adi)

        base64_gorsel=photo_to_base64(gecici_dosya_adi)

        response=client.chat.completions.create(
            model="gpt-4o",
            messages=[

                {
                    "role":"system",
                    "content":(
                        "Sen usta, enerjik ve pratik bir mutfak şefisin. "
                        "Kullanıcının gönderdiği fotoğraftaki yiyecek ve malzemeleri tespit et. "
                        "SADECE o fotoğrafta bulunan malzemeleri (ve evde bulunabilecek yağ, tuz, su gibi temel şeyleri) "
                        "kullanarak yapılabilecek en iyi 2 pratik tarifi adım adım yaz. "
                        "Eğer fotoğrafta yiyecek yoksa esprili bir şekilde 'Ben şefim, bu yenmez!' diyerek reddet."
                    )
                },
                {
                    "role":"user",
                    "content":[
                        {"type": "text", "text": "Bu fotoğrafta hangi malzemeler var ve bunlarla ne yemek yapabilirim?"},
                        
                        {
                            "type":"image_url",
                            "image_url":{"url":f"data:image/jpeg;base64,{base64_gorsel}"}
                        
                        }
                        
                    ]
                }
            ],
            max_tokens=800,
            temperature=0.6
        )

        ai_cevap=response.choices[0].message.content
        await mesaj_kutusu.edit_text(f"Şefin Tavsiyesi:\n\n{ai_cevap}")

        if os.path.exists(gecici_dosya_adi):
            os.remove(gecici_dosya_adi)
    except Exception as e:
        await mesaj_kutusu.edit_text("Eyvah, mutfakta bir kaza oldu tekrar deneyiniz.")

async def metin_mesaji_alindi(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("😅 Ben sadece fotoğraflardan anlıyorum. Lütfen bana malzemelerin fotoğrafını gönder!")


if __name__=="__main__":
    print("==================================================")
    print("🚀 DİGEM ŞEF BOTU BAŞLATILIYOR (Lütfen bekleyin...)")
    print("📱 Artık Telegram üzerinden bota mesaj ve fotoğraf atabilirsiniz.")
    print("🚨 Kodu durdurmak için terminalde CTRL+C tuşlarına basabilirsiniz.")
    print("==================================================")


    uygulama=Application.builder().token(telegram_token).build()
    uygulama.add_handler(CommandHandler("start",baslangic_mesaji))
    uygulama.add_handler(MessageHandler(filters.PHOTO, fotograf_alindi))
    uygulama.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, metin_mesaji_alindi))

    uygulama.run_polling()


    

        


