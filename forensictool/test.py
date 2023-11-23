from datetime import datetime, timezone

# 주어진 나노초 타임스탬프
timestamp_in_nano = 133452086226910000

# 나노초를 초로 변환
timestamp_in_seconds = timestamp_in_nano / 1e9

# 에포크 시간 (1970년 1월 1일 00:00:00 UTC)을 기준으로 한 날짜와 시간 계산
datetime_utc = datetime.utcfromtimestamp(timestamp_in_seconds).replace(tzinfo=timezone.utc)

# 결과 출력
print("변환된 날짜와 시간 (UTC):", datetime_utc)