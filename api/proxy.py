import requests
import json

def fetch_and_save_matches():
    url = 'https://api18.colatv88xd.cc/api/matches'
    output_file = 'matches.json'
    
    # Thêm User-Agent để tránh bị API block
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        print(f"Đang gọi API: {url}...")
        
        # Gọi API với phương thức GET
        response = requests.get(url, headers=headers)
        
        # Kiểm tra nếu HTTP status code không phải là 200 (Thành công)
        response.raise_for_status() 

        # Chuyển đổi dữ liệu trả về thành Dictionary/List trong Python
        data = response.json()

        # Ghi dữ liệu ra file JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print(f"✅ Đã lưu toàn bộ thông tin trận đấu vào file: {output_file}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Có lỗi mạng hoặc HTTP xảy ra: {e}")
    except json.JSONDecodeError:
        print("❌ Dữ liệu trả về không phải là chuẩn JSON.")
    except Exception as e:
        print(f"❌ Có lỗi không xác định xảy ra: {e}")

if __name__ == "__main__":
    fetch_and_save_matches()
