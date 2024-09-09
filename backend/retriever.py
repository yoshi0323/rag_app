import openai
import requests
import os
from dotenv import load_dotenv  # 環境変数をロード

# .env ファイルを読み込む
load_dotenv()

# Azure OpenAI APIキーとエンドポイントの設定
API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "8ef432a7466249f8b47bbfd578d88885")
ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "https://myapp0323.openai.azure.com/")

# Azure OpenAIのAPIキーとエンドポイントを設定
openai.api_type = "azure"
openai.api_key = API_KEY
openai.api_base = ENDPOINT
openai.api_version = "2023-05-15"  # APIバージョンを指定

# ナレッジベースURLの定義
KNOWLEDGE_BASE_URL = "https://iyashitour.com/meigen/theme/life"

def load_documents():
    """ナレッジベースの内容を取得してドキュメントに変換"""
    try:
        response = requests.get(KNOWLEDGE_BASE_URL)
        response.raise_for_status()  # エラーチェック
    except requests.exceptions.RequestException as e:
        print(f"Error fetching documents: {e}")
        return []
    
    content = response.text
    return content

async def get_response(question):
    """Azure OpenAI Serviceを使用して質問に対する回答を生成する"""
    # ドキュメントのロード
    documents = load_documents()
    if not documents:
        return "ドキュメントの読み込みに失敗しました。"

    # モデルにクエリを送信
    try:
        response = openai.ChatCompletion.create(
            engine="gpt-35-turbo",  # 使用するAzureのモデルエンジンを指定
            messages=[
                {"role": "system", "content": "あなたは名言を教えるアシスタントです。"},
                {"role": "user", "content": question},
            ],
            max_tokens=150,
            temperature=0.7,
        )
        answer = response.choices[0].message["content"].strip()
    except Exception as e:
        answer = f"Azure OpenAI APIリクエストでエラーが発生しました: {e}"

    return answer
