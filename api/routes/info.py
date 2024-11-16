import httpx
from bs4 import BeautifulSoup, Tag
from fastapi import APIRouter, status

from api.deps import TokenDep
from config import Config
from models import StudentInfo

router = APIRouter()


def get_text_from_soup(soup: BeautifulSoup, string):
    element = soup.find("th", string=string)
    if element:
        sibling = element.find_next_sibling("td")
        if sibling:
            return sibling.getText(strip=True)
    return None


def get_img_url(soup: BeautifulSoup):
    img_element = soup.find("img", id="photo")
    if img_element and isinstance(img_element, Tag):
        return f"{Config.BASE_URL}{img_element.attrs['src']}"
    return None


@router.get("/info")
async def get_info(token: TokenDep):
    headers = {
        "User-Agent": Config.USER_AGENT,
    }
    cookies = {Config.COOKIE_KEY: token}
    try:
        async with httpx.AsyncClient() as session:
            response = await session.get(
                f"{Config.BASE_URL}/student/profile", headers=headers, cookies=cookies
            )
            print(response.text)
            soup = BeautifulSoup(response.text, "html.parser")
            print(soup)
        name = get_text_from_soup(soup, "Name")
        dob = get_text_from_soup(soup, "Date of Birth")
        ad_no = get_text_from_soup(soup, "Admission No")
        uni_reg_no = get_text_from_soup(soup, "University Reg No")
        aadhar = get_text_from_soup(soup, "Aadhaar No")
        img_src = get_img_url(soup)
        print(name, dob, ad_no, uni_reg_no, aadhar, img_src)
        return StudentInfo(
            name=name,
            dob=dob,
            ad_no=ad_no,
            uni_reg_no=uni_reg_no,
            aadhar=aadhar,
            img_src=img_src,
        )
    except Exception as e:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": f"An error occurred: {e}",
        }
