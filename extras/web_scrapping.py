# INSTALANDO A APLICAÇÃO:
# python3 -m venv venv
# source venv/bin/activate
# pip install requests beautifulsoup4

import requests
from bs4 import BeautifulSoup

# CLASSES -----------------------------------------------
# Definição da Classe Notícia
class Noticia:
    def __init__(self, titulo, link):
        self.titulo = titulo
        self.link = link


# FUNÇÕES E VARIÁVEIS ------------------------------------
def getNoticias(busca = None):
    url = "https://www.r7.com/"
    response = requests.get(url)
    html = BeautifulSoup(response.text, 'html.parser')
    noticias = []

    for card in html.select('.card-font-primary'):
        a_tag = card.find('a')
        if a_tag and a_tag.has_attr('href'):
            titulo = a_tag.get_text().strip()
            link = a_tag['href']
            if(busca is None or busca.lower() in titulo.lower()):
                noticias.append(Noticia(titulo, link))
    return noticias



noticias = getNoticias('brasil')
print("Títulos encontrados:\n")
for i, noticia in enumerate(noticias, 1):
    print(f"{i:02d}. {noticia.titulo}")
    print(f"{noticia.link}\n")