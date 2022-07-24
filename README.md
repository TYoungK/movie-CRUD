# MovieCRUD

## 개요
Django Rest Framework를 사용한 Movie CRUD API입니다.<br>
<br>

## 기술
Framework : Django Rest Framework<br>
DataBase : sqlite3<br>
libraries : 
- pillow : Movie 모델에 이미지 필드 사용
- drf_spectacular : API Docs를 생성
<br><br>

## 세팅
가상환경을 생성할 경우 코드를 받은 디렉토리에서 커맨드 창을 열고

-window 명령 프롬프트
```console
python -m venv [가상환경 이름] 
[가상환경 이름]/Scripts/activate.bat
```

-window PowerShell
```console
python -m venv [가상환경 이름] 
[가상환경 이름]/Scripts/activate.ps1
```

-linux
```console
python -m venv [가상환경 이름] 
source [가상환경 이름]/scripts/activate
```
<br>
그 이후 필요한 패키지를 설치하고 마이그레이션을 진행합니다.

```console
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
```

서버를 실행합니다.

`python manage.py runserver`<br>

<br>

## 모델

-Movie : 영화 기본 정보<br>
-Video : Movie를 외래키로 가지며 1:N관계 <br><br>
자세한 내용은 하단의 API 문서에서 볼 수 있습니다.
<br><br>
## 테스트
명령어를 실행하면 제가 작성한 간단한 테스트 케이스를 실행합니다.

`python manage.py test` <br>

현재 디버그 모드로 설정되어 있으므로 서버를 실행 후  localhost:8000 으로 접속하면 DRF에서 제공하는 UI로 테스트해 볼 수 있습니다.
<br><br>

## API Docs

서버 실행 후 아래 url을 브라우저에서 접속하면 상세 내용과 모델 구성을 볼 수 있습니다.

- localhost:8000/docs/swagger
- localhost:8000/docs/redoc




