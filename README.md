## ArseinRubika

> Elegant, modern and fully asynchronous Rubika API framework in Python for official bots, user-bots, and Rubino class support

<p align="center">
    <img src="https://github.com/ArseinRubikaApp/ArseinRubika/blob/main/arsein/logo/logo_arsein.jpg" 
         alt="Arsein Rubika" 
         width="256" 
         height="256"
         style="border-radius: 50%; object-fit: cover;">
    <br>
    <strong>Library ArseinRubika</strong>
</p>

###  Arsein library documents soon...


### How to use UserBot

### How to import classes related to UserBot

``` python
from arsein import Messenger
```

### Or

``` python
from arsein import Robot_Rubika
```

## An example:

``` python
from arsein import Messenger

bot = Messenger("Your Auth Account"," key Account",TypePlat = "web")

gap = "your guid or gap or pv or channel"

bot.sendMessage(gap,"libraryArsein")
```

## And Or:

``` python
from arsein import Robot_Rubika

bot = Robot_Rubika("Your Auth Account"," key Account",TypePlat = "android")

gap = "your guid or gap or pv or channel"

bot.sendMessage(gap,"libraryArsein")
```

## Or:

``` python
from arsein import Robot_Rubika
from arsein.filters import userbot
from arsein.arsocket import ChatUpdate

auth = " "
key = " "


bots = Robot_Rubika(auth, key, TypePlat="web")


@ChatUpdate(userbot.is_link | userbot.is_ID)
def test(msg):
    bots.sendMessage(msg.object_guid, "تبلیغ ممنوع است")


bots.run()

```

## Or:

``` python
from arsein import Messenger
from arsein.filters import userbot
from arsein.arsocket import ChatUpdate

auth = " "
key = " "


bots = Messenger(auth, key, TypePlat="web")


@ChatUpdate(userbot.text_keywords("احمق", "دیوانه"))
def test(msg):
    bots.sendMessage(msg.object_guid, "این متن حاوی توهین می باشد")


bots.run()

```
## Or:

``` python
from arsein import Robot_Rubika
from arsein.filters import userbot
from arsein.arsocket import ChatUpdate

auth = " "
key = " "

bots = Robot_Rubika(auth, key, TypePlat="web")


@ChatUpdate(userbot.is_image)
def test(msg):

    name_file = msg.Photo.file_name
    bots.sendMessage(msg.object_guid, f"نام عکس {name_file} است")


bots.run()

```

## Or If you want, write a custom filter.:

``` python
from arsein import Robot_Rubika
from arsein.arsocket import ChatUpdate
from arsein.filters import userbot

auth = " "
key = " "

bots = Robot_Rubika(auth, key, TypePlat="web")


def test(msg):
    return msg.text.startswith("@")


@ChatUpdate(userbot.is_text & test)
def test1(msg):
    bots.sendMessage(msg.object_guid, "این متن است و اول متن @ دارد")


bots.run()

```


## فیلترها و عملگرهای پیام در یوزربات (با دکوریتور ChatUpdate)

