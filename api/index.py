from flask import Flask, jsonify, make_response
from flask_cors import CORS
import requests
import datetime

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
            if str(match.get('matchStatus')) == '2':
                anchors = match.get('anchorAppointmentVoList', [{}])
                stream_link = anchors[0].get('playStreamAddress') or anchors[0].get('playStreamAddress2') or ""
                
                ts = match.get('matchTime', 0)
                time_str = datetime.datetime.fromtimestamp(ts).strftime('%H:%M %d-%m')

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
        
        # --- CÁCH LÀM CHUẨN TRÊN VERCEL ---
        response = make_response(jsonify(result))
        
        # Thiết lập Cache: Vercel sẽ lưu lại JSON này ở CDN trong 60 giây.
        # Nghĩa là nếu có 1000 người truy cập API trong 1 phút, code fetch_data() 
        # chỉ chạy đúng 1 lần, 999 lần sau Vercel sẽ trả về kết quả JSON đã cache.
        # (Chức năng này thay thế hoàn hảo cho việc tạo file vật lý)
        response.headers['Cache-Control'] = 's-maxage=60, stale-while-revalidate'
        
        return response
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
