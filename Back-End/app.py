from flask import Flask, jsonify, request
from flask_cors import CORS
from chatbot import ask_bot
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return jsonify({"message": "Chatbot backend running"})


@app.route("/chat", methods=["POST"])
def chat():
    if request.is_json:
        user_msg = request.json.get("message")
    else:
        user_msg = request.form.get("message")

    reply = ask_bot(user_msg)
    return jsonify({"reply": reply})


@app.route("/upload", methods=["POST"])
def upload_pdf():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    from ingest import ingest_single_file
    ingest_single_file(filepath)

    return jsonify({"message": "PDF uploaded and ingested successfully"})


@app.route("/test")
def test_page():
    return """
    <h2>AI Academic Chatbot</h2>
    <form method="post" action="/chat">
        <input name="message" placeholder="Ask something..." style="width:300px;" />
        <button type="submit">Send</button>
    </form>
    """


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
