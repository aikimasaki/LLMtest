
function switchModel() {
    const selectedModel = document.getElementById("model-selector").value;

    fetch("/switch_model", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ model: selectedModel })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => console.error("モデル切り替えエラー:", error));
}

function sendMessage() {
    const messageInput = document.getElementById("message");
    const chatBox = document.getElementById("chat-box");
    const userMessage = messageInput.value.trim();

    if (!userMessage) return; // 空のメッセージは送信しない

    // ユーザーのメッセージをチャットボックスに追加
    chatBox.innerHTML += `<div class="chat-message user-message">${userMessage}</div>`;
    chatBox.scrollTop = chatBox.scrollHeight; // スクロールを最下部へ
    messageInput.value = ""; // 入力欄をクリア

    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage })
    })
    .then(response => response.json())
    .then(data => {
        // AI のメッセージをチャットボックスに追加
        chatBox.innerHTML += `<div class="chat-message bot-message">${data.response}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight; // スクロールを最下部へ
    })
    .catch(error => console.error("エラー:", error));
}

let uploadedFileId = ""; // OpenAI の file_id を保存
let fineTuneInterval; // ステータスチェック用のインターバル

function uploadFile() {
    const fileInput = document.getElementById("file-upload");
    const file = fileInput.files[0];

    if (!file) {
        alert("ファイルを選択してください！");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    fetch("/finetune/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.file_id) {
            uploadedFileId = data.file_id;
            alert("ファイルアップロード成功！ OpenAI File ID: " + uploadedFileId);
        } else {
            alert("アップロードエラー: " + data.error);
        }
    })
    .catch(error => console.error("アップロードエラー:", error));
}

function startFineTune() {
    if (!uploadedFileId) {
        alert("ファイルをアップロードしてください！");
        return;
    }

    fetch("/finetune/start", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ file_id: uploadedFileId }) // `file_id` を使用
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        checkFineTuneStatus(); // ステータス確認を開始
    })
    .catch(error => console.error("ファインチューニングエラー:", error));
}

function checkFineTuneStatus() {
    clearInterval(fineTuneInterval); // 既存のインターバルをクリア
    fineTuneInterval = setInterval(() => {
        fetch("/finetune/status")
        .then(response => response.json())
        .then(data => {
            const statusText = document.getElementById("fine-tune-status");
            const progressBar = document.getElementById("fine-tune-progress");

            if (data.status === "running") {
                statusText.innerText = "ステータス: 進行中...";
                progressBar.style.width = "50%";
                progressBar.innerText = "50%";
                progressBar.classList.add("bg-warning");
            } else if (data.status === "succeeded") {
                statusText.innerText = "ステータス: 完了 ✅";
                progressBar.style.width = "100%";
                progressBar.innerText = "100%";
                progressBar.classList.remove("bg-warning");
                progressBar.classList.add("bg-success");
                clearInterval(fineTuneInterval);
            } else if (data.status === "failed") {
                statusText.innerText = "ステータス: 失敗 ❌";
                progressBar.style.width = "100%";
                progressBar.innerText = "エラー";
                progressBar.classList.remove("bg-warning");
                progressBar.classList.add("bg-danger");
                clearInterval(fineTuneInterval);
            }
        })
        .catch(error => {
            console.error("ステータス取得エラー:", error);
            clearInterval(fineTuneInterval);
        });
    }, 5000); // 5秒ごとに更新
}