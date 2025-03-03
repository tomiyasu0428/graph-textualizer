"""
グラフテキスト化アプリのAPI接続モジュール
"""

import os
import config
from utils import fig_to_image, create_mock_summary


class GeminiAPIClient:
    """GeminiモデルAPIクライアント"""
    
    def __init__(self, api_key=None):
        """
        初期化関数
        
        Parameters:
        -----------
        api_key : str, optional
            使用するAPIのキー
        """
        self.api_key = api_key if api_key else config.GEMINI_API_KEY
        self.client = None
        self.setup_api()
        
    def setup_api(self):
        """APIの設定"""
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self.genai = genai
            self.model = genai.GenerativeModel(config.GEMINI_MODEL)
        except ImportError:
            raise ImportError("google-generativeai パッケージが必要です。pip install google-generativeai を実行してください。")
    
    def get_summary_prompt(self, additional_context="", detail_level="標準", language="日本語"):
        """
        要約用のプロンプトを生成
        
        Parameters:
        -----------
        additional_context : str
            追加のコンテキスト情報
        detail_level : str
            要約の詳細レベル ('簡潔', '標準', '詳細')
        language : str
            言語設定 ('日本語', 'English')
            
        Returns:
        --------
        prompt : str
            生成されたプロンプト
        """
        detail_instructions = config.DETAIL_INSTRUCTIONS.get(detail_level, config.DETAIL_INSTRUCTIONS["標準"])
        
        lang = "日本語" if language == "日本語" else "English"
        
        prompt = config.SUMMARY_PROMPT_TEMPLATE.format(
            language=lang,
            detail_instructions=detail_instructions,
            additional_context=additional_context
        )
        
        return prompt
    
    def summarize_graph(self, fig, additional_context="", detail_level="標準", language="日本語"):
        """
        グラフを言語化して要約する
        
        Parameters:
        -----------
        fig : matplotlib.figure.Figure
            要約するグラフ
        additional_context : str
            追加のコンテキスト情報
        detail_level : str
            要約の詳細レベル ('簡潔', '標準', '詳細')
        language : str
            言語設定 ('日本語', 'English')
            
        Returns:
        --------
        summary : str
            グラフの言語化された要約
        insights : list
            主要な洞察のリスト
        """
        # グラフをイメージに変換
        img = fig_to_image(fig)
        
        # プロンプトの作成
        prompt = self.get_summary_prompt(
            additional_context=additional_context,
            detail_level=detail_level,
            language=language
        )
        
        # APIによる要約の取得
        response = self.model.generate_content([prompt, img])
        summary = response.text
        
        # 主要な洞察を抽出
        insights = self.extract_insights(summary, language)
        
        return summary, insights
    
    def extract_insights(self, summary, language="日本語"):
        """
        要約から主要な洞察を抽出する
        
        Parameters:
        -----------
        summary : str
            グラフの要約テキスト
        language : str
            言語設定 ('日本語', 'English')
            
        Returns:
        --------
        insights : list
            主要な洞察のリスト
        """
        prompt = ""
        if language == "日本語":
            prompt = f"""
            以下のグラフ要約から主要な洞察やポイントを5つ抽出してください。
            各洞察は簡潔で、データに基づいた事実を述べるものにしてください。
            
            グラフ要約:
            {summary}
            """
        else:
            prompt = f"""
            Extract 5 key insights or points from the following graph summary.
            Each insight should be concise and state facts based on the data.
            
            Graph summary:
            {summary}
            """
        
        model = self.genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        insights_text = response.text
        
        # 洞察を行ごとに分割
        insights = insights_text.split('\n')
        
        # 番号や箇条書き記号を削除
        insights = [i.strip().lstrip('1234567890.-• ') for i in insights if i.strip()]
        
        # 最大5つまでに制限
        return insights[:5]


class MockAPIClient:
    """モックAPIクライアント (APIなしでテスト用)"""
    
    def __init__(self):
        """初期化関数"""
        pass
        
    def summarize_graph(self, fig, additional_context="", detail_level="標準", language="日本語"):
        """
        グラフを言語化して要約する (モック)
        
        Parameters:
        -----------
        fig : matplotlib.figure.Figure
            要約するグラフ
        additional_context : str
            追加のコンテキスト情報
        detail_level : str
            要約の詳細レベル ('簡潔', '標準', '詳細')
        language : str
            言語設定 ('日本語', 'English')
            
        Returns:
        --------
        summary : str
            グラフの言語化された要約 (モック)
        insights : list
            主要な洞察のリスト (モック)
        """
        # グラフの種類を推定（モック用）
        graph_type = "折れ線グラフ"  # デフォルト値
        
        if hasattr(fig, 'get_axes') and fig.get_axes():
            ax = fig.get_axes()[0]
            if ax.has_data():
                lines = len(ax.get_lines())
                bars = len([c for c in ax.get_children() if str(c).startswith('<BarContainer')])
                if bars > 0:
                    graph_type = "棒グラフ"
                elif lines > 0:
                    graph_type = "折れ線グラフ"
        
        # モック要約を生成
        summary, insights = create_mock_summary(graph_type)
        
        return summary, insights


def get_api_client(api_type, api_key=None):
    """
    APIタイプに基づいてAPIクライアントを取得
    
    Parameters:
    -----------
    api_type : str
        使用するAPIの種類 ('gemini' or 'mock (APIなし)')
    api_key : str, optional
        使用するAPIのキー
        
    Returns:
    --------
    client : GeminiAPIClient or MockAPIClient
        選択されたAPIクライアント
    """
    if api_type == "gemini":
        return GeminiAPIClient(api_key)
    elif api_type == "mock (APIなし)":
        return MockAPIClient()
    else:
        raise ValueError(f"サポートされていないAPIタイプ: {api_type}")
