create-version-file.exe version-metadata.yml --outfile version-metadata.txt
pyinstaller --clean --noupx --onefile --runtime-tmpdir . --icon=icon.ico --name TwitchGenshinWishSim --version-file version-metadata.txt main.py
copy dist\TwitchGenshinWishSim.exe pack\
copy config.json pack\
copy messages.json pack\
copy icon.png pack\
xcopy background\ pack\background\ /E/I
xcopy fonts\ pack\fonts\ /E/I
xcopy images\ pack\images\ /E/I
xcopy sound\ pack\sound\ /E/I
xcopy banners\ pack\banners\ /E/I