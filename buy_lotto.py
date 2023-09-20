from playwright.sync_api import Playwright, sync_playwright
import time
import sys
import requests

# 동행복권 아이디와 패스워드를 설정
USER_ID = sys.argv[1]
USER_PW = sys.argv[2]
SEL_AUTO = sys.argv[3]

def lotton_prediction():
    # 총 횟수 확인 (23/9/19 기준 1085회까지 진행됨)
    print("로또 현재 회차 찾기 ...")
    num=1085
    while True:
        url="https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=" + str(num)
        req=requests.get(url)
        result=req.json()
        if result.get("returnValue") == "fail":
            break
        num+=1

    print("로또 번호 크롤링 ...")
    count_num = {key: 0 for key in range(1, 46)}
    count_bonus = {key: 0 for key in range(1, 46)}
    for i in range(1, num):
        url="https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo="+str(i)
        req=requests.get(url)
        result=req.json()
        count_num[int(result["drwtNo1"])] += 1
        count_num[int(result["drwtNo2"])] += 1
        count_num[int(result["drwtNo3"])] += 1
        count_num[int(result["drwtNo4"])] += 1
        count_num[int(result["drwtNo5"])] += 1
        count_num[int(result["drwtNo6"])] += 1
        count_bonus[int(result["bnusNo"])] += 1

    global top_6_keys
    global bottom_6_keys
    global combined_count
    top_6_keys = sorted(count_num, key=lambda k: count_num[k], reverse=True)[:6]
    bottom_6_keys = sorted(count_num, key=lambda k: count_num[k])[:6]
    combined_count = {key: count_num[key] + count_bonus[key] for key in range(1, 46)}

    print("<", (num-1), "> 회차 까지 !!!")    
    print("가장 많이 뽑힌 번호:", sorted(top_6_keys))
    print("가장 적게 뽑힌 번호:", sorted(bottom_6_keys))
    print("[보너스포함] 가장 많이 뽑힌 번호:", sorted(sorted(combined_count, key=lambda k: combined_count[k], reverse=True)[:6]))
    print("[보너스포함] 가장 적게 뽑힌 번호:", sorted(sorted(combined_count, key=lambda k: combined_count[k])[:6]))

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
        manual_select(page, (top_6_keys))
        manual_select(page, (bottom_6_keys))
        manual_select(page, sorted(combined_count, key=lambda k: combined_count[k])[:6])
        manual_select(page, sorted(combined_count, key=lambda k: combined_count[k], reverse=True)[:6])
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
    lotton_prediction()

with sync_playwright() as playwright:
    run(playwright)
