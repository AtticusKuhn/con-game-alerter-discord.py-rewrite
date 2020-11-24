import os
import requests
API_KEY = os.environ.get('YOUTUBE_API_KEY')
async def search_video(channel,keyword):
    result = requests.get(f'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel}&maxResults=1&q={keyword}&key={API_KEY}').json()
    if not "items" in result:
        print(result)
        if "error" in result:
            return {
                "success":False,
                "message":result["error"]["message"]
            }
    return {
        "success":True,
        "message": result["items"][0]["id"]["videoId"]
    }