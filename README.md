# What is this?
This is a Telegram text-based adventure bot. It supports sending images and markup keyboards.

# How to use this?
1. Make sure you have Python installed
2. Install dependencies
```bash
pip install python-dotenv pyTelegramBotAPI
```
3. Clone the repository
```bash
git clone https://github.com/Aleph017/my_telegram_bot.git
cd my_telegram_bot
```
4. Set up a '.env' file in the directory and put your bot token into 'OLEG_ENV' variable.
5. Run the bot
```bash
python ./bot.py
```
6. Pray.

# How to add my own story?
1. Create 'raw.txt' file in the directory
```bash
touch raw.txt
```
2. Describe story blocks in such format in 'raw.txt':
```
label : Name_of_the_block_that_the_script_will_work_with
text : "Text that the bot will send"
choices : ("label_of_other_block_that_the_choice_leads_to" : "Text that will appear on according button"),("other_block_label" : "Corresponding text")
```
3. Run 'parser.py'
```bash
python ./parser.py
```
It will read 'raw.txt' and transform it into file 'test.json' that you can rename to story.json, filename that the bot expects, later.
Also you'll need to manually set images in that json file, sorry!
