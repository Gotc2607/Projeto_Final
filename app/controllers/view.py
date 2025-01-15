from bottle import template


class Application():

    def __init__(self):
        self.pages = {
            'index' : self.index

        }

    def render(self,page):
        #"""Método que recebe o nome da página e renderiza a página correspondente"""
         #Procura a função associada à página ou retorna a função helper por padrão
       content = self.pages.get(page, self.index)
       return content()


    def index(self):
        #renderiza a pagina index
        return template('app/views/html/index')

