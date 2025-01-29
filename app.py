from flask import Flask, render_template, request
import fitz  # PyMuPDF para leitura de PDFs
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import os

app = Flask(__name__)

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
        result = f"Texto processado: {processed_text}"
    
    elif file:
        if file.filename.endswith(".txt"):
            file_content = file.read().decode("utf-8")
            processed_text = preprocess_text(file_content)
            result = f"Arquivo .txt processado: {processed_text}"
        
        elif file.filename.endswith(".pdf"):
            extracted_text = extract_text_from_pdf(file)
            if not extracted_text.strip():
                return render_template("index.html", error="Não foi possível extrair texto do PDF.")
            
            processed_text = preprocess_text(extracted_text)
            result = f"Arquivo PDF processado: {processed_text}"
        
        else:
            return render_template("index.html", error="Formato de arquivo não suportado.")
    
    else:
        return render_template("index.html", error="Nenhum texto ou arquivo foi enviado.")
    
    return render_template("result.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
