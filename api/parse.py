import re
from bs4 import BeautifulSoup

def parse_grade(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    grade_table = soup.find('tbody', {'id': re.compile('WD0...-contentTBody')})
    column_names = ['이수학년도','이수학기','과목코드','과목명','과목학점','성적','등급','교수명','비고']
    check_text = lambda tag: tag.select_one('span').text if tag else None
    row_datas = [[check_text(td) for td in tr.select('td > span')] for tr in grade_table.select('tr')[1:]]
    grade_data = [{col_name:row_data for col_name, row_data in zip(column_names, row)} for row in row_datas]
    print(grade_data)
    return grade_data
