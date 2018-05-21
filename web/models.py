from web import db
# from datetime import date
# from hashlib import md5


# class Subscription(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     channel_id=db.Column(db.String(50),nullable=False,unique=True)
#     subscribersNum=db.Column(db.Integer)
#     titile=db.Column(db.String(200))
#     customUrl=db.Column(db.String(200))
#     publishedAt=db.Column(db.DateTime())
#     thumbnails_url=db.Column(db.String(200))
#     thumbnails_path = db.Column(db.String(100))
#     country=db.Column(db.String(70))
#
#     def __init__(self,channel_id,subscribersNum,titile,customUrl,publishedAt,thumbnails_url,thumbnails_path,country):
#         self.channel_id=channel_id
#         self.subscribersNum=subscribersNum
#         self.titile=titile
#         self.customUrl=customUrl
#         self.publishedAt=publishedAt
#         self.thumbnails_url=thumbnails_url
#         self.thumbnails_path=thumbnails_path
#         self.country=country
#
#     def __repr__(self):
#         return '<Subscription %r>' % self.title


class PlayList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    playlist_id=db.Column(db.String(100),nullable=False,unique=True)
    channel_id = db.Column(db.String(50), nullable=False, unique=True)
    publishedAt=db.Column(db.DateTime())
    title=db.Column(db.String(200))

    def __init__(self,playlist_id,channel_id,publishedAt,title,description):
        self.playlist_id=playlist_id
        self.channel_id=channel_id
        self.publishedAt=publishedAt
        self.title=title
        self.description=description

    def __repr__(self):
        return '<playlist %r>' % self.playlist_id


class Channels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    channel_id=db.Column(db.String(50),nullable=False,unique=True)
    title=db.Column(db.String(200))
    description = db.Column(db.String(1000),nullable=True)
    homeUrl=db.Column(db.String(200))
    publishedAt=db.Column(db.DateTime())
    thumbnails_path = db.Column(db.String(100))
    subscriberCount=db.Column(db.Integer,nullable=True)
    videoCount=db.Column(db.Integer,nullable=True)
    commentCount=db.Column(db.Integer,nullable=True)
    viewCount=db.Column(db.Integer,nullable=True)

    def __init__(self,channel_id,title,description,homeUrl,publishedAt,thumbnails_path,subscriberCount,videoCount,commentCount,viewCount):
        self.channel_id=channel_id
        self.title=title
        self.description=description
        self.homeUrl=homeUrl
        self.publishedAt=publishedAt
        self.thumbnails_path=thumbnails_path
        self.subscriberCount=subscriberCount
        self.videoCount=videoCount
        self.commentCount=commentCount
        self.viewCount=viewCount

    def __repr__(self):
        return '<Subscription %r>' % self.title


class Videos(db.Model):
    __tablename__ = 'yt_videos'
    id = db.Column(db.Integer, primary_key=True)
    video_id=db.Column(db.String(100),nullable=False,unique=True)
    video_url=db.Column(db.String(100),nullable=False,unique=True)
    video_embed_url=db.Column(db.String(100),nullable=False,unique=True)
    channel_id = db.Column(db.String(50))
    title=db.Column(db.String(200))
    publishedAt = db.Column(db.DateTime())
    video_path=db.Column(db.String(200))
    description = db.Column(db.String(500))
    tvlogo=db.Column(db.Integer,nullable=True)
    protest=db.Column(db.Integer,nullable=True)
    uploader=db.Column(db.String(100))
    show_img_path=db.Column(db.String(100))
    tvlogo_img_path=db.Column(db.String(100))
    protest_img_path=db.Column(db.String(100))
    viewCount=db.Column(db.Integer,nullable=True)
    likeCount=db.Column(db.Integer,nullable=True)
    commentCount=db.Column(db.Integer,nullable=True)

    def __init__(self,video_id,video_url,video_embed_url,channel_id,uploader,title=None,publishedAt=None,video_path=None,description=None,tvlogo=None,
                 protest=None,show_img_path=None,tvlogo_img_path=None,protest_img_path=None,viewCount=None,likeCount=None,commentCount=None):
        self.video_id=video_id
        self.video_url=video_url
        self.video_embed_url=video_embed_url
        self.channel_id=channel_id
        self.uploader=uploader
        self.title=title
        self.publishedAt=publishedAt
        self.video_path=video_path
        self.description=description
        self.tvlogo=tvlogo
        self.protest=protest
        self.show_img_path=show_img_path
        self.tvlogo_img_path=tvlogo_img_path
        self.protest_img_path=protest_img_path
        self.viewCount=viewCount
        self.likeCount=likeCount
        self.commentCount=commentCount

    def __repr__(self):
        return '<Video %r>' % self.video_id

class demo_video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.String(100), nullable=False, unique=True)

    def __init__(self,video_id):
        self.video_id=video_id

    def __repr__(self):
        return '<video id %r>'%self.video_id
