from flask import Flask, request, jsonify, render_template, send_from_directory
import os
from openai import OpenAI

app = Flask(__name__, static_folder='static', template_folder='templates')

# تنظیمات API با استفاده از CHATGPT_TOKEN
token = os.environ.get('chatgpt')
endpoint = "https://api.openai.com/v1"  # یا آدرس سفارشی شما
model_name = "gpt-4"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

# Route برای فایل‌های استاتیک
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

# صفحه اصلی
@app.route('/')
def home():
    return render_template('index.html')

# API چت
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7
        )
        
        return jsonify({
            "reply": response.choices[0].message.content
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
