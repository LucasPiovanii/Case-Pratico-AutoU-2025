from flask import Flask, render_template, request
import fitz # PyMuPDF
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import google.generativeai as genai

app = Flask(__name__)

# Configurar a API do Google Gemini
genai.configure(api_key="SUA_API_KEY")

# Função para extrair texto de PDFs com PyMuPDF
def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf") # Lê o arquivo diretamente do stream
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text.strip()

# Função de pré-processamento de NLP
def preprocess_text(text):
    nltk.download("stopwords") # Para stop words
    nltk.download("punkt") # Para tokenização
    nltk.download("wordnet") # Para lematização

    stop_words = set(stopwords.words("portuguese")) # Stopwords em português
    lemmatizer = WordNetLemmatizer()
    
    tokens = word_tokenize(text.lower()) # Tokeniza e coloca em minúsculo
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word.isalnum() and word not in stop_words]
    
    return " ".join(tokens)

# Função para classificar o texto usando Google Gemini
def classify_text_with_gemini(text):
    model = genai.GenerativeModel("gemini-pro")
    
    prompt = f"""
    Você é um assistente que classifica emails e mensagens como 'Produtivo' ou 'Improdutivo'.
    
    - **Produtivo:** Mensagens que requerem uma ação ou resposta específica. Exemplos:
      - Solicitação de suporte técnico.
      - Atualização sobre um caso em aberto.
      - Dúvidas sobre o sistema ou processos internos.
      - Pedidos que necessitam de uma resposta clara.

    - **Improdutivo:** Mensagens que não exigem ação imediata. Exemplos:
      - Felicitações, parabéns, saudações.
      - Agradecimentos simples que não exigem resposta.
      - Mensagens informativas sem necessidade de ação.

    Leia a seguinte mensagem e classifique-a como **'Produtivo'** ou **'Improdutivo'**:

    --- 
    {text}
    ---

    Responda apenas com 'Produtivo' ou 'Improdutivo'.
    """
    
    response = model.generate_content(prompt)
    return response.text.strip()

def generate_response_with_gemini(text, classification):
    model = genai.GenerativeModel("gemini-pro")

    prompt = f"""
    Você é um assistente que gera respostas automáticas para emails e mensagens.

    - **Se a mensagem for 'Produtivo'**, gere uma resposta clara, educada e objetiva, ajudando o remetente com o que for necessário.
    - **Se a mensagem for 'Improdutivo'**, responda de forma educada, mas breve, evitando prolongar a conversa sem necessidade.

    **Mensagem recebida:**  
    {text}

    **Classificação:** {classification}

    Gere uma resposta adequada para essa mensagem.
    """

    response = model.generate_content(prompt)
    return response.text.strip()

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
        classification = classify_text_with_gemini(processed_text)
        response = generate_response_with_gemini(processed_text, classification)
        result = f"Texto processado: {processed_text}"
    
    elif file:
        if file.filename.endswith(".txt"):
            file_content = file.read().decode("utf-8")
            processed_text = preprocess_text(file_content)
            classification = classify_text_with_gemini(processed_text)
            response = generate_response_with_gemini(processed_text, classification)
            result = f"Arquivo .txt processado: {processed_text}"
        
        elif file.filename.endswith(".pdf"):
            extracted_text = extract_text_from_pdf(file)
            if not extracted_text.strip():
                return render_template("index.html", error="Não foi possível extrair texto do PDF.")
            
            processed_text = preprocess_text(extracted_text)
            classification = classify_text_with_gemini(processed_text)
            response = generate_response_with_gemini(processed_text, classification)
            result = f"Arquivo PDF processado: {processed_text}"
        
        else:
            return render_template("index.html", error="Formato de arquivo não suportado.")
    
    else:
        return render_template("index.html", error="Nenhum texto ou arquivo foi enviado.")
    
    return render_template("result.html", result=result, classification=classification, response=response)

if __name__ == "__main__":
    app.run(debug=True)
