"""Burç Rehberi: OpenAI destekli masaüstü sohbet uygulaması.

Çalıştırmadan önce aşağıdaki API_KEY değişkenine kendi anahtarınızı yazın.
"""

import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

# Kendi OpenAI API anahtarınızı tırnakların arasına yazın.
# Örnek: API_KEY = "sk-proj-..."
API_ANAHTARI="ChatGPT API Anahtarı"



SYSTEM_PROMPT = """Sen yalnızca Türkçe konuşan, sıcak ve bilgili bir burç rehberisin.
Kullanıcıya burçların genel özellikleri, elementleri, tarih aralıkları, uyumları
ve eğlencelik günlük yorumlar konusunda yardımcı ol. Astrolojinin bilimsel olarak
kanıtlanmış bir yöntem olmadığını gerektiğinde nazikçe belirt. Kesin gelecek
tahminleri, tıbbi, hukuki veya finansal yönlendirme yapma. Burç ve astroloji
dışındaki bilimsel, tarihsel, politik, genel kültür veya diğer tüm konularda
bilgi verme; sadece "Yalnızca burçlar hakkında yardımcı olabilirim." de.
Cevapların kısa, anlaşılır ve samimi olsun."""

ASTROLOJI_ANAHTARLARI = (
    "burç", "burcun", "burcu", "burçlar", "astroloji", "astrolojik", "zodyak",
    "yükselen", "doğum haritası", "ay burcu", "güneş burcu", "burç uyumu",
    "burç uyum", "elementi", "elementler", "retro", "merkür retrosu",
)

BURCLAR = {
    "Koç": "21 Mart – 19 Nisan • Ateş", "Boğa": "20 Nisan – 20 Mayıs • Toprak",
    "İkizler": "21 Mayıs – 20 Haziran • Hava", "Yengeç": "21 Haziran – 22 Temmuz • Su",
    "Aslan": "23 Temmuz – 22 Ağustos • Ateş", "Başak": "23 Ağustos – 22 Eylül • Toprak",
    "Terazi": "23 Eylül – 22 Ekim • Hava", "Akrep": "23 Ekim – 21 Kasım • Su",
    "Yay": "22 Kasım – 21 Aralık • Ateş", "Oğlak": "22 Aralık – 19 Ocak • Toprak",
    "Kova": "20 Ocak – 18 Şubat • Hava", "Balık": "19 Şubat – 20 Mart • Su",
}


