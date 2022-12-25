from typing import Union,Optional
from fastapi import FastAPI
import requests
import get_grade
import parse
from pydantic import BaseModel
import uvicorn

# if __name__ == "__main__":
#     uvicorn.run("main:app", port=8080,host="0.0.0.0",workers=4, log-level="info")

class Item(BaseModel):
    id_: str
    passwd: str
    year: str
    semester: str

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello":"World"}


# @app.get("/token/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

#uvicorn main:app --host=0.0.0.0 --port=8080
@app.post("/grade/")
def get_token(item:Item):

    login_url = "https://smartid.ssu.ac.kr/Symtra_sso/smln_pcs.asp"
    user_data = {
        "userid": item.id_,
        "pwd": item.passwd
    }
    login_res = requests.post(login_url, data=user_data)
    token = login_res.cookies['sToken']
    saint=get_grade.Saint(token)
    saint._load_grade_page()

    page_res=saint._get_grade_page(item.year,item.semester)
    saint._close_connection()
    grade=parse.parse_grade(page_res)

    return grade

@app.post("/gradeTwo/")
def get_token(item:Item):

    login_url = "https://smartid.ssu.ac.kr/Symtra_sso/smln_pcs.asp"
    user_data = {
        "userid": item.id_,
        "pwd": item.passwd
    }
    login_res = requests.post(login_url, data=user_data)
    token = login_res.cookies['sToken']
    saint=get_grade.Saint(token)
    saint._load_grade_page()

    page_res_tuple=saint._get_grade_page_year()
    saint._close_connection()
    grade_first=parse.parse_grade(page_res_tuple[0])
    grade_second=parse.parse_grade(page_res_tuple[1])

    return [grade_first,grade_second]