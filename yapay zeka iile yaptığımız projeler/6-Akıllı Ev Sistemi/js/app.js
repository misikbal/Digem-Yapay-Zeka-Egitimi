const yanginAlarmi = document.getElementById('yangin-alarmi');
const evdeInsan = document.getElementById('evde-insan');
const odaSicakligi = document.getElementById('oda-sicakligi');
const tempValue = document.getElementById('temp-value');
const tempGaugeFill = document.getElementById('temp-gauge-fill');
const statusPanel = document.getElementById('status-panel');
const statusIcon = document.getElementById('status-icon');
const statusMessage = document.getElementById('status-message');
const alarmCard = document.getElementById('alarm-card');

const devices = {
  klima: document.getElementById('device-klima'),
  kombi: document.getElementById('device-kombi'),
  fiskiye: document.getElementById('device-fiskiye'),
  eko: document.getElementById('device-eko'),
};

function setDevice(name, active) {
  const el = devices[name];
  el.dataset.active = active ? 'true' : 'false';
  el.querySelector('.device__state').textContent = active ? 'Açık' : 'Kapalı';
}

function updateClock() {
  const now = new Date();
  document.getElementById('clock').textContent = now.toLocaleTimeString('tr-TR', {
    hour: '2-digit',
    minute: '2-digit',
  });
}

function updateTemperatureDisplay(temp) {
  tempValue.textContent = temp;
  const percent = ((temp - 10) / 35) * 100;
  tempGaugeFill.style.width = `${percent}%`;

  if (temp > 25) {
    tempValue.style.color = 'var(--hot)';
  } else if (temp < 18) {
    tempValue.style.color = 'var(--cold)';
  } else {
    tempValue.style.color = 'var(--success)';
  }
}

function guncelleSistem() {
  const alarmAktif = yanginAlarmi.checked;
  const insanVar = evdeInsan.checked;
  const sicaklik = Number(odaSicakligi.value);

  yanginAlarmi.closest('.toggle').querySelector('.toggle__label').textContent =
    alarmAktif ? 'Alarm Açık' : 'Alarm Kapalı';
  evdeInsan.closest('.toggle').querySelector('.toggle__label').textContent =
    insanVar ? 'Evde İnsan Var' : 'Ev Boş';

  alarmCard.classList.toggle('card--active', alarmAktif);
  updateTemperatureDisplay(sicaklik);

  setDevice('klima', false);
  setDevice('kombi', false);
  setDevice('fiskiye', false);
  setDevice('eko', false);

  statusPanel.className = 'status-panel';

  if (alarmAktif) {
    statusPanel.classList.add('status-panel--danger');
    statusIcon.textContent = '🚨';
    statusMessage.textContent =
      'Yangın alarmı aktif. Fıskiyeler çalıştırılıyor. İtfaiyeye haber veriliyor.';
    setDevice('fiskiye', true);
    return;
  }

  if (!insanVar) {
    statusPanel.classList.add('status-panel--warning');
    statusIcon.textContent = '🌿';
    statusMessage.textContent = 'Eko Mod açıldı (Enerji Modu Aktif)';
    setDevice('eko', true);
    return;
  }

  if (sicaklik > 25) {
    statusPanel.classList.add('status-panel--warning');
    statusIcon.textContent = '❄️';
    statusMessage.textContent = 'Klimalar çalıştırılıyor.';
    setDevice('klima', true);
  } else if (sicaklik < 18) {
    statusPanel.classList.add('status-panel--warning');
    statusIcon.textContent = '♨️';
    statusMessage.textContent = 'Kombi çalıştırılıyor.';
    setDevice('kombi', true);
  } else {
    statusIcon.textContent = '✓';
    statusMessage.textContent =
      'Konfor mod çalıştırıldı (Klima ve Kombi Açık Değil)';
  }
}

[yanginAlarmi, evdeInsan, odaSicakligi].forEach((el) => {
  el.addEventListener('input', guncelleSistem);
  el.addEventListener('change', guncelleSistem);
});

updateClock();
setInterval(updateClock, 1000);
guncelleSistem();
