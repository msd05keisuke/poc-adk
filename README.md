# poc-adk

Google ADK (Agent Development Kit) を使用して Vertex AI Search と Gemini を組み合わせた AI Agent を構築するプロジェクトです。

## 前提条件

- Vertex AI Search のデータストアが作成済みでデータが格納されていること

## 環境構築

### 1. uv のインストール

```bash
brew install uv
```

### 2. プロジェクトのクローン・セットアップ

```bash
# プロジェクトディレクトリに移動
cd /path/to/poc-adk

# Pythonの仮想環境とプロジェクトを初期化
uv sync
```

### 3. 依存関係のインストール

```bash
# 必要なパッケージを追加
uv add google-cloud-aiplatform[adk,agent_engines]
uv add python-dotenv
```

### 4. Google Cloud の認証設定

```bash
gcloud auth application-default login
```

### 5. 環境変数の設定

プロジェクトルートに `.env` ファイルを作成してください：

```bash
touch .env
```

`.env` ファイルの内容：

```properties
# Google Cloud プロジェクト設定
## 共通
GOOGLE_CLOUD_PROJECT="your-project-id"
GOOGLE_CLOUD_LOCATION="us-central1"
GOOGLE_GENAI_USE_VERTEXAI="True"

## Model
MODEL_NAME="gemini-2.0-flash-exp"

## Vertex AI Search
VAIS_LOCATION="global"
VAIS_COLLECTION="default_collection"
VAIS_DATA_STORE_ID="your-data-store-id"

## Deploy
STAGING_BUCKET="gs://your-bucket-name"

## Agent Engine (デプロイ後に設定)
AG_RESOURCE_PATH="projects/your-project-id/locations/your-location/reasoningEngines/your-reasoning-engine-id"
```

### 6. Vertex AI Search データストアの準備

1. [Google Cloud Console](https://console.cloud.google.com/) で Vertex AI Search にアクセス
2. 新しいデータストアを作成
3. データストア ID を `.env` ファイルの `VAIS_DATA_STORE_ID` に設定

## 使用方法

### ローカル

```bash
# ローカルのChat UIからエージェントを利用
adk web
```

### Agent Engine へのデプロイ

```bash
# Agent Engine にデプロイ
uv run python search_agent/deploy.py
```

### デプロイされた Agent の使用

```bash
# リモートAgentとの対話
uv run python search_agent/use_agent.py
```

## プロジェクト構造

```
poc-adk/
├── .env                    # 環境変数設定
├── .env.sample             # サンプル用環境変数設定
├── pyproject.toml         # プロジェクト設定
├── README.md              # このファイル
├── search_agent/          # AI Agent パッケージ
│   ├── __init__.py        # パッケージ初期化
│   ├── agent.py           # AI Agent 定義
│   ├── deploy.py          # デプロイスクリプト
│   └── use_agent.py       # Agent使用例
└── uv.lock               # 依存関係ロック
```

## 重要な注意事項

### 権限設定

Agent Engine にデプロイした際は、サービスエージェント（`xxx@gcp-sa-aiplatform-re.iam.gserviceaccount.com`）に以下の権限を付与してください：

- **Discovery Engine User** ロール
- **Vertex AI User** ロール

### セッション管理

Agent Engine は自動的にセッションを管理します。詳細は[公式ドキュメント](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/develop/adk?hl=ja)を参照してください。

## 開発コマンド

```bash
# 仮想環境の有効化
uv shell

# 依存関係の更新
uv sync

# 新しいパッケージの追加
uv add package-name

# 開発用パッケージの追加
uv add --dev package-name

# パッケージの削除
uv remove package-name

# Pythonスクリプトの実行
uv run python script.py
```

## トラブルシューティング

### よくある問題

1. **認証エラー**

   ```bash
   gcloud auth application-default login
   ```

2. **権限エラー**

   - プロジェクトの権限を確認
   - サービスエージェントの権限を確認

3. **データストアが見つからない**

   - `.env` ファイルの `VAIS_DATA_STORE_ID` を確認
   - データストアが正しく作成されているか確認

4. **モジュールが見つからない**
   ```bash
   uv sync
   ```

## 参考資料

- [Google ADK 公式ドキュメント](https://google.github.io/adk-docs/)
- [Vertex AI Search Built-in Tools](https://google.github.io/adk-docs/tools/built-in-tools/#vertex-ai-search)
- [ADK 日本語ドキュメント](https://zenn.dev/uxoxu/books/adk-docs-japanese/viewer/tools-built-in-tools#vertex-ai-%E3%82%B5%E3%83%BC%E3%83%81)
- [uv 公式ドキュメント](https://docs.astral.sh/uv/)
