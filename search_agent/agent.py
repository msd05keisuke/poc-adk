import os

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools import VertexAiSearchTool

# .envファイルから環境変数を読み込み（プロジェクトルートの.envファイルを指定）
load_dotenv(
    dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
)

# 環境変数から設定値を取得
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
VAIS_LOCATION = os.getenv("VAIS_LOCATION", "global")
VAIS_COLLECTION = os.getenv("VAIS_COLLECTION", "default_collection")
VAIS_DATA_STORE_ID = os.getenv("VAIS_DATA_STORE_ID")
MODEL_NAME = os.getenv("MODEL_NAME")

# 必須の環境変数をチェック
if not GOOGLE_CLOUD_PROJECT or not VAIS_DATA_STORE_ID:
    raise ValueError("GOOGLE_CLOUD_PROJECT and DATA_STORE_ID must be set in .env file")

# data_store_idの完全なパスを構築
full_data_store_id = f"projects/{GOOGLE_CLOUD_PROJECT}/locations/{VAIS_LOCATION}/collections/{VAIS_COLLECTION}/dataStores/{VAIS_DATA_STORE_ID}"

vertex_ai_search_tool = VertexAiSearchTool(
    data_store_id=full_data_store_id,
    max_results=3,
)

root_agent = LlmAgent(
    model=MODEL_NAME,  # Required: Specify the LLM
    name="search_agent",  # Required: Unique agent name
    instruction=f"""あなたは、ドキュメントストア「{VAIS_DATA_STORE_ID}」にある情報をもとに質問に答えるアシスタントです。
    回答する前に、検索ツールを使って関連情報を見つけてください。
    答えがドキュメントにない場合は、情報が見つからなかったと言ってください。
    """,
    description="特定のVertex AI Searchデータストアを使用して質問に回答します。",
    tools=[vertex_ai_search_tool],  # Provide an instance of the tool
)