| نام عملگر / تابع                        | توضیح فارسی                                                                 | مثال استفاده در یوزربات                              | نوع / توضیح اضافی                          |
|------------------------------------------|-----------------------------------------------------------------------------|-------------------------------------------------------|---------------------------------------------|
| `is_pv`                                  | پیام در چت خصوصی (پی‌وی / DM) دریافت شده                                  | `@ChatUpdate(is_pv)`                                  | چت با یک نفر                                |
| `is_gap`                                 | پیام در گروه یا سوپرگروه دریافت شده                                       | `@ChatUpdate(is_gap)`                                 | گروه معمولی یا سوپرگروه                    |
| `is_channel`                             | پیام در کانال دریافت شده                                                  | `@ChatUpdate(is_channel)`                             | کانال (معمولاً فقط ادمین‌ها می‌بینند)      |
| `is_bot`                                 | فرستنده پیام یک ربات است                                                  | `@ChatUpdate(is_bot)`                                 | —                                           |
| `is_image`                               | پیام شامل عکس (photo) است                                                 | `@ChatUpdate(is_image)`                               | —                                           |
| `is_video`                               | پیام شامل ویدئو است                                                        | `@ChatUpdate(is_video)`                               | —                                           |
| `is_gif`                                 | پیام شامل گیف (animated gif) است                                           | `@ChatUpdate(is_gif)`                                 | —                                           |
| `is_file`                                | پیام شامل فایل / سند (document) است                                       | `@ChatUpdate(is_file)`                                | —                                           |
| `is_voice`                               | پیام شامل ویس (voice note) است                                             | `@ChatUpdate(is_voice)`                               | —                                           |
| `is_music`                               | پیام شامل فایل صوتی / موزیک (audio) است                                   | `@ChatUpdate(is_music)`                               | —                                           |
| `is_sticker`                             | پیام شامل استیکر است                                                       | `@ChatUpdate(is_sticker)`                             | —                                           |
| `is_location`                            | پیام شامل موقعیت مکانی (location) است                                     | `@ChatUpdate(is_location)`                            | —                                           |
| `is_contact`                             | پیام شامل کارت تماس (contact) است                                         | `@ChatUpdate(is_contact)`                             | —                                           |
| `is_poll`                                | پیام شامل نظرسنجی (poll / quiz) است                                       | `@ChatUpdate(is_poll)`                                | —                                           |
| `is_text`                                | پیام شامل متن است (msg.text وجود دارد)                                    | `@ChatUpdate(is_text)`                                | —                                           |
| `is_link`                                | متن پیام شامل لینک / URL است                                              | `@ChatUpdate(is_link)`                                | تشخیص با regex                              |
| `is_ID`                                  | متن پیام شامل منشن (@username) است                                        | `@ChatUpdate(is_ID)`                                  | تشخیص با regex                              |
| `is_reply`                               | پیام پاسخ (reply) به پیام دیگری است                                       | `@ChatUpdate(is_reply)`                               | —                                           |
| `is_forwarded`                           | پیام فوروارد شده است (از هر منبعی)                                       | `@ChatUpdate(is_forwarded)`                           | —                                           |
| `forwarded_from_channel`                 | پیام از کانال فوروارد شده است                                            | `@ChatUpdate(forwarded_from_channel)`                 | —                                           |
| `forwarded_from_pv`                      | پیام از چت خصوصی فوروارد شده است                                         | `@ChatUpdate(forwarded_from_pv)`                      | —                                           |
| `forwarded_from_gap`                     | پیام از گروه فوروارد شده است                                              | `@ChatUpdate(forwarded_from_gap)`                     | —                                           |
| `is_edit_message`                        | پیام ویرایش‌شده است                                                       | `@ChatUpdate(is_edit_message)`                        | —                                           |
| `is_deleted_message`                     | پیام حذف‌شده است (در صورت پشتیبانی سرور)                                 | `@ChatUpdate(is_deleted_message)`                     | —                                           |
| `is_service`                             | پیام از نوع سرویس / اعلان سیستمی است                                      | `@ChatUpdate(is_service)`                             | ورود/خروج، تغییر عنوان و ...               |
| `new_member_gap`                         | عضو جدید به گروه اضافه شده                                                | `@ChatUpdate(new_member_gap)`                         | —                                           |
| `left_member_gap`                        | عضوی گروه را ترک کرده است                                                 | `@ChatUpdate(left_member_gap)`                        | —                                           |
| `add_member_gap`                         | عضو(ها) به گروه اضافه شده‌اند (توسط ادمین)                                | `@ChatUpdate(add_member_gap)`                         | —                                           |
| `remove_member_gap`                      | عضو(ها) از گروه حذف شده‌اند (توسط ادمین)                                 | `@ChatUpdate(remove_member_gap)`                      | —                                           |
| `message_pinned`                         | پیامی در گروه پین شده است                                                 | `@ChatUpdate(message_pinned)`                         | —                                           |
| `start_VoiceChat`                        | چت صوتی گروه شروع شده است                                                 | `@ChatUpdate(start_VoiceChat)`                        | —                                           |
| `Stop_VoiceChat`                         | چت صوتی گروه متوقف شده است                                                | `@ChatUpdate(Stop_VoiceChat)`                         | —                                           |
| `is_change_title`                        | عنوان گروه/کانال تغییر کرده است                                          | `@ChatUpdate(is_change_title)`                        | —                                           |
| `is_change_photo`                        | عکس گروه/کانال تغییر کرده است                                            | `@ChatUpdate(is_change_photo)`                        | —                                           |
| `is_delete_photo`                        | عکس گروه/کانال حذف شده است                                               | `@ChatUpdate(is_delete_photo)`                        | —                                           |
| `is_live`                                | پیام لایو (live stream) است                                                | `@ChatUpdate(is_live)`                                | —                                           |
| `is_spoil`                               | پیام شامل اسپویلر (spoiler) است                                           | `@ChatUpdate(is_spoil)`                               | —                                           |
| `is_fance_font`                          | متن پیام از فونت فانتزی/ویژه استفاده کرده                               | `@ChatUpdate(is_fance_font)`                          | —                                           |
| `is_font_bold`                           | متن پیام بولد (bold) است                                                  | `@ChatUpdate(is_font_bold)`                           | فرمت متن                                    |
| `is_font_Italic`                         | متن پیام ایتالیک (italic) است                                             | `@ChatUpdate(is_font_Italic)`                         | فرمت متن                                    |
| `is_font_Underline`                      | متن پیام زیرخط‌دار (underline) است                                        | `@ChatUpdate(is_font_Underline)`                      | فرمت متن                                    |
| `is_font_Strike`                         | متن پیام خط‌خورده (strikethrough) است                                    | `@ChatUpdate(is_font_Strike)`                         | فرمت متن                                    |
| `is_font_Spoiler`                        | متن پیام اسپویلر است                                                      | `@ChatUpdate(is_font_Spoiler)`                        | فرمت متن                                    |
| `is_font_Mono`                           | متن پیام مونواسپیس (code / monospace) است                                 | `@ChatUpdate(is_font_Mono)`                           | فرمت متن                                    |
| `is_font_MentionText`                    | متن پیام شامل منشن با فرمت خاص است                                        | `@ChatUpdate(is_font_MentionText)`                    | —                                           |
| `is_font_Link`                           | متن پیام شامل لینک با فرمت خاص است                                        | `@ChatUpdate(is_font_Link)`                           | —                                           |
| `text_startswith("متن")`                 | متن پیام با عبارت مشخص شروع می‌شود                                       | `@ChatUpdate(text_startswith("!ban"))`                | —                                           |
| `text_endswith("متن")`                   | متن پیام با عبارت مشخص تمام می‌شود                                       | `@ChatUpdate(text_endswith("خداحافظ"))`               | —                                           |
| `text_keywords("کلمه1", "کلمه2", ...)`   | متن پیام شامل حداقل یکی از کلمات کلیدی است (case-insensitive)            | `@ChatUpdate(text_keywords("خرید", "فروش"))`          | —                                           |
| `regex(r"الگو", flags=0)`                | متن پیام با الگوی regex مطابقت دارد                                       | `@ChatUpdate(regex(r"^\d{11}$"))`                     | —                                           |

