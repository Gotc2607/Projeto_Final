function toggleMenu() {
    const menu = document.getElementById("menu");
    menu.style.display = menu.style.display === "none" ? "block" : "none";
  }

  function goToPayment_fatura() {
    window.location.href = "/pagar_fatura"; 
  }
  function goToCard() {
    window.location.href = "/cartão"; 
  }
  function goToinvest() {
    window.location.href = "/investimentos"; 
  }