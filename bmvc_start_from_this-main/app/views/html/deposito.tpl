<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tela de depósito</title>
    <link rel="stylesheet" href="../../static/css/style_operacoes.css">
</head>
<body class="body">
    
    <div class="container-operacoes">

        <img src="../../static/img/logo-noxus.jpg" alt="">
            
        <h3>Depósito {{usuario}}</h3>

        <form action="/deposito" method="POST">
            <input type="text" name="valor" placeholder="Valor do depósito:">
            <input type="password" name="senha" placeholder="confirme sua senha:">
            <input type="submit" value="Depositar">
        </form>

        <a href="/tela_usuario">Voltar</a>
    </div>
</body>
</html>