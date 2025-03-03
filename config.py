"""
グラフテキスト化アプリの設定モジュール
"""

import os
from dotenv import load_dotenv

# .env ファイルから環境変数を読み込む
load_dotenv()

# アプリケーション設定
APP_TITLE = "グラフテキスト化アプリ"
APP_ICON = "📊"
APP_VERSION = "1.0.0"

# APIの設定
DEFAULT_API_TYPE = "gemini"  # デフォルトのAPI種類
ALLOWED_API_TYPES = ["gemini", "mock (APIなし)"]

# APIキー（環境変数から読み込み）
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# モデル設定
GEMINI_MODEL = "gemini-pro-vision"

# ファイルアップロード設定
ALLOWED_UPLOAD_EXTENSIONS = ["csv", "xlsx", "xls"]
ALLOWED_IMAGE_EXTENSIONS = ["png", "jpg", "jpeg"]
MAX_UPLOAD_SIZE_MB = 200  # 最大アップロードサイズ（MB）

# グラフ設定
GRAPH_TYPES = [
    "折れ線グラフ", 
    "棒グラフ", 
    "散布図", 
    "円グラフ", 
    "ヒストグラム", 
    "箱ひげ図", 
    "ヒートマップ"
]

GRAPH_STYLES = [
    "default", 
    "seaborn-v0_8", 
    "ggplot", 
    "dark_background", 
    "bmh", 
    "classic"
]

DEFAULT_GRAPH_WIDTH = 10
DEFAULT_GRAPH_HEIGHT = 6

# 要約設定
SUMMARY_DETAIL_LEVELS = ["簡潔", "標準", "詳細"]
DEFAULT_DETAIL_LEVEL = "標準"

# 言語設定
SUPPORTED_LANGUAGES = ["日本語", "English"]
DEFAULT_LANGUAGE = "日本語"

# プロンプト設定
SUMMARY_PROMPT_TEMPLATE = """
このグラフについて{language}で説明してください。

{detail_instructions}

グラフから読み取れる情報:
- 全体的なトレンド
- 最大値と最小値
- 特徴的なパターンや異常値
- データが示唆する洞察

追加情報: {additional_context}
"""

DETAIL_INSTRUCTIONS = {
    "簡潔": "要点のみを箇条書きで簡潔に説明してください。",
    "標準": "主要なトレンドと注目すべきポイントを含めて要約してください。",
    "詳細": "詳細な分析を提供し、考えられる要因や背景情報も含めて説明してください。"
}