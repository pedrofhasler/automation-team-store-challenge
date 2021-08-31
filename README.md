# Automation Challenge

## A aplicação

Desenvolvido um site para mostrar ao usuário as ofertas de outlet no site da Dafiti separado pelas marcas. 

Foram retirados alguns produtos do site apartir de web scraping, utilizando BeatifulSoup e requests, e adicionados no banco de dados apartir de um arquivo csv. A extração dos dos dados foi feita para pegar qualquer seja o tipo dos produtos, porém, foi criado um filtro para separá-los em suas marcas/brand visando a proporcionar o usuário a escolher a que mais o/a agrada

# Primeiros Passos

Instale o docker e escreva esses 3 comandos no terminal 

- Clone o repositório
- `docker-compose build`
- `docker-compose up`

Após esses comandos a API já deve estar funcional e rodando.

Agora você pode ir para http://localhost:8000 para ver o site ou http://localhost:8000/admin/ para entrar como administrador do site

## Stack

### Frontend 

- bootstrap

###  Backend

- pytest
- Docker
- Django
- Postgre SQL
- pandas

## Deploy no Heroku

Irei deixar um superuser criado para testes

Login:admin
Password:admin
