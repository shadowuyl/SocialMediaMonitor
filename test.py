import requests
key='AIzaSyCO0-E2U986dOwSfnQk5o6GBnr57Fr0Jvg'
channelId='UCupvZG-5ko_eiXAupbDfxWw'
param = {'key': key, 'part': 'snippet,contentDetails,statistics'}
param['id'] = channelId
r = requests.get('https://www.googleapis.com/youtube/v3/channels', params=param,proxies={'https':'socks5:127.0.0.1:1080'})
print(r.text)
