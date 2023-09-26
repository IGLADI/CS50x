import discord
from discord.ext import commands
import asyncio
import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from keep_alive import keep_alive
import os

# intents
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True 

# load the bot token from the json file
with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)
    TOKEN = config_data.get("bot_token", "")

# nitialize the bot
bot = commands.Bot(command_prefix='/', intents=intents)

# load/initialize news_channels.json
try:
    with open('news_channels.json', 'r') as file:
        news_channels = json.load(file)
except FileNotFoundError:
    news_channels = {}

# Initialize empty lists 
sent_articles_per_channel = {}
mute_status_per_channel = {}

# check if a channels are muted
def is_channel_muted(channel_id):
    return mute_status_per_channel.get(channel_id, False)

def is_channel_muted_error(channel_id):
    return mute_status_per_channel.get(f"{channel_id}_error", False)

# function to mute/unmute channels
def toggle_channel_mute(channel_id):
    mute_status_per_channel[channel_id] = not is_channel_muted(channel_id)
    save_mute_status()
    
def toggle_channel_mute_error(channel_id):
    mute_status_per_channel[f"{channel_id}_error"] = not is_channel_muted_error(channel_id)
    save_mute_status()

def save_mute_status():
    with open('mute_status.json', 'w') as file:
        json.dump(mute_status_per_channel, file)
        
        
# load/initialize mute status from mute_status.json
try:
    with open('mute_status.json', 'r') as file:
        mute_status_per_channel = json.load(file)
except FileNotFoundError:
    mute_status_per_channel = {}
    
# Ffnction to load sent articles from JSON files
def load_sent_articles(channel_id):
    filename = f'sent_articles_{channel_id}.json'
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return []

for channel_id in news_channels:
    sent_articles_per_channel[channel_id] = load_sent_articles(channel_id)

# function to save sent articles to a JSON file
def save_sent_articles(channel_id):
    filename = f'sent_articles_{channel_id}.json'
    with open(filename, 'w') as file:
        json.dump(sent_articles_per_channel[channel_id], file)

# when the bot is started
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    # load mute status from JSON file
    load_mute_status()
    # start the background task to fetch and send news updates
    bot.loop.create_task(fetch_and_send_news())
    
    
# load mute status from JSON file
def load_mute_status():
    global mute_status_per_channel
    try:
        with open('mute_status.json', 'r') as file:
            mute_status_per_channel = json.load(file)
    except FileNotFoundError:
        mute_status_per_channel = {}

# message from the bot when it joins a server
@bot.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(
                "Hello! I'm your friendly news bot. I can help you stay updated with news articles, anime episodes, and more from various platforms.\n\n"
                "To add a news site, use the `/news` command.\n\n"
                "For help on using the bot, type `/newshelp`.\n\n"
                "**Disclaimer:**\n"
                "This bot has been created as a final project for CS50x and for educational purposes. Users are responsible for ensuring the bot's usage complies with the terms and policies of the websites it accesses. Some websites may not authorize the use of bots for scraping or data collection."
            )
        break

# /news command
@bot.command(name='news', description='Add or remove news sites from the channel.')
async def news(ctx):
    global news_channels
    channel_id = str(ctx.channel.id)
    print("/news command executed in " + channel_id)

    await ctx.send('Do you want to add or remove a news site? Please reply with "add" or "remove".')

    try:
        response = await bot.wait_for('message', check=lambda m: m.author == ctx.author, timeout=30)
        response_text = response.content.strip().lower()

        if response_text == 'add':
            await ctx.send('Please enter the website link you want to add:')
            website_link = await bot.wait_for('message', check=lambda m: m.author == ctx.author, timeout=30)
            website_link = website_link.content.strip()

            # check provided URL
            if not is_valid_url(website_link):
                await ctx.send('Invalid URL. Please provide a valid website link starting with http:// or https://.')
                return

            await ctx.send('Please enter the CSS class used to identify news links on the website (type "no classes" if unsure):')
            css_class = await bot.wait_for('message', check=lambda m: m.author == ctx.author, timeout=30)
            css_class = css_class.content.strip()

            if css_class.lower() == 'no classes':
                css_class = None

            # check if the channel ID exists in news_channels
            if channel_id in news_channels:
                # append the new website information to the existing list
                news_channels[channel_id].append({
                    "url": website_link,
                    "css_class": css_class
                })
            else:
                # create a new list for this channel and add the website information
                news_channels[channel_id] = [{
                    "url": website_link,
                    "css_class": css_class
                }]

            with open('news_channels.json', 'w') as file:
                json.dump(news_channels, file)

            await ctx.send('News site added successfully.')

        elif response_text == 'remove':
            await ctx.send('Do you want to remove a specific news site by providing a link or remove all of them? Please reply with "specific" or "all".')

            try:
                remove_option = await bot.wait_for('message', check=lambda m: m.author == ctx.author, timeout=30)
                remove_option = remove_option.content.strip().lower()

                if remove_option == 'specific':
                    await ctx.send('Please enter the website link of the news site you want to remove:')
                    website_link_to_remove = await bot.wait_for('message', check=lambda m: m.author == ctx.author, timeout=30)
                    website_link_to_remove = website_link_to_remove.content.strip()

                    # check if the channel ID exists in news_channels
                    if channel_id in news_channels:
                        # remove the specific website from the list
                        news_channels[channel_id] = [site for site in news_channels[channel_id] if site["url"] != website_link_to_remove]

                        if not news_channels[channel_id]:
                            # if the list is empty, remove the channel entry
                            del news_channels[channel_id]

                        with open('news_channels.json', 'w') as file:
                            json.dump(news_channels, file)

                        await ctx.send('News site removed successfully.')
                    else:
                        await ctx.send('There are no news sites to remove in this channel.')

                elif remove_option == 'all':
                    # remove all news sites for this channel
                    if channel_id in news_channels:
                        del news_channels[channel_id]
                        with open('news_channels.json', 'w') as file:
                            json.dump(news_channels, file)

                        await ctx.send('All news sites in this channel have been removed successfully.')
                    else:
                        await ctx.send('There are no news sites to remove in this channel.')

                else:
                    await ctx.send('Invalid response. Please reply with "specific" or "all".')

            except asyncio.TimeoutError:
                await ctx.send('Timed out. Please try the /news command again.')

        else:
            await ctx.send('Invalid response. Please reply with "add" or "remove".')

    except asyncio.TimeoutError:
        await ctx.send('Timed out. Please try the /news command again.')

