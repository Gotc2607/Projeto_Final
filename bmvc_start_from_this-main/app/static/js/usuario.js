function toggleMenu() {
    const menu = document.getElementById("menu");
    menu.style.display = menu.style.display === "none" ? "block" : "none";
  }

  function goToPayment() {
    alert("Redirecionando para a página de pagamento..."); // Aqui você pode usar "window.location.href" para ir a outra página
    window.location.href = "/pagar-fatura"; // Simulação de redirecionamento
  }