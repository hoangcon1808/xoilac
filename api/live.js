export default async function handler(req, res) {
    const LIST_API_URL = "https://api-ls.cdnokvip.com/api/get-livestream-group?isHot=false&isLive=true&isToday=true&isTomorrow=false&offset=0";
    
    // Tạo header với IP ngẫu nhiên để tránh chặn request
    const fakeIp = `113.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}`;
    const headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "X-Forwarded-For": fakeIp,
        "Accept": "application/json"
    };

    try {
        // BƯỚC 1: Lấy danh sách trận đấu
        const listRes = await fetch(LIST_API_URL, { headers });
        if (!listRes.ok) throw new Error("Không thể kết nối API danh sách");
        
        const listData = await listRes.json();
        let matches = listData?.value?.datas || [];
        
        const currentTime = Math.floor(Date.now() / 1000);
        // Lọc trận đang diễn ra (trong vòng 3 tiếng)
        matches = matches.filter(match => match.matchTime <= currentTime && match.matchTime > (currentTime - 10800)).slice(0, 20);

        if (matches.length === 0) {
            return res.status(200).json({ success: true, message: "Không có trận nào đang live", data: [] });
        }

        // BƯỚC 2: Cào chi tiết trận đấu từ API mới
        const fetchMatchDetail = async (match) => {
            const matchId = match.id || match.matchId; // Đảm bảo lấy đúng ID
            const detailUrl = `https://fb-api.apiscoreflow.com/football/match/detail_live?id=${matchId}`;
            
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 3000);
            
            try {
                const detailRes = await fetch(detailUrl, { headers, signal: controller.signal });
                clearTimeout(timeoutId);
                
                if (!detailRes.ok) return { ...match, m3u8Link: "ERROR_API" };
                
                const detailData = await detailRes.json();
                
                /* 
                   LƯU Ý: Nếu link không hiện, hãy kiểm tra console.log(detailData) 
                   và thay đổi đường dẫn dưới đây cho khớp với cấu trúc API của họ.
                */
                const m3u8Link = detailData?.data?.live_url || detailData?.data?.stream || "LINK_NOT_FOUND";
                
                return { ...match, m3u8Link };
            } catch (err) {
                clearTimeout(timeoutId);
                return { ...match, m3u8Link: "TIMEOUT" };
            }
        };

        const results = await Promise.all(matches.map(fetchMatchDetail));

        // BƯỚC 3: Định dạng dữ liệu trả về
        const jsonData = results.map(item => ({
            league: item.leagueName || "Unknown",
            homeTeam: item.homeName || "Home",
            awayTeam: item.awayName || "Away",
            time: new Date(item.matchTime * 1000).toLocaleString('vi-VN', { timeZone: 'Asia/Ho_Chi_Minh' }),
            status: "ĐANG LIVE",
            streamLink: item.m3u8Link
        }));

        res.setHeader('Content-Type', 'application/json; charset=utf-8');
        res.setHeader('Cache-Control', 's-maxage=10, stale-while-revalidate=5');
        return res.status(200).json({ success: true, total: jsonData.length, data: jsonData });

    } catch (error) {
        return res.status(500).json({ success: false, message: error.message, data: [] });
    }
}