# /newshelp command 
@bot.command(name='newshelp', description='Get help on using the news bot.')
async def newshelp(ctx):
    help_message = (
        "Hello! I'm your friendly news bot. Here's how to use me:\n\n"
        "**To add a news site:**\n"
        "Use the command `/news` and follow the prompts. Provide the website link and the CSS class used to identify news links on the website.\n\n"
        "**How to find the website link and CSS class:**\n"
        "1. **Website Link**: Visit the news website you want to add and copy its address from the browser's address bar. Make sure it starts with `http://` or `https://`, and the link should typically end with a domain like `.com`, `.org`, or another valid top-level domain (TLD).\n"
        "2. **CSS Class**: This is a bit technical. You can ask the website administrator for the CSS class used to style news article links. If you don't know it, you can leave it blank for now, and I'll try to find the news links without it.\n"
        "   Note: When no CSS class is provided, I'll initially send a list of all links found on the webpage. After that, I'll only send new news articles.\n\n"
        "**To remove a news site:**\n"
        "Use the command `/news` and select 'remove.' You can choose to remove a specific news site by providing its link or remove all of them.\n\n"
        "Remember to make sure the website link starts with `http://` or `https://`.\n\n"
        "**Mute/Unmute Commands**:\n"
        "- To mute or unmute news updates in this channel, use `/newsmute`.\n"
        "- To mute or unmute error messages for news updates in this channel, use `/newsmuteerror`.\n\n"
    )
    await ctx.send(help_message)

# function to fetch and send new news articles
async def send_latest_news(channel_id, website_url, css_class):
    if is_channel_muted(channel_id):
        print(f"Channel {channel_id} is muted for news updates.")
        return

    try:
        print(f"Fetching latest news for channel {channel_id} from {website_url}")
        news_links = fetch_news_links(website_url, css_class)

        channel = bot.get_channel(int(channel_id))
        if channel:
            if not news_links:
                # if no news articles were found (old/new), send a message in the channel
                await channel.send(f"No news articles found on the website {website_url} with CSS class {css_class}.")
                return

            # get the list of sent articles for this channel
            channel_sent_articles = sent_articles_per_channel[channel_id]

            new_articles = [link for link in news_links if link not in channel_sent_articles]

            for i, link in enumerate(new_articles, start=1):
                print(f"Sending article {i}: {link}")
                await channel.send(link)
                channel_sent_articles.append(link)

            # update the list of sent articles for this channel
            save_sent_articles(channel_id)

        else:
            print(f"Channel {channel_id} not found.")

    except Exception as e:
        if not is_channel_muted_error(channel_id):
            error_message = f"An error occurred while sending the latest news for website {website_url} with CSS class {css_class}: {str(e)}"
            print(error_message)

            # send an error message in the corresponding channel
            channel = bot.get_channel(int(channel_id))
            if channel:
                await channel.send(error_message)

# fetch and send news articles to all channels
async def fetch_and_send_news():
    while not bot.is_closed():
        try:
            for channel_id, website_info_list in news_channels.items():
                for website_info in website_info_list:
                    website_url = website_info.get("url")
                    css_class = website_info.get("css_class")
                    await send_latest_news(channel_id, website_url, css_class)

            print("Waiting for 60 seconds...")
            await asyncio.sleep(60)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print("Waiting for 60 seconds...")
            await asyncio.sleep(60)

# fetch news links from a website
def fetch_news_links(website_url, css_class):
    response = requests.get(website_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    if css_class:
        link_elements = soup.find_all('a', class_=css_class)
    else:
        link_elements = soup.find_all('a')

    news_links = []

    for link_element in link_elements:
        link = link_element.get('href')

        if link and not link.startswith('#'):
            # check if the link starts with 'http' or 'https'
            if not link.startswith('http'):
                # if not, add actual URL to make it a complete link (for relative links)
                link = f'{website_url}{link}'

            news_links.append(link)

    print(f"Found {len(news_links)} article links.")
    return news_links

# function to check if a URL is valid
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

# mute/unmute commands for news updates
@bot.command(name='newsmute', description='Mute or unmute news updates in this channel.')
async def newsmute(ctx):
    channel_id = str(ctx.channel.id)
    toggle_channel_mute(channel_id)
    mute_status = is_channel_muted(channel_id)

    if mute_status:
        await ctx.send('News updates in this channel are now muted.')
    else:
        await ctx.send('News updates in this channel are now unmuted.')

# mute/unmute commands for error messages
@bot.command(name='newsmuteerror', description='Mute or unmute error messages for news updates in this channel.')
async def newsmuteerror(ctx):
    channel_id = str(ctx.channel.id)
    toggle_channel_mute_error(channel_id)
    mute_status = is_channel_muted_error(channel_id)

    if mute_status:
        await ctx.send('Error messages for news updates in this channel are now muted.')
    else:
        await ctx.send('Error messages for news updates in this channel are now unmuted.')

keep_alive()
# start the bot with the token in the config file
bot.run(TOKEN)
