# flask 활용하여 게시판 구현
```bash
flask를 활용하여 게시판을 구현
로그인/회원가입 기능을 추가하였음
게시판 글쓰기, 수정 시 관리자 계정으로만 수정 가능하게 구현하였음
-> 관리자 계정은 id=1 인 계정(제일 처음 생성한 계정)
```
## 개발환경
```bash
flask
```

## 환경 구축
```bash
$ pip install -r requirements.txt
$ pip install pymysql
```

## mysql DB 구축
```sql
CREATE DATABASE login;
USE login;

CREATE TABLE login_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL,
    user_type ENUM('teacher', 'general') NOT NULL,
    affiliation VARCHAR(100) NOT NULL,
    position VARCHAR(100) NOT NULL,
    agree_terms BOOLEAN NOT NULL
);

CREATE TABLE posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
