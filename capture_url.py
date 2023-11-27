from selenium import webdriver
from bs4 import BeautifulSoup
import re

# Configurando o WebDriver (use o driver específico para o seu navegador)
driver = webdriver.Chrome()
driver.get('https://appexchange.salesforce.com/appxStore?type=App')

url_of_app = ''
list_urls = []

# Obtendo o conteúdo da página com BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')
# Define a regex para encontrar as tags <style> e <script>
regex_style = re.compile(r'<style.*?</style>', re.DOTALL)
regex_script = re.compile(r'<script.*?</script>', re.DOTALL)

# Nome do arquivo de saída
output_file_name = 'html_content.txt'

# Iterar sobre cada caractere e armazenar no arquivo
with open(output_file_name, 'w', encoding='utf-8') as output_file:
    for char in str(soup):
        output_file.write(char)

print(f'Conteúdo HTML foi salvo em {output_file_name}')

# Nome do arquivo de entrada
input_file_name = 'html_content.txt'
stage = 0
# Iterar sobre cada caractere do arquivo
with open(input_file_name, 'r', encoding='utf-8') as input_file:
    for char in input_file.read():

        if   stage == 0: stage = (0 if char != 'l' else 1)
        elif stage == 1: stage = (0 if char != '=' else 2)
        elif stage == 2: stage = (0 if char != '"' else 3)
        elif stage == 3: stage = (0 if char != 'h' else 4)
        elif stage == 4:
            if char != '"':
                 url_of_app += char
            else:
                list_urls.append(f'h{url_of_app}')
                url_of_app = ''
                stage = 0        

print(list_urls)



# Feche o navegador no final
driver.quit()
