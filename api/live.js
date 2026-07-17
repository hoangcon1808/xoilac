/**
 * File: app.js
 * Mục đích: Lấy dữ liệu từ API và xử lý JSON
 */

const API_URL = 'https://api-v2.chuoichientv.net/v2/matches?page=1&limit=9&type=blv';

async function fetchMatches() {
    try {
        const response = await fetch(API_URL);
        
        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }

        const jsonResponse = await response.json();
        
        // Ghi log để bạn biết cấu trúc chính xác của JSON
        console.log('Dữ liệu thô nhận được:', jsonResponse);

        // Giả sử API trả về mảng dữ liệu nằm trong key 'data' hoặc 'items'
        // Bạn hãy kiểm tra console log để thay đổi dòng này cho khớp
        const matches = jsonResponse.data || []; 

        renderMatches(matches);

    } catch (error) {
        console.error('Lỗi khi lấy dữ liệu:', error);
    }
}

function renderMatches(matches) {
    const container = document.getElementById('match-container');
    if (!container) return;

    if (matches.length === 0) {
        container.innerHTML = '<p>Không có trận đấu nào.</p>';
        return;
    }

    container.innerHTML = matches.map(match => `
        <div class="match-card">
            <h3>${match.name || 'Đang cập nhật'}</h3>
            <p>Thời gian: ${match.time || 'Chưa rõ'}</p>
        </div>
    `).join('');
}

// Chạy hàm khi trang web đã tải xong
document.addEventListener('DOMContentLoaded', fetchMatches);
