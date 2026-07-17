from http.server import BaseHTTPRequestHandler
import requests
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = 'https://api18.colatv88xd.cc/api/matches'
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        try:
            # Gọi API
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

            # Trả về kết quả cho trình duyệt
            self.send_response(200)
            
            # Cấu hình CORS để có thể gọi từ giao diện HTML của bạn
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            # Xử lý lỗi
            self.send_response(500)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            error_msg = json.dumps({"error": str(e)}, ensure_ascii=False)
            self.wfile.write(error_msg.encode('utf-8'))
