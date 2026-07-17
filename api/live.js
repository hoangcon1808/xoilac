/**
 * API Handler: Lấy danh sách trận đấu đang live và link stream từ API Scoreflow
 */
export default async function handler(req, res) {
    const LIST_API_URL = "https://api-ls.cdnokvip.com/api/get-livestream-group?isHot=false&isLive=true&isToday=true&isTomorrow=false&offset=0";
    
    // Cấu hình headers để giả lập trình duyệt, quan trọng cho việc bypass chặn request
    const headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "Referer": "https://cdnokvip.com/",
        "Accept": "application/json"
    };

    try {
        // 1. Lấy danh sách trận đấu gốc
        const listRes = await fetch(LIST_API_URL, { headers });
        if (!listRes.ok) throw new Error("API List failed");
        
        const listData = await listRes.json();
        let matches = listData?.value?.datas || [];
        
        // Lọc trận đấu đang diễn ra trong vòng 3 giờ
        const now = Math.floor(Date.now() / 1000);
        matches = matches.filter(m => m.matchTime <= now && m.matchTime > (now - 10800)).slice(0, 20);

        // 2. Hàm lấy chi tiết link stream
        const fetchMatchDetail = async (match) => {
            const matchId = match.id || match.matchId;
            const detailUrl = `https://fb-api.apiscoreflow.com/football/match/detail_live?id=${matchId}`;
            
            try {
                const response = await fetch(detailUrl, { headers });
                const json = await response.json();
                
                // CẤU TRÚC JSON: Dựa trên kinh nghiệm, hãy tìm trường chứa '.m3u8'
                // Thay thế detailData.data.stream_url bằng key thực tế bạn thấy khi test
                const streamLink = json?.data?.stream_url || json?.data?.live_url || json?.data?.url || "LINK_NOT_FOUND";
                
                return {
                    league: match.leagueName,
                    homeTeam: match.homeName,
                    awayTeam: match.awayName,
                    status: "ĐANG LIVE",
                    streamLink: streamLink
                };
            } catch {
                return null;
            }
        };

        // 3. Xử lý đồng thời để đạt tốc độ cao
        const results = await Promise.all(matches.map(fetchMatchDetail));

        // 4. Trả về kết quả
        res.setHeader('Content-Type', 'application/json; charset=utf-8');
        res.setHeader('Cache-Control', 's-maxage=30, stale-while-revalidate=10'); // Cache 30 giây để giảm tải
        
        return res.status(200).json({
            success: true,
            total: results.filter(r => r !== null).length,
            data: results.filter(r => r !== null)
        });

    } catch (error) {
        return res.status(500).json({ success: false, message: error.message });
    }
}
