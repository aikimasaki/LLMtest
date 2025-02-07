# import openai
# import os
# import json
# from flask import Blueprint, request, jsonify, session
# from werkzeug.utils import secure_filename
# from config import OPENAI_API_KEY

# # Flask Blueprint 設定
# finetune_bp = Blueprint("finetune", __name__, url_prefix="/finetune")
# client = openai.OpenAI(api_key=OPENAI_API_KEY)

# # アップロードフォルダ設定
# UPLOAD_FOLDER = "static/uploads"
# ALLOWED_EXTENSIONS = {"json", "jsonl"}
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # Flask セッションの初期化
# def get_finetune_id():
#     return session.get("current_finetune_id")

# def set_finetune_id(finetune_id):
#     session["current_finetune_id"] = finetune_id

# def allowed_file(filename):
#     return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# # 📌 1. データアップロードエンドポイント
# @finetune_bp.route("/upload", methods=["POST"])
# def upload_file():
#     if "file" not in request.files:
#         return jsonify({"error": "ファイルが選択されていません"}), 400

#     file = request.files["file"]
#     if file.filename == "":
#         return jsonify({"error": "ファイルが選択されていません"}), 400

#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file_path = os.path.join(UPLOAD_FOLDER, filename)
#         file.save(file_path)

#         # `.json` を `.jsonl` に変換（必要なら）
#         if filename.endswith(".json"):
#             jsonl_path = convert_json_to_jsonl(file_path)
#             file_path = jsonl_path  # 変換後のファイルを使用

#         return jsonify({"message": "ファイルアップロード成功", "file_path": file_path})

#     return jsonify({"error": "許可されていないファイル形式"}), 400

# def convert_json_to_jsonl(json_path):
#     """JSON ファイルを JSONL に変換"""
#     jsonl_path = json_path.replace(".json", ".jsonl")
#     with open(json_path, "r", encoding="utf-8") as json_file, open(jsonl_path, "w", encoding="utf-8") as jsonl_file:
#         data = json.load(json_file)
#         for item in data:
#             jsonl_file.write(json.dumps(item) + "\n")
#     return jsonl_path

# # 📌 2. ファインチューニング開始エンドポイント
# @finetune_bp.route("/start", methods=["POST"])
# def start_finetune():
#     file_path = request.json.get("file_path")

#     if not file_path or not os.path.exists(file_path):
#         return jsonify({"error": "ファイルが存在しません"}), 400

#     try:
#         response = client.fine_tuning.jobs.create(training_file=file_path, model="gpt-3.5-turbo")
#         set_finetune_id(response.id)
#         return jsonify({"message": "ファインチューニング開始", "fine_tune_id": response.id})

#     except openai.OpenAIError as e:
#         return jsonify({"error": f"OpenAI API エラー: {str(e)}"}), 500

# # 📌 3. ファインチューニングのステータス確認エンドポイント
# @finetune_bp.route("/status", methods=["GET"])
# def finetune_status():
#     fine_tune_id = get_finetune_id()

#     if not fine_tune_id:
#         return jsonify({"error": "現在進行中のファインチューニングはありません"}), 400

#     try:
#         job_status = client.fine_tuning.jobs.retrieve(fine_tune_id)
#         return jsonify({
#             "fine_tune_id": fine_tune_id,
#             "status": job_status.status,
#             "fine_tuned_model": job_status.fine_tuned_model,
#             "created_at": job_status.created_at,
#             "completed_at": job_status.completed_at
#         })

#     except openai.OpenAIError as e:
#         return jsonify({"error": f"OpenAI API エラー: {str(e)}"}), 500
    






# import openai
# import os
# import json
# from flask import Blueprint, request, jsonify, session
# from werkzeug.utils import secure_filename
# from config import OPENAI_API_KEY

# # Flask Blueprint 設定
# finetune_bp = Blueprint("finetune", __name__, url_prefix="/finetune")
# client = openai.OpenAI(api_key=OPENAI_API_KEY)

# # アップロードフォルダ設定
# UPLOAD_FOLDER = "static/uploads"
# ALLOWED_EXTENSIONS = {"jsonl"}
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # セッション管理（ファインチューニングID）
# def get_finetune_id():
#     return session.get("current_finetune_id")

# def set_finetune_id(finetune_id):
#     session["current_finetune_id"] = finetune_id

# def allowed_file(filename):
#     """ 許可されたファイル形式をチェック """
#     return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# # 📌 1. データアップロード & OpenAI へのファイル登録
# @finetune_bp.route("/upload", methods=["POST"])
# def upload_file():
#     if "file" not in request.files:
#         return jsonify({"error": "ファイルが選択されていません"}), 400

#     file = request.files["file"]
#     if file.filename == "":
#         return jsonify({"error": "ファイルが選択されていません"}), 400

#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file_path = os.path.join(UPLOAD_FOLDER, filename)
#         file.save(file_path)

