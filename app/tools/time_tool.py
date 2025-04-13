import datetime
from langchain_core.tools import tool
import logging

# Configure logging
logger = logging.getLogger(__name__)

# 节气表，每年的节气日期 (阳历)
jieqi_table = {
    "小寒": (1, 5),
    "大寒": (1, 20),
    "立春": (2, 3),  # 春季开始
    "雨水": (2, 18),
    "惊蛰": (3, 5),
    "春分": (3, 20),
    "清明": (4, 4),
    "谷雨": (4, 19),
    "立夏": (5, 5),  # 夏季开始
    "小满": (5, 20),
    "芒种": (6, 5),
    "夏至": (6, 21),
    "小暑": (7, 7),
    "大暑": (7, 22),
    "立秋": (8, 7),  # 秋季开始
    "处暑": (8, 23),
    "白露": (9, 7),
    "秋分": (9, 23),
    "寒露": (10, 8),
    "霜降": (10, 23),
    "立冬": (11, 7),  # 冬季开始
    "小雪": (11, 22),
    "大雪": (12, 7),
    "冬至": (12, 21)
}

def get_season(month, day):
    """Get the current season based on solar terms."""
    current_year = datetime.datetime.now().year
    date = datetime.date(current_year, month, day)
    
    # Define season boundaries
    seasons = {
        "春季": (datetime.date(current_year, 2, 3), datetime.date(current_year, 5, 4)),  # 立春 to 立夏前
        "夏季": (datetime.date(current_year, 5, 5), datetime.date(current_year, 8, 6)),  # 立夏 to 立秋前
        "秋季": (datetime.date(current_year, 8, 7), datetime.date(current_year, 11, 6)),  # 立秋 to 立冬前
        "冬季": (datetime.date(current_year, 11, 7), datetime.date(current_year + 1, 2, 2))   # 立冬 to 立春前
    }
    
    for season, (start, end) in seasons.items():
        if start <= date <= end:
            return season
        # Handle winter which spans across year end
        if season == "冬季" and (date >= start or date <= end):
            return season
    
    return "未知季節"

def get_closest_jieqi(month, day):
    """Get the current and next solar term."""
    current_year = datetime.datetime.now().year
    current_date = datetime.date(current_year, month, day)
    jieqi_dates = [(name, datetime.date(current_year, m, d)) for name, (m, d) in jieqi_table.items()]
    jieqi_dates.sort(key=lambda x: x[1])
    
    # Find the current and next solar term
    current_jieqi = None
    next_jieqi = None
    
    for i, (name, date) in enumerate(jieqi_dates):
        if date <= current_date:
            current_jieqi = (name, date)
            next_jieqi = jieqi_dates[(i + 1) % len(jieqi_dates)]
    
    return current_jieqi, next_jieqi

def modern_to_dizhi(hour):
    """Convert modern hour to traditional Chinese time period."""
    time_mapping = {
        23: "子時", 0: "子時",
        1: "丑時", 2: "丑時",
        3: "寅時", 4: "寅時",
        5: "卯時", 6: "卯時",
        7: "辰時", 8: "辰時",
        9: "巳時", 10: "巳時",
        11: "午時", 12: "午時",
        13: "未時", 14: "未時",
        15: "申時", 16: "申時",
        17: "酉時", 18: "酉時",
        19: "戌時", 20: "戌時",
        21: "亥時", 22: "亥時"
    }
    
    return time_mapping.get(hour, "時間格式錯誤")

@tool
def get_time_and_season() -> str:
    """Get current time information including traditional Chinese time, period and season. 
    獲取當前的節氣、時辰
    
    Returns:
        str: A string containing current time information in both modern and traditional formats.
    """
    # Get current date and time
    now = datetime.datetime.now()
    
    # Format time
    formatted_time = now.strftime('%H:%M:%S')
    
    # Get current season
    season = get_season(now.month, now.day)
    
    # Get current and next solar term
    current_jieqi, next_jieqi = get_closest_jieqi(now.month, now.day)
    
    # Get traditional Chinese time period
    traditional_time = modern_to_dizhi(now.hour)
    
    # Combine all information
    result = (
        f"時間：{formatted_time}\n"
        f"時辰：{traditional_time}\n"
        f"季節：{season}\n"
        f"當前節氣：{current_jieqi[0] if current_jieqi else '無'}\n"
        f"下一個節氣：{next_jieqi[0] if next_jieqi else '無'}"
    )

    logger.info(f"Time information: {result}")
    
    return result 