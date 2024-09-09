from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from retriever import get_response  # retriever.pyからget_response関数をインポート

app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 必要に応じて特定のオリジンを指定
    allow_credentials=True,
    allow_methods=["*"],  # 必要に応じて許可するメソッドを指定
    allow_headers=["*"],
)

# リクエストデータのモデル定義
class Query(BaseModel):
    question: str

@app.get("/")
async def root():
    return {"message": "Welcome to the RAG Chatbot API"}

@app.post("/ask")
async def ask_question(query: Query):
    try:
        # クエリをログに記録
        print(f"Received question: {query.question}")

        # 回答を取得（非同期で実行）
        response = await get_response(query.question)
        
        # 応答をログに記録
        print(f"Generated answer: {response}")

        return {"answer": response}
    
    except Exception as e:
        # より詳細なエラー情報をログに記録
        print(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
