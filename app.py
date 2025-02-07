from flask import Flask, render_template, session
from api.chat import chat_bp
from api.finetune import finetune_bp
from api.model import model_bp

app = Flask(__name__)
app.secret_key = "your_secret_key"  # セッション管理のためのキー

# 各APIを登録
app.register_blueprint(chat_bp)
app.register_blueprint(finetune_bp)  # `/finetune/...` のエンドポイントが競合しないよう修正
app.register_blueprint(model_bp)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/finetune")
def finetune_page():
    return render_template("finetune.html")

if __name__ == "__main__":
    app.run(debug=True, port=5001)
