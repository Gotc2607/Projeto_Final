function toggleMenu() {
    const menu = document.getElementById("menu");
    menu.style.display = menu.style.display === "none" ? "block" : "none";
  }

  function goToPayment() {
    window.location.href = "/fatura"; // Simulação de redirecionamento
  }
  function goToinvest() {
    window.location.href = "/investimentos"; // Simulação de redirecionamento
  }