#  -*- coding: utf-8 -*-

from flask import render_template,request,url_for,redirect,session,flash,g
from PIL import Image
from web.models import *
import os,json,datetime
from sqlalchemy import or_,and_
from web import app
from sqlalchemy import and_,or_,desc,asc


def test():
    vids=['mIACpl68XH0', 'wglaDZpthK4', 'SjWKuIe57uY']
    for i in vids:
        url='https://www.youtube.com/embed/'+i
        video=Videos(i,url)
        db.session.add(video)
        db.session.commit()


@app.route('/')
def index():
    return redirect(url_for('yt_video_list'))


@app.route('/youtube_video')
def yt_video_list():
    bk_videos=Videos.query.filter_by(tvlogo=1).order_by(desc(Videos.publishedAt)).limit(6).all()
    pt_videos=Videos.query.filter_by(protest=1).order_by(desc(Videos.publishedAt)).limit(6).all()
    num_bk=0
    if bk_videos is not None:
        num_bk=len(bk_videos)
    num_pt = 0
    if pt_videos is not None:
        num_pt = len(pt_videos)
    return render_template('youtube_video.html',bk_videos=bk_videos,num_bk=num_bk,pt_videos=pt_videos,num_pt=num_pt)


@app.route('/channels')
def channels_home():
    channels=Channels.query.filter_by().all()
    return render_template('channels.html',channels=channels)


@app.route('/statistics')
def videos_statistics():
    nmvideos=Videos.query.filter_by().order_by(desc(Videos.viewCount)).limit(10).all()
    bkvideos=Videos.query.filter_by(tvlogo=1).order_by(desc(Videos.viewCount)).limit(10).all()
    ptvideos=Videos.query.filter_by(protest=1).order_by(desc(Videos.viewCount)).limit(10).all()
    return render_template('topStatistic.html',nmvideos=nmvideos,bkvideos=bkvideos,ptvideos=ptvideos)


def getDateRecent(end_date):
    datelist = []
    flag = 0
    month = int(end_date.month) - 6
    if month < 0:
        month = 12 + month
        flag = -1
    from_date = datetime.datetime(year=end_date.year + flag, month=month, day=1)
    flag = 0
    for i in range(8):
        newdate = None
        if i + from_date.month <= 12:
            newdate = datetime.datetime(year=from_date.year + flag, month=i + from_date.month, day=1)
        elif i + from_date.month > 12:
            flag = 1
            newdate = datetime.datetime(year=from_date.year + flag, month=(i + from_date.month) % 12, day=1)
        if newdate <= end_date:
            datelist.append(newdate)
    datelist = datelist[-6:]
    return datelist

def getRecent(end_date):
    datelist=getDateRecent(end_date)
    nm_list=[]
    bk_list=[]
    pt_list=[]
    for inx,date in enumerate(datelist):
        if inx != len(datelist)-1:
            nm_list.append(len(Videos.query.filter(Videos.publishedAt >=date,Videos.publishedAt<datelist[inx+1],Videos.protest==0,Videos.tvlogo==0).all()))
            bk_list.append(len(Videos.query.filter(Videos.publishedAt >=date,Videos.publishedAt<datelist[inx+1],Videos.tvlogo==1).all()))
            pt_list.append(len(Videos.query.filter(Videos.publishedAt >=date,Videos.publishedAt<datelist[inx+1],Videos.protest==1).all()))
        else:
            nm_list.append(len(Videos.query.filter(Videos.publishedAt >=date,Videos.protest==0,Videos.tvlogo==0).all()))
            bk_list.append(len(Videos.query.filter(Videos.publishedAt >=date,Videos.tvlogo==1).all()))
            pt_list.append(len(Videos.query.filter(Videos.publishedAt >=date,Videos.protest==1).all()))
    return datelist,nm_list,bk_list,pt_list

