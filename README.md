# auto_buy_lotto

참고 페이지 : https://velog.io/@king/githubactions-lotto

<참고페이지 대비 변경점>
1. Github의 Secrets을 통해, User ID/PW 인자값 전달되도록 변경 및 여러 사용자들 실행
  * python ./buy_lotto.py ${{secrets.USER_ID}} ${{secrets.USER_PW}}
  * python ./buy_lotto.py ${{secrets.USER_ID_2}} ${{secrets.USER_PW_2}}}   
2. 모두 완료후, 로그아웃
3. 예외처리 (초과구매시, 다른 팝업으로 이동되어 정상실행 안됨 ("closeLayer", try except 예외처리)
4. lotton_prediction 함수 구현
  * 가장많이 뽑힌/적게 번호 & (보너스번호 포함)가장많이 뽑힌/적게 번호  => 4가지 조합의 번호 확인
5. "혼합선택"으로 선택하여, 원하는 번호들로 구매 가능  (4번의 조합을 구매에 활용)
