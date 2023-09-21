from playwright.sync_api import Playwright, sync_playwright
import time
import sys

# 동행복권 아이디와 패스워드를 설정
USER_ID = sys.argv[1]
USER_PW = sys.argv[2]

# 크롤링된 번호를 사용 여부 ("auto":미사용, "manual":사용)
SEL_AUTO = sys.argv[3]

FILE_PATH="./auto_lotto/weekly/count.log"

count_num = {key: 0 for key in range(1, 46)}
count_bonus = {key: 0 for key in range(1, 46)}
combined_count = {key: 0 for key in range(1, 46)}

def load_lotto_count():
    rstr=""
    with open(FILE_PATH, "r") as file:
        rstr = file.read()

    rstr_split=rstr.split("\n")    
    count_num_str = rstr_split[1].split(';')
    count_bonus_str = rstr_split[2].split(';')

    idx=1
    for val in count_num_str:
        if (len(count_num_str) != idx):
            count_num[idx]=int(val)
        idx+=1
    idx=1
    for val in count_bonus_str:
        if (len(count_bonus_str) != idx):
            count_bonus[idx]=int(val)
        idx+=1

    combined_count = {key: count_num[key] + count_bonus[key] for key in range(1, 46)}

def manual_select(page, num_arr):
    print(num_arr)
    for val in num_arr:
        page.click('label:has-text("' + str(val) + '")')
    page.click("text=확인")

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://dhlottery.co.kr/user.do?method=login")
    page.click("[placeholder=\"아이디\"]")
    page.fill("[placeholder=\"아이디\"]", USER_ID)
    page.press("[placeholder=\"아이디\"]", "Tab")
    page.fill("[placeholder=\"비밀번호\"]", USER_PW)
    page.press("[placeholder=\"비밀번호\"]", "Tab")
    with page.expect_navigation():
        page.press("form[name=\"jform\"] >> text=로그인", "Enter")
    time.sleep(5)

    page.goto(url="https://ol.dhlottery.co.kr/olotto/game/game645.do")    
    # "비정상적인 방법으로 접속하였습니다. 정상적인 PC 환경에서 접속하여 주시기 바랍니다." 우회하기
    page.locator("#popupLayerAlert").get_by_role("button", name="확인").click()
    print(page.content())

    if (SEL_AUTO == "manual"):
        page.click("text=혼합선택")
        page.select_option("select", str(1))
        # 4회는 번호선택
        manual_select(page, (sorted(count_num, key=lambda k: count_num[k], reverse=True)[:6]))
        manual_select(page, (sorted(count_num, key=lambda k: count_num[k])[:6]))
        manual_select(page, (sorted(combined_count, key=lambda k: combined_count[k])[:6]))
        manual_select(page, (sorted(combined_count, key=lambda k: combined_count[k], reverse=True)[:6]))
        # 1회는 자동선택
        page.click('label:has-text("자동선택")')
        page.click("text=확인")
    else:
        # 5회 자동선택
        page.click("text=자동번호발급")
        page.select_option("select", str(5))
        page.click("text=확인")

    page.click("input:has-text(\"구매하기\")")
    time.sleep(2)
    page.click("text=확인 취소 >> input[type=\"button\"]")
    try:
        page.click("input[name=\"closeLayer\"]")
    except:
        print("(예외처리) 구매한도초과 팝업에서 closeLayer 버튼 없음")

    page.goto("https://dhlottery.co.kr/user.do?method=logout&returnUrl=")
    context.close()
    browser.close()

if (SEL_AUTO == "manual"):
    load_lotto_count()

with sync_playwright() as playwright:
    run(playwright)
