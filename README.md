https://github.com/xvzc/boj-cli  
위 파일을 약간 수정한 백준 cli 채점 프로그램, 다중 사용자 버전으로 개선 ( 다중 세션 저장 및 비동기 제출 가능 )
반드시 "파이썬 3.11 버전"이어야 함. ( 필자는 3.11.9 ) 

0. pip install boj-cli ( 파일은 내껄 써야 하지만 수많은 모듈들을 자동으로 설치해줌 )
1. 파이썬 설치 위치/Lib/site-packages 안에 boj 디렉터리가 생겼을 것이다. ( 내 경로 : ~/AppData/Local/Programs/Python/Python311/Lib/site-packages/boj )
2. boj 디렉터리를 본 저장소에 있는 boj로 대체한다.
3. .py , .cpp 파일 등 본인이 제출하고 싶은 소스코드가 있는 디렉터리로 이동 후, .boj/config.yaml 디렉터리와 파일을 만든다.
4. boj init
5. boj login ( 셀레니움 크롤링 브라우저에 백준 로그인 창이 뜬다. 로그인하면 ~/boj-cli/username 디렉터리에 암호화된 세션값과 키가 저장된다 )
6. boj add 문제번호 -t py -f  ( 파이썬 기준, problems/문제번호 디렉터리 생성됨 )
7. problems 디렉터리로 이동 후 "boj run 문제번호" 하면 테스트 케이스 실행됨 ( 제출되는 코드는 문제번호 디렉터리의 main.py 이다 )
8. problems 디렉터리에서 "boj submit 문제번호 {username}" 하면 백준에 코드가 제출되고 결과를 받아볼 수 있음.

config.yaml 파일은 명령어를 python3 $file 에서 py $file로 변경했다. 기존 python3 명령어는 왠지 모르게 출력값이 "Python" 으로 고정되었기 때문.
기타 다른 언어를 사용하는 방법은 원본 깃허브 참고 바람.
