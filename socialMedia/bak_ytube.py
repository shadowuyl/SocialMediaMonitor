# "youtube-dl --config-location ytdl.conf --flat-playlist -j '%'"%playlist_url
# "youtube-dl --config-location ytdl.conf -f 'bestvideo[height<=480]' '%' "%video_url
#
# import youtube_dl
#
# ydl_opts = {}
# with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#     # ydl.
#     ydl.download(['https://www.youtube.com/watch?v=BaW_jenozKc'])

from __future__ import unicode_literals
import youtube_dl,os,requests,datetime
from web.models import *

# com1="youtube-dl --proxy socks5://127.0.0.1:1080 --flat-playlist --date 20180101 -j '{}' > 1.json".format(playlist_url)
# com2="youtube-dl --proxy socks5://127.0.0.1:1080 -o --dateafter {} '{}' ".format(20180202,playlist_url)

# with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#     meta = ydl.extract_info(playlist_url, download=False)
#     print(meta)
#     # print(meta['upload_date'],meta['id'],meta['title'],meta['playlist'])

# def getVideos(vids):
#     for i in vids:
#         url='https://www.youtube.com/watch?v='+i
#         # os.system(com0+url)
#     print('ok..')

com_down="youtube-dl --proxy socks5://127.0.0.1:1080 -o '~/wyl/youtube_datas/%(id)s.%(ext)s' -f 'bestvideo[height<=480]' "
com_playlist="youtube-dl --proxy socks5://127.0.0.1:1080 -j --flat-playlist "
prefix_video='https://www.youtube.com/watch?v='
prefix_embed='https://www.youtube.com/embed/'
prefix_path='/home/qyk/wyl/youtube_datas/'
channel_ids=['UCaUw6szjlvBf4cDsXiAn-FA',]
videoIdList=['4dPXZGrCB6Y','Qd4Sk9muT8s','igV5l_ReOgY','THSJmOEuPQw','vDsycjT1_QE','jwBE17j-fj4','GVBou6cAbf0',
             '7OEvK9nO94Y','v4d6c6Mr0c4','5aX9XiddAvA','Sai2gqP2tJU','WFqMAo7u16I','kJSBph8R7N4','eQKd7pYFx5Y','H0_eMLM5DD8',
             '6lUiKC8s_ys','NwtSZU876O8','i59mEp46n-M','3Jxt6sY0rLA','tJnqoagfVRU','z3CyVVb_WPs']

def download_video(video_id):
    if video_id is None:
        return None
    vid = Videos.query.filter_by(video_id=video_id).first()
    if vid is not None:
        return None
    os.system(com_down + video_id)
    vpath = ''
    if os.path.isfile(os.path.join(prefix_path, video_id + '.mp4')):
        vpath = os.path.join(prefix_path, video_id + '.mp4')
    elif os.path.isfile(os.path.join(prefix_path, video_id + '.webm')):
        vpath = os.path.join(prefix_path, video_id + '.webm')
    return vpath


def addSingleVideo(video_id):
    ydl_opts = {'proxy': 'socks5://127.0.0.1:1080'}
    vpath = download_video(video_id)
    if vpath is not None:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(prefix_video + video_id, download=False)
            video = Videos(video_id=video_id, video_url=prefix_video+video_id,video_embed_url=prefix_embed + video_id, uploader=meta['uploader'],
                           title=meta['title'], publishedAt=meta['upload_date'], video_path=vpath)
            db.session.add(video)
            db.session.commit()
    print('done..')


def updatePlaylist(playlist_url):
    comd=com_playlist+playlist_url+' >1.out'
    os.system(comd)
    ydl_opts = {'proxy': 'socks5://127.0.0.1:1080'}
    with open("1.out",'r') as f:
        lines=f.readlines()
        for i in lines:
            if i is not None and len(i)>4:
                s=eval(i.strip("/n"))
                if s.get("id"):
                    video_id=s.get("id")
                    addSingleVideo(video_id)
    print('done..')


def getPlaylists(channelId):
    # import socket,socks
    # socks.set_default_proxy(socks.SOCKS5, "localhost", 1080)
    # socket.socket = socks.socksocket
    param = {'key': 'AIzaSyDLuRZADGLobwK3IZWm8uE_M-CeYE3kmS4', 'part': 'snippet,contentDetails', 'maxResults': 50}
    param['channelId'] = channelId
    proxies = {'https': 'socks5:127.0.0.1:1080'}
    r=requests.get('https://www.googleapis.com/youtube/v3/playlists',params=param,proxies=proxies)
    if r.json() is not None:
        playlists_num=r.json()['pageInfo']['totalResults']
        if playlists_num>0 :
            for i in r.json()['items']:
                publishedAt=i['snippet']['publishedAt']
                publishedAt=datetime.datetime(int(publishedAt[0:4]),int(publishedAt[5:7]),int(publishedAt[8:10]),int(publishedAt[11:13]),
                                              int(publishedAt[14:16]),int(publishedAt[17:19]))
                # publishedAt=datetime.datetime.strptime(publishedAt, "%Y-%m-%dT%H:%M:%S.*")
                tmp=PlayList.query.filter_by(playlist_id=i['id']).first()
                if tmp is None:
                    playlist=PlayList(playlist_id=i['id'],channel_id=channelId,publishedAt=publishedAt,title=i['snippet']['title'],description=i['snippet']['description'])
                    db.session.add(playlist)
                    db.session.commit()
    print('done..')


# def getSubscriptions(channelId):
#     proxies = {'https': 'socks5:127.0.0.1:1080'}
#     param = {'key': 'AIzaSyDLuRZADGLobwK3IZWm8uE_M-CeYE3kmS4', 'part': 'snippet,contentDetails'}
#     param['channelId'] = channelId
#     r = requests.get('https://www.googleapis.com/youtube/v3/playlists', params=param, proxies=proxies)

def solve_singleVideos():
    for i in videoIdList:
        addSingleVideo(i)

if __name__ == '__main__':
    solve_singleVideos()

    # getPlaylists('UC4GQAbqmzNTQEY_UnyBkxug')
    # updatePlaylist('https://www.youtube.com/playlist?list=PL8mG-RkN2uTyqrtG2AttO3tj8G_cPRIIr')
    # os.system(com3+playlist_url)
    # getVideos(['mIACpl68XH0','wglaDZpthK4','SjWKuIe57uY'])
