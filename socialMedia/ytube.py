
from __future__ import unicode_literals
import youtube_dl,os,requests,datetime
import sys,os 
sys.path.insert(0,os.getcwd())
from web.models import *
from configs.config import *

proxies = {'https': 'socks5:127.0.0.1:1080'}
com_down="youtube-dl --proxy socks5://127.0.0.1:1080 -o '"+prefix_path+"%(id)s.%(ext)s' -f 'bestvideo"+comd_video_qulity+"' "
com_playlist="youtube-dl --proxy socks5://127.0.0.1:1080 -j --flat-playlist "
prefix_video='https://www.youtube.com/watch?v='
prefix_embed='https://www.youtube.com/embed/'


channelList=['UC16niRr50-MSBwiO3YDb3RA','UCupvZG-5ko_eiXAupbDfxWw','UCpwvZwUam-URkxB7g4USKpg','UCaUw6szjlvBf4cDsXiAn-FA','UCTaMB_RdaghZ26wtaLu2kdA',
             'UCvsye7V9psc-APX6wV1twLg','UC9KqIwTPyFlnSlIWwdjc_oA','UCuUJ0ByfT_9idrRzIFu9OyA']
videoIdList=['NwtSZU876O8','3Jxt6sY0rLA','tJnqoagfVRU','z3CyVVb_WPs','4dPXZGrCB6Y','Qd4Sk9muT8s','igV5l_ReOgY','THSJmOEuPQw','vDsycjT1_QE','jwBE17j-fj4','GVBou6cAbf0',
             '7OEvK9nO94Y','v4d6c6Mr0c4','5aX9XiddAvA','Sai2gqP2tJU','WFqMAo7u16I','kJSBph8R7N4','eQKd7pYFx5Y','H0_eMLM5DD8',
             '6lUiKC8s_ys','ZzKW5Ob8yv0','M3F0goGysfI','3J9h0cCuozk','AcNa6f-bKxI','3Jxt6sY0rLA','kPHXApvGwQU']



def checkVideoSize(video_id):
    param = {'key': 'AIzaSyDLuRZADGLobwK3IZWm8uE_M-CeYE3kmS4', 'part': 'snippet,contentDetails,statistics'}
    param['id'] = video_id
    r = requests.get('https://www.googleapis.com/youtube/v3/videos', params=param, proxies=proxies)
    vlen=r.json()['items'][0]['contentDetails']['duration'][2:]
    if vlen is not None:
        tmp=0
        h=0
        m=0
        for i in vlen:
            if i>='0' and i<='9':
                tmp=tmp*10+int(i)
            elif i=='H':
                h=tmp
                tmp=0
            elif i=='M':
                m=tmp
                tmp=0
            elif i=='S':
                tmp=0
        if h>=1 and m>=1:
            return False
    return True



def download_video(video_id):
    if video_id is None:
        return None
    vid = Videos.query.filter_by(video_id=video_id).first()
    if vid is not None:
        return None
    if not checkVideoSize(video_id):
        return None
    os.system(com_down + video_id)
    vpath = ''
    if os.path.isfile(os.path.join(prefix_path, video_id + '.mp4')):
        vpath = os.path.join(prefix_path, video_id + '.mp4')
    elif os.path.isfile(os.path.join(prefix_path, video_id + '.webm')):
        vpath = os.path.join(prefix_path, video_id + '.webm')
    return vpath


def addSingleVideo(video_id):
    param = {'key': 'AIzaSyDLuRZADGLobwK3IZWm8uE_M-CeYE3kmS4', 'part': 'snippet,contentDetails,statistics'}
    param['id']=video_id
    vpath = download_video(video_id)
    if vpath is not None:
        r = requests.get('https://www.googleapis.com/youtube/v3/videos', params=param, proxies=proxies)
        if r.json() is not None and len(r.json()['items'])>0:
            detail=r.json()['items'][0]['statistics']
            meta=r.json()['items'][0]['snippet']
            imgName = video_id + '.jpg'
            url=''
            if meta['thumbnails'].get('standard') is not None:
                url=meta['thumbnails']['standard']['url']
            elif meta['thumbnails'].get('high') is not None:
                url=meta['thumbnails']['high']['url']
            img = requests.get(url, proxies=proxies)
            if img.status_code == 200:
                if not os.path.isfile(os.path.join(yt_video_normalframe_dir,imgName)):
                    open(os.path.join(yt_video_normalframe_dir,imgName), 'wb').write(img.content)
            publishedAt = meta['publishedAt']
            viewCount,commentCount,likeCount=0,0,0
            if detail.get('viewCount') is not None:
                viewCount=int(detail['viewCount'])
            if detail.get('commentCount') is not None:
                commentCount=int(detail['commentCount'])
            if detail.get('likeCount') is not None:
                likeCount=int(detail['likeCount'])
            publishedAt = datetime.datetime(int(publishedAt[0:4]), int(publishedAt[5:7]), int(publishedAt[8:10]),
                                            int(publishedAt[11:13]),int(publishedAt[14:16]), int(publishedAt[17:19]))
            video = Videos(video_id=video_id, video_url=prefix_video+video_id,video_embed_url=prefix_embed + video_id,channel_id= meta['channelId'],uploader=meta['channelTitle'],show_img_path='yt_frame/'+imgName,title=meta['title'], publishedAt=publishedAt, video_path=vpath,description=meta['description'][0:500],
                           viewCount=viewCount,likeCount=likeCount,commentCount=commentCount)
            db.session.add(video)
            db.session.commit()
    print('done..')


