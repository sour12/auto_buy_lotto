# auto_buy_lotto

참고 페이지 : https://velog.io/@king/githubactions-lotto

<참고페이지 대비 변경점>
[buy_lotto.py 수정사항]
1. "혼합선택"으로 선택하여, 크롤링된 번호들로 구매 가능  (4번의 조합을 구매에 활용)

[yml 수정사항]
1. Github의 Secrets을 통해, User ID/PW 인자값 전달되도록 변경 및 여러 사용자들 실행
  * python ./buy_lotto.py ${{secrets.USER_ID}} ${{secrets.USER_PW}}
  * python ./buy_lotto.py ${{secrets.USER_ID_2}} ${{secrets.USER_PW_2}}}   
2. 캐시 restore/delete/save 추가 (크롤링된 번호들 캐쉬에 저장하고, 크롤링시 사용 : 크롤링수행시 시간 오래걸림)

[crawling_lotto.py 추가사항]
1. 가장많이 뽑힌/적게 번호 & (보너스번호 포함)가장많이 뽑힌/적게 번호  => 4가지 조합의 번호 확인가능

<동작주기>
- 월요일 > crawling_lotto.py 실행      : 로또 번호 클롤링 및 캐쉬 업데이트
- 수요일 > buy_lotto.py 실행 (USER #1) : 크롤링된 데이터를 기반으로 번호선택
- 금요일 > buy_lotto.py 실행 (USER #2) : 자동번호 선택
