# Zulip to Discord

This scirpt is created to transfer new messages from Zulip to Discord. For fetching messages it use selenium. The answer for question why, is because in my situation I don`t have direct access to manage bots on Zulip.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. Note that the script is only tested on Windows, you may have to make changes if you want to use it on Linux.

### Prerequisites

Before using this script you have to download [ChromeDriver](https://chromedriver.chromium.org/getting-started) and Chrome for it.

### Installing

A step by step series of examples that tell you how to get a development env running

Clone repository or download it:
```
git clone https://github.com/TheGreyCore/Zulip-to-Discord
```

I recommend use virtual environment:
```
python -m venv PATH
```
Install requirements:
```
pip install -r requirements.txt
```
**The config.cfg faile must be edited before running main.py.**

Run main.py
```
python main.py
```

## Built With

* [Selenium](https://selenium-python.readthedocs.io/) - For fetch data from Zulip
* [Discord.py](https://discordpy.readthedocs.io/en/stable//) - To send messages to DMs

## Contributing

Everyone can contribute to this project by adhering to GitHub norms

## Authors

* **Dmitri Matetski** - *Initial work* - [TheGreyCore](https://github.com/TheGreyCore)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details