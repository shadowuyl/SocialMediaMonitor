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
    bk_videos=Videos.query.filter_by(tvlogo=1).order_by(desc(Videos.publishedAt)).limit(10).all()
    pt_videos=Videos.query.filter_by(protest=1).order_by(desc(Videos.publishedAt)).limit(10).all()
    num_bk=0
    if bk_videos is not None:
        num_bk=len(bk_videos)
    num_pt = 0
    if pt_videos is not None:
        num_pt = len(pt_videos)
    return render_template('youtube_video.html',bk_videos=bk_videos,num_bk=num_bk,pt_videos=pt_videos,num_pt=num_pt)
