import psycopg2

def connect_with_connector():
    # sslmode=verify-full
    conn = psycopg2.connect("""
        host=rc1a-n3ys01pphw5kvtmp.mdb.yandexcloud.net
        port=6432
        dbname=db1
        user=user1
        password=Qwerty!23
        target_session_attrs=read-write
    """)

    return conn