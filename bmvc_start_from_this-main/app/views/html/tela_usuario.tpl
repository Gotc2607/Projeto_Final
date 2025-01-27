<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bem vindo</title>
    <link rel="stylesheet" href="../../static/css/style_usuario.css?v={{time}}">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
</head>
<body>

    <div class="top-bar">

        <div class="user-info">
          <img src="../../static/img/logo-noxus.jpg" alt="Foto do usuário">
          <span>{{usuario}}</span>
        </div>

        <button class="menu-button" onclick="toggleMenu()">☰</button>

    </div>
    <div class="menu" id="menu">
        <a href="">Meu perfil</a>
        <a href="">Configurações</a>
        <a href="/login">Logout</a>
    </div>

    <div class="saldo">

      <h1>R${{saldo}}</h1>

    </div>

    <div class="operations">
      
      <div class="operation">
        <div>
          <i class="fas fa-money-bill-wave" style="color: black; font-size: 30px;"></i>
        </div>
        <a href="/deposito">Depósito</a>
      </div>
      
      <div class="operation">
        <div class="fas fa-file-alt" style="font-size: 30px;" ></div>
        <div class="operation-label">Extrato</div>
      </div>

      <div class="operation">
        <div class="operation-icon"></div>
        <div class="operation-label">Transferência</div>
      </div>

      <div class="operation">
        <div class="fas fa-file-invoice-dollar" style="font-size: 30px;"></div>
        <div class="operation-label">Pagamento</div>
      </div>

      <div class="operation">
        <div class="material-icons">credit_card</div>
        <div class="operation-label">Investir</div>
      </div>
    </div>

    <div class="Blocks">
      <div class="credit-card-info">
        <h3>Cartão de Crédito</h3>
        <span>Fatura Atual: R$ {{fatura}}</span>
      </div>
  
      <div class="credit-card-arrow" onclick="goToPayment()"> > </div>

  <script src="../../static/js/usuario.js"></script>  
</body>
</html>