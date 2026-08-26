// ===== Le Bon VTC — interactions =====
(function () {
  "use strict";

  // Header au scroll
  var header = document.querySelector(".site-header");
  function onScroll() {
    if (window.scrollY > 30) header.classList.add("scrolled");
    else header.classList.remove("scrolled");
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // Menu mobile
  var toggle = document.querySelector(".nav-toggle");
  var links = document.querySelector(".nav-links");
  if (toggle && links) {
    toggle.addEventListener("click", function () {
      var open = links.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    links.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        links.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  // Année footer
  var y = document.getElementById("year");
  if (y) y.textContent = new Date().getFullYear();

  // Formulaire -> mailto (secours, pas de backend)
  var form = document.getElementById("booking-form");
  var status = document.getElementById("form-status");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var data = new FormData(form);
      var nom = (data.get("name") || "").toString().trim();
      var tel = (data.get("phone") || "").toString().trim();
      var mail = (data.get("email") || "").toString().trim();
      var veh = (data.get("vehicule") || "").toString();
      var date = (data.get("date") || "").toString();
      var msg = (data.get("message") || "").toString().trim();

      if (!nom || !tel) {
        status.textContent = "Merci de renseigner votre nom et téléphone.";
        return;
      }
      var subject = "Demande de course - Le Bon VTC (" + veh + ")";
      var body =
        "Nom : " + nom + "\n" +
        "Téléphone : " + tel + "\n" +
        "Email : " + mail + "\n" +
        "Catégorie : " + veh + "\n" +
        "Date & heure : " + date + "\n" +
        "Trajet : " + msg;
      var href = "mailto:lazeregg98@gmail.com?subject=" +
        encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
      window.location.href = href;
      status.textContent = "Ouverture de votre messagerie… (vous pouvez aussi nous appeler directement)";
    });
  }
})();
