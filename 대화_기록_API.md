과제 내용을 정리하면, 5주차 프로그램에 외부 API를 붙여 기능을 업데이트하고, branch → PR → main merge 흐름으로 제출하는 과제입니다. 마감이 내일(11/4) 자정이라 시간이 빠듯하니, 바로 따라할 수 있게 전체 흐름을 정리해 드릴게요.



1\. 브랜치 만들기

bash

git checkout main

git pull

git checkout -b feature/api

2\. UV 환경 세팅

bash

uv init            # 이미 pyproject.toml이 있으면 생략

uv add requests python-dotenv

uv run main.py     # 실행 확인



pyproject.toml과 uv.lock을 반드시 커밋해야 "재현 가능" 점수(6점)를 받을 수 있습니다. 채점자는 git clone 후 uv sync, uv run main.py만으로 실행할 수 있어야 합니다.



3\. API 키 관리



.env (커밋하지 않음):



API\_KEY=여기에\_실제\_키



.env.example (커밋함, 형식 안내용):



API\_KEY=your\_api\_key\_here



코드에서 불러오기:



python

import os

from dotenv import load\_dotenv



load\_dotenv()

API\_KEY = os.getenv("API\_KEY")

if not API\_KEY:

&#x20;   raise RuntimeError(".env 파일에 API\_KEY를 설정하세요.")

4\. .gitignore (저장소 관리 점수용)

.env

.venv/

\_\_pycache\_\_/

\*.pyc

.DS\_Store

.idea/

.vscode/

5\. 제출해야 할 파일 구성

├── main.py (등 기존 코드)

├── api-plan.md        ← 기획안

├── README.md          ← 3페이지 이내 코드 설명 + 키 설정 방법

├── .env.example

├── .gitignore

├── pyproject.toml

├── uv.lock

└── ai-log/            ← AI와의 대화 원문 (예: conversation.md)



api-plan.md에는 사용할 API와 선택 이유, 추가할 기능, 입력/출력 흐름, 예외 처리 계획(키 없음, 네트워크 오류, 호출 제한) 정도를 적으면 됩니다. README에는 프로젝트 소개, 실행 방법(uv sync, .env 작성법), 코드 구조와 주요 함수 설명, API 호출 흐름을 담으세요. "코드 이해도" 평가 항목이라 본인 말로 설명하는 게 중요합니다. 이 대화도 AI 대화 원문에 포함하면 됩니다.



6\. 커밋과 PR

bash

git add .

git commit -m "Add weather API integration"   # 의미 있는 단위로 나눠 커밋

git push -u origin feature/api



그다음 GitHub에서 Pull Request를 만들고 main에 merge합니다. “fix”, “asdf” 같은 커밋 메시지는 감점 요인이니 피하세요. 제출 전에 git status로 .env가 추적되지 않는지 꼭 확인하세요.



이제 실제 코드를 같이 작성하려면, 5주차 프로그램이 무엇인지 알아야 합니다. 5주차 코드(또는 어떤 프로그램인지 설명)를 보내주시면, 어울리는 API 추천부터 코드 수정, api-plan.md와 README 초안까지 함께 만들어 드릴게요.



.env가 untracked 목록에 보인다는 건 .gitignore가 제대로 작동하지 않고 있다는 뜻이에요. 이대로 git add .을 하면 API 키가 GitHub에 올라가니, 지금은 절대 git add .을 하지 마세요.



1\. 원인 확인

powershell

Get-Content .gitignore

git check-ignore -v .env



check-ignore 결과에 아무것도 안 나오면 .gitignore가 .env를 무시하지 못하고 있는 거예요. 보통 메모장 저장 시 인코딩 문제이거나, .env 줄이 저장이 안 된 경우입니다.



2\. .gitignore 다시 만들기



아래 명령을 통째로 복사해서 PowerShell에 붙여넣으세요. 올바른 인코딩으로 .gitignore를 새로 씁니다.



powershell

@"

\# Python

\_\_pycache\_\_/

\*.py\[oc]

build/

dist/

\*.egg-info

.venv/



\# API key

.env



\# 실행 데이터

todos.json

"@ | Set-Content .gitignore -Encoding ascii



그다음 다시 확인하세요.



powershell

git check-ignore -v .env

git status



.gitignore:12:.env    .env 같은 줄이 나오고, git status에서 .env가 사라지면 해결된 거예요.



3\. "수정된 파일이 많다"는 부분



이건 상황을 봐야 정확히 알 수 있어요. .gitignore를 고친 뒤 나오는 git status 결과를 그대로 복사하거나 캡처해서 보내주세요. 어떤 파일을 커밋하고 어떤 건 빼야 하는지 하나씩 정리해 드릴게요.



지금 이상황이야



아주 좋은 상태예요. 하나씩 보면 다 정상입니다.



git check-ignore 결과에 .gitignore:1:.env가 나왔으니 .env는 제대로 무시되고 있어요. 실제로 git status의 Untracked 목록에도 .env가 없죠. 아까 보신 건 수정 전 상태였던 것 같아요. 그리고 수정된 파일들도 전부 우리가 바꾼 것들이에요. 이름 변경(To do list.py.py → main.py), 날씨 기능 추가(main.py), uv 설정 수정(pyproject.toml, uv.lock), 새 파일 4개입니다.



커밋 전에 확인 하나



uv run main.py가 이제 정상 실행되나요? 실행돼서 날씨 줄이 보이면(키 활성화 전이면 오류 문구라도) 아래로 진행하세요.



커밋하기 (한 줄씩 순서대로)



이미 스테이징된 이름 변경부터 단독으로 커밋합니다.



powershell

git commit -m "Rename To do list.py.py to main.py"

git add pyproject.toml uv.lock

git commit -m "Fix uv config to run as a script project"

git add weather.py

git commit -m "Add OpenWeatherMap forecast client"

git add main.py

git commit -m "Show daily weather and umbrella alert in todo app"

git add api-plan.md .env.example

git commit -m "Add API plan and env example"

git add README.md

git commit -m "Add README"

남은 정리 확인

powershell

git ls-files



여기에 plan.md.md나 todos.json이 보이면 아래도 실행해 주세요. 안 보이면 건너뛰면 돼요.



powershell

git mv plan.md.md plan.md

git rm --cached todos.json

git commit -m "Clean up plan file name and stop tracking todos.json"



다 끝나면 git log --oneline과 git status 결과를 보내주세요. 확인되면 AI 대화 기록 추가하고 push하는 마지막 단계로 넘어갈게요.

