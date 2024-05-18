import scrapetube
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import json

SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS = Credentials.from_service_account_file('google_creds.json', scopes=SCOPE)

file = open("my_creds.json", 'r', encoding='utf-8')
data = json.load(file)
URL = data["URL"]
BOT_TOKEN = data["BOT_TOKEN"]
CHAT_IDS = data["CHAT_IDS"]

PREFIX = "https://www.youtube.com/watch_videos?video_ids="
SIZE = 35
NOW = datetime.now()


def read_file(file_path):
    client = gspread.authorize(CREDS)
    sheet = client.open_by_url(file_path)
    worksheet = sheet.worksheet('all_data (копия)')
    data = worksheet.get_all_values()

    worksheet = sheet.worksheet('STRING')
    msg = [item[0] for item in worksheet.get_all_values()]

    worksheet = sheet.worksheet('Categories')
    categories = {item[0]: item[1] for item in worksheet.get_all_values()[1:]}

    worksheet = sheet.worksheet('exercises')
    exs = worksheet.get_all_values()
    exs_out = dict()
    i = 0
    for cat in categories:
        exs_out[cat] = exs[(NOW.day + 12//len(categories)*i) % 12][0]
        i += 1

    out = [{'Nickname': row[0], 'Channels': row[1], 'ShortsQnt': row[2], 'Category': row[3]} for row in data[1:]]
    return out, exs_out, msg, categories


def get_videos(data, categories):
    ans = {key: set() for key in categories.keys()}
    print(data)
    for row in data:
        videos = scrapetube.get_channel(channel_username=row['Channels'], content_type='videos')
        shorts = []
        if int(row['ShortsQnt']) != 0:
            shorts = scrapetube.get_channel(channel_username=row['Channels'], content_type='shorts', limit=int(row['ShortsQnt']))

        print(row)
        try:
            for vid in videos:
                try:
                    length = vid['lengthText']['simpleText'].split(':')
                    if len(length) == 1 or len(length) == 2 and (int(length[0]) < 10 or int(length[0]) == 10 and int(length[1]) == 00):
                        ans[row['Category']].add(vid['videoId'])
                        break
                except:
                    print("   Video error")
                    continue
        except:
            print("   Video error")
            pass
        try:
            for vid in shorts:
                try:
                    ans[row['Category']].add(vid['videoId'])
                except:
                    print("   Short error")
                    continue
        except:
            print("   Short error")
            pass
    return ans


def create_playlists(vids):
    playlists = []
    iter = 0
    playlist = PREFIX
    for vid in vids:
        playlist += f"{vid},"
        iter += 1
        if iter == SIZE:
            playlists.append(playlist[:-1])
            playlist = PREFIX
            iter = 0
    if iter != 0:
        playlists.append(playlist[:-1])
    return playlists


def create_message(playlists, msg, exs, ref):
    ans = msg[0]
    for i in range(len(playlists)):
        ans += f"\n\n✔️ <a href='{playlists[i]}'>Плейлист #{i+1} от {NOW.date().strftime("%d/%m/%Y")}</a>"
    ans += (f"\n\n{msg[1]}"
            f"<i>{exs}</i>"
            f"{msg[2]}<a href='{ref}'>Гугл форму</a>"
            f"\n{msg[3]}")
    return ans


def all_way():
    msgs = dict()
    file, exs, msg, cats = read_file(URL)
    vids_ids = get_videos(file, cats)
    for cat in cats:
        playlist = create_playlists(vids_ids[cat])
        msgs[cat] = create_message(playlist, msg, exs[cat], cats[cat])
    return msgs
