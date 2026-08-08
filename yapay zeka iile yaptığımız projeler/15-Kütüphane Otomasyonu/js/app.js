const kutuphaneVeritabani = {
  uyeler: [
    {
      kullanici_adi: "ahmet",
      sifre: "123",
      ad_soyad: "Ahmet Yılmaz",
      odunc_kitaplar: [],
    },
    {
      kullanici_adi: "besse",
      sifre: "123",
      ad_soyad: "Besse Tuğtekin",
      odunc_kitaplar: [],
    },
    {
      kullanici_adi: "ali",
      sifre: "123",
      ad_soyad: "Ali Yülkebir Güneş",
      odunc_kitaplar: [],
    },
  ],
  kitaplar: [
    { id: 1, ad: "Zamanın Kısa Tarihi", yazar: "Stephen Hawking", stok: 3, gorsel: "img/1.jpg" },
    { id: 2, ad: "Kozmos", yazar: "Carl Sagan", stok: 4, gorsel: "img/2.jpg" },
    { id: 3, ad: "Gen Bencil midir?", yazar: "Richard Dawkins", stok: 2, gorsel: "img/3.jpg" },
    { id: 4, ad: "Türlerin Kökeni", yazar: "Charles Darwin", stok: 5, gorsel: "img/4.jpg" },
    { id: 5, ad: "Sapiens", yazar: "Yuval Noah Harari", stok: 6, gorsel: "img/5.jpg" },
    { id: 6, ad: "Gen", yazar: "Siddhartha Mukherjee", stok: 3, gorsel: "img/6.jpg" },
    { id: 7, ad: "Acelecilere Astrofizik", yazar: "Neil deGrasse Tyson", stok: 4, gorsel: "img/7.jpg" },
    { id: 8, ad: "Zarif Evren", yazar: "Brian Greene", stok: 2, gorsel: "img/8.jpg" },
    { id: 9, ad: "Sessiz Bahar", yazar: "Rachel Carson", stok: 1, gorsel: "img/9.jpg" },
    { id: 10, ad: "Henrietta Lacks'in Ölümsüz Yaşamı", yazar: "Rebecca Skloot", stok: 3, gorsel: "img/10.jpg" },
    { id: 11, ad: "Hızlı ve Yavaş Düşünme", yazar: "Daniel Kahneman", stok: 0, gorsel: "img/11.jpg" },
    { id: 12, ad: "Karanlık Bir Dünyada Bilimin Mum Işığı", yazar: "Carl Sagan", stok: 2, gorsel: "img/12.jpg" },
    { id: 13, ad: "Tüfek, Mikrop ve Çelik", yazar: "Jared Diamond", stok: 4, gorsel: "img/13.jpg" },
    { id: 14, ad: "İkili Sarmal", yazar: "James D. Watson", stok: 3, gorsel: "img/14.jpg" },
    { id: 15, ad: "Neden Uyuruz?", yazar: "Matthew Walker", stok: 5, gorsel: "img/15.jpg" },
    { id: 16, ad: "Ağaçların Gizli Yaşamı", yazar: "Peter Wohlleben", stok: 4, gorsel: "img/16.jpg" },
    { id: 17, ad: "Kaos", yazar: "James Gleick", stok: 0, gorsel: "img/17.jpg" },
    { id: 18, ad: "Evrenin Dokusu", yazar: "Brian Greene", stok: 2, gorsel: "img/18.jpg" },
    { id: 19, ad: "Homo Deus", yazar: "Yuval Noah Harari", stok: 3, gorsel: "img/19.jpg" },
    { id: 20, ad: "Altıncı Yok Oluş", yazar: "Elizabeth Kolbert", stok: 4, gorsel: "img/20.jpg" },
  ],
};

let aktifUye = null;

const loginScreen = document.getElementById("login-screen");
const appScreen = document.getElementById("app-screen");
const loginForm = document.getElementById("login-form");
const loginError = document.getElementById("login-error");
const togglePin = document.getElementById("toggle-pin");
const loginPin = document.getElementById("login-pin");
const logoutBtn = document.getElementById("logout-btn");
const toastEl = document.getElementById("toast");

const viewMeta = {
  catalog: { eyebrow: "Katalog", title: "Kitap Listele" },
  borrow: { eyebrow: "İşlem", title: "Kitap Ödünç Al" },
  mine: { eyebrow: "Hesabım", title: "Aldığım Kitaplar" },
};

function uyeGiris(kullaniciAdi, sifre) {
  return (
    kutuphaneVeritabani.uyeler.find(
      (uye) => uye.kullanici_adi === kullaniciAdi && uye.sifre === sifre
    ) || null
  );
}

function kitapOduncAl(uye, kitapId) {
  const kitap = kutuphaneVeritabani.kitaplar.find((k) => k.id === kitapId);
  if (!kitap) {
    showToast("Geçersiz kitap ID", "err");
    return false;
  }
  if (kitap.stok <= 0) {
    showToast(`Üzgünüz, "${kitap.ad}" kitabı tükendi.`, "err");
    return false;
  }
  kitap.stok -= 1;
  uye.odunc_kitaplar.push({
    id: kitap.id,
    ad: kitap.ad,
    yazar: kitap.yazar,
    gorsel: kitap.gorsel,
  });
  showToast("Kitap başarılı bir şekilde ödünç verildi", "ok");
  return true;
}

function showToast(message, type = "ok") {
  toastEl.textContent = message;
  toastEl.className = `toast toast--${type}`;
  toastEl.hidden = false;
  clearTimeout(showToast._t);
  showToast._t = setTimeout(() => {
    toastEl.hidden = true;
  }, 2800);
}

