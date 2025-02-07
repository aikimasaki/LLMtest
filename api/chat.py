import openai
from flask import Blueprint, request, jsonify
from config import OPENAI_API_KEY

chat_bp = Blueprint("chat", __name__)
client = openai.OpenAI(api_key=OPENAI_API_KEY)

chat_history = []
current_model = "gpt-3.5-turbo"  # デフォルトモデル

@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "メッセージが空です"}), 400

    chat_history.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model=current_model,
            messages=chat_history
        )

        bot_message = response.choices[0].message.content
        chat_history.append({"role": "assistant", "content": bot_message})

        return jsonify({"response": bot_message})

    except openai.OpenAIError as e:
        return jsonify({"error": f"OpenAI API エラー: {str(e)}"}), 500
