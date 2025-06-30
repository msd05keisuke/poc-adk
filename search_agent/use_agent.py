import os

from dotenv import load_dotenv
from vertexai import agent_engines

# .envファイルから環境変数を読み込み
load_dotenv(
    dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
)

# 環境変数から設定値を取得
AG_RESOURCE_PATH = os.getenv("AG_RESOURCE_PATH")

remote_agent = agent_engines.get(AG_RESOURCE_PATH)

user_id = "hoge"
session = remote_agent.create_session(user_id=user_id)


for event in remote_agent.stream_query(
    user_id=user_id,
    session_id=session["id"],
    message="あなたの役割を教えてください。",
):
    print(event)
