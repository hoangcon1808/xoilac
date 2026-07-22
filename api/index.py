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

def format_match_data(match):
    """
    Hàm xử lý định dạng chung cho 1 trận đấu
    """
    anchors = match.get('anchorAppointmentVoList') or []
    if not anchors:
        anchors = [{}] # Đảm bảo không bị lỗi nếu mảng rỗng
        
    stream_link = ""
    fallback_link = ""
    commentator = "NHÀ ĐÀI"
    
    # 1. ƯU TIÊN TÌM LINK M3U8
    for anchor in anchors:
        if not anchor: 
            continue
            
        addr1 = anchor.get('playStreamAddress') or ""
        addr2 = anchor.get('playStreamAddress2') or ""
        
        # Lưu lại link đầu tiên tìm được làm phương án dự phòng (fallback)
        if not fallback_link:
            fallback_link = addr1 or addr2
            commentator = anchor.get('nickName', 'NHÀ ĐÀI')
            
        # Kiểm tra nếu link có đuôi m3u8 thì lấy luôn và ngắt vòng lặp
        if '.m3u8' in addr1.lower():
            stream_link = addr1
            commentator = anchor.get('nickName', 'NHÀ ĐÀI')
            break
        if '.m3u8' in addr2.lower():
            stream_link = addr2
            commentator = anchor.get('nickName', 'NHÀ ĐÀI')
            break
            
    # Nếu không tìm thấy link m3u8 nào, sử dụng link dự phòng
    if not stream_link:
        stream_link = fallback_link

    # Xử lý thời gian
    ts = match.get('matchTime', 0)
    time_str = datetime.datetime.fromtimestamp(ts).strftime('%H:%M %d-%m')

    # Trạng thái trận đấu (Tùy chọn: có thể thay đổi text cho phù hợp)
    status_code = str(match.get('matchStatus', ''))
    status_text = status_code
    if status_code == '1': status_text = "SẮP DIỄN RA"
    elif status_code in ['2', '3', '4', '5']: status_text = "ĐANG LIVE"
    elif status_code == '-1': status_text = "KẾT THÚC"

    return {
        "league": match.get('competitionName'),
        "homeTeam": match.get('homeTeamName'),
        "awayTeam": match.get('awayTeamName'),
        "time": time_str,
        "timestamp": ts,
        "statusCode": status_code,
        "status": status_text,
        "commentator": commentator,
        "homeLogo": match.get('homeTeamLogo'),
        "awayLogo": match.get('awayTeamLogo'), # Thêm logo đội khách cho đầy đủ
        "streamLink": stream_link
    }

# ==========================================
# ROUTE 1: Chỉ lấy các trận ĐANG LIVE
# ==========================================
@app.route('/api/live', methods=['GET'])
def get_live_matches():
    try:
        data = fetch_data()
        matches_dict = data.get('data', {})
        formatted_list = []

        for key, match in matches_dict.items():
            # Thường status 2,3,4,5 là các trạng thái đang đá (Hiệp 1, Nghỉ giữa hiệp, Hiệp 2, ...)
            if str(match.get('matchStatus')) in ['2', '3', '4', '5']:
                item = format_match_data(match)
                item["status"] = "ĐANG LIVE" # Ép kiểu text thành Đang Live
                formatted_list.append(item)

        result = {"success": True, "total": len(formatted_list), "data": formatted_list}
        response = make_response(jsonify(result))
        response.headers['Cache-Control'] = 's-maxage=60, stale-while-revalidate'
        return response
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# ==========================================
# ROUTE 2: Lấy TẤT CẢ các trận đấu
# ==========================================
@app.route('/api/matches', methods=['GET'])
def get_all_matches():
    try:
        data = fetch_data()
        matches_dict = data.get('data', {})
        formatted_list = []

        for key, match in matches_dict.items():
            item = format_match_data(match)
            formatted_list.append(item)

        # Có thể sort list theo thời gian (timestamp) để sắp xếp trận đấu từ mới tới cũ hoặc ngược lại
        formatted_list.sort(key=lambda x: x['timestamp'])

        result = {"success": True, "total": len(formatted_list), "data": formatted_list}
        response = make_response(jsonify(result))
        
        # Cache 60s cho Vercel (giảm tải API gốc)
        response.headers['Cache-Control'] = 's-maxage=60, stale-while-revalidate'
        return response
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
