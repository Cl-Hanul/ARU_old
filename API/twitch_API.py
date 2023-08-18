import requests
from json import load,loads

with open("key.json","r",encoding="utf-8") as file:
    readFile = load(file)
    client_id = readFile["twitch"]["api"]["id"]
    client_secret = readFile["twitch"]["api"]["secret"]

class _TwitchStream:
    def __init__(self,channel_data:dict) -> None:
        try:
            if channel_data[0]['type'] == 'live':
                self.stream = True
                self.title = channel_data[0]['title']
                self.type = channel_data[0]['type']
                self.user_login = channel_data[0]['user_login']
                self.user_name = channel_data[0]['user_name']
                self.category = channel_data[0]['game_name']
                self.thumbnail_url = channel_data[0]['thumbnail_url']
        except:
            self.stream = False

class _TwitchUser:
    def __init__(self,user_data) -> None:
        try:
            user_data[0]
        except:
            self.exist = False
        else:
            self.exist = True
            self.login = user_data[0]["login"]
            self.display_name = user_data[0]["display_name"]
            self.description = user_data[0]["description"]
            self.profile_image_url = user_data[0]["profile_image_url"]
            self.offline_image_url = user_data[0]["offline_image_url"]
            
def get_stream(streamer_id):
    oauth_key = requests.post("https://id.twitch.tv/oauth2/token?client_id=" + client_id + "&client_secret=" + client_secret + "&grant_type=client_credentials")
    authorization = 'Bearer ' + loads(oauth_key.text)["access_token"]
    headers = {'client-id':client_id,'Authorization':authorization}
    res = requests.get('https://api.twitch.tv/helix/streams?user_login=' + streamer_id,headers=headers)
    channel_data = res.json()['data']
    return _TwitchStream(channel_data)

def get_user(user_login):
    oauth_key = requests.post("https://id.twitch.tv/oauth2/token?client_id=" + client_id + "&client_secret=" + client_secret + "&grant_type=client_credentials")
    authorization = 'Bearer ' + loads(oauth_key.text)["access_token"]
    headers = {'client-id':client_id,'Authorization':authorization}
    res = requests.get('https://api.twitch.tv/helix/users?login=' + user_login,headers=headers)
    user_data = res.json()["data"]
    
    return _TwitchUser(user_data)
    
if __name__ == "__main__":
    from os import chdir
    chdir("V2")
    #print(get_stream("m0ngh4").title)
    print(get_user("m0ngh4"))