#         try:
#             with open(file_path, "rb") as f:
#                 response = client.files.create(file=f, purpose="fine-tune")

#             file_id = response.id  # OpenAI の `file_id` を取得

#             return jsonify({"message": "ファイルアップロード成功", "file_id": file_id})

#         except openai.OpenAIError as e:
#             return jsonify({"error": f"OpenAI API エラー（ファイル登録失敗）: {str(e)}"}), 500

#     return jsonify({"error": "許可されていないファイル形式（.jsonlのみ許可）"}), 400

# # 📌 2. ファインチューニング開始エンドポイント
# @finetune_bp.route("/start", methods=["POST"])
# def start_finetune():
#     data = request.get_json()
#     file_id = data.get("file_id")  # `file_path` ではなく `file_id` を使用

#     if not file_id:
#         return jsonify({"error": "ファイルIDが指定されていません"}), 400

#     try:
#         response = client.fine_tuning.jobs.create(training_file=file_id, model="gpt-3.5-turbo")
#         set_finetune_id(response.id)

#         return jsonify({"message": "ファインチューニング開始", "fine_tune_id": response.id})

#     except openai.OpenAIError as e:
#         return jsonify({"error": f"OpenAI API エラー: {str(e)}"}), 500

# # 📌 3. ファインチューニングのステータス確認エンドポイント
# @finetune_bp.route("/status", methods=["GET"])
# def finetune_status():
#     fine_tune_id = get_finetune_id()

#     if not fine_tune_id:
#         return jsonify({"error": "現在進行中のファインチューニングはありません"}), 400

#     try:
#         job_status = client.fine_tuning.jobs.retrieve(fine_tune_id)

#         return jsonify({
#             "fine_tune_id": fine_tune_id,
#             "status": job_status.status,
#             "fine_tuned_model": job_status.fine_tuned_model,
#             "created_at": job_status.created_at,
#             "completed_at": job_status.completed_at
#         })

#     except openai.OpenAIError as e:
#         return jsonify({"error": f"OpenAI API エラー: {str(e)}"}), 500
    

import openai
import os
import json
from flask import Blueprint, request, jsonify, session
from werkzeug.utils import secure_filename
from config import OPENAI_API_KEY

# Flask Blueprint 設定
finetune_bp = Blueprint("finetune", __name__, url_prefix="/finetune")
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# アップロードフォルダ設定
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"jsonl"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# セッション管理（ファインチューニングID）
def get_finetune_id():
    return session.get("current_finetune_id")

def set_finetune_id(finetune_id):
    session["current_finetune_id"] = finetune_id

def allowed_file(filename):
    """ 許可されたファイル形式をチェック """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# 📌 1. データアップロード & OpenAI へのファイル登録
@finetune_bp.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "ファイルが選択されていません"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "ファイルが選択されていません"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        try:
            with open(file_path, "rb") as f:
                response = client.files.create(file=f, purpose="fine-tune")

            file_id = response.id  # OpenAI の `file_id` を取得

            return jsonify({"message": "ファイルアップロード成功", "file_id": file_id})

        except openai.OpenAIError as e:
            return jsonify({"error": f"OpenAI API エラー（ファイル登録失敗）: {str(e)}"}), 500

    return jsonify({"error": "許可されていないファイル形式（.jsonlのみ許可）"}), 400

# 📌 2. ファインチューニング開始エンドポイント
@finetune_bp.route("/start", methods=["POST"])
def start_finetune():
    data = request.get_json()
    file_id = data.get("file_id")  # `file_path` ではなく `file_id` を使用

    if not file_id:
        return jsonify({"error": "ファイルIDが指定されていません"}), 400

    try:
        response = client.fine_tuning.jobs.create(training_file=file_id, model="gpt-3.5-turbo")
        set_finetune_id(response.id)
        return jsonify({"message": "ファインチューニング開始", "fine_tune_id": response.id})

    except openai.OpenAIError as e:
        return jsonify({"error": f"OpenAI API エラー: {str(e)}"}), 500

# 📌 3. ファインチューニングのステータス確認エンドポイント
@finetune_bp.route("/status", methods=["GET"])
def finetune_status():
    fine_tune_id = get_finetune_id()

    if not fine_tune_id:
        return jsonify({"error": "現在進行中のファインチューニングはありません"}), 400

    try:
        job_status = client.fine_tuning.jobs.retrieve(fine_tune_id)

        # `completed_at` が存在しない場合は None として返す
        completed_at = getattr(job_status, "completed_at", None)

        return jsonify({
            "fine_tune_id": fine_tune_id,
            "status": job_status.status,
            "fine_tuned_model": job_status.fine_tuned_model,
            "created_at": job_status.created_at,
            "completed_at": completed_at
        })

    except openai.OpenAIError as e:
        return jsonify({"error": f"OpenAI API エラー: {str(e)}"}), 500