class BurcRehberi:
    def __init__(self, root):
        self.root = root
        self.root.title("ORBIT • Burç Rehberi")
        self.root.geometry("1180x850")
        self.root.minsize(1000, 760)
        self.root.configure(bg="#090B17")
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        self.client = None
        self.busy = False
        self.make_ui()
        self.add_message("asistan", "Merhaba! Ben Burç Rehberi. Burcun, uyumlar veya günlük yorumlar hakkında ne öğrenmek istersin?")

    def make_ui(self):
        # Üst marka alanı
        header = tk.Frame(self.root, bg="#11142A", padx=34, pady=22)
        header.pack(fill="x")
        brand = tk.Frame(header, bg="#11142A")
        brand.pack(side="left")
        tk.Label(brand, text="✦", font=("Segoe UI Symbol", 27, "bold"), fg="#DCA8FF", bg="#11142A").pack(side="left", padx=(0, 11))
        title_box = tk.Frame(brand, bg="#11142A")
        title_box.pack(side="left")
        tk.Label(title_box, text="ORBIT", font=("Segoe UI", 20, "bold"), fg="#FAFAFF", bg="#11142A").pack(anchor="w")
        tk.Label(title_box, text="KİŞİSEL BURÇ REHBERİN", font=("Segoe UI", 8, "bold"), fg="#9DA4C7", bg="#11142A").pack(anchor="w")
        status = tk.Frame(header, bg="#20264C", padx=12, pady=7)
        status.pack(side="right", pady=6)
        self.status_label = tk.Label(status, text="✦  KİŞİSEL ASTROLOJİ ASİSTANI", font=("Segoe UI", 9, "bold"), fg="#DCA8FF", bg="#20264C")
        self.status_label.pack()

        hero = tk.Frame(self.root, bg="#201735", padx=30, pady=20)
        hero.pack(fill="x", padx=28, pady=(18, 0))
        hero_copy = tk.Frame(hero, bg="#201735")
        hero_copy.pack(side="left", fill="x", expand=True)
        tk.Label(hero_copy, text="KENDİ EVRENİNİ KEŞFET", bg="#201735", fg="#E3B775", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        tk.Label(hero_copy, text="Burcunu tanı. Kendine yeni bir gözle bak.", bg="#201735", fg="#FFF5EB", font=("Segoe UI", 23, "bold")).pack(anchor="w", pady=(5, 6))
        tk.Label(hero_copy, text="Karakterin, ilişkilerin ve merak ettiklerin için kişisel bir sohbet başlat.", bg="#201735", fg="#BAB0CA", font=("Segoe UI", 10)).pack(anchor="w")
        tk.Button(hero, text="Sohbete başla  ↗", command=lambda: self.entry.focus_set(), bg="#E3B775", fg="#21172F", activebackground="#F0CE9D", relief="flat", bd=0, padx=20, pady=13, cursor="hand2", font=("Segoe UI", 11, "bold")).pack(side="right", padx=(18, 0))

        body = tk.Frame(self.root, bg="#090B17", padx=28, pady=25)
        body.pack(fill="both", expand=True)
        side = tk.Frame(body, bg="#12162B", width=238, padx=16, pady=18)
        side.pack(side="left", fill="y", padx=(0, 20))
        side.pack_propagate(False)
        tk.Label(side, text="KEŞFET", font=("Segoe UI", 9, "bold"), fg="#A981FF", bg="#12162B").pack(anchor="w")
        tk.Label(side, text="Burcunu seç", font=("Segoe UI", 16, "bold"), fg="#F7F7FE", bg="#12162B").pack(anchor="w", pady=(1, 2))
        tk.Label(side, text="Özelliklerini ve uyumlarını keşfet.", font=("Segoe UI", 9), fg="#8F96B7", bg="#12162B").pack(anchor="w", pady=(0, 13))
        for burc, bilgi in BURCLAR.items():
            button = tk.Button(side, text=f"{burc:<9}   {bilgi.split(' • ')[1]}", command=lambda b=burc: self.ask_burc(b), justify="left", anchor="w", font=("Segoe UI", 9, "bold"), fg="#DEE1F6", bg="#1A1F3B", activebackground="#7C4DCC", activeforeground="white", relief="flat", bd=0, padx=12, pady=7, cursor="hand2")
            button.pack(fill="x", pady=2)
        tk.Label(side, text="12 burç · Sana özel sorular", font=("Segoe UI", 8), fg="#A99BBB", bg="#12162B").pack(side="bottom", anchor="w")

        chat_area = tk.Frame(body, bg="#090B17")
        chat_area.pack(side="left", fill="both", expand=True)
        chat_header = tk.Frame(chat_area, bg="#090B17")
        chat_header.pack(fill="x", pady=(0, 12))
        tk.Label(chat_header, text="Keşfin burada başlıyor", font=("Segoe UI", 18, "bold"), fg="#F7F7FE", bg="#090B17").pack(side="left")
        tk.Label(chat_header, text="  BURÇ ODAKLI", font=("Segoe UI", 8, "bold"), fg="#DCA8FF", bg="#2A1F47", padx=9, pady=5).pack(side="right")
        # Alt alan önce yerleştirilir: pencere küçülünce prompt görünür kalır.
        composer = tk.Frame(chat_area, bg="#171B34", padx=16, pady=12, highlightbackground="#76608E", highlightthickness=1)
        composer.pack(side="bottom", fill="x", pady=(12, 0))
        tk.Label(composer, text="SORUNU YAZ", bg="#171B34", fg="#E3B775", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.entry = tk.Text(composer, height=3, wrap="word", font=("Segoe UI", 11), bg="#171B34", fg="#F7F7FE", relief="flat", bd=0, insertbackground="#F7F7FE", padx=2, pady=8)
        self.entry.pack(fill="x")
        self.entry.bind("<Return>", self.send_message)
        self.entry.bind("<Shift-Return>", lambda event: None)
        controls = tk.Frame(composer, bg="#171B34")
        controls.pack(fill="x")
        tk.Label(controls, text="Enter: gönder · Shift+Enter: yeni satır", bg="#171B34", fg="#989EBB", font=("Segoe UI", 8)).pack(side="left")
        self.send_btn = tk.Button(controls, text="Yanıtını keşfet  →", command=self.send_message, font=("Segoe UI", 10, "bold"), bg="#E3B775", fg="#21172F", activebackground="#F0CE9D", relief="flat", bd=0, padx=18, pady=9, cursor="hand2")
        self.send_btn.pack(side="right")
        suggestions = tk.Frame(chat_area, bg="#090B17")
        suggestions.pack(fill="x", pady=(0, 12))
        for title, prompt in [("✦ Burcumu tanı", "Terazi burcunun özellikleri nelerdir?"), ("♡ İlişki uyumu", "Koç ve Terazi burçlarının uyumu nasıldır?"), ("☾ Yükselen burç", "Yükselen burç ne anlama gelir?")]:
            tk.Button(suggestions, text=title, command=lambda p=prompt: self.fill_prompt(p), bg="#231D35", fg="#DBC5F4", activebackground="#423257", relief="flat", bd=0, padx=12, pady=9, cursor="hand2", font=("Segoe UI", 9)).pack(side="left", padx=(0, 8))
        chat_card = tk.Frame(chat_area, bg="#12162B", padx=1, pady=1)
        chat_card.pack(fill="both", expand=True)
        self.chat = scrolledtext.ScrolledText(chat_card, height=6, wrap="word", font=("Segoe UI", 11), bg="#12162B", fg="#ECE6F4", relief="flat", padx=22, pady=18, state="disabled", selectbackground="#574375")
        self.chat.pack(fill="both", expand=True)
        self.chat.tag_config("user", foreground="#CAA2FF", font=("Segoe UI", 10, "bold"), spacing1=8)
        self.chat.tag_config("asistan", foreground="#E3B775", font=("Segoe UI", 10, "bold"), spacing1=8)
        self.chat.tag_config("metin", foreground="#D8D9E7", font=("Segoe UI", 11), spacing1=5, spacing2=4)

        tk.Label(self.root, text="Astroloji eğlence ve kişisel keşif amaçlıdır. Yanıtlar yapay zekâ tarafından oluşturulur.", bg="#090B17", fg="#8F96B7", font=("Segoe UI", 8)).pack(side="bottom", pady=(0, 10))

    def add_message(self, sender, text):
        label = "Sen" if sender == "user" else "Burç Rehberi"
        self.chat.configure(state="normal")
        self.chat.insert("end", f"{label}\n", sender); self.chat.insert("end", f"{text}\n\n", "metin")
        self.chat.configure(state="disabled"); self.chat.see("end")

    def ask_burc(self, burc):
        self.fill_prompt(f"{burc} burcu hakkında bilgi verir misin?")

    def fill_prompt(self, prompt):
        self.entry.delete("1.0", "end")
        self.entry.insert("1.0", prompt)
        self.entry.focus_set()

    @staticmethod
    def is_astroloji_sorusu(question):
        """Burç dışı konuların API'ye gönderilmesini engeller."""
        question = question.lower().replace("i̇", "i")
        return any(keyword in question for keyword in ASTROLOJI_ANAHTARLARI)

    def send_message(self, event=None):
        question = self.entry.get("1.0", "end-1c").strip()
        if not question or self.busy:
            return "break"
        self.entry.delete("1.0", "end"); self.add_message("user", question)
        if not self.is_astroloji_sorusu(question):
            self.add_message("asistan", "Yalnızca burçlar ve astroloji hakkında yardımcı olabilirim. Örneğin: “Terazi burcunun özellikleri nelerdir?”")
            return "break"
        self.messages.append({"role": "user", "content": question})
        self.busy = True
        self.send_btn.config(state="disabled", text="Düşünüyor...")
        threading.Thread(target=self.get_answer, daemon=True).start()
        return "break"

    def finish_request(self):
        self.busy = False
        self.send_btn.config(state="normal", text="Yanıtını keşfet  →")

    def get_answer(self):
        try:
            if OpenAI is None:
                raise RuntimeError("OpenAI paketi kurulu değil. Terminalde: pip install openai")
            if self.client is None:
                if not API_KEY:
                    raise RuntimeError("API_KEY boş. Dosyanın başındaki API_KEY değişkenine anahtarınızı yazın.")
                self.client = OpenAI(api_key=API_KEY)
            response = self.client.chat.completions.create(model="gpt-4o-mini", messages=self.messages)
            answer = response.choices[0].message.content
            self.messages.append({"role": "assistant", "content": answer})
            self.root.after(0, lambda: self.add_message("asistan", answer))
        except Exception as error:
            self.root.after(0, lambda message=str(error): messagebox.showerror("Bağlantı sorunu", message))
        finally:
            self.root.after(0, self.finish_request)


if __name__ == "__main__":
    window = tk.Tk()
    BurcRehberi(window)
    window.mainloop()
