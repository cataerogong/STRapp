rd /S /Q build
pyinstaller -F -w --collect-binaries webui --icon strapp.ico strapp.py
