# Documentation Helper Llamaindex

Este projeto é um RAG com a documentação do Llamaindex.


[RAG](https://github.com/user-attachments/assets/e80822c2-981f-4e1f-bfa1-cf17c4a201d9)


## Instalação

### Instale o Poetry

Para instalar o Poetry, execute o seguinte comando no seu terminal:

```sh
curl -sSL https://install.python-poetry.org | python3 -
```

Claro! Aqui está a seção adicional para o README com instruções sobre como usar o `pyenv` para configurar a versão do Python 3.12.4:

---

### Configuração da Versão do Python com Pyenv

Se você precisa usar uma versão específica do Python, como a 3.12.4, recomendamos o uso do [pyenv](https://github.com/pyenv/pyenv) para gerenciar múltiplas versões do Python no seu sistema.

#### 1. Instale o Pyenv

Para instalar o `pyenv`, execute os seguintes comandos:

```bash
# Clona o repositório do pyenv no seu diretório home
curl https://pyenv.run | bash

# Adiciona pyenv ao caminho e inicializa, caso use zsh, escreva em **~/.zshrc**
echo -e '\n# Pyenv' >> ~/.bashrc
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
source ~/.bashrc
```

#### 2. Instale a Versão do Python 3.12.4

Use o `pyenv` para instalar a versão 3.12.4 do Python:

```bash
pyenv install 3.12.4
```

#### 3. Defina a Versão do Python no Projeto

Para começar, clone o repositório do projeto:

```bash
git clone https://github.com/seu-usuario/documentation-helper-llamaindex.git
cd documentation-helper-llamaindex
```

```bash
pyenv local 3.12.4
```

#### 4. Verifique a Versão do Python

Certifique-se de que a versão correta do Python está sendo usada:

```bash
python --version
```

Isso deve retornar `Python 3.12.4`.

Agora você está pronto para seguir com a instalação das dependências e a configuração do Poetry conforme descrito nas seções anteriores.

### Configurar o Poetry para criar ambientes virtuais no projeto

Abra seu terminal e configure o Poetry para criar ambientes virtuais dentro do projeto:

```sh
poetry config virtualenvs.in-project true
```

Executar o python do ambiente virtual:

```sh
poetry config virtualenvs.prefer-active-python true
```

### Ativar o ambiente virtual

Após a instalação do Poetry, ative o ambiente virtual:

```sh
poetry shell
```

### Verificar ambiente 

```sh
poetry env list
```
Deve Imprimir:

```
.venv (Activated)
```

### Instalar as dependências do projeto

Instale as dependências necessárias:

```sh
poetry add requests beautifulsoup4 llama-index openai python-dotenv pinecone-client llama-index-vector-stores-pinecone unstructured streamlit
```

Instale as dependências de desenvolvimento:

```sh
poetry --group dev add ignr black
```

### Dependências

Aqui está a lista de dependências definidas no `pyproject.toml`:

```toml
[tool.poetry.dependencies]
python = ">=3.12,<3.13"
requests = "^2.32.3"
beautifulsoup4 = "^4.12.3"
llama-index = "^0.10.59"
openai = "^1.38.0"
python-dotenv = "^1.0.1"
pinecone-client = "^5.0.1"
llama-index-vector-stores-pinecone = "^0.1.9"
unstructured = "^0.15.0"
streamlit = "^1.37.1"

[tool.poetry.group.dev.dependencies]
ignr = "^2.2"
black = "^24.8.0"
```

## Configuração do Pinecone

Para configurar o Pinecone, acesse [Pinecone](https://app.pinecone.io/) e obtenha sua chave de API e o nome do índice.

Crie um arquivo `.env` na raiz do projeto e adicione as seguintes variáveis:

```env
OPENAI_API_KEY=
PINECONE_API_KEY=
PINECONE_INDEX_NAME=
```

Preencha os valores das variáveis com suas respectivas chaves de API e nome do índice.

## Baixar a documentação

Execute o script `download_docs.py` para fazer o download da documentação em HTML:

```sh
python download_docs.py
```

## Ingestão dos documentos

Para rodar o arquivo `ingest.py`, execute o seguinte comando:

```sh
python ingest.py
```

## Rodar o Streamlit

Para rodar a aplicação Streamlit, execute:

```sh
streamlit run app.py
```

---

Este README deve fornecer todas as instruções necessárias para configurar e executar o projeto `Documentation Helper Llamaindex`.
