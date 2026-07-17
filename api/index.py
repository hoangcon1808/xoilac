from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
# Tự động xử lý cấu hình CORS cho tất cả các request
CORS(app)

@app.route('/api/matches', methods=['GET'])
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
        # Nếu lỗi (do timeout hoặc bị Cloudflare chặn), trả về JSON thông báo lỗi chuẩn xác
        return jsonify({
            "status": "error",
            "message": "Không thể lấy dữ liệu.",
            "details": str(e)
        }), 500

# Require của Vercel để chạy được app
if __name__ == '__main__':
    app.run(debug=True)
