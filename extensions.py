from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = "routes.login"  # 로그인 페이지로 리디렉션될 뷰를 설정합니다.
