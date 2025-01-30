# Case-Pratico-AutoU-2025

## Descrição: 
Repositório que contém o código fonte para solução do desafio proposto para vaga de estagiário na empresa AutoU.
A solução apresentada se baseou na utilização do Google Gemini como LLM para classificação de emails (anexados como .pdf ou .txt ou escritos manualmente) entre produtivos ou improdutivos, bem como para a geração de uma resposta recomendada para o email.

## Candidato:
Lucas Piovani Ferreira
- lucaspiovani1004@gmail.com
- (19)99531-6349

## Diretório
```bash
/project
  ├── static
  │     └── index.css
  │     └── result.css
  ├── templates
  │     └── index.html
  │     └── result.html
  └── app.py
```

## Execução local

Para rodar a aplicação localmente, siga os seguintes passos:

### 1. Criação do Ambiente Virtual
É recomendável criar um ambiente virtual para isolar as dependências:

```bash
python3 -m venv venv
source venv/bin/activate  # Para macOS/Linux
venv\Scripts\activate     # Para Windows
```

### 2. Instalação das Dependências

Instale as dependências do projeto a partir do arquivo requirements.txt

```bash
pip install -r requirements.txt
```

As dependências incluem:
- Flask: Framework para a criação da aplicação web.
- PyMuPDF (fitz): Para manipulação de arquivos PDF.
- nltk: Biblioteca para processamento de linguagem natural.
- google-generativeai: Biblioteca para interação com a API do Google Gemini.

### 3. Configuração da API do Google Gemini

Por fim, vá até o site do Google AI Studio (https://aistudio.google.com/u/2/apikey?pli=1), crie sua API-KEY e a insira na linha 12 do arquivo app.py.

```bash
genai.configure(api_key="SUA-API-KEY")
```

### 4. Execução da Aplicação

Após a configuração, execute a aplicação com o comando:

```bash
python3 app.py
```

A aplicação estará disponível em http://127.0.0.1:5000