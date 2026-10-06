import json
from openai import OpenAI
from telegram import (Update, InlineKeyboardButton,InlineKeyboardMarkup)
from telegram.ext import (ApplicationBuilder,CommandHandler,CallbackQueryHandler,ContextTypes)




telegram_token="xxxx:AAFSq1Qp6UkIihFXBnOvUAdH7ASuQTF3KHk"
openai_api_key="sk-proj-xxx-M9eDCmCAOxEnj6knfg9w-Q2KriK8-IL3-DEA"

client=OpenAI(api_key=openai_api_key)



def ai_soru_uret(sinav,ders,seviye):

    prompt=f"""
        Sen Türkiye'deki sınavlara yönelik soru hazırlayan deneyimli bir eğitim uzmanısın.

        Sınav:
        {sinav}

        Ders:
        {ders}

        Seviye:
        {seviye}

        Bu sınav ve derse uygun TEK BİR çoktan seçmeli soru oluştur.

        Kurallar:

        - Türkçe yaz.
        - 5 seçenek oluştur.
        - Seçenekler A, B, C, D ve E olsun.
        - Sadece bir doğru cevap olsun.
        - Soru seçilen sınavın tarzına uygun olsun.
        - Soru seviyesi verilen seviyeye uygun olsun.
        - Doğru cevabın kısa ve öğretici açıklamasını yaz.
        - Sorunun cevabı tartışmalı olmasın.
        - Sadece JSON formatında cevap ver.

        JSON formatı:

        {{
            "question": "Soru metni",
            "options": {{
                "A": "A seçeneği",
                "B": "B seçeneği",
                "C": "C seçeneği",
                "D": "D seçeneği",
                "E": "E seçeneği"
            }},
            "correct_answer": "A",
            "explanation": "Doğru cevabın açıklaması"
        }}


    """

    response=client.responses.create(
        model="gpt-6-luna",
        input=prompt
    )


    sonuc=response.output_text.strip()
    sonuc=sonuc.replace("```json","")
    sonuc = sonuc.replace("```", "")
    sonuc = sonuc.strip()
    return json.loads(sonuc)


async def start(update:Update,context: ContextTypes.DEFAULT_TYPE):



    keyboard = [
        [
            InlineKeyboardButton(
                "YKS",
                callback_data="exam_yks"
            ),
            InlineKeyboardButton(
                "KPSS",
                callback_data="exam_kpss"
            )
        ],
        [
            InlineKeyboardButton(
                "ALES",
                callback_data="exam_ales"
            ),
            InlineKeyboardButton(
                "DGS",
                callback_data="exam_dgs"
            )
        ],
        [
            InlineKeyboardButton(
                "LGS",
                callback_data="exam_lgs"
            )
        ]
    ]


    await update.message.reply_text(
        "Hangi sınava hazırlanıyorsun?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def sinav_sec(update: Update,context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    sinavlar = {
        "exam_yks": "YKS",
        "exam_kpss": "KPSS",
        "exam_ales": "ALES",
        "exam_dgs": "DGS",
        "exam_lgs": "LGS"
    }

    sinav = sinavlar[query.data]
    context.user_data["exam"] = sinav
    keyboard = [
        [
            InlineKeyboardButton(
                "Türkçe",
                callback_data="lesson_turkce"
            ),
            InlineKeyboardButton(
                "Matematik",
                callback_data="lesson_matematik"
            )
        ],
        [
            InlineKeyboardButton(
                "Tarih",
                callback_data="lesson_tarih"
            ),
            InlineKeyboardButton(
                "Coğrafya",
                callback_data="lesson_cografya"
            )
        ],
        [
            InlineKeyboardButton(
                "Vatandaşlık",
                callback_data="lesson_vatandaslik"
            ),
            InlineKeyboardButton(
                "Fen",
                callback_data="lesson_fen"
            )
        ]
    ]

    await query.edit_message_text(
        text=f"Sınav: {sinav}\n\nDers seç:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def ders_sec(update: Update,context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    dersler = {
        "lesson_turkce": "Türkçe",
        "lesson_matematik": "Matematik",
        "lesson_tarih": "Tarih",
        "lesson_cografya": "Coğrafya",
        "lesson_vatandaslik": "Vatandaşlık",
        "lesson_fen": "Fen"
    }

    ders = dersler[query.data]
    context.user_data["lesson"] = ders

    keyboard = [
        [
            InlineKeyboardButton(
                "Kolay",
                callback_data="level_easy"
            ),
            InlineKeyboardButton(
                "Orta",
                callback_data="level_medium"
            ),
            InlineKeyboardButton(
                "Zor",
                callback_data="level_hard"
            )
        ]
    ]

    await query.edit_message_text(
        text=f"Sınav: {context.user_data.get('exam', '-')}\nDers: {ders}\n\nSeviye seç:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def seviye_sec(update: Update,context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    seviyeler = {
        "level_easy": "Kolay",
        "level_medium": "Orta",
        "level_hard": "Zor"
    }

    seviye = seviyeler[query.data]

    context.user_data["level"] = seviye

    await query.edit_message_text(
        "Soru hazırlanıyor..."
    )

    await soru_gonder(
        query,
        context
    )


