
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from perguntar import responder

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
CORS(app)


@app.route("/")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/api/perguntar", methods=["POST"])
def api_perguntar():
    dados = request.get_json(silent=True) or {}
    pergunta = (dados.get("pergunta") or "").strip()

    if not pergunta:
        return jsonify({"erro": "Envie uma pergunta no campo 'pergunta'."}), 400

    try:
        resposta = responder(pergunta)
        return jsonify({"resposta": resposta})
    except Exception as e:
        print(f"Erro ao processar pergunta: {e}")
        return jsonify({"erro": "Não foi possível processar sua pergunta agora. Tente novamente."}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
