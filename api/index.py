from flask import Flask, jsonify
from flask_cors import CORS
import requests
import datetime
import json  # Code thêm: Import thư viện json

app = Flask(__name__)
CORS(app)

def fetch_data():
    url = 'https://api18.colatv88xd.cc/api/matches'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()

@app.route('/api/live', methods=['GET'])
def get_formatted_live_matches():
    try:
        data = fetch_data()
        matches_dict = data.get('data', {})
        formatted_list = []

        for key, match in matches_dict.items():
            # Chỉ lấy trận đang live (matchStatus == 2)
            if str(match.get('matchStatus')) == '2':
                # Chọn link stream: ưu tiên playStreamAddress, nếu không có thì lấy playStreamAddress2
                anchors = match.get('anchorAppointmentVoList', [{}])
                stream_link = anchors[0].get('playStreamAddress2') or anchors[0].get('playStreamAddress') or ""
                
                # Định dạng thời gian
                ts = match.get('matchTime', 0)
                time_str = datetime.datetime.fromtimestamp(ts).strftime('%H:%M %d-%m')

                # Ánh xạ vào cấu trúc mới
                item = {
                    "league": match.get('competitionName'),
                    "homeTeam": match.get('homeTeamName'),
                    "awayTeam": match.get('awayTeamName'),
                    "time": time_str,
                    "timestamp": ts,
                    "status": "ĐANG LIVE",
                    "commentator": anchors[0].get('nickName', 'NHÀ ĐÀI'),
                    "homeLogo": match.get('homeTeamLogo'),
                    "streamLink": stream_link
                }
                formatted_list.append(item)

        result = {
            "success": True,
            "total": len(formatted_list),
            "data": formatted_list
        }
        
        # --- Code thêm: Ghi kết quả ra file JSON ---
        # File sẽ được lưu cùng thư mục với script này với tên 'live_matches.json'
        with open('live_matches.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        # -------------------------------------------
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
