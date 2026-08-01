(() => {
  "use strict";

  const STORAGE_KEY = "ziraat_bank_v1";

  const DEFAULT_USERS = [
    {
      musteri_id: 101,
      kullanici_id: "ahmet",
      pin: "1234",
      ad_soyad: "Ahmet Yılmaz",
      hesaplar: [
        {
          id: "vadesiz",
          ad: "Vadesiz TL Hesabı",
          tip: "vadesiz",
          iban: "TR33 0001 0001 2345 6789 1010 01",
          bakiye: 4500,
        },
        {
          id: "birikim",
          ad: "Birikim Hesabı",
          tip: "birikim",
          iban: "TR33 0001 0001 2345 6789 1010 02",
          bakiye: 1200,
        },
      ],
      gecmis: [
        { tip: "havale_in", tutar: 500, aciklama: "Havale alındı", hesap: "vadesiz", tarih: daysAgo(5) },
        { tip: "alisveris", tutar: -150, aciklama: "Market alışverişi", hesap: "vadesiz", tarih: daysAgo(3) },
      ],
    },
    {
      musteri_id: 102,
      kullanici_id: "ayşe",
      pin: "1234",
      ad_soyad: "Ayşe Çınar",
      hesaplar: [
        {
          id: "vadesiz",
          ad: "Vadesiz TL Hesabı",
          tip: "vadesiz",
          iban: "TR44 0001 0002 3456 7890 1020 01",
          bakiye: 1500,
        },
        {
          id: "birikim",
          ad: "Birikim Hesabı",
          tip: "birikim",
          iban: "TR44 0001 0002 3456 7890 1020 02",
          bakiye: 800,
        },
      ],
      gecmis: [
        { tip: "havale_in", tutar: 100, aciklama: "Havale alındı", hesap: "vadesiz", tarih: daysAgo(7) },
        { tip: "alisveris", tutar: -250, aciklama: "Market alışverişi", hesap: "vadesiz", tarih: daysAgo(2) },
      ],
    },
    {
      musteri_id: 103,
      kullanici_id: "mehmet",
      pin: "1234",
      ad_soyad: "Mehmet Yılmaz",
      hesaplar: [
        {
          id: "vadesiz",
          ad: "Vadesiz TL Hesabı",
          tip: "vadesiz",
          iban: "TR55 0001 0003 4567 8901 1030 01",
          bakiye: 12400,
        },
        {
          id: "birikim",
          ad: "Birikim Hesabı",
          tip: "birikim",
          iban: "TR55 0001 0003 4567 8901 1030 02",
          bakiye: 3500,
        },
      ],
      gecmis: [],
    },
  ];

  function daysAgo(n) {
    const d = new Date();
    d.setDate(d.getDate() - n);
    return d.toISOString();
  }

  function loadUsers() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) return JSON.parse(raw);
    } catch (_) { /* ignore */ }
    return structuredClone(DEFAULT_USERS);
  }

  function saveUsers(users) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(users));
  }

  let users = loadUsers();
  let aktif = null;
  let pendingConfirm = null;

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];

  const loginScreen = $("#login-screen");
  const appScreen = $("#app-screen");
  const toastEl = $("#toast");
  const modal = $("#modal");
  const sidebar = $(".sidebar");
  const sidebarOverlay = $("#sidebar-overlay");

  /* ---------- helpers ---------- */
  function formatMoney(n) {
    return (
      new Intl.NumberFormat("tr-TR", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      }).format(n) + " ₺"
    );
  }

  function formatDate(iso) {
    return new Intl.DateTimeFormat("tr-TR", {
      day: "2-digit",
      month: "short",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    }).format(new Date(iso));
  }

  function totalBalance(user) {
    return user.hesaplar.reduce((s, h) => s + h.bakiye, 0);
  }

  function getHesap(user, id) {
    return user.hesaplar.find((h) => h.id === id);
  }

  function findUser(kullaniciId) {
    return users.find((u) => u.kullanici_id === kullaniciId);
  }

  function refreshAktif() {
    if (!aktif) return;
    aktif = findUser(aktif.kullanici_id);
  }

  function showToast(msg, type = "ok") {
    toastEl.textContent = msg;
    toastEl.hidden = false;
    toastEl.className = `toast toast--${type} is-show`;
    clearTimeout(showToast._t);
    showToast._t = setTimeout(() => {
      toastEl.classList.remove("is-show");
      setTimeout(() => {
        toastEl.hidden = true;
      }, 250);
    }, 2800);
  }

  function openModal(title, body, onConfirm) {
    $("#modal-title").textContent = title;
    $("#modal-body").textContent = body;
    pendingConfirm = onConfirm;
    modal.hidden = false;
  }

  function closeModal() {
    modal.hidden = true;
    pendingConfirm = null;
  }

  function initials(name) {
    return name
      .split(" ")
      .map((p) => p[0])
      .slice(0, 2)
      .join("")
      .toUpperCase();
  }

  /* ---------- login ---------- */
  $("#login-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const user = $("#login-user").value.trim().toLowerCase();
    const pin = $("#login-pin").value.trim();
    const err = $("#login-error");

    const found = users.find(
      (u) => u.kullanici_id === user && u.pin === pin
    );

    if (!found) {
      err.textContent = "Kullanıcı adı veya şifre hatalı. Lütfen kontrol edin.";
      err.hidden = false;
      return;
    }

    err.hidden = true;
    aktif = found;
    enterApp();
  });

  $$(".demo-chip").forEach((btn) => {
    btn.addEventListener("click", () => {
      $("#login-user").value = btn.dataset.user;
      $("#login-pin").value = btn.dataset.pin;
      $("#login-error").hidden = true;
    });
  });

  $("#toggle-pin").addEventListener("click", () => {
    const input = $("#login-pin");
    input.type = input.type === "password" ? "text" : "password";
  });

  $("#logout-btn").addEventListener("click", () => {
    aktif = null;
    loginScreen.hidden = false;
    appScreen.hidden = true;
    $("#login-pin").value = "";
    closeSidebar();
  });

  /* ---------- navigation ---------- */
  function showView(name) {
    $$(".view").forEach((v) => v.classList.remove("is-visible"));
    $$(".nav__item").forEach((n) => n.classList.remove("is-active"));
    const view = $(`#view-${name}`);
    if (view) view.classList.add("is-visible");
    const nav = $(`.nav__item[data-view="${name}"]`);
    if (nav) nav.classList.add("is-active");
    closeSidebar();
    renderAll();
  }

  $$(".nav__item").forEach((btn) => {
    btn.addEventListener("click", () => showView(btn.dataset.view));
  });

  document.addEventListener("click", (e) => {
    const goto = e.target.closest("[data-goto]");
    if (goto) showView(goto.dataset.goto);
  });

  $("#menu-toggle").addEventListener("click", () => {
    sidebar.classList.add("is-open");
    sidebarOverlay.hidden = false;
  });

  function closeSidebar() {
    sidebar.classList.remove("is-open");
    sidebarOverlay.hidden = true;
  }

  sidebarOverlay.addEventListener("click", closeSidebar);

  /* ---------- render ---------- */
  function enterApp() {
    loginScreen.hidden = true;
    appScreen.hidden = false;
    const now = new Date();
    $("#today-date").textContent = new Intl.DateTimeFormat("tr-TR", {
      weekday: "long",
      day: "numeric",
      month: "long",
      year: "numeric",
    }).format(now);
    showView("dashboard");
  }

  function renderAll() {
    if (!aktif) return;
    refreshAktif();

    $("#greeting-text").textContent = `Hoş geldiniz, ${aktif.ad_soyad.split(" ")[0]}`;
    $("#user-name").textContent = aktif.ad_soyad;
    $("#user-id").textContent = `Müşteri No: ${aktif.musteri_id}`;
    $("#user-avatar").textContent = initials(aktif.ad_soyad);

    $("#total-balance").textContent = formatMoney(totalBalance(aktif));
    $("#account-count").textContent = `${aktif.hesaplar.length} hesap`;

    renderAccounts("#dashboard-accounts", true);
    renderAccountsFull();
    renderHistory("#dashboard-history", 5);
    renderHistory("#history-full", 50);
    fillAccountSelects();
    fillHavaleRecipients();
  }

  function renderAccounts(selector, compact) {
    const el = $(selector);
    if (!el) return;
    el.innerHTML = aktif.hesaplar
      .map(
        (h) => `
      <div class="account-row">
        <div class="account-row__icon ${h.tip === "birikim" ? "account-row__icon--savings" : ""}">
          ${h.tip === "birikim" ? "BK" : "TL"}
        </div>
        <div class="account-row__info">
          <p class="account-row__name">${h.ad}</p>
          <p class="account-row__iban">${h.iban}</p>
        </div>
        <p class="account-row__balance">${formatMoney(h.bakiye)}</p>
      </div>`
      )
      .join("");
  }

  function renderAccountsFull() {
    const el = $("#accounts-full");
    el.innerHTML = aktif.hesaplar
      .map(
        (h) => `
      <article class="account-card ${h.tip === "birikim" ? "account-card--savings" : ""}">
        <p class="account-card__type">${h.tip === "birikim" ? "Birikim" : "Vadesiz"}</p>
        <p class="account-card__name">${h.ad}</p>
        <p class="account-card__balance">${formatMoney(h.bakiye)}</p>
        <p class="account-card__iban">${h.iban}</p>
      </article>`
      )
      .join("");
  }

  function txMeta(tx) {
    const labels = {
      havale_in: "Gelen Havale",
      havale_out: "Giden Havale",
      transfer: "Hesaplar Arası",
      cekme: "Para Çekme",
      yatirma: "Para Yatırma",
      alisveris: "Alışveriş",
    };
    return labels[tx.tip] || tx.aciklama;
  }

  function renderHistory(selector, limit) {
    const el = $(selector);
    if (!el) return;
    const list = [...aktif.gecmis].reverse().slice(0, limit);

    if (!list.length) {
      el.innerHTML = `<p class="tx-empty">Henüz işlem bulunmuyor.</p>`;
      return;
    }

    el.innerHTML = list
      .map((tx) => {
        const isIn = tx.tutar > 0;
        return `
        <div class="tx-item">
          <div class="tx-item__icon ${isIn ? "tx-item__icon--in" : "tx-item__icon--out"}">
            ${isIn ? "↓" : "↑"}
          </div>
          <div class="tx-item__info">
            <p class="tx-item__title">${tx.aciklama || txMeta(tx)}</p>
            <p class="tx-item__meta">${txMeta(tx)} · ${formatDate(tx.tarih)}</p>
          </div>
          <p class="tx-item__amount ${isIn ? "tx-item__amount--in" : "tx-item__amount--out"}">
            ${isIn ? "+" : ""}${formatMoney(tx.tutar)}
          </p>
        </div>`;
      })
      .join("");
  }

  function fillSelect(sel, accounts, excludeId) {
    const list = excludeId
      ? accounts.filter((h) => h.id !== excludeId)
      : accounts;
    sel.innerHTML = list
      .map(
        (h) =>
          `<option value="${h.id}">${h.ad} — ${formatMoney(h.bakiye)}</option>`
      )
      .join("");
  }

  function fillAccountSelects() {
    [
      "#havale-from",
      "#transfer-from",
      "#transfer-to",
      "#withdraw-account",
      "#deposit-account",
    ].forEach((id) => {
      const sel = $(id);
      if (sel) fillSelect(sel, aktif.hesaplar);
    });

    const from = $("#transfer-from");
    const to = $("#transfer-to");
    if (from && to && from.value === to.value && aktif.hesaplar.length > 1) {
      to.value = aktif.hesaplar.find((h) => h.id !== from.value)?.id || to.value;
    }
  }

  function fillHavaleRecipients() {
    const sel = $("#havale-to");
    const others = users.filter((u) => u.kullanici_id !== aktif.kullanici_id);
    sel.innerHTML = others
      .map(
        (u) =>
          `<option value="${u.kullanici_id}">${u.ad_soyad} (${u.musteri_id})</option>`
      )
      .join("");
    updateHavaleToAccounts();
  }

  function updateHavaleToAccounts() {
    const toUser = findUser($("#havale-to").value);
    const sel = $("#havale-to-account");
    if (!toUser) {
      sel.innerHTML = "";
      return;
    }
    fillSelect(sel, toUser.hesaplar);
  }

  $("#havale-to").addEventListener("change", updateHavaleToAccounts);

  /* ---------- amount chips ---------- */
  document.addEventListener("click", (e) => {
    const chip = e.target.closest(".amount-chip");
    if (!chip) return;
    const form = chip.closest("form");
    const input = form?.querySelector('input[type="number"]');
    if (input) {
      input.value = chip.dataset.amount;
      input.focus();
    }
  });

  /* ---------- swap accounts ---------- */
  $("#swap-accounts").addEventListener("click", () => {
    const from = $("#transfer-from");
    const to = $("#transfer-to");
    const tmp = from.value;
    from.value = to.value;
    to.value = tmp;
  });

  /* ---------- transactions ---------- */
  function addTx(user, tx) {
    user.gecmis.push({ ...tx, tarih: new Date().toISOString() });
  }

  function parseAmount(el) {
    const n = parseFloat(el.value);
    return Number.isFinite(n) ? Math.round(n * 100) / 100 : NaN;
  }

  $("#havale-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const fromId = $("#havale-from").value;
    const toUserId = $("#havale-to").value;
    const toAccId = $("#havale-to-account").value;
    const amount = parseAmount($("#havale-amount"));
    const note = $("#havale-note").value.trim() || "Havale";

    const fromHesap = getHesap(aktif, fromId);
    const alici = findUser(toUserId);
    const toHesap = getHesap(alici, toAccId);

    if (!amount || amount <= 0) {
      showToast("Geçersiz tutar girdiniz.", "err");
      return;
    }
    if (amount > fromHesap.bakiye) {
      showToast("Yetersiz bakiye.", "err");
      return;
    }

    openModal(
      "Havale Onayı",
      `${formatMoney(amount)} tutarını ${alici.ad_soyad} adlı müşteriye göndermek istediğinize emin misiniz?`,
      () => {
        fromHesap.bakiye -= amount;
        toHesap.bakiye += amount;

        addTx(aktif, {
          tip: "havale_out",
          tutar: -amount,
          aciklama: `${note} → ${alici.ad_soyad}`,
          hesap: fromId,
        });
        addTx(alici, {
          tip: "havale_in",
          tutar: amount,
          aciklama: `${note} ← ${aktif.ad_soyad}`,
          hesap: toAccId,
        });

        saveUsers(users);
        $("#havale-amount").value = "";
        $("#havale-note").value = "";
        closeModal();
        showToast(`Havale başarılı: ${formatMoney(amount)} gönderildi.`);
        renderAll();
      }
    );
  });

  $("#transfer-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const fromId = $("#transfer-from").value;
    const toId = $("#transfer-to").value;
    const amount = parseAmount($("#transfer-amount"));

    if (fromId === toId) {
      showToast("Kaynak ve hedef hesap aynı olamaz.", "err");
      return;
    }
    if (!amount || amount <= 0) {
      showToast("Geçersiz tutar girdiniz.", "err");
      return;
    }

    const fromHesap = getHesap(aktif, fromId);
    const toHesap = getHesap(aktif, toId);

    if (amount > fromHesap.bakiye) {
      showToast("Yetersiz bakiye.", "err");
      return;
    }

    openModal(
      "Transfer Onayı",
      `${formatMoney(amount)} tutarını ${fromHesap.ad} hesabından ${toHesap.ad} hesabına aktarmak istiyor musunuz?`,
      () => {
        fromHesap.bakiye -= amount;
        toHesap.bakiye += amount;
        addTx(aktif, {
          tip: "transfer",
          tutar: -amount,
          aciklama: `${fromHesap.ad} → ${toHesap.ad}`,
          hesap: fromId,
        });
        addTx(aktif, {
          tip: "transfer",
          tutar: amount,
          aciklama: `${toHesap.ad} ← ${fromHesap.ad}`,
          hesap: toId,
        });
        saveUsers(users);
        $("#transfer-amount").value = "";
        closeModal();
        showToast("Hesaplar arası transfer tamamlandı.");
        renderAll();
      }
    );
  });

  $("#withdraw-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const accId = $("#withdraw-account").value;
    const amount = parseAmount($("#withdraw-amount"));
    const hesap = getHesap(aktif, accId);

    if (!amount || amount <= 0) {
      showToast("Geçersiz tutar girdiniz.", "err");
      return;
    }
    if (amount > hesap.bakiye) {
      showToast("Yetersiz bakiye.", "err");
      return;
    }

    openModal(
      "Para Çekme Onayı",
      `${hesap.ad} hesabından ${formatMoney(amount)} çekmek istediğinize emin misiniz?`,
      () => {
        hesap.bakiye -= amount;
        addTx(aktif, {
          tip: "cekme",
          tutar: -amount,
          aciklama: "ATM / Şube para çekme",
          hesap: accId,
        });
        saveUsers(users);
        $("#withdraw-amount").value = "";
        closeModal();
        showToast(`${formatMoney(amount)} çekildi.`);
        renderAll();
      }
    );
  });

  $("#deposit-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const accId = $("#deposit-account").value;
    const amount = parseAmount($("#deposit-amount"));
    const hesap = getHesap(aktif, accId);

    if (!amount || amount <= 0) {
      showToast("Geçersiz tutar girdiniz.", "err");
      return;
    }

    openModal(
      "Para Yatırma Onayı",
      `${hesap.ad} hesabına ${formatMoney(amount)} yatırmak istediğinize emin misiniz?`,
      () => {
        hesap.bakiye += amount;
        addTx(aktif, {
          tip: "yatirma",
          tutar: amount,
          aciklama: "Para yatırma",
          hesap: accId,
        });
        saveUsers(users);
        $("#deposit-amount").value = "";
        closeModal();
        showToast(`${formatMoney(amount)} yatırıldı.`);
        renderAll();
      }
    );
  });

  /* ---------- modal ---------- */
  $("#modal-confirm").addEventListener("click", () => {
    if (typeof pendingConfirm === "function") pendingConfirm();
  });

  $$("[data-close-modal]").forEach((el) => {
    el.addEventListener("click", closeModal);
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      closeModal();
      closeSidebar();
    }
  });
})();
