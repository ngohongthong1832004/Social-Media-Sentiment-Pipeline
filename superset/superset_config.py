# superset_config.py

# SECRET_KEY cần đủ mạnh và ngẫu nhiên
SECRET_KEY = "sjd9as8d7asd7as8d7as8d7as8d7as8d7as8d7asd="

# Một số config cơ bản khác (có thể thêm nếu cần)
# Ví dụ: Giới hạn session tồn tại trong bao lâu (ở đây là 1 ngày)
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False  # Nếu có SSL/HTTPS thì để True
PERMANENT_SESSION_LIFETIME = 86400  # 1 ngày = 86400 giây

# Đặt thêm nếu muốn debug
# DEBUG = False
# ENABLE_PROXY_FIX = True
