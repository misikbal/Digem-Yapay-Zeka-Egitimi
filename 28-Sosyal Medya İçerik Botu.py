import base64
import http.server
import json
import logging
import re
import secrets
import sys
import urllib.parse
import webbrowser
from datetime import date, timedelta
from functools import wraps
from pathlib import Path
 
import httpx
from openai import (
    APITimeoutError,
    AsyncOpenAI,
    AuthenticationError,
    BadRequestError,
    OpenAIError,
    PermissionDeniedError,
    RateLimitError,
)
from telegram import InlineKeyboardButton as Dugme
from telegram import InlineKeyboardMarkup as Klavye
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

TELEGRAM_BOT_TOKEN = "8961939471:xxxx"
OPENAI_API_ANAHTARI = "sk-proj-xxxxx"



IZINLI_KULLANICI_IDLERI = {967336300}


ISLETME_ADI = "Kıyı Kahve"
SEKTOR = "butik kahve dükkânı"
TON = "samimi ve sıcak" 


METIN_MODELI = "gpt-4o-mini"
GORSEL_MODELI = "gpt-image-2"
GORSEL_KALITESI = "low"
GORSEL_BOYUTU = "1536x1024"

openai_istemcisi = AsyncOpenAI(api_key=OPENAI_API_ANAHTARI, timeout=120.0)



OZEL_GUNLER = [
    (1, 1, "Yeni Yıl", "Yeni yıl dilekleri, yeni hedefler, müşterilere teşekkür."),
    (2, 14, "Sevgililer Günü", "Samimi ve hafif bir dil."),
    (3, 8, "Dünya Kadınlar Günü", "Saygılı bir kutlama; indirim dili kullanma."),
    (4, 23, "23 Nisan Çocuk Bayramı", "Çocuk bayramı kutlaması, umut vurgusu."),
    (5, 1, "Emek ve Dayanışma Günü", "Ekibe ve çalışanlara teşekkür."),
    (5, 19, "19 Mayıs Gençlik ve Spor Bayramı", "Saygılı ve sade; satış dili kullanma."),
    (8, 30, "30 Ağustos Zafer Bayramı", "Saygılı ve sade; satış dili kullanma."),
    (10, 1, "Dünya Kahve Günü", "Kahve kültürü, sohbet, müşteri anıları."),
    (10, 29, "29 Ekim Cumhuriyet Bayramı", "Saygılı ve sade; satış dili kullanma."),
    (11, 10, "10 Kasım Atatürk'ü Anma Günü", "Anma mesajı; kesinlikle satış dili kullanma."),
    (11, 24, "Öğretmenler Günü", "Öğretmenlere teşekkür."),
    (12, 31, "Yılbaşı Gecesi", "Yıl özeti, teşekkür ve iyi dilekler."),
]


def yaklasan_ozel_gunler(kac_gun_icinde: int=60) -> list[dict]:

    bugun=date.today()
    yaklasanlar=[]

    for ay, gun, isim, aciklama in OZEL_GUNLER:
        tarih=date(bugun.year, ay, gun)

        if tarih<bugun:
            tarih=date(bugun.year+1, ay, gun)

        if (tarih-bugun).days <= kac_gun_icinde:
            yaklasanlar.append({"tarih": tarih, "isim": isim, "aciklama": aciklama})
        yaklasanlar.sort(key=lambda x: x["tarih"])

        return yaklasanlar[:6]


SYSTEM_PROMPT="""

Sen Türkiye'deki küçük işletmeler için çalışan deneyimli bir LinkedIn içerik editörüsün.
Verilen işletme bilgisine ve isteğe göre TEK bir paylaşım hazırlarsın.
 
Kurallar:
- Metin Türkçe olsun ve istenen tona uysun.
- İlk satır dikkat çekici olsun. Kısa paragraflar kullan. 600-1200 karakter.
- En fazla 2-3 emoji kullan. Sonda kısa bir soru veya davet olsun.
- Bilmediğin bilgiyi uydurma: fiyat, adres, telefon, indirim oranı yazma.
- Özel gün ise verilen nota uy.
- etiketler: 3-5 adet, '#' işareti olmadan, boşluksuz.
- gorsel_promptu: İNGİLİZCE, tek paragraf; konu, ışık, kompozisyon ve stil belirt.
  Görselde yazı, harf, logo OLMASIN.
- alt_metin: Görseli anlatan, Türkçe tek cümle.
 
Yanıtı YALNIZCA şu JSON biçiminde ver:
{"gonderi_metni": "...", "etiketler": ["..."], "gorsel_promptu": "...", "alt_metin": "..."}
"""


