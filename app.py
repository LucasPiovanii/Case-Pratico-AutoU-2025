from flask import Flask, render_template, request
import fitz  # PyMuPDF para leitura de PDFs
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

# Função para extrair texto de PDFs
def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")  # Lê o arquivo diretamente do stream
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text.strip()

# Função de pré-processamento de NLP
def preprocess_text(text):
    stop_words = set(stopwords.words("portuguese"))  # Usar stopwords em português
    lemmatizer = WordNetLemmatizer()
    
    tokens = word_tokenize(text.lower())  # Tokeniza e coloca tudo em minúsculo
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word.isalnum() and word not in stop_words]
    
    return " ".join(tokens)

def classify_text(text):
    prompt = f"""Classifique o seguinte e-mail em "Produtivo" ou "Improdutivo" com base na seguinte definição:

    **Categorias**:
    - **Produtivo**: E-mails que requerem uma ação ou resposta específica (ex.: solicitações de suporte técnico, atualização sobre casos em aberto, dúvidas sobre o sistema).
    - **Improdutivo**: E-mails que não necessitam de uma ação imediata (ex.: mensagens de felicitações, agradecimentos).

    **Texto do e-mail:**
    {text}

    Retorne apenas "Produtivo" ou "Improdutivo", sem explicações adicionais.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Ou "gpt-3.5-turbo" se quiser algo mais barato
        messages=[{"role": "system", "content": "Você é um assistente que classifica e-mails."},
                  {"role": "user", "content": prompt}],
        temperature=0  # Define a saída mais determinística
    )

    classification = response["choices"][0]["message"]["content"].strip()
    return classification  # Retorna "Produtivo" ou "Improdutivo"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    user_text = request.form.get("text_input")
    file = request.files.get("file_input")
    
    if user_text and file:
        return render_template("index.html", error="Por favor, envie apenas texto OU arquivo.")
    
    if user_text:
        processed_text = preprocess_text(user_text)
        classification = classify_text(processed_text)
        result = f"Texto processado: {processed_text}\nClassificação: {classification}"
    
    elif file:
        if file.filename.endswith(".txt"):
            file_content = file.read().decode("utf-8")
            processed_text = preprocess_text(file_content)
            classification = classify_text(processed_text)
            result = f"Arquivo .txt processado: {processed_text}\nClassificação: {classification}"
        
        elif file.filename.endswith(".pdf"):
            extracted_text = extract_text_from_pdf(file)
            if not extracted_text.strip():
                return render_template("index.html", error="Não foi possível extrair texto do PDF.")
            
            processed_text = preprocess_text(extracted_text)
            classification = classify_text(processed_text)
            result = f"Arquivo PDF processado: {processed_text}\nClassificação: {classification}"
        
        else:
            return render_template("index.html", error="Formato de arquivo não suportado.")
    
    else:
        return render_template("index.html", error="Nenhum texto ou arquivo foi enviado.")
    
    return render_template("result.html", result=processed_text, classification=classification)

if __name__ == "__main__":
    app.run(debug=True)