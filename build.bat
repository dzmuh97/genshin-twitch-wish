create-version-file.exe version-metadata.yml --outfile version-metadata.txt
pyinstaller --clean --noupx --onefile --runtime-tmpdir . --icon=icon.ico --name TwitchGenshinWishSim --version-file version-metadata.txt main.py
copy dist\TwitchGenshinWishSim.exe genshin-twitch-wish_win64\
copy config.json genshin-twitch-wish_win64\
copy messages.json genshin-twitch-wish_win64\
copy icon.png genshin-twitch-wish_win64\
xcopy background\ genshin-twitch-wish_win64\background\ /E/I
xcopy fonts\ genshin-twitch-wish_win64\fonts\ /E/I
xcopy images\ genshin-twitch-wish_win64\images\ /E/I
xcopy sound\ genshin-twitch-wish_win64\sound\ /E/I
xcopy banners\ genshin-twitch-wish_win64\banners\ /E/I