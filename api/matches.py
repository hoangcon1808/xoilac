from http.server import BaseHTTPRequestHandler
import requests
import json

class handler(BaseHTTPRequestHandler):
    # 1. Bắt buộc phải có hàm này để trình duyệt cho phép gọi chéo (CORS)
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()

    def do_GET(self):
        url = 'https://api18.colatv88xd.cc/api/matches'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json'
        }

        try:
            # Gọi API gốc với timeout 10s
            response = requests.get(url, headers=headers, timeout=10)
            
            # Cố gắng đọc JSON. Nếu API trả về HTML (do Cloudflare chặn), đoạn này sẽ báo lỗi và nhảy xuống except
            data = response.json()

            # 2. Trả về JSON thành công
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            # 3. Kể cả khi lỗi, vẫn ép Vercel trả về định dạng JSON để hiển thị rõ nguyên nhân
            self.send_response(500)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_data = {
                "status": "error",
                "message": "Không thể lấy dữ liệu. Có thể IP của Vercel đã bị API gốc chặn (Cloudflare).",
                "details": str(e)
            }
            self.wfile.write(json.dumps(error_data, ensure_ascii=False).encode('utf-8'))
            self.wfile.write(error_msg.encode('utf-8'))
