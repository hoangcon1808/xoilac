export default async function handler(req, res) {
    const URL = 'https://api-v2.chuoichientv.net/v2/matches?page=1&limit=9&type=blv';
    
    try {
        const response = await fetch(URL, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Referer': 'https://chuoichientv.net/',
                'Accept': 'application/json'
            },
            signal: AbortSignal.timeout(8000) // Timeout sau 8 giây
        });

        if (!response.ok) throw new Error(`Server API phản hồi lỗi: ${response.status}`);
        
        const data = await response.json();
        return res.status(200).json(data);

    } catch (error) {
        console.error('Lỗi chi tiết:', error);
        return res.status(500).json({ error: error.message });
    }
}
