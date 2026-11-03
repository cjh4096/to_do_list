# -*- coding: utf-8 -*-
"""OpenWeatherMap 5일 예보(Forecast) API 연동 모듈
- 외부 라이브러리 없이 표준 라이브러리(urllib, json)만 사용
- .env 파일에서 API 키와 도시 이름을 읽어온다"""
import json, os, urllib.error, urllib.parse, urllib.request
from collections import defaultdict
from datetime import datetime, timedelta, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
API_URL = "https://api.openweathermap.org/data/2.5/forecast"
ICONS = {"Clear": "☀", "Clouds": "☁", "Rain": "🌧", "Drizzle": "🌦", "Thunderstorm": "⛈", "Snow": "❄"}
WET = ("Rain", "Drizzle", "Thunderstorm", "Snow")


def load_env(path=os.path.join(BASE_DIR, ".env")):
    """.env 파일의 KEY=VALUE 줄을 읽어 환경변수로 등록한다."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


class WeatherError(Exception):
    """날씨 정보를 가져오지 못했을 때 화면에 보여줄 메시지를 담는 예외"""


class WeatherClient:
    """OpenWeatherMap 예보를 받아 날짜별 요약으로 바꿔주는 클래스"""

    def __init__(self):
        load_env()
        self.api_key = os.environ.get("OPENWEATHER_API_KEY", "").strip()
        self.city = os.environ.get("WEATHER_CITY", "Seoul,KR").strip()

    def fetch_daily(self):
        """{"YYYY-MM-DD": {"min", "max", "desc", "icon", "rain"}} 형태의 딕셔너리를 반환한다."""
        if not self.api_key:
            raise WeatherError("API 키가 없습니다 (.env 확인)")
        query = urllib.parse.urlencode({"q": self.city, "appid": self.api_key, "units": "metric", "lang": "kr"})
        try:
            with urllib.request.urlopen(f"{API_URL}?{query}", timeout=8) as resp:
                data = json.load(resp)
        except urllib.error.HTTPError as e:
            msg = {401: "API 키가 올바르지 않거나 아직 활성화되지 않았습니다", 404: "도시를 찾을 수 없습니다"}
            raise WeatherError(msg.get(e.code, f"서버 오류 (HTTP {e.code})")) from e
        except (urllib.error.URLError, TimeoutError) as e:
            raise WeatherError("인터넷 연결을 확인하세요") from e
        return self._summarize(data)

    @staticmethod
    def _summarize(data):
        """3시간 간격 예보 목록을 현지 날짜별로 묶어 최저/최고 기온과 대표 날씨를 계산한다."""
        tz = timezone(timedelta(seconds=data["city"].get("timezone", 0)))
        days = defaultdict(list)
        for item in data["list"]:
            local = datetime.fromtimestamp(item["dt"], tz)       # API 시간(UTC) → 현지 시간
            days[local.strftime("%Y-%m-%d")].append((local.hour, item))

        result = {}
        for date, items in days.items():
            temps = [it["main"]["temp"] for _, it in items]
            _, noon = min(items, key=lambda x: abs(x[0] - 12))  # 정오에 가장 가까운 예보를 대표값으로
            main = noon["weather"][0]["main"]
            result[date] = {
                "min": round(min(temps)), "max": round(max(temps)),
                "desc": noon["weather"][0]["description"], "icon": ICONS.get(main, "🌫"),
                "rain": any(it["weather"][0]["main"] in WET for _, it in items),
            }
        return result
