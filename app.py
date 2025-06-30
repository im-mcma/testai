from flask import Flask, request, jsonify, render_template
import os
from openai import OpenAI

app = Flask(__name__)

# تنظیمات API
token = token = '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'
endpoint = "https://models.github.ai/inference"
model_name = "openai/gpt-4o"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ],
            temperature=1.0,
            top_p=1.0,
            max_tokens=1000,
            model=model_name
        )
        
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
    
    except Exception as e:
        return jsonify({"reply": f"خطا در پردازش درخواست: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