def updatePlaylist(playlist_url):
    comd=com_playlist+playlist_url+' >1.out'
    os.system(comd)
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

    r=requests.get('https://www.googleapis.com/youtube/v3/playlists',params=param,proxies=proxies)
    if r.json() is not None:
        playlists_num=r.json()['pageInfo']['totalResults']
        if playlists_num>0 :
            for i in r.json()['items']:
                publishedAt=i['snippet']['publishedAt']
                publishedAt=datetime.datetime(int(publishedAt[0:4]),int(publishedAt[5:7]),int(publishedAt[8:10]),int(publishedAt[11:13]),
                                              int(publishedAt[14:16]),int(publishedAt[17:19]))
                tmp=PlayList.query.filter_by(playlist_id=i['id']).first()
                if tmp is None:
                    playlist=PlayList(playlist_id=i['id'],channel_id=channelId,publishedAt=publishedAt,title=i['snippet']['title'],description=i['snippet']['description'][0:500])
                    db.session.add(playlist)
                    db.session.commit()
    print('done..')


def getActivities(channelId,pageToken=None):
    param = {'key': 'AIzaSyDLuRZADGLobwK3IZWm8uE_M-CeYE3kmS4', 'part': 'snippet,contentDetails','maxResults':10}
    param['channelId'] = channelId
    if pageToken is not None:
        param['pageToken']=pageToken
    r = requests.get('https://www.googleapis.com/youtube/v3/activities', params=param, proxies=proxies)
    if r.json() is not None and r.json()['pageInfo']['totalResults']>0:
        for i in r.json()['items']:
            if i['snippet']['type']=='upload':
                addSingleVideo(i['contentDetails']['upload']['videoId'])
                print(i['contentDetails']['upload']['videoId'])
        if 'nextPageToken' in r.json().keys():
            getActivities(channelId,r.json()['nextPageToken'])


def getChannelsInfoById(channelId):
    param = {'key': 'AIzaSyDLuRZADGLobwK3IZWm8uE_M-CeYE3kmS4', 'part': 'snippet,contentDetails,statistics'}
    param['id'] = channelId
    r = requests.get('https://www.googleapis.com/youtube/v3/channels', params=param, proxies=proxies)
    if r.json() is not None:
        statistics = r.json()['items'][0]['statistics']
        snippet = r.json()['items'][0]['snippet']
        publishedAt = snippet['publishedAt']
        publishedAt = datetime.datetime(int(publishedAt[0:4]), int(publishedAt[5:7]), int(publishedAt[8:10]),
                                        int(publishedAt[11:13]), int(publishedAt[14:16]), int(publishedAt[17:19]))
        imgName=channelId+'.jpg'
        img=requests.get(snippet['thumbnails']['high']['url'],proxies=proxies)
        if img.status_code == 200:
            if not os.path.isfile(prefix_img_dir+imgName):
                open(prefix_img_dir+imgName, 'wb').write(img.content)
        channel=Channels(channel_id=channelId,title=snippet['title'],description=snippet['description'][0:1000],homeUrl='https://www.youtube.com/channel/'+channelId,
                         publishedAt=publishedAt,thumbnails_path='thumbnails/'+imgName,subscriberCount=int(statistics['subscriberCount']),videoCount=int(statistics['videoCount']),
                         commentCount=int(statistics['commentCount']),viewCount=int(statistics['viewCount']))
        tmp=Channels.query.filter_by(channel_id=channelId).first()
        if tmp is None:
            db.session.add(channel)
            db.session.commit()



def solve_singleVideos():
    for i in videoIdList:
        addSingleVideo(i)


def solve_channelVideos():
#    for i in channelList:
#        tmp = Channels.query.filter_by(channel_id=i).first()
#        if tmp is None:
#            getChannelsInfoById(i)
    for i in channelList:
        getActivities(i)
        

def updateVideoInfo():
    param = {'key': 'AIzaSyDLuRZADGLobwK3IZWm8uE_M-CeYE3kmS4', 'part': 'snippet,contentDetails,statistics'}
    rows=Videos.query.filter_by(viewCount=0).all()
    for i in rows:
        param['id']=i.video_id
        r = requests.get('https://www.googleapis.com/youtube/v3/videos', params=param, proxies=proxies)
        if r.json() is not None and len(r.json()['items'])>0:
            detail=r.json()['items'][0]['statistics']
            viewCount,commentCount,likeCount=0,0,0
            if detail.get('viewCount') is not None:
                i.viewCount=int(detail['viewCount'])
            if detail.get('commentCount') is not None:
                i.commentCount=int(detail['commentCount'])
            if detail.get('likeCount') is not None:
                i.likeCount=int(detail['likeCount'])
            db.session.commit()



if __name__ == '__main__':
    #solve_singleVideos()
    # getActivities('UC4GQAbqmzNTQEY_UnyBkxug')
    #solve_channelVideos()
    updateVideoInfo()
