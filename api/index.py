from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

def fetch_data():
    # Gọi trực tiếp đến API gốc
    target_url = 'https://api18.colatv88xd.cc/api/matches'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json'
    }

    # Gọi thẳng API gốc với timeout 15s
    response = requests.get(target_url, headers=headers, timeout=15)
    response.raise_for_status()
    return response.json()

# --- TRANG CHỦ ---
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "success",
        "message": "Server Vercel Flask đang hoạt động!",
        "endpoints": {
            "all_matches": "/api/matches",
            "live_matches": "/api/live"
        }
    })

# --- LẤY TẤT CẢ TRẬN ĐẤU ---
@app.route('/api/matches', methods=['GET'])
def get_all_matches():
    try:
        data = fetch_data()
        return jsonify(data)
    except Exception as e:
        return jsonify({"status": "error", "message": "Lỗi khi gọi API gốc", "details": str(e)}), 500

# --- LỌC NHỮNG TRẬN ĐANG ĐÁ ---
@app.route('/api/live', methods=['GET'])
def get_live_matches():
    try:
        data = fetch_data()
        
        # Trích xuất phần 'data' (là một dictionary chứa các trận đấu)
        matches_dict = data.get('data', {})
        live_matches = {}
        
        # Duyệt qua các key (slug) và value (thông tin trận)
        for match_key, match_info in matches_dict.items():
            
            # Quét trường matchStatus. Số 2 có nghĩa là đang trực tiếp (live)
            match_status = match_info.get('matchStatus')
            
            # Chấp nhận matchStatus là int 2 hoặc chuỗi '2'
            if str(match_status) == '2':
                live_matches[match_key] = match_info

        # Trả về kết quả giữ nguyên cấu trúc chuẩn của API gốc
        response_data = {
            "code": data.get("code", "0000"),
            "status": data.get("status", 0),
            "data": live_matches
        }

        return jsonify(response_data)

    except Exception as e:
        return jsonify({"status": "error", "message": "Lỗi khi lọc trận đang đá", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
