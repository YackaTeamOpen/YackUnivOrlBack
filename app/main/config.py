import os

environments = {
    "local": {
        "env_name": "local",
        "db": "mysql+pymysql://admin_yackuniv:YackUnivDbPass@localhost/yackunivdb",
        "host": "127.0.0.1",
        "server_port": 5000,
        "debug": True,
        "api_app_path": "./app/",
        "api_url": "http://localhost:5000",
        "web_manager_url": "http://localhost:3000",
        "app_url": "*",
        "smtp_server": "ssl0.ovh.net",
        "mail": "ne-pas-repondre-test@yackapp.fr",
        "mail_pass": "YackUnivMailPass",
        "secret_key": "YackUnivOrlKey",
        "permanent_session_lifetime_days": 30,
        "remember_cookie_duration_minutes": 120,
        "session_cookie_secure": None,
        "session_cookie_httponly": False,
        "lat_to_meters": 111000,  # équivalence degrés de latitude - mètres en CVL *
        "long_to_meters": 74870,  # équivalence degrés de longitude - mètres en CVL
        "avatar_size" : 60,
    },
    "test":{
        "password": "6aa07aaf6f8a0a553d257f048770304d483c92fdfea159c7ebcdbe3b72df49ea"
    }
}

config_name = os.environ.get("FLASK_ENV", "local")
os.environ["PASSWORD_TEST"]="6aa07aaf6f8a0a553d257f048770304d483c92fdfea159c7ebcdbe3b72df49ea"
password_user=os.environ["PASSWORD_TEST"]
