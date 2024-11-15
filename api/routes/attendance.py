import requests
from bs4 import BeautifulSoup, Tag
from fastapi import APIRouter, status

from api.deps import TokenDep
from config import Config

router = APIRouter()


@router.get("/attendance")
async def get_attendance(token: TokenDep, current_semester: int):
    """
    Get current semester attendance
    """
    headers = {
        "User-Agent": Config.USER_AGENT,
    }
    cookies = {Config.COOKIE_KEY: token}

    try:
        response = requests.get(
            f"{Config.BASE_URL}/ktuacademics/student/viewattendancesubject/{current_semester}",
            headers=headers,
            cookies=cookies,
        )
        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.find("table")

        headings = []
        contents = []
        if table and isinstance(table, Tag):
            for th in table.find_all("tr")[0].find_all("th"):
                headings.append(th.text.strip())

            for td in table.find_all("tr")[1].find_all("td"):
                contents.append(td.text.strip())

        uni_reg_no = contents[0]
        roll_no = contents[1]
        name = contents[2]
        [attended, total] = contents[-2].split("/")
        total_percentage = contents[-1]
        attendance_dict = {}

        headings, contents = headings[3:-2], contents[3:-2]
        for heading, content in zip(headings, contents):
            content = content.split()
            [attended, total] = content[0].split("/")
            percentage = content[1].replace("(", "").replace(")", "").replace("%", "")
            attendance_dict[heading] = {
                "attended": attended,
                "total": total,
                "percentage": percentage,
            }

        return {
            "uni_reg_no": uni_reg_no,
            "roll_no": roll_no,
            "name": name,
            "total_attended": attended,
            "total_classes": total,
            "total_percentage": total_percentage,
            "attendance": attendance_dict,
        }
    except Exception as e:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": f"An error occurred: {e}",
        }
        pass
