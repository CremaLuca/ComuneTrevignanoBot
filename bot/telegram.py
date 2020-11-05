import env_file
import requests

envs = env_file.get()
token = envs['TELEGRAM_BOT_TOKEN']
channel_id = envs['TELEGRAM_CHANNEL_ID']

def send_message(content : str, disable_web_preview : bool = True):
    post_content = {
        'Accept': 'application/json',
        'parse_mode': 'MarkdownV2',
        'disable_web_page_preview': disable_web_preview,
        'chat_id': channel_id,
        'text': content
        }
    r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage", json=post_content)
    response = r.json()
    if(not response['ok']):
        print(response)

def send_photo_url(content : str, photo_url : str, disable_web_preview : bool = True):
    post_content = {
        'Accept': 'application/json',
        'parse_mode': 'MarkdownV2',
        'disable_web_page_preview': disable_web_preview,
        'chat_id': channel_id,
        'caption': content,
        'photo': photo_url
        }
    r = requests.post(f"https://api.telegram.org/bot{token}/sendPhoto", json=post_content)
    response = r.json()
    if(not response['ok']):
        print(response)

def escape_text(text : str):
    '''
    Places \ before every telegram's required character to use MarkdownV2 interpreter.
    '''
    return text.translate(str.maketrans({"-":  r"\-",
                                          "\\": r"\\",
                                          "^":  r"\^",
                                          "*":  r"\*",
                                          ".":  r"\.",
                                          "_":  r"\_",
                                          "[":  r"\[",
                                          "]":  r"\]",
                                          "(":  r"\(",
                                          ")":  r"\)",
                                          "~":  r"\~",
                                          "`":  r"\`",
                                          ">":  r"\>",
                                          "#":  r"\#",
                                          "+":  r"\+",
                                          "=":  r"\=",
                                          "|":  r"\|",
                                          "{":  r"\{",
                                          "}":  r"\}",
                                          "!":  r"\!"}))
