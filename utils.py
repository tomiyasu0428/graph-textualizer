"""
グラフテキスト化アプリのユーティリティ関数
"""

import io
import base64
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import tempfile
import os
import requests
from PIL import Image
from urllib.parse import urlparse


def load_data_from_file(uploaded_file):
    """
    アップロードされたファイルからデータを読み込む
    
    Parameters:
    -----------
    uploaded_file : UploadedFile
        Streamlitでアップロードされたファイルオブジェクト
        
    Returns:
    --------
    pandas.DataFrame
        読み込まれたデータフレーム
    """
    file_ext = uploaded_file.name.split(".")[-1].lower()
    
    if file_ext == "csv":
        try:
            df = pd.read_csv(uploaded_file)
        except UnicodeDecodeError:
            # エンコーディングを自動検出して再試行
            df = pd.read_csv(uploaded_file, encoding="shift-jis")
    elif file_ext in ["xlsx", "xls"]:
        df = pd.read_excel(uploaded_file)
    else:
        raise ValueError(f"サポートされていないファイル形式: {file_ext}")
    
    return df


def load_data_from_url(data_url):
    """
    URLからデータを読み込む
    
    Parameters:
    -----------
    data_url : str
        データのURL（CSVまたはExcel）
        
    Returns:
    --------
    pandas.DataFrame
        読み込まれたデータフレーム
    """
    # URLの拡張子を確認
    url_path = urlparse(data_url).path
    file_ext = url_path.split(".")[-1].lower()
    
    # データをダウンロード
    response = requests.get(data_url)
    
    # 一時ファイルにダウンロードしたデータを保存
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_ext}") as tmp_file:
        tmp_file.write(response.content)
        tmp_file_path = tmp_file.name
    
    try:
        # ファイル形式に基づいて読み込み
        if file_ext == "csv":
            try:
                df = pd.read_csv(tmp_file_path)
            except UnicodeDecodeError:
                # エンコーディングを自動検出して再試行
                df = pd.read_csv(tmp_file_path, encoding="shift-jis")
        elif file_ext in ["xlsx", "xls"]:
            df = pd.read_excel(tmp_file_path)
        else:
            raise ValueError("サポートされていないファイル形式です。CSVまたはExcelを使用してください。")
    finally:
        # 一時ファイルを削除
        os.unlink(tmp_file_path)
    
    return df


def generate_sample_data(sample_option):
    """
    サンプルデータを生成する
    
    Parameters:
    -----------
    sample_option : str
        サンプルデータの種類
        
    Returns:
    --------
    pandas.DataFrame
        生成されたサンプルデータ
    """
    if sample_option == "月次売上データ":
        # 月次売上データのサンプル
        np.random.seed(42)
        dates = pd.date_range(start='2023-01-01', periods=12, freq='M')
        sales = np.random.normal(100, 15, 12).cumsum()
        df = pd.DataFrame({'売上（百万円）': sales}, index=dates)
        df.index.name = '日付'
        
    elif sample_option == "都市別気温データ":
        # 都市別気温データのサンプル
        months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
        tokyo = [5.2, 5.7, 8.7, 13.9, 18.2, 21.4, 25.0, 26.4, 22.8, 17.5, 12.1, 7.6]
        osaka = [6.0, 6.3, 9.4, 15.1, 19.7, 23.5, 27.4, 28.8, 24.7, 18.6, 13.0, 8.6]
        sapporo = [-3.6, -3.1, 0.6, 7.1, 12.4, 17.3, 20.5, 22.3, 18.1, 11.8, 4.9, -0.9]
        
        df = pd.DataFrame({
            '東京': tokyo,
            '大阪': osaka,
            '札幌': sapporo
        }, index=months)
        df.index.name = '月'
        
    elif sample_option == "株価推移データ":
        # 株価推移のサンプル
        np.random.seed(123)
        dates = pd.date_range(start='2023-01-01', periods=252, freq='B')
        
        # 乱数ウォークで株価を生成
        price_a = 1000 + np.random.normal(0, 1, 252).cumsum() * 5
        price_b = 2000 + np.random.normal(0, 1, 252).cumsum() * 8
        price_c = 500 + np.random.normal(0, 1, 252).cumsum() * 3
        
        df = pd.DataFrame({
            '企業A': price_a,
            '企業B': price_b,
            '企業C': price_c
        }, index=dates)
        df.index.name = '日付'
    
    else:
        raise ValueError(f"サポートされていないサンプルオプション: {sample_option}")
    
    return df


