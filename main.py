from flask import Flask, jsonify, request, render_template
import random
import csv
import os

app = Flask(__name__, static_folder='static')

def load_word_bank():
    word_dict = {}
    csv_path = os.path.join(os.path.dirname(__file__), 'data', 'words.csv')
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 2:  # 防止空行
                    word_dict[row[0].strip()] = row[1].strip()
    except FileNotFoundError:
        print(f"警告：未找到 {csv_path}，使用默认词库")
        word_dict = {
            "apple": "苹果",
            "banana": "香蕉",
            # ... 保留原有默认词库
        }
    return word_dict

word_bank = load_word_bank()  # 初始化词库

@app.route('/get_question')
def get_question():
    word = random.choice(list(word_bank.keys()))
    correct_translation = word_bank[word]
    wrong_translations = random.sample([v for k, v in word_bank.items() if v != correct_translation], 3)
    options = wrong_translations + [correct_translation]
    random.shuffle(options)
    return jsonify({
        "word": word,
        "options": options,
        "correct_answer": correct_translation
    })

@app.route('/check_answer', methods=['POST'])
def check_answer():
    data = request.json
    user_answer = data.get("answer")
    correct_answer = data.get("correct_answer")
    is_correct = (user_answer == correct_answer)
    return jsonify({"is_correct": is_correct})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)