async def soru_gonder(query,context):

    sinav = context.user_data["exam"]
    ders = context.user_data["lesson"]
    seviye = context.user_data["level"]


    try:
        soru=ai_soru_uret(sinav,ders,seviye)


        context.user_data["current_question"] = soru

        options = soru["options"]

        mesaj = f"""
            📘 {sinav}

            📚 Ders: {ders}

            🎯 Seviye: {seviye}


            ❓ SORU

            {soru["question"]}


            A) {options["A"]}

            B) {options["B"]}

            C) {options["C"]}

            D) {options["D"]}

            E) {options["E"]}
        """



        keyboard = [
            [
                InlineKeyboardButton(
                    "A",
                    callback_data="answer_A"
                ),
                InlineKeyboardButton(
                    "B",
                    callback_data="answer_B"
                ),
                InlineKeyboardButton(
                    "C",
                    callback_data="answer_C"
                )
            ],
            [
                InlineKeyboardButton(
                    "D",
                    callback_data="answer_D"
                ),
                InlineKeyboardButton(
                    "E",
                    callback_data="answer_E"
                )
            ]
        ]

        await query.edit_message_text(
            text=mesaj,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    except Exception as hata:

        await query.edit_message_text(
            f"Soru oluşturulurken hata oluştu:\n\n{hata}"
        )




async def cevap_kontrol( update: Update,context: ContextTypes.DEFAULT_TYPE):


    query = update.callback_query

    await query.answer()
    user_answer=query.data.replace("answer_","")
    soru = context.user_data.get(
        "current_question"
    )

    if soru is None:

        await query.edit_message_text(
            "Aktif soru bulunamadı. /start yaz."
        )

        return
    correct_answer = soru["correct_answer"].upper()


    if user_answer==correct_answer:
         mesaj = f"""
        ✅ DOĞRU

        Doğru cevap: {correct_answer}

        📘 Açıklama:

        {soru["explanation"]}
        """

    else:

        mesaj = f"""
        ❌ YANLIŞ

        Senin cevabın: {user_answer}

        Doğru cevap: {correct_answer}

        📘 Açıklama:

        {soru["explanation"]}
        """


    keyboard = [
        [
            InlineKeyboardButton(
                "Yeni Soru",
                callback_data="new_question"
            )
        ],
        [
            InlineKeyboardButton(
                "Ders Değiştir",
                callback_data="change_lesson"
            )
        ],
        [
            InlineKeyboardButton(
                "Sınav Değiştir",
                callback_data="change_exam"
            )
        ]
    ]

    await query.edit_message_text(
        text=mesaj,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )



async def yeni_soru(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    await query.edit_message_text(
        "Yeni soru hazırlanıyor..."
    )

    await soru_gonder(
        query,
        context
    )


async def ders_degistir(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton(
                "Türkçe",
                callback_data="lesson_turkce"
            ),
            InlineKeyboardButton(
                "Matematik",
                callback_data="lesson_matematik"
            )
        ],
        [
            InlineKeyboardButton(
                "Tarih",
                callback_data="lesson_tarih"
            ),
            InlineKeyboardButton(
                "Coğrafya",
                callback_data="lesson_cografya"
            )
        ],
        [
            InlineKeyboardButton(
                "Vatandaşlık",
                callback_data="lesson_vatandaslik"
            ),
            InlineKeyboardButton(
                "Fen",
                callback_data="lesson_fen"
            )
        ]
    ]

    await query.edit_message_text(
        "Yeni ders seç:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def sinav_degistir(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton(
                "YKS",
                callback_data="exam_yks"
            ),
            InlineKeyboardButton(
                "KPSS",
                callback_data="exam_kpss"
            )
        ],
        [
            InlineKeyboardButton(
                "ALES",
                callback_data="exam_ales"
            ),
            InlineKeyboardButton(
                "DGS",
                callback_data="exam_dgs"
            )
        ],
        [
            InlineKeyboardButton(
                "LGS",
                callback_data="exam_lgs"
            )
        ]
    ]

    await query.edit_message_text(
        "Yeni sınav seç:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


def main():

    app = (
        ApplicationBuilder()
        .token(telegram_token)
        .build()
    )

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            sinav_sec,
            pattern="^exam_"
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            ders_sec,
            pattern="^lesson_"
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            seviye_sec,
            pattern="^level_"
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            cevap_kontrol,
            pattern="^answer_"
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            yeni_soru,
            pattern="^new_question$"
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            ders_degistir,
            pattern="^change_lesson$"
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            sinav_degistir,
            pattern="^change_exam$"
        )
    )

    print("Bot çalışıyor...")

    app.run_polling()


if __name__ == "__main__":
    main()



