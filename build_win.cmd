pyinstaller -F -c ^
            --hide-console hide-early ^
            --collect-binaries webui ^
            --add-data stre.js:. ^
            --icon strapp.ico ^
            strapp.py
