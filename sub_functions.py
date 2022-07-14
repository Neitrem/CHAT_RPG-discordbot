def TimeString(time_sec: int) -> str:
    """Creating time string from amount if seconds"""
    res: str = ""
    if time_sec // 31104000 > 0:
        res += f"{time_sec // 31104000} Y"
        time_sec = time_sec % 31104000
    if time_sec // 1036800 > 0:
        res += f"{time_sec // 2592000} M"
        time_sec = time_sec % 2592000
    if time_sec // 86400 > 0:
        res += f"{time_sec // 86400} D"
        time_sec = time_sec % 86400
    if time_sec // 3600 > 0:
        res += f"{time_sec // 3600} h"
        time_sec = time_sec % 3600
    if time_sec // 60 > 0:
        res += f"{time_sec // 60} m"

    return res
