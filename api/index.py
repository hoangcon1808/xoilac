from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# 1. Bắt đường dẫn trang chủ gốc (Tránh lỗi Not Found khi vừa mở link Vercel)
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "success",
        "message": "Server đang hoạt động! Hãy thêm /api/matches hoặc /matches vào cuối đường dẫn URL của bạn."
    })

# 2. Bắt cả 2 trường hợp đường dẫn để không bao giờ xịt
@app.route('/api/matches', methods=['GET'])
@app.route('/matches', methods=['GET'])
def get_matches():
    url = 'https://api18.colatv88xd.cc/api/matches'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        return jsonify(data)
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Lỗi lấy dữ liệu từ API gốc",
            "details": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
