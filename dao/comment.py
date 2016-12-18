class Comment:
    def __init__(self, comment, username, avatarpath, content=None, postid = None ,commentid=None, albumcover=None, songname=None, artistname=None,cdate=None):
        self.comment = comment
        self.username = username
        self.avatarpath = avatarpath
        self.content = content
        self.albumcover = albumcover
        self.songname = songname
        self.artistname = artistname
        self.postid = postid
        self.commentid=commentid
        self.cdate = cdate