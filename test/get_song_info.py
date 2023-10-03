import yt_dlp as youtube_dl

ydl_options = {'format': 'bestaudio'}

url = "https://www.youtube.com/watch?v=PLevj9bdRRA&ab_channel=%E3%83%94%E3%83%8E%E3%82%AD%E3%82%AA%E3%83%94%E3%83%BCPINOCCHIOPOFFICIALCHANNEL"

with youtube_dl.YoutubeDL(ydl_options) as ydls:
    info = ydls.extract_info(url,download=False)

print(info)

print(info['title'])
print(info['uploader'])
print(info['url'])
print(info['original_url'])
print(info['thumbnail'])