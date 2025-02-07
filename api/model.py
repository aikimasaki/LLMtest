from flask import Blueprint, request, jsonify

model_bp = Blueprint("model", __name__)

available_models = ["gpt-3.5-turbo", "gpt-4"]
current_model = available_models[0]

@model_bp.route("/switch_model", methods=["POST"])
def switch_model():
    global current_model

    data = request.get_json()
    new_model = data.get("model")

    if new_model not in available_models:
        return jsonify({"error": "無効なモデルです"}), 400

    current_model = new_model
    return jsonify({"message": f"モデルが {current_model} に変更されました", "current_model": current_model})
