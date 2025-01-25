<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bem vindo</title>
    <link rel="stylesheet" href="../../static/css/style_usuario.css?v={{time}}">
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

    </div>

    <div class="operacoes">
    

    </div>
    
  <script src="../../static/js/usuario.js"></script>  
</body>
</html>