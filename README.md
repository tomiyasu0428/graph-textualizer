# グラフテキスト化アプリ (Graph Textualizer)

## 概要

グラフテキスト化アプリは、データの可視化結果を自然言語で説明・要約するためのブラウザベースのツールです。アップロードされたデータやグラフ画像を分析し、AIを活用して図表の内容を言語化します。このアプリケーションは、データの解釈を支援し、視覚障害者のアクセシビリティを向上させることを目的としています。

## 特徴

- **複数のデータ入力方法**: ファイルアップロード、URL共有、サンプルデータから選択可能
- **グラフ画像の直接アップロード**: 既存のグラフ画像の分析が可能
- **多様なグラフタイプ**: 折れ線グラフ、棒グラフ、散布図、円グラフなど、多様なグラフタイプに対応
- **AIによる言語化**: グラフを自然言語で説明し、主要なインサイトを抽出
- **Gemini APIサポート**: GoogleのGemini APIを使用した画像理解と言語生成
- **モックモード**: API無しでもテスト可能
- **要約のエクスポート**: 生成された要約をコピーまたはJSONとして保存可能

## インストール方法

### 前提条件

- Python 3.8以上
- pip (Pythonパッケージマネージャー)

### 手順

1. リポジトリをクローンまたはダウンロードします:
```bash
git clone https://github.com/tomiyasu0428/graph-textualizer.git
cd graph-textualizer
```

2. 仮想環境を作成して有効化します（推奨）:
```bash
python -m venv venv
# Windowsの場合
venv\Scripts\activate
# macOS/Linuxの場合
source venv/bin/activate
```

3. 必要なパッケージをインストールします:
```bash
pip install -r requirements.txt
```

4. アプリケーションを起動します:
```bash
streamlit run app.py
```

5. ブラウザで自動的に開くか、手動で `http://localhost:8501` にアクセスします。

## 使用方法

1. **データの読み込み**:
   - CSVまたはExcelファイルをアップロード
   - データのURLを共有
   - サンプルデータから選択
   - または既存のグラフ画像を直接アップロード

2. **グラフの生成**:
   - グラフの種類を選択
   - タイトルや軸ラベルを設定
   - 表示するデータ列を選択
   - 追加設定でグラフをカスタマイズ

3. **要約の生成**:
   - 使用するAI APIを選択し、キーを入力（モックモードではAPIキー不要）
   - 要約の詳細度を選択
   - 「グラフの要約を生成」ボタンをクリック
   - 生成された要約とインサイトを確認
   - 必要に応じて要約をコピーまたは保存

## APIキーの取得方法

### Gemini API
1. [Google AI Studio](https://makersuite.google.com/app/apikey) にアクセス
2. Googleアカウントでログイン
3. 「APIキーを作成」をクリック
4. 生成されたキーをコピー
5. 生成したキーを`.env`ファイルに`GEMINI_API_KEY=あなたのキー`の形式で保存

## 制限事項

- 現在のバージョンでは、標準的なグラフタイプと一般的なデータ形式のみをサポートしています
- アップロード可能なファイルサイズに制限があります
- APIによっては、リクエスト数や処理能力に制限がある場合があります
- モックモードでは事前定義された応答のみが返されます

## 開発者向け情報

### プロジェクト構造
```
graph-textualizer/
├── app.py               # メインアプリケーションファイル
├── requirements.txt     # 必要なパッケージリスト
├── README.md            # このドキュメント
├── .gitignore           # Gitが無視するファイルリスト
└── assets/              # 静的アセット（画像など）
```

### カスタマイズ方法

- 新しいグラフタイプの追加:
  `app.py` の `tab2` セクションでグラフ生成部分を拡張

- 新しいAPIの追加:
  サイドバーの `api_type` 選択肢とAPI呼び出し部分を拡張

- UIのカスタマイズ:
  Streamlitのスタイル設定やCSSを変更

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細については、LICENSEファイルを参照してください。

## 問い合わせ

バグ報告や機能リクエストは、Githubのイシュートラッカーからお願いします。