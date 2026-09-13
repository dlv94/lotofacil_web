# Gerador de Jogos da Lotofácil — versão web

Esta versão substitui a interface Tkinter por uma aplicação web em **Flask**, mantendo as regras de validação, geração aleatória de jogos únicos e exportação para Excel. O sistema funciona em computador e celular por meio do navegador.

## Executar localmente

No terminal, dentro desta pasta:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Depois, acesse `http://127.0.0.1:5000`.

## Publicar no PythonAnywhere

1. Crie uma aplicação web do tipo **Flask** usando Python 3.10 ou mais recente.
2. Envie todos os arquivos desta pasta para um diretório, por exemplo `/home/SEU_USUARIO/lotofacil`.
3. Abra um console Bash e instale as dependências no virtualenv configurado para a aplicação:

```bash
cd /home/SEU_USUARIO/lotofacil
pip install --user -r requirements.txt
```

Se você usar um virtualenv no PythonAnywhere, instale com o caminho do Python desse ambiente:

```bash
/home/SEU_USUARIO/.virtualenvs/lotofacil/bin/pip install -r requirements.txt
```

4. Na aba **Web**, informe o diretório do código-fonte e abra o arquivo WSGI. Deixe o conteúdo semelhante a:

```python
import sys
path = '/home/SEU_USUARIO/lotofacil'
if path not in sys.path:
    sys.path.append(path)

from app import application
```

5. Se estiver usando virtualenv, informe-o na seção **Virtualenv** da aba Web.
6. Clique em **Reload** e acesse a URL da aplicação.

## Observações

A chave `SECRET_KEY` em `app.py` deve ser substituída por uma sequência aleatória antes da publicação. O sistema não persiste configurações ou resultados em banco de dados: cada geração é independente e a planilha é baixada diretamente pelo navegador.

Os arquivos antigos da interface desktop foram mantidos para referência, mas o ponto de entrada da versão web é `app.py`. O prazo de expiração que existia no `main.py` desktop não foi levado para o sistema web, pois criava uma interrupção automática da aplicação sem relação com a hospedagem.
