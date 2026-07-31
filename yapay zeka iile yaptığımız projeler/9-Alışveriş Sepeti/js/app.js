/**
 * 9-alışveris-sepeti.py mantığını web arayüzünde çalıştırır.
 * sepet.append / sepet.remove / len(sepet)
 * 1000 TL üzeri → kargo ücretsiz
 */

const KARGO_UCRETI = 99;
const UCRETSIZ_KARGO_LIMITI = 1000;

const KATALOG = [
  { ad: 'Telefon', ikon: '📱', fiyat: 18500 },
  { ad: 'Kulaklık', ikon: '🎧', fiyat: 1299 },
  { ad: 'Laptop', ikon: '💻', fiyat: 24999 },
  { ad: 'Tablet', ikon: '📟', fiyat: 8990 },
  { ad: 'Mouse', ikon: '🖱️', fiyat: 349 },
  { ad: 'Klavye', ikon: '⌨️', fiyat: 899 },
];

/** Python: sepet = ["Telefon", "Kulaklık"] — fiyatlarla */
let sepet = [
  { ad: 'Telefon', fiyat: 18500 },
  { ad: 'Kulaklık', fiyat: 1299 },
];

const productsEl = document.getElementById('products');
const cartListEl = document.getElementById('cart-list');
const cartEmptyEl = document.getElementById('cart-empty');
const cartCountEl = document.getElementById('cart-count');
const cartBadgeEl = document.getElementById('cart-badge');
const cartSummaryEl = document.getElementById('cart-summary');
const araToplamEl = document.getElementById('ara-toplam');
const kargoUcretiEl = document.getElementById('kargo-ucreti');
const kargoHintEl = document.getElementById('kargo-hint');
const kargoRowEl = document.getElementById('kargo-row');
const genelToplamEl = document.getElementById('genel-toplam');
const addForm = document.getElementById('add-form');
const removeForm = document.getElementById('remove-form');
const yeniUrunInput = document.getElementById('yeni-urun');
const yeniFiyatInput = document.getElementById('yeni-fiyat');
const silinecekInput = document.getElementById('silinecek-urun');
const toastEl = document.getElementById('toast');
const cartPanel = document.getElementById('cart-panel');
const cartToggle = document.getElementById('cart-toggle');
const cartClose = document.getElementById('cart-close');

let toastTimer = null;

function formatTL(tutar) {
  return `${tutar.toLocaleString('tr-TR')} TL`;
}

function araToplamHesapla() {
  return sepet.reduce((toplam, urun) => toplam + urun.fiyat, 0);
}

function kargoHesapla(araToplam) {
  return araToplam > UCRETSIZ_KARGO_LIMITI ? 0 : KARGO_UCRETI;
}

function toast(mesaj, tip = 'ok') {
  clearTimeout(toastTimer);
  toastEl.hidden = false;
  toastEl.textContent = mesaj;
  toastEl.className = `toast toast--${tip} is-visible`;
  toastTimer = setTimeout(() => {
    toastEl.classList.remove('is-visible');
    setTimeout(() => {
      toastEl.hidden = true;
    }, 300);
  }, 2400);
}

function bumpBadge() {
  cartBadgeEl.classList.remove('is-bump');
  void cartBadgeEl.offsetWidth;
  cartBadgeEl.classList.add('is-bump');
  setTimeout(() => cartBadgeEl.classList.remove('is-bump'), 300);
}

function katalogFiyati(ad) {
  const urun = KATALOG.find(
    (item) => item.ad.toLocaleLowerCase('tr') === ad.toLocaleLowerCase('tr')
  );
  return urun ? urun.fiyat : null;
}

/** Python: sepet.append(yeni_urun) */
function urunEkle(ad, fiyat) {
  const urunAdi = ad.trim();
  if (!urunAdi) return;

  let urunFiyati = Number(fiyat);
  if (!Number.isFinite(urunFiyati) || urunFiyati <= 0) {
    const katalogdan = katalogFiyati(urunAdi);
    if (katalogdan == null) {
      toast('Geçerli bir fiyat giriniz', 'err');
      return;
    }
    urunFiyati = katalogdan;
  }

  sepet.push({ ad: urunAdi, fiyat: Math.round(urunFiyati) });
  sepetiCiz();
  bumpBadge();
  toast(`"${urunAdi}" sepete eklendi`, 'ok');
}

/** Python: if silinecek_urun in sepet: sepet.remove(...) else: "Ürün Bulunamadı" */
function urunSil(ad) {
  const urun = ad.trim();
  if (!urun) return;

  const index = sepet.findIndex(
    (item) => item.ad.toLocaleLowerCase('tr') === urun.toLocaleLowerCase('tr')
  );

  if (index === -1) {
    toast('Ürün Bulunamadı', 'err');
    return;
  }

  const silinen = sepet[index];
  sepet.splice(index, 1);
  sepetiCiz();
  bumpBadge();
  toast(`"${silinen.ad}" sepetten silindi`, 'ok');
}

