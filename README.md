# **Симулятор молитв Genshin Impact для Twitch**

*genshin-twitch-wish не связан с HoYoverse. Genshin Impact, контент и материалы игры являются товарными знаками и принадлежат HoYoverse.*

![Пример работы](https://media.discordapp.net/attachments/706496930414592080/980878745894260806/dCB9_I5UULE.jpg)

Симулятор написан на Python и использует PyGame для вывода анимации, TwitchIO для взаимодействия с чатом и наградами на трансляции.

Возможности:
 - База персонажей и предметов актуальна для патча `2.8`, обновляется с выходом обновлений в игре
 - Поддерживаются как одиночные молитвы так и множественные (от 2 до бесконечности)
 - Поддерживается работа с чатом на трансляции и использование баллов канала зрителями
 - Поддерживается загрузка пользовательских фонов (даже анимированных), звуков и шрифтов
 - Настройка времени и показа стадий анимации (показ ника зрителя, анимация падения, анимация результата молитвы)
 - Запись истории молитв зрителей в `CSV` формате (WIP)
 - Полная настройка всех шансов и мягкого гаранта при молитвах
 - Полная настройка сообщений чатбота и баллов канала
 - Чатбот умеет сам делать молитвы, а также подсказывать зрителям, когда они снова могут пользоваться командами (по таймауту)
 - Здесь можно выбить скины

Симулятор не использует систему баннеров, вместо этого при каждой молитве есть одинаковый шанс на выпадение любого доступного предмета или персонажа.

## Настройка

Переходим по ссылке на последний [релиз](https://github.com/dzmuh97/genshin-twitch-wish/releases/latest), скачиваем архив `genshin-twitch-wish_win64.zip`, распаковываем в любую удобную папку. Симулятор состоит из:
- **TwitchGenshinWishSim.exe** - сам симулятор
- **icon.png** - иконка для окна симулятора
- **config.json** - файл настроек
- **auth.json** - появится после первого запуска, файл с токенами
- **database.sqlite** - появится после первого запуска, база данных с молитвами зрителей
- **sound** - папка со звуками
- **logs** - папка с файлами журналов работы симулятора
- **images** - папка с изображениями
- **fonts** - папка с шрифтами
- **background** - папка с файлами для фоновых анимаций

По умолчанию включен тестовый режим. Можно сразу запустить симулятор `TwitchGenshinWishSim.exe` и посмотреть на результат 100 тестовых молитв. Тестовый режим отключается в файле конфигурации, параметр **test_mode**

Чтобы симулятор отображался на трансляции, нужно добавить захват окна в OBS:
![Окно захвата](https://media.discordapp.net/attachments/706496930414592080/980878746200453120/Sxxgzt6h_Ao.jpg)

И настроить фильтр для корректной работы прозрачности окна:
![Окно фильтра](https://media.discordapp.net/attachments/706496930414592080/980878745659375726/1HahxRWaJBF1kzE3BaChFSsMspC-LWBOcPf-kcj_f9g52D-Ia53P2osjQkR4F4wZXmfmu2-Gaavy5D7rU78ilhnS.jpg)

В симуляторе используется 2 вида бота: чатбот, который читает сообщения из чата (секция **chat_bot**), и бот, который ждет использование баллов канала (секция **event_bot**). Так как эти боты работают раздельно друг от друга, возможны 2 варианта настройки:

 - Использовать разные учетные записи Twitch. Первая будет чатботом, вторая - аккаунт стримера, для баллов канала
 - Использовать одну учетную запись и для чатбота и для баллов канала

При первом запуске будет предложено настроить аккаунты. Настройка автоматическая и интерактивная, нужно лишь следовать инструкциям и отвечать y или n (y - да, n - нет). Когда файл `auth.json` будет создан симулятор больше не будет предлагать настроить аккаунты. Далее можно переходить к настройкам симулятора в секцию [Описание config.json](#описание-configjson)

### Регистрируем приложение на Twitch

*Этот и следующие разделы можно пропустить, если сработала интерактивная настройка*

Заходим в свой основной аккаунт Twitch, переходим в [панель разработчика](https://dev.twitch.tv/console/apps), жмем кнопку `Регистрация приложения` 
![панель разработчика](https://media.discordapp.net/attachments/706496930414592080/984117056448372806/unknown.png)

Заполняем по порядку:
 - Название приложения (должно быть уникальным, можно добавить название канала)
 - Ссылка, куда будет передаваться токен, указываем `https://twitchtokengenerator.com`
 - Категория `Chat Bot`

Проходим капчу и подтверждаем создание приложения.
![enter image description here](https://media.discordapp.net/attachments/706496930414592080/986298587069710336/unknown.png)

Переходим обратно к списку всех приложений и выбираем то, которое только что создали, жмем `Управление`
![данные приложения](https://media.discordapp.net/attachments/706496930414592080/984119131135672370/unknown.png)

Жмем на кнопку `Новый секретный код`, появится новое поле. Оставляем текущую вкладку с данными открытой.

### Создаем токен

Открываем в новой вкладке (вкладку с данными, если она есть, не закрываем) [генератор Twitch токенов](https://twitchtokengenerator.com/), жмем на `Uhhhh what? Just take me to the site`
![заполняем поля данным из предыдущей вкладки](https://media.discordapp.net/attachments/706496930414592080/984120049344335922/unknown.png)

Заполняем поля данными из предыдущей вкладки (если пропустили предыдущий пункт то не трогаем):
 - **CLIENT ID** = **Идентификатор клиента**
 - **CLIENT SECRET** = **Секретный код клиента**

Если для чатбота и для баллов канала будет использоваться один и тот же аккаунт, то отмечаем пункты:

 - **chat:read** - чтобы читать сообщения из чата
 - **chat:edit** - чтобы писать в чат
 - **channel:read:redemptions** - чтобы видеть использование балов канала

Если разные:

 -  Для чатбота отмечаем:
	 - **chat:read** - чтобы читать сообщения из чата
	 - **chat:edit** - чтобы писать в чат
  - Для бота баллов канала (аккаунт, *с которого будет вестись трансляция*):
	 - **channel:read:redemptions** - чтобы видеть использование балов канала

![если используется один и тот же аккаунт](https://media.discordapp.net/attachments/706496930414592080/984121657838932018/unknown.png) 
Прокручиваем до конца списка и жмем кнопку `Generate Token!` Обязательно проверяем, что вверху страницы указано название нашего приложения (если создавали) и имя нужного нам аккаунта. После чего нас перекинет на предыдущую страницу.

![здесь будет токен](https://media.discordapp.net/attachments/706496930414592080/984123646178107422/unknown.png)
Копируем токен и вставляем в файл конфигурации `config.json`:
 - если используем один и тот же аккаунт для чабота и для баллов канала: 
   - вставляем токен в **bot_token** и **channel_token**
 - если аккаунты для чатбота и баллов канала разные:
   - токен, полученный за аккаунт стримера (с которого *будет вестись трансляция* и у которого мы отметили пункт *channel:read:redemptions*) вставляем в **channel_token**
   - выходим из своей учетной записи Twitch
   - входим в учетную запись, которая будет использоваться как чатбот
   - повторяем шаги из [Создаем токен](#создаем-токен) (страницу с генератором токенов нужно будет обновить после перезахода в другой Twitch аккаунт)
   - второй токен вставляем в **bot_token** (должны быть пункты *chat:read* и *chat:edit*)

## Описание `config.json`
 
 - **window_name** - название окна для захвата в OBS
 - **chat_bot** - секция для настройки чат-бота
   - **enabled** - включение или отключение секции (true или false)
   - **wish_command** - команда, на которую бот должен реагировать
   - **wish_command_prefix** - префикс для команды
   - **wish_global_timeout** - общее ограничение для всех пользователей на команду бота (в секундах)
   - **wish_timeout** - как часто каждый пользователь может использовать команды бота (в секундах)
     - **broadcaster** - для автора канала
     - **mod** - для модераторов
     - **subscriber** - для подписчиков
     - **user** - все остальные
   - **send_notify** - отправлять ли уведомление в чат когда пользователь снова может использовать **wish_command** 
   - **wish_count** - количество молитв, которое будет делаться за одно использование команды
   - **self_wish** - режим, при котором бот сам использует команду
   - **self_wish_every** - как часто (если включено) бот будет использовать команду
   - **enable_colors** - включить цветные ники
 - **event_bot** - секция для настройки баллов канала
   - **enabled** - включение или отключение секции (true или false)
   - **default_color** - цвет для ников
   - **rewards** - секция настройки наград за баллы канала
     - **event_name** - название награды
     - **wish_count** - сколько молитв делать при использовании
 - **animations** - секция настройки анимаций
   - **chroma_color** - цвет хромакея
   - **draw_states** - какие стадии анимации будут показаны при молитве
     - **draw_usertext** - вывод ника зрителя с текстом и **user_background** (если включен)
     - **draw_fall** - вывод анимации падения звезды
     - **draw_wishes** - вывод анимации результат молитвы
   - **start_delay** - как долго будет показан ник пользователя сделавшего молитву (в секундах)
   - **end_delay** - как долго будет показан результат молитвы (в секундах) если была сделана всего 1 молитва
     - **3** - для 3*
     - **4** - для 4*
     - **5** - для 5*
   - **end_delay_milti** - как долго будет показан результат молитвы (в секундах) если было сделано больше 1 молитвы
     - **3** - для 3*
     - **4** - для 4*
     - **5** - для 5*
   - **user_background** - секция настройки пользовательских фонов
     - **enabled** - включение или отключение секции (true или false)
     - **path** - название файла в папке background (только имя файла, не полный путь)
     - **type** - тип фона, `static` для JPG или PNG, `gif` для GIF и тд.
   - **font** - секция настройки шрифтов и текста
     - **path** - название файла в папке fonts (только имя файла, не полный путь)
     - **user_uid_size** - размер текста для отображения ника пользователя в правом нижнем углу
     - **wish_name_size** - размер текста для сплеш анимации (названия оружий и имена персонажей)
   - **fps** - частота обновления анимаций (все анимации настроены на 30 кадров в секунду)
 - **sound** - секция настройки звука (все файлы должны лежать в папке **sound**)
   - **enabled** - включение или отключение секции (true или false)
   - **fall** - для анимации падения
   - **3** - во время сплеш анимации для 3*
   - **4** - во время сплеш анимации для 4*
   - **5** - во время сплеш анимации для 5*
 - **history_file** - секция настройки записи истории молитв
   - **enabled** - включение или отключение секции (true или false)
   - **path** - имя файла (не полный путь, вместе с расширением), куда будет записываться история
   - **3** - записывать ли выпадение 3*
   - **4** - записывать ли выпадение 4*
   - **5** - записывать ли выпадение 5*
 - **wish_fo_garant** - сколько молитв должен сделать пользователь до гаранта 4*
 - **wish_fo_chance** - общий шанс выпадения 4* (от 0.01 до 99.99)
 - **wish_fi_garant** - сколько молитв должен сделать пользователь до гаранта 5*
 - **wish_fi_chance** - общий шанс выпадения 5* (от 0.01 до 99.99)
 - **wish_fi_soft_a** - после какой молитвы начнет работать мягкий гарант (должен быть меньше **wish_fi_garant**)
 - **send_dev_stats** - включение или отключение отправки анонимной статистики
 - **test_mode** - режим тестирования, твич бот не включается, автоматически делаются 100 молитв  

### Описание секции MESSAGES

Здесь перечислены блоки с текстом, которые симулятор или чатбот используют во время работы. В каждый блок можно добавлять или удалять строки. В каждом блоке должна быть минимум 1 строка.

- **user_splash_text** - отображается во время первой стадии анимации под ником зрителя
- **chatbot_text** - чатбот использует в ответах зрителям в чате на трансляции
- **notify_text** - используется для напоминания зрителям, когда их таймаут заканчивается
- **chanel_points_text** - используется для ответа зрителям, которые использовали баллы канала
- **stats_message** - одна строка, текст для сервисной команды **!gbot_status**

### Параметры в ответах чатбота зрителям

В сообщениях бота можно указывать параметры:
 - Общие для блоков **chatbot_text** и **chanel_points_text**
   - **username** - упоминание пользователя, который использовал команду
   - **wish_count** - сколько всего молитв сделал пользователь
   - **wish_count_w4** - сколько было сделано молитв после последней выпавшей 4*
   - **wish_count_w5** - сколько было сделано молитв после последней выпавшей 5*
   - **wishes_in_cmd** - сколько будет сделано молитв за использоание команды
   - **que_num** - номер в очереди молитв
 - Для блока **chatbot_text**
   - **user_wish_delay** - сколько пользователю придется подождать перед следующим использованием команды (параметр **wish_timeout**)
   - **global_wish_delay** - как часто весь чат может использовать команду
 - Для блока **chanel_points_text**
   - **reward_cost** - стоимость награды в баллах, которую активировал пользователь
 - Для блока **notify_text**
   - **username** - упоминание пользователя, который использовал команду
   - **command** - команда в виде **wish_command_prefix** + **wish_command**

## Сервисные команды для чатбота

 - **!gbot_status** - выводит общую информацию о боте и молитвах в чат
 - **!gbot_sound** - включает или отключает звук во время молитв
 - **!gbot_pause** - включает или отключает обработку молитв. Бот по прежнему будет реагировать на использование баллов канала или команды чата, но анимации молитв воспроизводится не будут, при этом все молитвы будут находится в очереди пока обработка не будет снова включена

*Проект собирает анонимную статистику. В нее входят время запуска и название канала из файла конфигурации. Никакие личные данные, IP адреса или токены от каналов\ботов не передаются.*