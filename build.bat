pyinstaller --onefile --icon=icon.ico --name TwitchGenshinWishSim main.py
del logs\*.* /F/Q
copy dist\TwitchGenshinWishSim.exe pack\
copy config.json pack\
copy icon.png pack\
xcopy background\ pack\background\ /E/I
xcopy fonts\ pack\fonts\ /E/I
xcopy images\ pack\images\ /E/I
xcopy sound\ pack\sound\ /E/I
xcopy logs\ pack\logs\ /E/I
pause