async def gonderi_uret(istek: str, ozel_gun: dict | None = None) -> dict:

    satirlar = [
        f"İşletme adı: {ISLETME_ADI}",
        f"Sektör: {SEKTOR}",
        f"İstenen ton: {TON}",
    ]
    if ozel_gun:
        satirlar.append(f"Özel gün: {ozel_gun['ad']} (Not: {ozel_gun['not']})")
    satirlar.append(f"İstek: {istek}")


    try:
        yanit = await openai_istemcisi.chat.completions.create(
            model=METIN_MODELI,
            temperature=0.8,
            response_format={"type": "json_object"},   # modelden geçerli JSON ister
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": "\n".join(satirlar)},
            ],
        )




    except OpenAIError as hata:
        print("Herhangi bir hata oluştur", hata)


    try:
        veri = json.loads(yanit.choices[0].message.content)
        return {
            "metin": str(veri["gonderi_metni"]).strip(),
            "etiketler": [str(e) for e in veri.get("etiketler", [])][:5],
            "gorsel_istegi": str(veri["gorsel_promptu"]).strip(),
            "alt_metin": str(veri.get("alt_metin", "")).strip() or ISLETME_ADI,
        }
    except (json.JSONDecodeError, KeyError, TypeError) as hata:
        print("Bir hata oluştu: JSON yanıtını ayrıştırırken veya beklenen alanları alırken", hata)


    
 
async def gorsel_uret(gorsel_istegi: str, gorsel_yazisi: str = "") -> bytes:

    if gorsel_yazisi:
        kural = (
            f'\n\nRender exactly this text prominently and legibly in the image, '
            f'spelled exactly as written, with correct Turkish characters: "{gorsel_yazisi}". '
            "No other text, no logos, no watermarks."
        )
    else:
        kural = "\n\nNo text, no letters, no logos, no watermarks in the image."

    try:
        sonuc = await openai_istemcisi.images.generate(
            model=GORSEL_MODELI,
            prompt=gorsel_istegi + kural,
            size=GORSEL_BOYUTU,
            quality=GORSEL_KALITESI,
            n=1,
        )

    except OpenAIError as hata:
        print("Görsel üretiminde bir hata oluştu:", hata)
        return b""

    return base64.b64decode(sonuc.data[0].b64_json)



def yetkili_olmali(fonksiyon):
    """Yalnızca IZINLI_KULLANICI_IDLERI içindeki kullanıcılar botu kullanabilir."""
 
    @wraps(fonksiyon)
    async def sarmalayici(update: Update, context: ContextTypes.DEFAULT_TYPE):
        kullanici_id = update.effective_user.id
        if kullanici_id not in IZINLI_KULLANICI_IDLERI:
            await update.effective_chat.send_message(
                f"Bu bot özel kullanım içindir.\nTelegram ID'niz: {kullanici_id}"
            )
            return
        return await fonksiyon(update, context)
 
    return sarmalayici



def ana_menu() -> Klavye:
    return Klavye([[Dugme("📅 Özel gün içeriği", callback_data="gunler")]])
 
 
def taslak_klavyesi() -> Klavye:
    return Klavye(
        [
            [Dugme("🔄 Yeniden üret", callback_data="yenile"), Dugme("🖼 Görseli yenile", callback_data="gorsel")],
            [Dugme("✏️ Görsele yazı ekle", callback_data="yazi")],
            [Dugme("📤 Paylaş", callback_data="paylas")],
        ]
    )




def son_metin(taslak: dict) -> str:
    """Gönderi metni + hashtag'ler."""
    etiketler = " ".join("#" + e.replace(" ", "").lstrip("#") for e in taslak["etiketler"])
    return f"{taslak['metin']}\n\n{etiketler}".strip()
 
 
async def taslak_olustur(sohbet, context, istek: str, ozel_gun: dict | None = None) -> None:
    """Metin + görsel üretir, taslağı kullanıcıya gösterir."""
    durum = await sohbet.send_message("⏳ Metin yazılıyor...")

    taslak = await gonderi_uret(istek, ozel_gun)
    await durum.edit_text("🎨 Görsel üretiliyor (30-60 sn sürebilir)...")
    taslak["gorsel_yazisi"] = ""
    taslak["gorsel"] = await gorsel_uret(taslak["gorsel_istegi"])


    taslak["istek"] = istek
    taslak["ozel_gun"] = ozel_gun
    context.user_data["taslak"] = taslak      # butonlar için taslağı hatırla
    await durum.delete()
    await sohbet.send_photo(photo=taslak["gorsel"])
    await sohbet.send_message(f"📝 TASLAK\n\n{son_metin(taslak)}", reply_markup=taslak_klavyesi())


async def gorseli_yenile(sohbet, taslak: dict) -> None:
    """Taslağın görselini (varsa üzerine yazılacak metinle) yeniden üretir ve taslağı tekrar gösterir."""
    durum = await sohbet.send_message("🎨 Yeni görsel üretiliyor...")
    gorsel = await gorsel_uret(taslak["gorsel_istegi"], taslak.get("gorsel_yazisi", ""))
    await durum.delete()
    if gorsel:
        taslak["gorsel"] = gorsel
    else:
        await sohbet.send_message("⚠️ Görsel üretilemedi, önceki görsel korunuyor.")
    await sohbet.send_photo(photo=taslak["gorsel"])
    await sohbet.send_message(f"📝 TASLAK\n\n{son_metin(taslak)}", reply_markup=taslak_klavyesi())