### نکات مهم ترکیب و استفاده

```python
# ترکیب چند شرط

@ChatUpdate(userbot.is_gap & userbot.text_startswith("!ban") & \~userbot.is_bot)
def ban_handler(msg):
    ...

# فقط پیام‌های متنی در پی‌وی

@ChatUpdate(userbot.is_pv & userbot.is_text & \~userbot.is_bot)
def pv_text(msg):
    ...

# دستورات با پیشوندهای مختلف

@ChatUpdate(userbot.is_gap & userbot.regex(r"^[!/.]start\s*$", re.IGNORECASE))
def start_cmd(msg):
    ...

```

## If the web socket library is not installed

```bash
pip install websocket-client
```


## What is the TypePlat parameter?

You specify your account type with the TypePlat parameter.

In this parameter you can enter one of these 3 values: "web" or "android" or "pwa"


### How to use Bot

### How to import classes related to Bot

``` python
from arsein import Bot
```

## An example:

``` python
from arsein import Bot

bot = Bot("Your Token Bot")

chat_id = "your chat_id or gap or pv or channel"

bot.sendMessage(chat_id,"libraryArsein")
```
### Or

``` python
from arsein import Bot
from arsein.keypad import (KeypadRow, Button, ChatKeypad, ButtonCalendar)
from arsein.enums import (ButtonTypeEnum, ButtonCalendarTypeEnum,ChatKeypadTypeEnum)
from arsein.filters import bot

bots = Bot(" ")

message_ids = []

calendar_model = ButtonCalendar(
    type=ButtonCalendarTypeEnum.DatePersian,
    min_year="1300",
    max_year="1500",
    title="انتخاب تاریخ"
)

calendar_button = Button(
    id="200",
    type=ButtonTypeEnum.Calendar,
    button_text="📅 انتخاب تاریخ",
    button_calendar=calendar_model
)

chat_kp = ChatKeypad(
    rows=[
        KeypadRow(
            buttons=[
                Button(id="100", type=ButtonTypeEnum.Simple, button_text="Add Account")
            ]
        ),
        KeypadRow(
            buttons=[
                Button(id="101", type=ButtonTypeEnum.Simple, button_text="Edit Account"),
                Button(id="102", type=ButtonTypeEnum.Simple, button_text="Remove Account")
            ]
        ),
        KeypadRow(
            buttons=[
                calendar_button
            ]
        )
    ]
)

@bots.getUpdate(bot.is_user & bot.is_image)
def test(msg):
    if not msg.message_id in message_ids:
        message_ids.append(msg.message_id)
        message = bots.sendMessage(
            chat_id=msg.chat_id, text="arsein", inline_keypad=chat_kp
        )


bots.run()

```
### Or

