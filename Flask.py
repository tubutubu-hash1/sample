from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

# Excelファイルのパス
EXCEL_FILE = 'results.xlsx'

# 初期化関数
def initialize_excel():
    if not os.path.exists(EXCEL_FILE):
        df = pd.DataFrame(columns=['試合数', 'あなたの手', 'AIの手', '結果'])
        df.to_excel(EXCEL_FILE, index=False)

@app.route('/save', methods=['POST'])
def save_result():
    data = request.json
    user_hand = data['user']
    ai_hand = data['ai']
    outcome = data['outcome']

    # Excelに結果を保存
    df = pd.read_excel(EXCEL_FILE)
    new_row = {'試合数': len(df) + 1, 'あなたの手': user_hand, 'AIの手': ai_hand, '結果': outcome}
    df = df.append(new_row, ignore_index=True)
    df.to_excel(EXCEL_FILE, index=False)
    return jsonify({'status': 'success'})

@app.route('/reset', methods=['POST'])
def reset_results():
    df = pd.DataFrame(columns=['試合数', 'あなたの手', 'AIの手', '結果'])
    df.to_excel(EXCEL_FILE, index=False)
    return jsonify({'status': 'reset'})

if __name__ == '__main__':
    initialize_excel()
    app.run(debug=True)
