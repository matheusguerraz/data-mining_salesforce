import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re

# Configurando o WebDriver (use o driver específico para o seu navegador)
driver = webdriver.Chrome()
driver.get('https://appexchange.salesforce.com/appxStore?type=App')

# Set a limit for requests (avoids getting stuck in the loop)
iterations_limit = 161

# Lista para armazenar URLs já coletadas
collected_urls = []

def scrape():
    global collected_urls
    url_of_app = ''
    new_urls = []

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
            if stage == 0:
                stage = 1 if char == 'l' else 0
            elif stage == 1:
                stage = 2 if char == '=' else 0
            elif stage == 2:
                stage = 3 if char == '"' else 0
            elif stage == 3:
                stage = 4 if char == 'h' else 0
            elif stage == 4:
                if char != '"':
                    url_of_app += char
                else:
                    full_url = f'h{url_of_app}'
                    # Verifique se a URL já foi coletada anteriormente
                    if full_url not in collected_urls:
                        new_urls.append(full_url)
                        collected_urls.append(full_url)
                    url_of_app = ''
                    stage = 0

    # Retorne apenas as novas URLs coletadas nesta iteração
    return new_urls

# Nome do arquivo Excel
excel_file_name = 'output_urls.xlsx'

# Loop para clicar no botão "Ver Mais" enquanto ele estiver presente
for _ in range(iterations_limit):
    try:
        # Espera até que o botão "Ver Mais" esteja visível na página
        ver_mais_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//span[text()="Show More"]'))
        )
        
        # Rola a página para tornar o botão visível
        driver.execute_script("arguments[0].scrollIntoView();", ver_mais_button)
        
        # Clique no botão "Ver Mais" usando JavaScript
        driver.execute_script("arguments[0].click();", ver_mais_button)

        # Espera explícita para garantir que a nova página seja carregada
        WebDriverWait(driver, 10).until(
            EC.staleness_of(ver_mais_button)
        )
        
        # Realize o scrape após clicar no botão 'Show More'
        new_urls = scrape()
        
        # Faça algo com as novas URLs, por exemplo, imprimir
        print(f"Novas URLs coletadas: {new_urls}")

    except Exception as e:
        # Se ocorrer algum erro (por exemplo, se o botão não estiver mais presente), pare o loop
        print(f"Erro: {e}")
        break

# Cria um DataFrame com todas as URLs coletadas
df = pd.DataFrame(collected_urls, columns=['URLs'])

# Salva o DataFrame no arquivo Excel
df.to_excel(excel_file_name, index=False)

# Feche o navegador no final
driver.quit()
