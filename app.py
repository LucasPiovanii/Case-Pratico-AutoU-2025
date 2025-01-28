from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    # Verifica se o usuário enviou texto ou arquivo
    user_text = request.form.get("text_input")
    file = request.files.get("file_input")
    
    if user_text and file:
        return render_template("index.html", error="Por favor, envie apenas texto OU arquivo.")
    
    if user_text:
        result = f"Texto recebido: {user_text}"
    elif file:
        if file.filename.endswith(".txt"):
            result = f"Arquivo recebido: {file.filename}"
        elif file.filename.endswith(".pdf"):
            result = f"Arquivo PDF recebido: {file.filename}"
        else:
            return render_template("index.html", error="Formato de arquivo não suportado.")
    else:
        return render_template("index.html", error="Nenhum texto ou arquivo foi enviado.")
    
    # Renderiza a nova página com o resultado
    return render_template("result.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
