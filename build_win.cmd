rd /S /Q build
pyinstaller -F -c ^
            --hide-console hide-early ^
            --collect-binaries webui ^
            --icon strapp.ico ^
            strapp.py
