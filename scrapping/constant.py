LOGIN_URL = "https://smartid.ssu.ac.kr/Symtra_sso/smln_pcs.asp"
PORTAL_URL = "https://saint.ssu.ac.kr/irj/portal"
GRADE_URL = 'https://ecc.ssu.ac.kr/sap/bc/webdynpro/sap/ZCMB3W0017'
SAPTOKEN_URL = "https://saint.ssu.ac.kr/webSSO/sso.jsp?sToken="


SESSION_HEADERS = {
    'Accept': '*/*',
    'Accept-Encoding': "gzip, deflate, br",
    "Accept-Language": "ko-KR",
    'Connection': 'keep-alive',
    'Host': "ecc.ssu.ac.kr",
    'Sec-Fetch-Dest': 'documnet',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'X-XHR-Logon': 'accept',
    'Upgrade-Insecure-Requests': '1',
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}

# NEW_SESSION_HEADERS = {
#     'Accept': '*/*',
#     "Accept-Language": "ko-KR",
#     # 'Connection': 'keep-alive',
#     # 'Host': "ecc.ssu.ac.kr",
#     'Sec-Fetch-Dest': 'empty',
#     'Sec-Fetch-Mode': 'cors',
#     'Sec-Fetch-Site': 'same-origin',
#     'X-XHR-Logon': 'accept',
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
# }