def getOneRecent(end_date,channelId):
    datelist = getDateRecent(end_date)
    nm_list = []
    bk_list = []
    pt_list = []
    for inx, date in enumerate(datelist):
        if inx != len(datelist) - 1:
            nm_list.append(len(Videos.query.filter(Videos.publishedAt >= date, Videos.publishedAt < datelist[inx + 1],
                                                   Videos.protest == 0, Videos.tvlogo == 0,Videos.channel_id==channelId).all()))
            bk_list.append(len(Videos.query.filter(Videos.publishedAt >= date, Videos.publishedAt < datelist[inx + 1],
                                                   Videos.tvlogo == 1,Videos.channel_id==channelId).all()))
            pt_list.append(len(Videos.query.filter(Videos.publishedAt >= date, Videos.publishedAt < datelist[inx + 1],
                                                   Videos.protest == 1,Videos.channel_id==channelId).all()))
        else:
            nm_list.append(
                len(Videos.query.filter(Videos.publishedAt >= date, Videos.protest == 0, Videos.tvlogo == 0).all()))
            bk_list.append(len(Videos.query.filter(Videos.publishedAt >= date, Videos.tvlogo == 1,Videos.channel_id==channelId).all()))
            pt_list.append(len(Videos.query.filter(Videos.publishedAt >= date, Videos.protest == 1,Videos.channel_id==channelId).all()))
    return datelist, nm_list, bk_list, pt_list


@app.route('/channelsStisticsRecent',methods=['GET', 'POST'])
def channelsStisticsRecent():
    if request.method == 'POST':
        channel_name = request.form['channel_name'].strip()
        channel=Channels.query.filter(Channels.title==channel_name).first()
        if channel is not None:
            end_date=datetime.datetime.today()
            datelist, nm_list, bk_list, pt_list = getRecent(end_date)
            # print(datelist,nm_list,bk_list,pt_list)
            # Months=["一月","二月","三月","四月","五月","六月","七月","八月","九月","十月","十一月","十二月"]
            month=[]
            for i in datelist:
                month.append(i.month-1)

            # print(getOneRecent(end_date,'UC16niRr50-MSBwiO3YDb3RA'))
            _, nm1, bk1, pt1=getOneRecent(end_date,channel.channel_id)
            return render_template('recentStistics.html',nm_list=nm_list,bk_list=bk_list,pt_list=pt_list,month=month,
                                   nm1=nm1, bk1=bk1, pt1=pt1)
        else:
            return 'channel name not find...'
    else:
        end_date = datetime.datetime.today()
        datelist, nm_list, bk_list, pt_list = getRecent(end_date)
        month = []
        for i in datelist:
            month.append(i.month - 1)
        return render_template('recentStistics.html', nm_list=nm_list, bk_list=bk_list, pt_list=pt_list, month=month,
                               nm1=None,bk1=None,pt1=None)






@app.route('/demo', methods=['GET', 'POST'])
def demo():
    # video_id='sFx9oDTREm0'
    if request.method == 'POST':
        from socialMedia.ytube import addSingleVideo
        video_id=request.form['video_url'].strip()[-11:]
        addSingleVideo(video_id)
        return '1'
    else:
        return render_template('demo.html')

@app.route('/demo_res',methods=['GET', 'POST'])
def demo_res():
    if request.method == 'POST':
        print(request.form['video_url'])
        video_id = request.form['video_url'].strip()[-11:]
        video = Videos.query.filter_by(video_id=video_id).first()
        tvlogo = "2"
        protest = "2"
        print(video,video['tvlogo'])
        if video is not None:
            if video['tvlogo'] is not None:
                tvlogo = video['tvlogo']
            if video['protest'] is not None:
                protest = video['protest']
        return tvlogo + protest
    else:
        video_id = request.args['video_url'].strip()[-11:]
        video = Videos.query.filter_by(video_id=video_id).first()
        tvlogo = "2"
        protest = "2"
        if video is not None:
            if video['tvlogo'] is not None:
                tvlogo = video['tvlogo']
            if video['protest'] is not None:
                protest = video['protest']
        return tvlogo + protest