def fig_to_image(fig):
    """
    Matplotlibの図をPIL Imageに変換
    
    Parameters:
    -----------
    fig : matplotlib.figure.Figure
        変換するグラフ
        
    Returns:
    --------
    image : PIL.Image
        変換された画像
    """
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    img = Image.open(buf)
    return img


def fig_to_base64(fig):
    """
    Matplotlibの図をbase64文字列に変換
    
    Parameters:
    -----------
    fig : matplotlib.figure.Figure
        変換するグラフ
        
    Returns:
    --------
    base64_str : str
        base64エンコードされた画像文字列
    """
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    base64_str = base64.b64encode(buf.read()).decode('utf-8')
    return base64_str


def get_download_link(data, filename, text):
    """
    データのダウンロードリンクを生成
    
    Parameters:
    -----------
    data : str
        ダウンロードするデータ
    filename : str
        ダウンロードするファイル名
    text : str
        ダウンロードリンクのテキスト
        
    Returns:
    --------
    href : str
        HTMLダウンロードリンク
    """
    b64 = base64.b64encode(data.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">{text}</a>'
    return href


def create_mock_summary(graph_type):
    """
    モック要約を生成（APIなしで使用）
    
    Parameters:
    -----------
    graph_type : str
        グラフの種類
        
    Returns:
    --------
    summary : str
        生成されたモック要約
    insights : list
        主要なインサイトのリスト
    """
    if graph_type == "折れ線グラフ":
        mock_summary = """
        # グラフ要約
        
        このグラフは時系列データの上昇トレンドを示しています。全体的に右肩上がりの傾向が見られます。
        
        ## 主要ポイント
        
        1. データは時間経過とともに増加傾向を示しています
        2. 特に中間地点からの上昇率が高くなっています
        3. いくつかの小さな変動はありますが、全体的なトレンドは上昇です
        4. 始点と終点を比較すると、約30%の成長が見られます
        
        ## 詳細分析
        
        このデータからは持続的な成長パターンが読み取れます。短期的な変動はあるものの、長期的には安定して上昇していることがわかります。
        """
    elif graph_type == "棒グラフ":
        mock_summary = """
        # グラフ要約
        
        このグラフはカテゴリ別の比較データを示しています。カテゴリ間で値に明確な差異があります。
        
        ## 主要ポイント
        
        1. 最大値と最小値の間には約2倍の差があります
        2. 中央値付近のカテゴリが最も多く分布しています
        3. 特に注目すべきカテゴリが2つあり、他と比較して高い値を示しています
        4. 全体的なバランスは比較的均等ですが、いくつかの外れ値が存在します
        
        ## 詳細分析
        
        このデータからはカテゴリ間の明確な差異パターンが読み取れます。特定のカテゴリが突出しており、全体のバランスに影響を与えています。
        """
    else:
        mock_summary = """
        # グラフ要約
        
        このグラフはデータの分布と相関関係を示しています。複数の要素間に一定のパターンが見られます。
        
        ## 主要ポイント
        
        1. データは全体的に偏りなく分布しています
        2. いくつかの外れ値が存在し、全体の傾向から逸脱しています
        3. 複数の変数間に中程度の相関関係が見られます
        4. 集中した値のクラスターがいくつか形成されています
        
        ## 詳細分析
        
        このデータからは複合的なパターンが読み取れます。全体的な分布は均等ですが、特定の領域に集中する傾向があります。
        """
    
    insights = [
        "データには明確な上昇/下降トレンドがあります",
        "最大値は平均値より約30%高い値を示しています",
        "データの変動は中間地点で最も大きくなっています",
        "全体的なパターンから逸脱する外れ値が2点存在します",
        "長期的には安定した成長/減少傾向が見られます"
    ]
    
    return mock_summary, insights