from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

def fetch_data_via_proxy():
    # 1. Khai báo link gốc và link proxy của bạn
    target_url = 'https://api18.colatv88xd.cc/api/matches'
    proxy_url = f'https://fancy-rice-6d07.hoangcon.workers.dev/?{target_url}'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json'
    }

    # Gọi qua proxy thay vì gọi thẳng
    response = requests.get(proxy_url, headers=headers, timeout=15)
    response.raise_for_status()
    return response.json()

# --- TRANG CHỦ ---
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "success",
        "message": "Server đang hoạt động!",
        "endpoints": {
            "all_matches": "/api/matches",
            "live_matches": "/api/live"
        }
    })

# --- LẤY TẤT CẢ TRẬN ĐẤU ---
@app.route('/api/matches', methods=['GET'])
def get_all_matches():
    try:
        data = fetch_data_via_proxy()
        return jsonify(data)
    except Exception as e:
        return jsonify({"status": "error", "message": "Lỗi khi gọi Proxy", "details": str(e)}), 500

# --- LỌC NHỮNG TRẬN ĐANG ĐÁ ---
@app.route('/api/live', methods=['GET'])
def get_live_matches():
    try:
        data = fetch_data_via_proxy()
        
        # Xác định danh sách trận đấu (tùy thuộc API trả về List hay Dict)
        matches_list = data if isinstance(data, list) else data.get('data', [])
        
        live_matches = []
        for match in matches_list:
            # 2. Quét các từ khóa/cờ nhận diện "đang đá" phổ biến trong các API bóng đá
            is_live = match.get('is_live')
            status = str(match.get('status', '')).lower()
            match_status = str(match.get('match_status', '')).lower()
            
            if (is_live in [1, '1', True]) or \
               ('live' in status or 'đang' in status or status == '2') or \
               ('live' in match_status or 'đang' in match_status or match_status == '2'):
                
                live_matches.append(match)

        # Nếu dữ liệu gốc là Dict, chỉ ghi đè mảng data để giữ nguyên cấu trúc
        if isinstance(data, dict):
            data['data'] = live_matches
            return jsonify(data)
            
        return jsonify(live_matches)

    except Exception as e:
        return jsonify({"status": "error", "message": "Lỗi khi lọc trận đang đá", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
