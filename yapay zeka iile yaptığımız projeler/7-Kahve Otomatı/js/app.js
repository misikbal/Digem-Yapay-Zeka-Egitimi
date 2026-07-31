/**
 * 7-Kahve Otomatı.py mantığını web arayüzünde çalıştırır.
 */

const URUNLER = {
  1: { ad: 'Ekspreso', fiyat: 40, ikon: '☕' },
  2: { ad: 'Latte', fiyat: 50, ikon: '🥛' },
  3: { ad: 'Mocha', fiyat: 60, ikon: '🍫' },
  4: { ad: 'Çay', fiyat: 10, ikon: '🍵' },
};

const lcd = document.getElementById('lcd');
const lcdTitle = document.getElementById('lcd-title');
const lcdMessage = document.getElementById('lcd-message');
const lcdSub = document.getElementById('lcd-sub');
const paymentSection = document.getElementById('payment-section');
const insertedAmountEl = document.getElementById('inserted-amount');
const btnConfirm = document.getElementById('btn-confirm');
const btnCancel = document.getElementById('btn-cancel');
const dispenserCup = document.getElementById('dispenser-cup');
const machine = document.getElementById('machine');
const drinkCards = document.querySelectorAll('.drink');
const selectKeys = document.querySelectorAll('.key--select');
const moneyKeys = document.querySelectorAll('.key--money');

let secim = null;
let atilanPara = 0;
let durum = 'bekleme'; // bekleme | odeme | hazirlaniyor | tamamlandi

function lcdGuncelle(baslik, mesaj, alt = '', hata = false) {
  lcdTitle.textContent = baslik;
  lcdMessage.textContent = mesaj;
  lcdSub.textContent = alt;
  lcd.classList.toggle('lcd--error', hata);
  lcd.classList.toggle('lcd--success', !hata && durum === 'tamamlandi');
}

function icecekSec(secimNo) {
  if (durum !== 'bekleme') return;

  const urun = URUNLER[secimNo];
  if (!urun) {
    lcdGuncelle('Hata', 'Hatalı Tuşlama Yaptınız', 'Program Sonlandırılıyor', true);
    setTimeout(sifirla, 2500);
    return;
  }

  secim = urun;
  atilanPara = 0;
  durum = 'odeme';

  drinkCards.forEach((card) => {
    card.classList.toggle('drink--selected', card.dataset.id === String(secimNo));
  });

  selectKeys.forEach((key) => {
    key.disabled = true;
  });

  paymentSection.hidden = false;
  insertedAmountEl.textContent = '0 TL';

  lcdGuncelle(
    `Seçilen: ${urun.ad}`,
    `Ödemeniz Gereken Tutar: ${urun.fiyat} TL`,
    'Lütfen otomata para yükleyiniz'
  );
}

function paraYukle(miktar) {
  if (durum !== 'odeme') return;

  atilanPara += miktar;
  insertedAmountEl.textContent = `${atilanPara} TL`;

  if (atilanPara >= secim.fiyat) {
    lcdSub.textContent = `Yeterli bakiye. Onaylayın veya fazla para yükleyin.`;
  } else {
    const eksik = secim.fiyat - atilanPara;
    lcdSub.textContent = `${eksik} TL daha yüklemeniz gerek`;
  }
}

function odemeOnayla() {
  if (durum !== 'odeme' || !secim) return;

  if (atilanPara >= secim.fiyat) {
    const paraUstu = atilanPara - secim.fiyat;
    durum = 'hazirlaniyor';
    machine.classList.add('machine--brewing');

    paymentSection.hidden = true;
    moneyKeys.forEach((key) => {
      key.disabled = true;
    });
    btnConfirm.disabled = true;

    const secilenKart = document.querySelector(`.drink[data-name="${secim.ad}"]`);
    if (secilenKart) {
      secilenKart.classList.add('drink--dispensing');
    }

    lcdGuncelle(
      secim.ad,
      `${secim.ad} hazırlanıyor... Lütfen Bekleyiniz.`,
      ''
    );

    setTimeout(() => {
      durum = 'tamamlandi';
      machine.classList.remove('machine--brewing');

      if (secilenKart) {
        secilenKart.classList.remove('drink--dispensing');
      }

      dispenserCup.textContent = secim.ikon;
      dispenserCup.hidden = false;

      lcdGuncelle(
        'İşlem Tamamlandı',
        `Para üstünüz: ${paraUstu} TL`,
        'Afiyet Olsun!'
      );

      setTimeout(sifirla, 4000);
    }, 2200);
  } else {
    const eksik = secim.fiyat - atilanPara;
    lcdGuncelle(
      'Yetersiz Bakiye!',
      `${secim.ad} için ${eksik} TL daha yüklemeniz gerek`,
      '',
      true
    );
  }
}

function sifirla() {
  secim = null;
  atilanPara = 0;
  durum = 'bekleme';

  drinkCards.forEach((card) => {
    card.classList.remove('drink--selected', 'drink--dispensing');
  });

  selectKeys.forEach((key) => {
    key.disabled = false;
  });

  moneyKeys.forEach((key) => {
    key.disabled = false;
  });

  btnConfirm.disabled = false;
  paymentSection.hidden = true;
  insertedAmountEl.textContent = '0 TL';
  dispenserCup.hidden = true;
  machine.classList.remove('machine--brewing');

  lcdGuncelle('Hoş Geldiniz', 'Lütfen bir içecek seçiniz', '');
}

function iptal() {
  if (durum === 'hazirlaniyor') return;
  sifirla();
}

selectKeys.forEach((key) => {
  key.addEventListener('click', () => {
    icecekSec(key.dataset.select);
  });
});

drinkCards.forEach((card) => {
  card.addEventListener('click', () => {
    icecekSec(card.dataset.id);
  });
  card.style.cursor = 'pointer';
});

moneyKeys.forEach((key) => {
  key.addEventListener('click', () => {
    paraYukle(Number(key.dataset.money));
  });
});

btnConfirm.addEventListener('click', odemeOnayla);
btnCancel.addEventListener('click', iptal);

lcdGuncelle('Hoş Geldiniz', 'Lütfen bir içecek seçiniz', '');
