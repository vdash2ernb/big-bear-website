@echo off
title Big Bear - Local Website Preview
echo Open http://127.0.0.1:5500 in your browser.
echo Keep this window open while editing. Press Ctrl+C to stop.
python -m http.server 5500 --bind 127.0.0.1 --directory "%~dp0dist"
pause
