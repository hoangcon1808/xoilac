async function getMatchData() {
    const liveApiUrl = 'https://seo.alpro-api-service.com/v1/live-data';
    const baseUrl = 'https://thapcamtv2026a.com/app/uploads/match-streamers/';

    // Headers để giả lập giống trình duyệt, tránh bị chặn
    const headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
        'Origin': 'https://thapcamtv2026a.com',
        'Referer': 'https://thapcamtv2026a.com/'
    };

    try {
        // 1. Gọi API lấy danh sách trận đấu
        const response = await fetch(liveApiUrl, { headers });
        const liveData = await response.json();

        // Giả sử dữ liệu trả về là một mảng, bạn lọc lấy trận đấu cần thiết
        // Thay [0] bằng logic lọc trận đấu của bạn (ví dụ theo tên đội)
        const targetMatch = liveData[0]; 
        const matchId = targetMatch.match_id;

        console.log("Đã tìm thấy Match ID:", matchId);

        // 2. Gọi URL lấy chi tiết trận đấu
        const timestamp = Date.now();
        const streamUrl = `${baseUrl}${matchId}.json?t=${timestamp}`;
        
        const streamResponse = await fetch(streamUrl, { headers });
        const streamData = await streamResponse.json();

        console.log("Dữ liệu trận đấu:", streamData);
        return streamData;

    } catch (error) {
        console.error("Lỗi khi lấy dữ liệu:", error);
    }
}

// Chạy hàm
getMatchData();