function stokBadge(stok) {
  if (stok > 0) {
    return `<span class="badge badge--ok">Stokta ${stok} adet</span>`;
  }
  return `<span class="badge badge--out">Stok yok</span>`;
}

function bookCover(kitap) {
  return `
    <div class="book-card__cover">
      <img src="${kitap.gorsel}" alt="${kitap.ad} kapak" loading="lazy">
      <span class="book-card__id">#${kitap.id}</span>
    </div>
  `;
}

function renderCatalog() {
  const grid = document.getElementById("catalog-grid");
  grid.innerHTML = kutuphaneVeritabani.kitaplar
    .map(
      (kitap, i) => `
      <article class="book-card" role="listitem" style="animation-delay:${i * 0.05}s">
        ${bookCover(kitap)}
        <h3 class="book-card__title">${kitap.ad}</h3>
        <p class="book-card__author">${kitap.yazar}</p>
        <div class="book-card__meta">${stokBadge(kitap.stok)}</div>
      </article>
    `
    )
    .join("");
}

function renderBorrow() {
  const grid = document.getElementById("borrow-grid");
  grid.innerHTML = kutuphaneVeritabani.kitaplar
    .map(
      (kitap, i) => `
      <article class="book-card" role="listitem" style="animation-delay:${i * 0.05}s">
        ${bookCover(kitap)}
        <h3 class="book-card__title">${kitap.ad}</h3>
        <p class="book-card__author">${kitap.yazar}</p>
        <div class="book-card__meta">
          ${stokBadge(kitap.stok)}
          <button
            type="button"
            class="btn ${kitap.stok > 0 ? "btn--primary" : "btn--soft"}"
            data-borrow="${kitap.id}"
            ${kitap.stok > 0 ? "" : "disabled"}
          >
            ${kitap.stok > 0 ? "Ödünç Al" : "Tükendi"}
          </button>
        </div>
      </article>
    `
    )
    .join("");
}

function renderMine() {
  const list = document.getElementById("mine-list");
  if (!aktifUye.odunc_kitaplar.length) {
    list.innerHTML = `
      <div class="empty">
        <p class="empty__title">Henüz ödünç kitap yok</p>
        <p>Katalogdan stokta olan bir kitabı ödünç alabilirsiniz.</p>
      </div>
    `;
    return;
  }

  list.innerHTML = aktifUye.odunc_kitaplar
    .map(
      (kitap, i) => `
      <div class="mine-item" style="animation-delay:${i * 0.05}s">
        <img class="mine-item__cover" src="${kitap.gorsel}" alt="${kitap.ad}" loading="lazy">
        <div>
          <p class="mine-item__title">${kitap.ad}</p>
          <p class="mine-item__author">${kitap.yazar}</p>
        </div>
      </div>
    `
    )
    .join("");
}

function refreshViews() {
  renderCatalog();
  renderBorrow();
  renderMine();
}

function setView(name) {
  document.querySelectorAll(".nav__item").forEach((btn) => {
    btn.classList.toggle("is-active", btn.dataset.view === name);
  });

  document.getElementById("view-catalog").hidden = name !== "catalog";
  document.getElementById("view-borrow").hidden = name !== "borrow";
  document.getElementById("view-mine").hidden = name !== "mine";

  const meta = viewMeta[name];
  document.getElementById("view-eyebrow").textContent = meta.eyebrow;
  document.getElementById("view-title").textContent = meta.title;

  if (name === "mine") renderMine();
  if (name === "catalog") renderCatalog();
  if (name === "borrow") renderBorrow();
}

function enterApp(uye) {
  aktifUye = uye;
  loginScreen.hidden = true;
  appScreen.hidden = false;

  document.getElementById("user-name").textContent = uye.ad_soyad;
  document.getElementById("user-handle").textContent = `@${uye.kullanici_adi}`;
  document.getElementById("user-avatar").textContent = uye.ad_soyad
    .charAt(0)
    .toUpperCase();
  document.getElementById("greeting").textContent = `Hoş geldin, ${uye.ad_soyad}`;

  refreshViews();
  setView("catalog");
  showToast(`Giriş başarılı. Hoş geldin ${uye.ad_soyad}`, "ok");
}

function exitApp() {
  aktifUye = null;
  appScreen.hidden = true;
  loginScreen.hidden = false;
  loginForm.reset();
  loginError.hidden = true;
  showToast("Çıkış yapıldı. İyi okumalar!", "ok");
}

loginForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const kullaniciAdi = document.getElementById("login-user").value.trim();
  const sifre = loginPin.value.trim();
  const uye = uyeGiris(kullaniciAdi, sifre);

  if (uye) {
    loginError.hidden = true;
    enterApp(uye);
  } else {
    loginError.textContent = "Hatalı kullanıcı adı veya şifre!";
    loginError.hidden = false;
  }
});

togglePin.addEventListener("click", () => {
  const isPass = loginPin.type === "password";
  loginPin.type = isPass ? "text" : "password";
});

document.querySelectorAll(".demo-chip").forEach((chip) => {
  chip.addEventListener("click", () => {
    document.getElementById("login-user").value = chip.dataset.user;
    loginPin.value = chip.dataset.pin;
    loginError.hidden = true;
  });
});

document.querySelectorAll(".nav__item").forEach((btn) => {
  btn.addEventListener("click", () => setView(btn.dataset.view));
});

logoutBtn.addEventListener("click", exitApp);

document.getElementById("borrow-grid").addEventListener("click", (e) => {
  const btn = e.target.closest("[data-borrow]");
  if (!btn || !aktifUye) return;
  const id = Number(btn.dataset.borrow);
  if (kitapOduncAl(aktifUye, id)) {
    refreshViews();
  }
});
