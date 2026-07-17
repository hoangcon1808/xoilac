from http.server import BaseHTTPRequestHandler
import requests

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # API gốc bạn muốn lấy
        target_url = "https://seo.alpro-api-service.com/v1/live-data"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
            "Origin": "https://thapcamtv2026a.com",
            "Referer": "https://thapcamtv2026a.com/"
        }
        
        try:
            # Lấy dữ liệu
            response = requests.get(target_url, headers=headers)
            
            # Trả về kết quả
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*') # Cho phép mọi nguồn gọi
            self.end_headers()
            self.wfile.write(response.content)
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())
        return