function toplamGuncelle() {
  const ara = araToplamHesapla();
  const kargo = kargoHesapla(ara);
  const genel = ara + kargo;
  const ucretsiz = kargo === 0 && ara > 0;

  araToplamEl.textContent = formatTL(ara);
  genelToplamEl.textContent = formatTL(genel);

  if (sepet.length === 0) {
    kargoUcretiEl.textContent = '—';
    kargoUcretiEl.classList.remove('is-free');
    kargoRowEl.classList.remove('is-free');
    kargoHintEl.textContent = `1000 TL üzeri alışverişlerde kargo ücretsiz.`;
    cartSummaryEl.textContent = 'Sepetiniz boş.';
    return;
  }

  if (ucretsiz) {
    kargoUcretiEl.textContent = 'Ücretsiz';
    kargoUcretiEl.classList.add('is-free');
    kargoRowEl.classList.add('is-free');
    kargoHintEl.textContent = 'Tebrikler! Kargo ücretsiz.';
  } else {
    kargoUcretiEl.textContent = formatTL(KARGO_UCRETI);
    kargoUcretiEl.classList.remove('is-free');
    kargoRowEl.classList.remove('is-free');
    const kalan = UCRETSIZ_KARGO_LIMITI - ara;
    kargoHintEl.textContent = `${formatTL(kalan)} daha ekleyin, kargo ücretsiz olsun.`;
  }

  cartSummaryEl.textContent = `Sepetiniz: ${sepet.map((u) => u.ad).join(', ')}`;
}

function sepetiCiz() {
  const sayi = sepet.length; // len(sepet)
  cartCountEl.textContent = String(sayi);
  cartBadgeEl.textContent = String(sayi);

  cartEmptyEl.hidden = sayi > 0;
  cartListEl.hidden = sayi === 0;

  cartListEl.innerHTML = sepet
    .map(
      (urun, i) => `
      <li class="cart-item" data-index="${i}">
        <span class="cart-item__index">${i + 1}</span>
        <div class="cart-item__info">
          <span class="cart-item__name">${escapeHtml(urun.ad)}</span>
          <span class="cart-item__price">${formatTL(urun.fiyat)}</span>
        </div>
        <button type="button" class="cart-item__remove" data-remove="${escapeAttr(urun.ad)}" aria-label="${escapeAttr(urun.ad)} sil">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
            <path d="M5 7h14M10 11v6M14 11v6M8 7l1-2h6l1 2M9 7v12a1 1 0 001 1h4a1 1 0 001-1V7"/>
          </svg>
        </button>
      </li>`
    )
    .join('');

  toplamGuncelle();
}

function katalogCiz() {
  productsEl.innerHTML = KATALOG.map(
    (urun) => `
    <button type="button" class="product" data-add="${escapeAttr(urun.ad)}" data-fiyat="${urun.fiyat}" role="listitem">
      <span class="product__visual" aria-hidden="true">${urun.ikon}</span>
      <span class="product__name">${escapeHtml(urun.ad)}</span>
      <span class="product__price">${formatTL(urun.fiyat)}</span>
    </button>`
  ).join('');
}

function escapeHtml(text) {
  return String(text)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function escapeAttr(text) {
  return escapeHtml(text).replace(/'/g, '&#39;');
}

function sepetiAc() {
  cartPanel.classList.add('is-open');
  document.body.style.overflow = 'hidden';
}

function sepetiKapat() {
  cartPanel.classList.remove('is-open');
  document.body.style.overflow = '';
}

/* Events */
productsEl.addEventListener('click', (e) => {
  const btn = e.target.closest('[data-add]');
  if (!btn) return;
  urunEkle(btn.dataset.add, btn.dataset.fiyat);
});

cartListEl.addEventListener('click', (e) => {
  const btn = e.target.closest('[data-remove]');
  if (!btn) return;
  urunSil(btn.dataset.remove);
});

addForm.addEventListener('submit', (e) => {
  e.preventDefault();
  urunEkle(yeniUrunInput.value, yeniFiyatInput.value);
  yeniUrunInput.value = '';
  yeniFiyatInput.value = '';
  yeniUrunInput.focus();
});

removeForm.addEventListener('submit', (e) => {
  e.preventDefault();
  urunSil(silinecekInput.value);
  silinecekInput.value = '';
  silinecekInput.focus();
});

cartToggle.addEventListener('click', sepetiAc);
cartClose.addEventListener('click', sepetiKapat);

cartPanel.addEventListener('click', (e) => {
  if (e.target === cartPanel) sepetiKapat();
});

window.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') sepetiKapat();
});

/* Init */
katalogCiz();
sepetiCiz();