@yetkili_olmali
async def baslat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start komutu."""
    await update.message.reply_text(
        f"Merhaba! {ISLETME_ADI} için içerik üretelim.\n\n"
        "✍️ Bir konu yazın (örn: yeni sezon kahvelerimizi tanıtan bir gönderi)\n"
        "📅 ya da özel gün seçin:",
        reply_markup=ana_menu(),
    )
 
 
@yetkili_olmali
async def metin_isle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kullanıcının yazdığı her mesaj bir içerik isteğidir (görsel yazısı beklenirken hariç)."""
    metin = update.message.text.strip()

    if context.user_data.pop("yazi_bekleniyor", False):
        taslak = context.user_data.get("taslak")
        if taslak:
            taslak["gorsel_yazisi"] = "" if metin == "-" else metin[:100]
            await gorseli_yenile(update.effective_chat, taslak)
            return

    await taslak_olustur(update.effective_chat, context, update.message.text.strip()[:500])
 
 
@yetkili_olmali
async def buton_isle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Buton basışları. callback_data: 'gunler', 'gun:2', 'yenile', 'gorsel', 'paylas'."""
    sorgu = update.callback_query
    await sorgu.answer()
    eylem, _, deger = sorgu.data.partition(":")
    sohbet = update.effective_chat
 
    if eylem == "gunler":
        gunler = yaklasan_ozel_gunler()
        context.user_data["gunler"] = gunler
        if not gunler:
            await sorgu.edit_message_text("Yakın zamanda özel gün yok. Bir konu yazabilirsiniz.")
            return
        satirlar = [
            [Dugme(f"{g['tarih']:%d.%m} · {g['ad']}", callback_data=f"gun:{sira}")]
            for sira, g in enumerate(gunler)
        ]
        await sorgu.edit_message_text("Hangi özel gün için içerik üretelim?", reply_markup=Klavye(satirlar))
 
    elif eylem == "gun":
        gunler = context.user_data.get("gunler", [])
        if not deger.isdigit() or int(deger) >= len(gunler):
            await sorgu.edit_message_text("Liste eskimiş. /start yazıp tekrar deneyin.")
            return
        gun = gunler[int(deger)]
        await sorgu.edit_message_text(f"Seçildi: {gun['ad']}")
        await taslak_olustur(sohbet, context, f"{gun['ad']} için paylaşım", gun)
 
    elif eylem in ("yenile", "gorsel", "yazi", "paylas"):
        taslak = context.user_data.get("taslak")
        if not taslak:
            await sohbet.send_message("Taslak bulunamadı. Yeni bir konu yazın.")
            return
        await sorgu.edit_message_reply_markup(reply_markup=None)   # eski butonları kaldır
 
        if eylem == "yenile":
            await taslak_olustur(sohbet, context, taslak["istek"], taslak["ozel_gun"])
 
        elif eylem == "gorsel":
            await gorseli_yenile(sohbet, taslak)

        elif eylem == "yazi":
            context.user_data["yazi_bekleniyor"] = True
            await sohbet.send_message(
                "✏️ Görselin üzerinde yazmasını istediğiniz metni gönderin (en fazla 100 karakter).\n"
                "Yazıyı kaldırmak için - gönderin."
            )

        elif eylem == "paylas":
            sonuc = await taslagi_paylas(taslak)
            await sohbet.send_message(f"📤 {sonuc}", reply_markup=taslak_klavyesi())
 
 
# =============================================================================
# BÖLÜM 5 — PAYLAŞIM (2. HAFTA)
# =============================================================================
 
async def taslagi_paylas(taslak: dict) -> str:
    """2. HAFTA: Taslağı LinkedIn'de paylaşacak. Şimdilik yalnızca bilgi mesajı döndürür.
 
    Gelecek hafta burası doldurulacak. Elinizde hazır olanlar:
        son_metin(taslak)     → paylaşılacak metin (hashtag'lerle birlikte)
        taslak["gorsel"]      → görselin baytları
        taslak["alt_metin"]   → görsel açıklaması
    Fonksiyon, paylaşım bağlantısını (ya da hata mesajını) metin olarak döndürmeli.
    """
    return "Paylaşım özelliği gelecek hafta eklenecek."
 
 
# =============================================================================
# BAŞLATMA
# =============================================================================
 
def botu_baslat() -> None:
    if TELEGRAM_BOT_TOKEN.startswith("BURAYA") or OPENAI_API_ANAHTARI.startswith("BURAYA"):
        print("HATA: Dosyanın başındaki TELEGRAM_BOT_TOKEN ve OPENAI_API_ANAHTARI'nı doldurun.")
 
    uygulama = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    uygulama.add_handler(CommandHandler("start", baslat))
    uygulama.add_handler(CallbackQueryHandler(buton_isle))
    uygulama.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, metin_isle))
    uygulama.run_polling()
 
 
if __name__ == "__main__":
    botu_baslat()
 