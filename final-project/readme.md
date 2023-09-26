# News Discord Bot

News Bot - Stay Updated with the Latest News and More

## Project Description

The News Bot is a versatile Discord bot designed to keep your server members informed and engaged with automated news updates, anime episodes, and more from various platforms. This bot allows you to configure it to send news from your favorite websites and sources directly to your Discord server, enhancing the community's knowledge and interaction.

**Disclaimer:**
This bot was developed as a final project for CS50x and for educational purposes. It's essential for users to ensure that the bot's usage aligns with the terms and policies of the websites it accesses. Some websites may prohibit the use of bots for scraping or data collection.

**Important Note:**
This project makes use of ChatGPT for generating text content, as English is not the developer's native language. The primary goal is to provide a valuable educational experience and a free service to the Discord community.

**Academic Honesty:**
Users are encouraged to use this project as a learning resource. If you choose to incorporate any code or concepts from this project into your work, please adhere to the academic honesty policy of your educational institution, such as CS50x or Harvard's academic honesty policy. 

## CS50 Video Presentation

You can watch the project presentation video [here](https://youtu.be/aUQMRz3hCaM).

## Features

- **Add Custom News Sources:** Configure the bot to collect news articles from websites of your choice.
- **Customize News Feeds:** Select the specific CSS classes to identify news articles, tailoring your server's news feed.
- **Automatic Updates:** Receive news updates in your Discord channels automatically at regular intervals.
- **Source Management:** Easily remove specific news sources or clear the entire list.
- **Channel Muting:** Temporarily mute or unmute news updates and error messages in specific channels.
- **Helpful Commands:** Utilize the comprehensive `/newshelp` command to navigate and use the bot effectively.

## Usage

Using the News Bot is a straightforward process:

1. **Invite the Bot:** Invite the bot to your Discord server.
2. **Configuration:** Set up your preferred news sources and configure CSS classes to identify news articles using the `/news` command.
3. **Stay Informed:** Enjoy automatic news updates directly in your Discord channels.
4. **Control Notifications:** Use the mute/unmute commands to manage notifications as per your preference.
5. **Get Assistance:** Access helpful commands and guidelines with the `/newshelp` command.

## Installation

To run the News Bot on your server, follow these steps:

1. **Clone Repository:** Clone this repository to your local machine.
2. **Install Dependencies:** Install the required dependencies listed in `requirements.txt`.
3. **Configure Token:** Create a `config.json` file and add your bot token to it.
4. **Start the Bot:** Run the bot using `python bot.py`.

## Bot Commands

### /news Command

The `/news` command allows you to manage your news sources. You can add or remove news websites and configure the CSS classes used to identify news articles on those websites.

**Usage:**
1. Type `/news` in a channel where you want to add or remove news sources.
2. Choose between "add" to add a new source or "remove" to remove a source.
3. Follow the prompts to provide the website link and CSS class.

### /newshelp Command

The `/newshelp` command provides assistance on using the News Bot effectively. It offers step-by-step instructions and tips on configuring news sources and managing notifications.

**Usage:**
- Type `/newshelp` to access the comprehensive help guide.

### /newsmute Command

The `/newsmute` command allows you to temporarily mute news updates in a specific channel. Once muted, the bot will stop sending news updates to that channel.

**Usage:**
1. Type `/newsmute` in the channel where you want to mute news updates.
2. To unmute, use the command again.

### /newsmuteerror Command

The `/newsmuteerror` command allows you to mute error messages related to news updates in a specific channel. This can be useful if you want to suppress error notifications.

**Usage:**
1. Type `/newsmuteerror` in the channel where you want to mute error messages.
2. To unmute error messages, use the command again.

## Contributing

Contributions are highly welcome! If you'd like to enhance the bot or fix any issues, feel free to fork this project and submit pull requests. 

## License

This project is licensed under the MIT License.
