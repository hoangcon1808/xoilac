export default async function handler(req, res) {
    // API gốc lấy danh sách
    const LIST_API_URL = "https://api-ls.cdnokvip.com/api/get-livestream-group?isHot=false&isLive=true&isToday=true&isTomorrow=false&offset=0";
    
    const headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "Referer": "https://cdnokvip.com/",
        "Origin": "https://cdnokvip.com",
        "Accept": "application/json, text/plain, */*"
    };

    try {
        const listRes = await fetch(LIST_API_URL, { headers });
        const listData = await listRes.json();
        
        // Lấy danh sách, nếu không có 'datas' thì kiểm tra xem nó nằm ở đâu (debug)
        let matches = listData?.value?.datas || listData?.data || [];
        
        // DEBUG: Bỏ comment dòng dưới nếu vẫn bị total: 0 để xem cấu trúc thực tế
        // console.log("List API Response:", JSON.stringify(listData));

        // NỚI LỎNG ĐIỀU KIỆN: Chỉ cần có dữ liệu là lấy, không lọc thời gian quá gắt
        // Nếu API trả về list trống, vấn đề nằm ở API gốc
        const rawMatches = matches.slice(0, 10); 

        const fetchMatchDetail = async (match) => {
            // Thay đổi ID tùy vào key của API gốc (thử id, matchId, hoặc slugUrl)
            const matchId = match.id || match.matchId || match.slug;
            if (!matchId) return null;

            const detailUrl = `https://fb-api.apiscoreflow.com/football/match/detail_live?id=${matchId}`;
            
            try {
                const response = await fetch(detailUrl, { headers });
                const json = await response.json();
                
                // Trả về dữ liệu nếu tìm thấy link stream
                const streamLink = json?.data?.stream_url || json?.data?.live_url || json?.data?.url || null;
                
                if (!streamLink) return null;

                return {
                    league: match.leagueName || "Unknown",
                    homeTeam: match.homeName || "Home",
                    awayTeam: match.awayName || "Away",
                    streamLink: streamLink
                };
            } catch (e) {
                return null;
            }
        };

        const results = await Promise.all(rawMatches.map(fetchMatchDetail));
        const finalData = results.filter(r => r !== null);

        res.setHeader('Content-Type', 'application/json; charset=utf-8');
        return res.status(200).json({
            success: true,
            total: finalData.length,
            data: finalData
        });

    } catch (error) {
        return res.status(500).json({ success: false, message: error.message });
    }
}
