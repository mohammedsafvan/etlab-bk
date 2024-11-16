import httpx
from bs4 import BeautifulSoup, Tag
from fastapi import APIRouter, status

from api.deps import TokenDep
from config import Config

router = APIRouter()


@router.get("/timetable")
async def get_timetable(token: TokenDep):
    headers = {
        "User-Agent": Config.USER_AGENT,
    }
    cookies = {Config.COOKIE_KEY: token}

    try:
        async with httpx.AsyncClient() as session:
            response = await session.get(
                f"{Config.BASE_URL}/student/timetable",
                headers=headers,
                cookies=cookies,
            )

        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.find("table")
        if table and isinstance(table, Tag):
            rows = table.find_all("tr")

            timetable = {}
            for row in rows[1:]:
                subs = row.find_all("td")
                lis = []
                for sub in subs[1:]:
                    lis.append(sub.text.strip())
                timetable[subs[0].text.strip()] = lis
            return timetable
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "No timetable found",
        }
    except Exception as e:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": f"An error occurred: {e}",
        }
