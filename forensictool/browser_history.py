import sqlite3
import os
from collections import Counter

def connect_to_chrome_history():
    chrome_history_path = os.path.expanduser('~') + '/AppData/Local/Google/Chrome/User Data/Default/History'
    try:
        return sqlite3.connect(chrome_history_path)
    except sqlite3.OperationalError as e:
        print(f"데이터베이스 연결에 실패했습니다: {e}")
        return None
    
def fetch_cookies():
    cookies_path = os.path.expanduser('~') + '/AppData/Local/Google/Chrome/User Data/Default/Cookies'
    try:
        conn = sqlite3.connect(cookies_path)
        cursor = conn.cursor()
        cursor.execute("SELECT host_key, name, value FROM cookies;")
        cookies = cursor.fetchall()
        cursor.close()
        conn.close()
        return cookies
    except sqlite3.OperationalError as e:
        print(f"쿠키 데이터베이스 연결에 실패했습니다: {e}")
        return []    

def fetch_titles(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT title FROM urls;")
    titles = [title for (title,) in cursor.fetchall()]
    cursor.close()
    return titles

def fetch_custom_query(conn, query_str):
    cursor = conn.cursor()
    cursor.execute(query_str)
    records = cursor.fetchall()
    cursor.close()
    return records

def extract_last_words(titles):
    return [title.split()[-1] for title in titles if title.split()]

def count_words(words):
    return Counter(words)

if __name__ == "__main__":
    browser = input("브라우저를 입력하세요 ex) chrome, edge, firefox: ")

    choice = input("인터넷 사용기록과 쿠키를 선택 하세요 ex) cookie, history: ")
    if choice == "cookie":
        cookies = fetch_cookies()
        for host_key, name, value in cookies:
            print(f"Host: {host_key}, Cookie Name: {name}, Value: {value}")

    elif choice == "history":
        title_list = input("타이틀리스트들을 보여드릴까요? ex)Y,N: ")
        conn = connect_to_chrome_history()
        if conn is not None:
            if title_list == "Y":
                titles = fetch_titles(conn)
                last_words = extract_last_words(titles)
                word_counts = count_words(last_words)
                for word, count in word_counts.items():
                    print(f"{word}: {count}회")
            else:
                text = input("타이틀의 특정 문자열을 검색하세요: ")
                date = input("검색할 날짜를 입력하세요: ")
                conditions = []
                if text:
                    conditions.append(f"title LIKE '%{text}%'")
                if date:
                    conditions.append(f"visit_time BETWEEN '{date} 00:00:00' AND '{date} 23:59:59'")
                query_str = f"SELECT url, datetime((last_visit_time/1000000)-11644473600, 'unixepoch', 'localtime') as visit_time, title FROM urls WHERE {' AND '.join(conditions)} ORDER BY last_visit_time;" if conditions else ""
                records = fetch_custom_query(conn, query_str)
                for url, visit_time, title in records:
                    print(f"URL: {url}, 방문 시간: {visit_time}, 타이틀: {title}")

            conn.close()
