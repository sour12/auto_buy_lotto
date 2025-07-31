from playwright.sync_api import Playwright, sync_playwright
import time
import sys

# 동행복권 아이디와 패스워드를 설정
USER_ID = sys.argv[1]
USER_PW = sys.argv[2]

# 크롤링된 번호를 사용 여부 ("auto":미사용, "manual":사용)
SEL_AUTO = sys.argv[3]

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
    
    # manual_select(page, [2, 3, 7, 12, 14, 22])
        
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

with sync_playwright() as playwright:
    run(playwright)