``` python
from arsein import Bot
from arsein.keypad import KeypadRow, Button, ChatKeypad, ButtonNumberPicker
from arsein.enums import ButtonTypeEnum,ChatKeypadTypeEnum
from arsein.filters import bot

bots = Bot(" ")

message_ids = []

picker_model = ButtonNumberPicker(
    min_value="4",
    max_value="20",
    title="تعداد انتخاب",
    default_value="5"
)

number_btn = Button(
    id="200",
    type=ButtonTypeEnum.NumberPicker,
    button_text="انتخاب عدد",
    button_number_picker=picker_model   
)

chat_kp = ChatKeypad(
    rows=[
        KeypadRow(buttons=[Button(id="100", type=ButtonTypeEnum.Simple, button_text="robot arsein")]),
        KeypadRow(buttons=[
            Button(id="101", type=ButtonTypeEnum.Simple, button_text="support arsein"),
            Button(id="102", type=ButtonTypeEnum.Simple, button_text="Remove Account")
        ]),
        KeypadRow(buttons=[number_btn])
    ]
)

@bots.getUpdate(bot.is_user & bot.is_image)   
def test(msg):
    if msg.message_id not in message_ids:
        message_ids.append(msg.message_id)
        bots.sendMessage(
            chat_id=msg.chat_id,
            text="arsein",
            chat_keypad_type = ChatKeypadTypeEnum.New,
            keypad=chat_kp 
        )

bots.run()
```

### Or

``` python
from arsein import Bot
from arsein.commands import BotCommands, BotCommand
from arsein.filters import bot

bots = Bot(" ")


comm = BotCommands(
    commands=[
        BotCommand(command="test1", description="com1"),
        BotCommand(command="test2", description="com2"),
    ]
)

message = bots.setCommands(bot_commands=comm)
print(message)

```

## Or If you want, write a custom filter.:

``` python

from arsein import Bot
from arsein.filters import bot

bots = Bot(" ")

message_ids = []

def test(msg):
    return msg.text.startswith("@")

@bots.getUpdate(bot.is_text & test)
def test1(msg):
    if not msg.message_id in message_ids:
        message_ids.append(msg.message_id)
        bots.sendMessage(chat_id=msg.chat_id,text="این متن است و اول متن @ دارد")

bots.run()

```


## فیلترها و عملگرهای پیام در بات (با دکوریتور getUpdate)

| نام عملگر / تابع                          | توضیح فارسی                                                                 | توضیح انگلیسی                                              | مثال استفاده با getUpdate                            |
|--------------------------------------------|-----------------------------------------------------------------------------|-------------------------------------------------------------|-------------------------------------------------------|
| `is_image`                                 | پیام شامل عکس است                                                           | Message contains an image/photo                             | `@bot.getUpdate(is_image)`                            |
| `is_music`                                 | پیام شامل فایل موسیقی / آهنگ است                                           | Message contains music/audio file                           | `@bot.getUpdate(is_music)`                            |
| `is_voice`                                 | پیام شامل ویس (voice note) است                                              | Message contains a voice note                               | `@bot.getUpdate(is_voice)`                            |
| `is_video`                                 | پیام شامل ویدئو است                                                         | Message contains a video                                    | `@bot.getUpdate(is_video)`                            |
| `is_poll`                                  | پیام شامل نظرسنجی (poll / quiz) است                                        | Message contains a poll or quiz                             | `@bot.getUpdate(is_poll)`                             |
| `is_location`                              | پیام شامل موقعیت مکانی (location) است                                      | Message contains a location                                 | `@bot.getUpdate(is_location)`                         |
| `is_text`                                  | پیام فقط متن ساده دارد                                                     | Message has plain text content                              | `@bot.getUpdate(is_text)`                             |
| `is_sticker`                               | پیام شامل استیکر است                                                        | Message contains a sticker                                  | `@bot.getUpdate(is_sticker)`                          |
| `is_file`                                  | پیام شامل فایل / سند (document) است                                        | Message contains a document/file                            | `@bot.getUpdate(is_file)`                             |
| `is_contact`                               | پیام شامل کارت تماس (contact) است                                          | Message contains a contact card                             | `@bot.getUpdate(is_contact)`                          |
| `is_forwarded`                             | پیام فوروارد شده است (از هر منبعی)                                        | Message is forwarded (from any source)                      | `@bot.getUpdate(is_forwarded)`                        |
| `is_forwarded_no_link`                     | پیام فوروارد شده بدون لینک قابل کلیک است                                  | Forwarded message without clickable link                    | `@bot.getUpdate(is_forwarded_no_link)`                |
| `is_link`                                  | متن پیام شامل لینک یا URL است                                              | Message text contains a link/URL                            | `@bot.getUpdate(is_link)`                             |
| `is_ID`                                    | متن پیام شامل منشن (@username) است                                         | Message text contains a mention (@username)                 | `@bot.getUpdate(is_ID)`                               |
| `text_startswith(متن)`                     | متن پیام با عبارت مشخص شروع می‌شود                                        | Text starts with specified string                           | `@bot.getUpdate(text_startswith("سلام"))`             |
| `text_endswith(متن)`                       | متن پیام با عبارت مشخص تمام می‌شود                                        | Text ends with specified string                             | `@bot.getUpdate(text_endswith("خداحافظ"))`            |
| `text_keywords(کلمه1, کلمه2, ...)`         | متن پیام حداقل یکی از کلمات کلیدی را دارد (case-insensitive)              | Text contains any of the keywords (case-insensitive)        | `@bot.getUpdate(text_keywords("خرید", "فروش"))`       |
| `regex(الگو, flags=0)`                     | متن پیام با الگوی regex مطابقت دارد                                        | Text matches the regex pattern                              | `@bot.getUpdate(regex(r"^\d{11}$"))`                  |
| `on_chatkeypad("button_id")`               | کاربر روی دکمه کیبورد معمولی (chat keypad) با آیدی مشخص کلیک کرده       | User pressed chat keypad button with this ID                | `@bot.getUpdate(on_chatkeypad("101"))`                |
| `on_command("command")`                    | کاربر دستور مشخصی ارسال کرده (مثلاً /start یا /help)                     | Specific command received (automatically adds / if missing) | `@bot.getUpdate(on_command("/start"))` <br>یا<br>`@bot.getUpdate(on_command("start"))` |
| `is_user`                                  | پیام از یک کاربر معمولی (نه ربات، نه کانال) است                          | Message from a regular user (not bot/channel)               | `@bot.getUpdate(is_user)`                             |
| `is_gap`                                   | پیام در گروه (گروه/سوپرگروه) دریافت شده                                   | Message received in group/supergroup                        | `@bot.getUpdate(is_gap)`                              |
| `is_channel`                               | پیام در کانال دریافت شده                                                  | Message received in channel                                 | `@bot.getUpdate(is_channel)`                          |
| `is_bot`                                   | پیام از یک ربات ارسال شده است                                              | Message sent by a bot                                       | `@bot.getUpdate(is_bot)`                              |
| `is_stopped`                               | پیام مربوط به توقف چیزی است (معمولاً در context خاص)                     | Message indicates something stopped                         | `@bot.getUpdate(is_stopped)`                          |

