import requests
from pathlib import Path


# web.antaq.gov.br/Sistemas/ArquivosAnuario/Arquivos/2019TemposAtracacao.zip
# web.antaq.gov.br/Sistemas/ArquivosAnuario/Arquivos/2019Atracacao.zip
# web.antaq.gov.br/Sistemas/ArquivosAnuario/Arquivos/2019Carga.zip

request = requests.get('http://web.antaq.gov.br/Sistemas/ArquivosAnuario/Arquivos/2019Atracacao.zip')
status = request.status_code
print(status)

total_tries = 0
max_tries = 20
'''
while status != 200 and total_tries < max_tries:
    print('Retrying download, total tries: ', total_tries)
    request = requests.get('http://web.antaq.gov.br/Sistemas/ArquivosAnuario/Arquivos/2019Atracacao.zip')
    status = request.status_code
    total_tries += 1
    t.sleep(5)
'''
if status == 200:
    filename = 'teste.zip'
    open(Path('.') / filename, 'wb').write(request.content)
