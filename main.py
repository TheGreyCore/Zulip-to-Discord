import asyncio
import configparser
from datetime import datetime, timedelta
import discord
from discord.ext import commands
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Get variables from config file.
config = configparser.ConfigParser()
config.read('config.cfg')

DISCORD_BOT_TOKEN = config.get('Keys', 'DISCORD_BOT_TOKEN')
LOG_IN_USERNAME = config.get('Keys', 'LOG_IN_USERNAME')
LOG_IN_PASSWORD = config.get('Keys', 'LOG_IN_PASSWORD')
TARGET_USER = config.get('Keys', 'TARGET_USER')
DEBUGGING = config.get('Settings', 'DEBUGGING')
LINK = config.get('Link', 'LINK')

# Configure logging
logging.basicConfig(
    level=logging.INFO if DEBUGGING else logging.CRITICAL,
    format='%(asctime)s [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


# Set chrome to ""Background mode"
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument('headless')
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-features=CSSGridLayout")
chrome_options.add_argument("--blink-settings=imagesEnabled=false")
chrome_options.add_argument("--disable-domain-reliability")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_experimental_option('prefs', {
    'profile.default_content_setting_values': {
        'images': 2,  # 2: Do not load images
        'javascript': 1,  # 1: Do not load JavaScript
        'plugins': 2,  # 2: Do not load plugins
        'css': 2,  # 2: Do not load CSS
        'video': 2  # 2: Do not load videos
    }
})

# Start driver
driver = webdriver.Chrome(options=chrome_options)

try:
    if __name__ == "__main__":
        # Initialize the bot and set a command prefix
        intents = discord.Intents.default()
        intents.typing = True
        intents.dm_messages = True
        intents.message_content = True
        bot = commands.Bot(command_prefix='!', intents=intents)
    else:
        exit()
except KeyboardInterrupt:
    driver.quit()
    exit()


# Function to log in to Zulip
def loginToZulip():
    logging.info("Trying to login to Zulip...")
    driver.get(LINK)
    if driver.current_url != LINK:
        login_form = driver.find_element(By.XPATH, '//*[@id="id_username"]')
        login_form.send_keys(LOG_IN_USERNAME)
        password = driver.find_element(By.XPATH, '//*[@id="id_password"]')
        password.send_keys(LOG_IN_PASSWORD)
        password.send_keys(Keys.ENTER)
        logging.info("Successfully!")
    else:
        logging.info("Log in not needed. Pass.")
    return True


# Fetch to get last message
# Return data in format (Last Topic, Last Sender, Last Message)
def fetchLastMessage():
    global driver
    try:
        logging.info("Trying to fetch information...")
        # Check for new messages
        driver.get(LINK)
        if driver.current_url == LINK:
            messages = driver.find_elements(By.CSS_SELECTOR, 'div.message_content')
            last_message = messages[-1].text
            # Check for last sender
            senders_names = driver.find_elements(By.CSS_SELECTOR, 'span.sender_name')
            last_sender = senders_names[-1].text
            # Check for last topic
            topics = driver.find_elements(By.CSS_SELECTOR, 'a.narrows_by_topic')
            last_topic = topics[-1].text
            logging.info("Information was successfully fetched!")
            return last_topic, last_sender, last_message
        else:
            logging.info("Log in needed!")
            loginToZulip()
    except IndexError as e:
        logging.warning(e)
        fetchLastMessage()
    except Exception as e:
        if driver:
            driver.quit()
        driver = webdriver.Chrome(options=chrome_options)
        loginToZulip()
        fetchLastMessage()
        logging.error(e)
        logging.info("Restarting chrome...")


# Main function
async def main():
    last_sent_message = ()
    loginToZulip()

    while True:
        # Get last message
        new_fetched_message = fetchLastMessage()

        if new_fetched_message != last_sent_message and new_fetched_message is not None:
            logging.info("Trying to send message...")
            try:
                user = await bot.fetch_user(int(TARGET_USER))
                embed = discord.Embed(
                    title="",
                    description="",
                    color=0xb700ff
                )
                embed.add_field(name=new_fetched_message[1], value=new_fetched_message[2])
                embed.timestamp = datetime.utcnow() + timedelta(hours=3)
                embed.set_author(name=new_fetched_message[0])
                await user.send(embed=embed)

                last_sent_message = new_fetched_message
                logging.info('Messages was successfully sent!')
            except AttributeError as e:
                logging.warning(e)

        await asyncio.sleep(60)


# Bot event: When the bot is ready
@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user.name} ({bot.user.id})')
    bot.loop.create_task(main())

bot.run(DISCORD_BOT_TOKEN)