### نکات مهم برای این بات

- دکوریتور اصلی: `@bot.getUpdate`
- ترکیب فیلترها با `&` (و)، `|` (یا)، `\~` (نه) امکان‌پذیر است:
  
```python
  @bot.getUpdate(bot.is_gap & bot.text_startswith("!ban") & \~bot.is_bot)
  def handle_ban(msg):
      ...
```
### How to use Rubino

### How to import classes related to Rubino

``` python
from arsein import Rubino
```

## An example:

``` python
from arsein import Rubino

bot = Rubino("Your Auth Rubino")

get_my_pages = bot.getProfileList(10)
print(get_my_pages)
```

---

And if pip was filtered, enter the following code in the terminal to install the library

``` bash
pip install --trusted-host https://pypi.tuna.tsinghua.edu.cn -i https://pypi.tuna.tsinghua.edu.cn/simple/Arsein==8.8.5
```

## ❌ یا اگه با روش بالا نصب نشد

## 📌 راهنمای نصب ArseinRubika از GitHub

به دلیل عدم دسترسی به حساب PyPI، نسخه‌های جدید کتابخانه ArseinRubika تنها از طریق GitHub منتشر می‌شوند:

``` bash
https://github.com/ArseinRubikaApp/ArseinRubika
```

### 🔹 نصب در ترمینال Pydroid

در محیط Pydroid ابزار git وجود ندارد، بنابراین باید از فایل ZIP استفاده کنید:

``` bash
pip install https://github.com/ArseinRubikaApp/ArseinRubika/archive/refs/heads/main.zip
```

### 🔹 نصب در Termux

### در Termux می‌توانید git را نصب کرده و مستقیم ریپو را دریافت کنید:

``` bash
pkg install python git
pip install git+https://github.com/ArseinRubikaApp/ArseinRubika.git
```

---

### Made by Team ArianBot


### Key Features

- Ready: Install ArseinRubika with pip and start building your applications right away.
- Easy: Makes the Rubika API simple and intuitive, while still allowing advanced usages.
- Elegant: Low-level details are abstracted and re-presented in a more convenient way.
- Fast: Boosted up by pycryptodome, a high-performance cryptography library written in C.
- Async: Fully asynchronous (also usable synchronously if wanted, for convenience).
- Powerful: Full access to Rubika's API to execute any official client action and more.


### Our channel in messengers

Our channel in Ita
```bash
https://eitaa.com/ArseinTeam
```
Our channel in Soroush Plus
```bash
https://splus.ir/ArseinTeam
```
Our channel in Rubika
```bash
https://rubika.ir/Support_libdaryArseinRubika
```
Our channel in the Gap
```bash
https://gap.im/ArseinTeam
```
Our channel on Telegram
```bash
https://t.me/ArseinTeam
```
