import asyncio
import aiohttp

from bs4 import BeautifulSoup as BS

async def loadpage(link:str):
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as response:
            html = await response.text()
    soup = BS(html,"html.parser")
    balls = [ball.get_text() for ball in soup.find_all("span",{"class":f"ball_645"})]
    print(balls)

asyncio.run(loadpage("http://dhlottery.co.kr/gameResult.do?method=byWin&drwNo=943"))
