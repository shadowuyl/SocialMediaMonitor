#  -*- coding: utf-8 -*-

from flask import render_template,request,url_for,redirect,session,flash,g
from PIL import Image
from web.models import *
import os,json
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

