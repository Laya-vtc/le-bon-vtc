// Année footer
document.getElementById('year').textContent = new Date().getFullYear();

// Menu mobile
const toggle = document.querySelector('.nav-toggle');
const links = document.querySelector('.nav-links');
if (toggle && links) {
  toggle.addEventListener('click', () => {
    const open = links.classList.toggle('open');
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  links.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => {
      links.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
    });
  });
}

// Formulaire : validation simple + message (sans backend, on confirme localement)
const form = document.getElementById('booking-form');
const status = document.getElementById('form-status');
if (form) {
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const name = form.name.value.trim();
    const phone = form.phone.value.trim();
    const email = form.email.value.trim();
    if (!name || !phone || !email) {
      status.textContent = 'Merci de remplir le nom, le téléphone et l\'email.';
      status.className = 'form-status err';
      return;
    }
    status.textContent = 'Merci ' + name + ' ! Votre demande est prise en compte, nous vous recontactons rapidement.';
    status.className = 'form-status ok';
    form.reset();
  });
}
