import os.path
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from openai import OpenAI
import time

# --- AYARLAR ---
# Sadece mailleri OKUMA izni istiyoruz (Silme veya gönderme yetkisi yok - Güvenlik!)
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.path.join(BASE_DIR, 'credentials.json')
TOKEN_PATH = os.path.join(BASE_DIR, 'token.json')
API_ANAHTARI="ChatGPT API Anahtarı"
client = OpenAI(api_key=API_ANAHTARI)

SISTEM_KURALLARI = """
Sen profesyonel bir E-Posta asistanısın. Gelen mesajı oku, konusunu/kategorisini belirle 
ve cevap olarak gönderilmek üzere kısa, kibar bir taslak yanıt (Draft) oluştur.
Format:
[KATEGORİ]: ...
[TASLAK YANIT]: ...
"""

def gmail_baglantisi_kur():
    """Google OAuth 2.0 ile güvenli oturum açar ve token.json dosyasını yönetir."""
    creds = None
    # Eğer daha önce giriş yapıldıysa token.json dosyasından bilgileri oku
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    
    # Geçerli bir kimlik yoksa veya süresi dolduysa kullanıcıdan tarayıcıda onay iste
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        # Bir sonraki çalışma için onayı kaydet
        with open(TOKEN_PATH, 'w') as token_file:
            token_file.write(creds.to_json())

    # Gmail servisini başlat ve döndür
    return build('gmail', 'v1', credentials=creds)

def okunmamis_mailleri_getir(service):
    """Gelen kutusundaki okunmamış ilk 3 e-postayı çeker."""
    print("📥 Gmail'e bağlanıldı. Okunmamış mailler aranıyor...")
    
    # 'INBOX' ve 'UNREAD' etiketine sahip ilk 3 maili bul
    sonuc = service.users().messages().list(userId='me', labelIds=['INBOX', 'UNREAD'], maxResults=3).execute()
    mesajlar = sonuc.get('messages', [])
    
    if not mesajlar:
        print("✅ Harika! Okunmamış yeni e-posta yok.")
        return []

    mail_listesi = []
    for msg in mesajlar:
        # Mailin sadece temel metnini (snippet) çekiyoruz (Kod karmaşasını önlemek için)
        mail_detay = service.users().messages().get(userId='me', id=msg['id'], format='metadata').execute()
        
        # Gönderen ve Konu bilgisini başlıklardan (headers) ayıklama
        headers = mail_detay['payload']['headers']
        gonderen = next(header['value'] for header in headers if header['name'] == 'From')
        konu = next(header['value'] for header in headers if header['name'] == 'Subject')
        ozet_metin = mail_detay.get('snippet', '') # Mailin ilk 200 karakterlik özeti
        
        mail_listesi.append({
            "gonderen": gonderen,
            "konu": konu,
            "mesaj": ozet_metin
        })
    return mail_listesi

# --- ANA PROGRAM AKIŞI ---
if __name__ == '__main__':
    print("==================================================")
    print("🌐 DİGEM GMAIL & AI ENTEGRASYON SİSTEMİ")
    print("==================================================")
    
    try:
        gmail_servisi = gmail_baglantisi_kur()
        yeni_mailler = okunmamis_mailleri_getir(gmail_servisi)
        
        for mail in yeni_mailler:
            print(f"\n📩 GÖNDEREN: {mail['gonderen']}")
            print(f"📌 KONU: {mail['konu']}")
            print(f"📝 METİN (Özet): {mail['mesaj']}...")
            print("⏳ Yapay Zeka Taslak Hazırlıyor...\n")
            
            ai_istegi = f"Gönderen: {mail['gonderen']}\nKonu: {mail['konu']}\nMesaj: {mail['mesaj']}"
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": SISTEM_KURALLARI},
                    {"role": "user", "content": ai_istegi}
                ],
                temperature=0.3
            )
            
            print(response.choices[0].message.content)
            print("-" * 50)
            time.sleep(1) # API güvenlik limiti için bekleme

    except Exception as e:
        print(f"❌ Kritik Sistem Hatası: {e}")