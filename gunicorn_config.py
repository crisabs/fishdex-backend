import os

workers = int(os.getenv("WEB_CONCURRENCY", "3"))
bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"

loglevel = "debug"

accesslog = "-"
errorlog = "-"

capture_output = True
