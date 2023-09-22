GitHub Actions를 사용한 Lotto 번호 선택

이 프로젝트는 GitHub Actions를 활용하여 주기적으로 로또 번호를 선택하는 방법을 보여줍니다. 아래 참고 페이지를 참조하여 크롤링과 GitHub Secrets를 사용한 업데이트를 진행했습니다.

참고 페이지: https://velog.io/@king/githubactions-lotto

buy_lotto.py 수정사항

	1.	“혼합선택”으로 선택 가능하도록 수정되었습니다. 크롤링된 번호들로 번호를 선택할 수 있습니다.

yml 수정사항

	1.	GitHub Secrets을 통해 User ID와 PW를 인자값으로 전달하도록 변경되었습니다. 이로써 여러 사용자가 스크립트를 실행할 수 있습니다.
	•	예시: python ./buy_lotto.py ${{secrets.USER_ID}} ${{secrets.USER_PW}}
	•	예시: python ./buy_lotto.py ${{secrets.USER_ID_2}} ${{secrets.USER_PW_2}}
	2.	캐시 관련 작업이 추가되었습니다. 크롤링된 번호들은 캐시에 저장되고, 크롤링을 수행할 때 사용됩니다. 이렇게 함으로써 크롤링 시간이 줄어듭니다.

crawling_lotto.py 추가사항

	1.	가장 많이 뽑힌/적게 뽑힌 번호 및 보너스 번호까지의 4가지 조합의 번호를 확인할 수 있습니다.

동작 주기

	•	월요일: crawling_lotto.py 실행하여 로또 번호를 크롤링하고 캐시를 업데이트합니다.
	•	수요일: buy_lotto.py 실행 (USER #1): 크롤링된 데이터를 기반으로 번호를 선택합니다.
	•	금요일: buy_lotto.py 실행 (USER #2): 자동으로 번호를 선택합니다.

이 내용을 기반으로 한 리포지토리의 업데이트 내용을 설명해 드렸습니다.