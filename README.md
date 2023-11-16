*Эта страница доступна на русском языке, смотри [README_RU](https://github.com/dzmuh97/genshin-twitch-wish/blob/master/README_RU.md)*

# **Genshin Wish Twitch Simulator**

*genshin-twitch-wish is not related to HoYoverse. Genshin Impact, content and game materials are trademarks and belong HoYoverse.*

*This simulator uses content and materials from Honey Impact - Genshin Impact DB and Tools.*

![Example](https://media.discordapp.net/attachments/706496930414592080/980878745894260806/dCB9_I5UULE.jpg)
![Example](https://media.discordapp.net/attachments/873930944560648254/1151323661706461204/image.png)

Simulator is written in Python and uses PyGame to display animation, TwitchIO for interaction with chat and rewards on broadcast.

Features:
 - [x] Database of characters and items is relevant for patch `4.1`, is updated with release of updates in game
 - [x] Both single wishes and multiple wishes are supported (from 2 to infinity)
 - [x] Broadcast's chat and the usage of channel points by viewers are supported
 - [x] Custom backgrounds usage (even animated), sounds and fonts are supported
 - [x] Setting time and display stages of animations are available (showing viewer's nickname, fall animation, wish result animation)
 - [x] Recording history of viewers' wishes in `CSV` format
 - [x] Rendering history of viewers' wishes in `HTML` format
 - [x] Full customization of all chances and soft pity in wishes
 - [x] Full customization of chat-bot messages and channel points
 - [x] Full customization of banners and wish drop
 - [x] Chat-bot can do wishes by itself and prompts viewers when they can use commands again (by timeout)
 - [x] Service chat-bot commands to mute sound or stop simulator (pause) during important moments of broadcast
 - [x] Different languages for text and items are supported
 - [x] Opportunity to get skins


## Settings

Follow the link to the latest [release](https://github.com/dzmuh97/genshin-twitch-wish/releases/latest), download archive `genshin-twitch-wish_win64.zip`, unpack to any convenient folder. Simulator consists of:
- **banners** - folder, banners gor simulator
- **sound** - folder, sounds for animations
- **logs** - folder, simulator log files
- **images** - folder, sprites for simulator
- **fonts** - folder, fonds for text
- **background** - folder, background sprites for animations
- **text** - folder, all text files
- **ui** - folder, UI files
- **TwitchGenshinWishSim.exe** - simulator itself
- **icon.png** - icon for simulator window
- **config.json** - settings file
- **config_def.json** - default settings file
- **messages.json** - file with messages for simulator and chat-bot
- **auth.json** - will appear after the first launch, file with Twitch tokens
- **database.sqlite** - will appear after the first launch, database with viewers' actions

Test mode is enabled by default. Simulator can be lauched immediately `TwitchGenshinWishSim.exe` to look at the result of `100` test wishes. Test mode is disabled in configuration file, **test_mode** parameter

<details><summary>OBS settings</summary>

In order for simulator to be displayed on broadcast, it is needed to add a window capture to OBS:
![Window capture](https://media.discordapp.net/attachments/706496930414592080/980878746200453120/Sxxgzt6h_Ao.jpg)

And configure filter for the window transparency to work correctly:
![Filter window](https://media.discordapp.net/attachments/706496930414592080/980878745659375726/1HahxRWaJBF1kzE3BaChFSsMspC-LWBOcPf-kcj_f9g52D-Ia53P2osjQkR4F4wZXmfmu2-Gaavy5D7rU78ilhnS.jpg)

</details>

There are 2 types of bots which are used in simulator: chat-bot - reading messages from chat (section **chat_bot**), channel points bot -  waiting for the use of rewards by viewers (section **event_bot**). Since these bots work separately from each other, there are 2 configuration options:

 - Use different Twitch accounts. The first one will work as a chat-bot, and the second as a streamer account, for channel points
 - Use one account for both chat-bot and channel points

Setting up accounts will be offered at the first launch. Setup is automatic and interactive, just follow the instructions and answer y or n (y - yes, n - no). When file `auth.json` will be created, simulator will no longer offer to set up accounts

<details><summary>Receiving tokens manually through own app</summary>

### Application registration on Twitch

*This and the following sections can be skipped if the interactive setup worked*

Log into main Twitch account, go to [developer console](https://dev.twitch.tv/console/apps), click `Register Your Application` 
![developer console](https://media.discordapp.net/attachments/706496930414592080/984117056448372806/unknown.png)

Fill in order:
 - Application name (must be unique, you can add channel name)
 - Link where token will be transferred, indicate `https://twitchtokengenerator.com`
 - Category `Chat Bot`

Solve captcha and confirm the creation of the application
![enter image description here](https://media.discordapp.net/attachments/706496930414592080/986298587069710336/unknown.png)

Go back to list of all applications and select the just created one, click `Manage`
![application data](https://media.discordapp.net/attachments/706496930414592080/984119131135672370/unknown.png)

Click `New Secret`, new field will appear. Leave the current data tab open.

### Creating token

Open in new tab (data tab, if it exist, then do not close it) [Twitch token generator](https://twitchtokengenerator.com/), click `Uhhhh what? Just take me to the site`
![fill in fields with data from previous tab](https://media.discordapp.net/attachments/706496930414592080/984120049344335922/unknown.png)

Fill in fields with data from previous tab (if the previous paragraph was skipped, then do not touch)



If the same account will be used for chat-bot and channel points, then select the following points:

 - **chat:read** - to read messages from chat
 - **chat:edit** - to write in chat
 - **channel:read:redemptions** - to see channel points usage

If different accounts will be used:

 -  For chat-bot select:
	 - **chat:read** - to read messages from chat
	 - **chat:edit** - to write in chat
  - For channel points bot (account, *which will be used to broadcast*):
	 - **channel:read:redemptions** - to see channel points usage

![if using the same account](https://media.discordapp.net/attachments/706496930414592080/984121657838932018/unknown.png) 
Scroll to the bottom of list and click `Generate Token!` Be sure to check that name of application (if created) and name of desire account are indicated at the top of page. We'll be transferred to the previous page after that

![there will be token](https://media.discordapp.net/attachments/706496930414592080/984123646178107422/unknown.png)
Copy token and paste it into configuration file `config.json`:
 - if the same account will be used for chat-bot and channel points: 
   - paste token in **bot_token** and **channel_token**
 - if different accounts will be used:
   - token received for streamer account (which *will be used to broadcast* and for which there was selected point *channel:read:redemptions*) paste in **channel_token**
   - log out of Twitch account
   - log in to account which will be used as chat-bot
   - repeat steps from [Creating token](#creating-token) (token generator page will need to be refreshed after re-entering another Twitch account)
   - paste the second token in **bot_token** (there must be *chat:read* and *chat:edit* points)

</details>

## Description `config.json`
 
 - **window_name** - window's name for OBS capture
 - **banner** - banner's name from `banners` folder, which will use simulator
 - **chat_bot** - section for chat-bot settings
   - **enabled** - enable or disable section (true or false)
   - **wish_command** - command the bot is responding to
   - **wish_command_prefix** - command prefix
   - **wish_global_timeout** - general limit for all users per bot commands (in seconds)
   - **wish_timeout** - how often each user can use bot commands (in seconds)
     - **broadcaster** - for broadcaster
     - **mod** - for moderators
     - **vip** - for VIP viewers
     - **turbo** - for Twitch Turbo viewers
     - **subscriber** - for subscribers
     - **user** - for everyone else
   - **send_notify** - whether to send chat notification when user can use **wish_command** again
   - **wish_count** - number of wishes that will be done in one use of command
   - **self_wish** - mode in which bot uses the command by itself
   - **self_wish_every** - how often bot will use the command (if enabled)
   - **enable_colors** - enable colored nickname
 - **event_bot** - section for channel points settings
   - **enabled** - enable or disable section (true or false)
   - **default_color** - color for nicknames
   - **rewards** - section for rewards for channel points settings
     - **event_name** - name of reward
     - **wish_count** - number of wishes that will be done by using
 - **animations** - section for animations settings
   - **chroma_color** - chromakey color
   - **draw_states** - stages of animation that will be shown when the wish is performed
     - **draw_usertext** - viewer nickname output with text and **user_background** (if enabled)
     - **draw_fall** - star fall animation output
     - **draw_wishes** - wish result animation output
   - **start_delay** - how long nickname of user who done wish will be shown (in seconds)
   - **end_delay** - how long wish result will be shown (in seconds) if only 1 wish was done
     - **3** - for 3★
     - **4** - for 4★
     - **5** - for 5★
   - **end_delay_multi** - how long wish result will be shown (in seconds) if more than 1 wish was done
     - **3** - for 3★
     - **4** - for 4★
     - **5** - for 5★
   - **user_background** - section for user backgrounds settings
     - **enabled** - enable or disable section (true or false)
     - **path** - name of file in background folder (just file name, not the full path)
     - **type** - background type, `static` for JPG or PNG, `gif` for GIF (video files like `.mp4` may also work)
   - **font** - section for fonts and text settings
     - **path** - name of file in fonts (just file name, not the full path)
     - **user_uid_size** - text size for displaying user's nickname in the lower right corner
     - **wish_name_size** - text size for splash animation (weapon names and character names)
   - **fps** - animation refresh rate (all animations are set to 30 frames per second)
 - **sound** - section for sound settings (all files must be in **sound** folder)
   - **enabled** - enable or disable section (true or false)
   - **fall** - for fall animation
   - **3** - during splash animation for 3★
   - **4** - during splash animation for 4★
   - **5** - during splash animation for 5★
 - **history_file** - section for wish history settings
   - **enabled** - enable or disable section (true or false)
   - **path** - file name (not the full path, along with file type), where history will be written
   - **3** - whether to write 3★
   - **4** - whether to write 4★
   - **5** - whether to write 5★
 - **language** - section for language simulator settings, type file name (without file type) from folder `text`
   - **text** - text language in simulator, logs and error messages
   - **wish_items** - items language in simulator (must be same as language in **banner** banner)
   - **messages** - chat messages language
   - **html_template** - template file for render wish history to HTML
 - **gbot_config** - section for service commands settings
   - **gbot_command** - command for which settings apply (all commands are [here](#service-commands))
     - **enabled** - enable or disable command (true or false)
     - **timeout** - how often command can be used (in seconds)
     - **permissions** - what categories of viewers command is available to
       - **broadcaster** - for broadcaster
       - **mod** - for moderators
       - **vip** - for VIP viewers
       - **turbo** - for Twitch Turbo viewers
       - **subscriber** - for subscribers
       - **user** - for everyone else
 - **send_dev_stats** - enable or disable sending anonymous statistics
 - **test_mode** - test mode, Twitch bot does not turn on, 100 wishes are automatically done

## Description `messages.json`

Blocks with text that the simulator or chat-bot uses at runtime are listed here. You can add or delete lines to each block. There must be at least 1 line in each block

- **user_splash_text** - displayed during the first stage of animation under viewer's nickname
- **chatbot_text** - chat-bot uses in responses to viewers in broadcast's chat
- **notify_text** - used to remind viewers when their timeout ends
- **channel_points_text** - used to respond to viewers who have used channel points
- **status_message** - one line, text for service command **gbot_status**
- **stats_message** - one line, text for service command **gbot_stats**

## Parameters in chat-bot responses to viewers

In bot messages you can specify parametres:
 - Common for blocks **chatbot_text** and **channel_points_text**
   - **username** - mention of user who used command
   - **wish_count** - how many wishes user has done in total
   - **wish_count_w4** - how many wishes have been done since the last 4★
   - **wish_count_w5** - how many wishes have been done since the last 5★
   - **wishes_in_cmd** - how many wishes will be done for using command
   - **que_num** - number in wish queue
 - For block **chatbot_text**
   - **user_wish_delay** - how long user will have to wait before using the next command (parameter **wish_timeout**)
   - **global_wish_delay** - how often whole chat can use the command
 - For block **channel_points_text**
   - **reward_cost** - value of reward in channel points, which was activated by user
 - For block **notify_text**
   - **username** - mention of user who used command
   - **command** - command in form **wish_command_prefix** + **wish_command**
 - For block **user_splash_text**
   - **wish_count** - how many wishes user has done in total
   - **wishes_in_cmd** - how many wishes will be done for using command
   - **gems_in_cmd** - how much wishes cost in primogems
 - For **status_message**
   - **user_mention** - viewer who wrote command
   - **proj_name** - simulator name
   - **proj_ver** - simulator version
   - **proj_url** - link to github simulator page
   - **wcommand** - wish command for chat-bot
   - **wcommand_c** - how many `wcommand` were used
   - **rcommand_c** - how many commands for channel points were used
   - **wish_points** - how many channel points were spent by viewers on wishes
   - **wish_gems** - how many primogems were spent by viewers (total wishes * 160)
   - **wish_queue_size** - wishes queue size
 - For **stats_message**
   - **user_mention** - viewer who wrote command
   - **user_wish_all** - how many wishes were done by viewer
   - **user_wish_epic** - how many wishes have been done since the last guaranteed 4★
   - **user_wish_leg** - how many wishes have been done since the last guaranteed 5★
   - **user_primo** - how many primogems were spent by viewer (viewer's wishes * 160)

## Banners

Simulator uses banner system similar to the game's. Customizable banners are in `banners` folder. `all_in_one.json` banner is enabled by default, which contains all items (weapons, characters and skins)

Each banner is `JSON` file:

 - **banner_name** - banner name
 - **wish_fo_garant** - how many wishes user need to do before the guaranteed 4★
 - **wish_fo_chance** - overall chance of getting 4★ (from 0.01 to 99.99)
 - **wish_fi_garant** - how many wishes user need to do before the guaranteed 5★
 - **wish_fi_chance** - overall chance of getting 5★ (from 0.01 to 99.99)
 - **wish_fi_soft_a** - after what wish will soft pity start working (shold be less than **wish_fi_garant**)
 - **wishes** - section with banner items

Inside **wishes** are sections **5**, **4** and **3** that indicate the number of stars that item has. Inside each of them are items available for this banner:

 - **char** - characters and skins
 - **weapon** - weapons
 - **garant** - guaranteed items and 50/50 system

All sections must contain at least one item, if there is at least one item in **garant**, then the system of guaranteed items will work

<details><summary>List of all available items for banners</summary>

Characters, 5★
 - `Albedo`
 - `Kamisato Ayaka`
 - `Kamisato Ayato`
 - `Diluc`
 - `Eula`
 - `Ganyu`
 - `Hu Tao`
 - `Arataki Itto`
 - `Jean`
 - `Kaedehara Kazuha`
 - `Keqing`
 - `Klee`
 - `Sangonomiya Kokomi`
 - `Yae Miko`
 - `Mona`
 - `Qiqi`
 - `Raiden Shogun`
 - `Shenhe`
 - `Tartaglia`
 - `Venti`
 - `Xiao`
 - `Yoimiya`
 - `Zhongli`
 - `Aloy`
 - `Yelan`
 - `Tighnari`
 - `Nilou`
 - `Cyno`
 - `Nahida`
 - `Wanderer`
 - `Alhaitham`
 - `Baizhu`
 - `Dehya`
 - `Lyney`
 - `Neuvillette`
 - `Wriothesley`
 - `Furina`
 - `Navia`

Weapons, 5★
 - `Haran Geppaku Futsu`
 - `Mistsplitter Reforged`
 - `Skyward Blade`
 - `Aquila Favonia`
 - `Summit Shaper`
 - `Freedom-Sworn`
 - `Primordial Jade Cutter`
 - `Key of Khaj-Nisut`
 - `Song of Broken Pines`
 - `The Unforged`
 - `Skyward Pride`
 - `Redhorn Stonethresher`
 - `Wolf’s Gravestone`
 - `Calamity Queller`
 - `Engulfing Lightning`
 - `Staff of Homa`
 - `Vortex Vanquisher`
 - `Primordial Jade Winged-Spear`
 - `Skyward Spine`
 - `Staff of the Scarlet Sands`
 - `Elegy for the End`
 - `Polar Star`
 - `Skyward Harp`
 - `Amos’ Bow`
 - `Thundering Pulse`
 - `Aqua Simulacra`
 - `Hunter’s Path`
 - `Memory of Dust`
 - `Skyward Atlas`
 - `Lost Prayer to the Sacred Winds`
 - `Kagura’s Verity`
 - `Everlasting Moonglow`
 - `A Thousand Floating Dreams`
 - `Tulaytullah’s Remembrance`
 - `The First Great Magic`
 - `Beacon of the Reed Sea`
 - `Jadefall’s Splendor`
 - `Light of Foliar Incision`
 - `Cashflow Supervision`
 - `Tome of the Eternal Flow`
 - `Splendor of Tranquil Waters`
 - `Considered Judgment`

Characters, 4★
 - `Amber`
 - `Barbara`
 - `Beidou`
 - `Bennett`
 - `Chongyun`
 - `Diona`
 - `Fischl`
 - `Gorou`
 - `Kaeya`
 - `Lisa`
 - `Ningguang`
 - `Noelle`
 - `Razor`
 - `Rosaria`
 - `Kujou Sara`
 - `Sayu`
 - `Sucrose`
 - `Thoma`
 - `Xiangling`
 - `Xingqiu`
 - `Xinyan`
 - `Yanfei`
 - `Yun Jin`
 - `Kuki Shinobu`
 - `Shikanoin Heizou`
 - `Dori`
 - `Collei`
 - `Candace`
 - `Layla`
 - `Faruzan`
 - `Freminet`
 - `Kaveh`
 - `Lynette`
 - `Yaoyao`
 - `Kirara`
 - `Mika`
 - `Charlotte`
 - `Chevreuse`

Weapons, 4★
 - `Blackcliff Longsword`
 - `The Black Sword`
 - `Sacrificial Sword`
 - `Iron Sting`
 - `Prototype Rancour`
 - `Festering Desire`
 - `The Flute`
 - `Favonius Sword`
 - `Sword of Descension`
 - `Royal Longsword`
 - `Cinnabar Spindle`
 - `Lion’s Roar`
 - `The Alley Flash`
 - `Amenoma Kageuchi`
 - `Prized Isshin Blade`
 - `Prized Isshin Blade`
 - `Kagotsurube Isshin`
 - `Sapwood Blade`
 - `Xiphos’ Moonlight`
 - `Blackcliff Slasher`
 - `Sacrificial Greatsword`
 - `Prototype Archaic`
 - `The Bell`
 - `Serpent Spine`
 - `Royal Greatsword`
 - `Katsuragikiri Nagamasa`
 - `Lithic Blade`
 - `Snow-Tombed Starsilver`
 - `Rainslasher`
 - `Favonius Greatsword`
 - `Luxurious Sea-Lord`
 - `Whiteblind`
 - `Akuoumaru`
 - `Forest Regalia`
 - `Makhaira Aquamarine`
 - `Blackcliff Pole`
 - `Deathmatch`
 - `Wavebreaker’s Fin`
 - `Prototype Starglitter`
 - `Crescent Pike`
 - `Kitain Cross Spear`
 - `Royal Spear`
 - `Favonius Lance`
 - `Dragonspine Spear`
 - `Lithic Spear`
 - `Dragon’s Bane`
 - `“The Catch”`
 - `Moonpiercer`
 - `Missive Windspear`
 - `Blackcliff Warbow`
 - `Sacrificial Bow`
 - `Predator`
 - `Hamayumi`
 - `Compound Bow`
 - `Rust`
 - `Prototype Crescent`
 - `Alley Hunter`
 - `Windblume Ode`
 - `Mouun’s Moon`
 - `Royal Bow`
 - `The Viridescent Hunt`
 - `Mitternachts Waltz`
 - `Favonius Warbow`
 - `The Stringless`
 - `Fading Twilight`
 - `King’s Squire`
 - `End of the Line`
 - `Blackcliff Agate`
 - `Sacrificial Fragments`
 - `Solar Pearl`
 - `Prototype Amber`
 - `Frostbearer`
 - `The Widsith`
 - `Eye of Perception`
 - `Oathsworn Eye`
 - `Mappa Mare`
 - `Royal Grimoire`
 - `Hakushin Ring`
 - `Favonius Codex`
 - `Dodoco Tales`
 - `Wine and Song`
 - `Fruit of Fulfillment`
 - `Wandering Evenstar`
 - `Toukabou Shigure`
 - `Ballad of the Fjords`
 - `Finale of the Deep`
 - `Fleuve Cendre Ferryman`
 - `Flowing Purity`
 - `Mailed Flower`
 - `Ibis Piercer`
 - `Rightful Reward`
 - `Sacrificial Jade`
 - `Scion of the Blazing Sun`
 - `Song of Stillness`
 - `Talking Stick`
 - `Tidal Shadow`
 - `Wolf-Fang`
 - `Ballad of the Boundless Blue`
 - `The Dockhand’s Assistant`
 - `Portable Power Saw`
 - `Prospector’s Drill`
 - `Range Gauge`
 - `Sword of Narzissenkreuz`
 - `"Ultimate Overlord's Mega Magic Sword"`

Weapons, 3★
 - `Cool Steel`
 - `Fillet Blade`
 - `Dark Iron Sword`
 - `Harbinger of Dawn`
 - `Traveler’s Handy Sword`
 - `Skyrider Sword`
 - `White Iron Greatsword`
 - `Bloodtainted Greatsword`
 - `Ferrous Shadow`
 - `Debate Club`
 - `Skyrider Greatsword`
 - `Black Tassel`
 - `White Tassel`
 - `Halberd`
 - `Slingshot`
 - `Messenger`
 - `Raven Bow`
 - `Sharpshooter’s Oath`
 - `Recurve Bow`
 - `Thrilling Tales of Dragon Slayers`
 - `Magic Guide`
 - `Otherworldly Story`
 - `Twin Nephrite`
 - `Emerald Orb`
 - `Amber Bead`

Skins, 4★ and 5★
 - `Summertime Sparkle`
 - `Sea Breeze Dandelion`
 - `Orchid’s Evening Gown`
 - `Opulent Splendor`
 - `Ein Immernachtstraum`
 - `To the Church’s Free Spirit`
 - `Pact of Stars and Moon`
 - `100% Outrider`
 - `Gunnhildr’s Legacy`
 - `Sailwind Shadow`
 - `Blossoming Starlight`
 - `Springbloom Missive`
 - `Red Dead of Night`

</details>

## Service commands

All commands are preceded by prefix from **wish_command_prefix**

 - **gbot_stats** - displays statistics of wishes in chat
 - **gbot_status** - displays information about simulator
 - **gbot_sound** - turn sound on and off during wishes
 - **gbot_pause** - toggles wishes procesing on and off. Bot will still respond to using channel points or chat commands, but wish animations will not play, and all wishes will be in queue until processing is enabled again
 - **gbot_history** - will generate wish history in html for the viewer who used command and send public link to view it
 - **gbot_history_all** - same as `gbot_history`, but for all viewers

*Project collects anonymous statistics. It includes start time and channel name from configuration file. No personal data, IP addresses or tokens from channels/bots are transmitted.*