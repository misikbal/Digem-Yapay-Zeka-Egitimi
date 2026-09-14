from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from openai import OpenAI
import os.path
import time
import base64


SCOPES=['https://www.googleapis.com/auth/gmail.readonly']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.path.join(BASE_DIR, 'credentials.json')
TOKEN_PATH = os.path.join(BASE_DIR, 'token.json')
API_ANAHTARI="ChatGPT API Anahtarı"
client=OpenAI(api_key=API_ANAHTARI)
SISTEM_KURALLARI="""
Sen profesyonel bir E-Posta asistanısın. Gelen mesajı oku, konusunu/kategorisini belirle 
ve cevap olarak gönderilmek üzere kısa, kibar bir taslak yanıt (Draft) oluştur. Sadece kritik gördüğün önemli mailleri ilet ve yorumla.
Format:
[KATEGORİ]: ...
[TASLAK YANIT]: ...
"""
def gmail_baglantisi_kur():
    creds=None
    if os.path.exists(TOKEN_PATH):
        creds=Credentials.from_authorized_user_file(TOKEN_PATH,SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow=InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH,SCOPES)
            creds=flow.run_local_server(port=0)
        with open(TOKEN_PATH,"w") as token:
            token.write(creds.to_json())

    return build("gmail","v1",credentials=creds)

def okunmamis_mailleri_getir(gmail_service):
    sonuc=gmail_service.users().messages().list(userId="me",q="is:unread").execute()
    mesajlar=sonuc.get("messages",[])
    
    if not mesajlar:
        print("Okunmamis mesaj bulunamadi.")

        return []

    mail_listesi=[]
    for mesaj in mesajlar:
        mail_detay=gmail_service.users().messages().get(userId="me",id=mesaj["id"], format="metadata").execute()

        headers=mail_detay["payload"]["headers"]
        gonderen = next(header['value'] for header in headers if header['name'] == 'From')
        konu = next(header['value'] for header in headers if header['name'] == 'Subject')
        ozet_metin = mail_detay.get('snippet', '')

        mail_listesi.append({
            "gonderen":gonderen,
            "konu":konu,
            "mesaj":ozet_metin
        })

    return mail_listesi


if __name__=="__main__":


    try:
        gmail_servisi=gmail_baglantisi_kur()
        yeni_mailler=okunmamis_mailleri_getir(gmail_servisi)

        for mail in yeni_mailler:
            print(f"\n GÖNDEREN: {mail['gonderen']}")
            print(f" KONU: {mail['konu']}")
            print(f" METİN (Özet): {mail['mesaj']}...")
            print(" Yapay Zeka Taslak Hazırlıyor...\n")

            ai_istegi=f"Gönderen: {mail['gonderen']}\nKonu: {mail['konu']}\nMesaj: {mail['mesaj']}"

            response=client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role":"system","content":SISTEM_KURALLARI},
                    {"role":"user","content":ai_istegi}
                ],
                temperature=0.3
            )
            print(response.choices[0].message.content)
            print("-" * 50)
            time.sleep(1) # API güvenlik limiti için bekleme

    except Exception as e:
        print(f"❌ Kritik Sistem Hatası: {e}")
