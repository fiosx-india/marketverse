# modules/guardian_config.py

PROJECT_NAME = "MarketVerse AI"

WATCH_MODULES = [
    "app.py",

    "modules/news.py",
    "modules/news_analysis.py",
    "modules/ai_engine.py",
    "modules/market_events.py",
    "modules/market_scanner.py",
    "modules/performance_tracker.py",
    "modules/trade_executor.py",
    "modules/system_manager.py",
    "modules/dashboard_utils.py",
]

IGNORE_FOLDERS = [
    "__pycache__",
    ".git",
    ".streamlit",
    "logs"
]

ALLOWED_EXTENSIONS = [
    ".py"
]
