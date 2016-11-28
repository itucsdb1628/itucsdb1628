class Comment:
    def __init__(self, comment, username, avatarpath, content=None, albumcover=None , postid = None ,commentid=None, cdate=None):
        self.comment = comment
        self.username = username
        self.avatarpath = avatarpath
        self.content = content
        self.albumcover = albumcover
        self.postid = postid
        self.commentid=commentid
        self.cdate = cdate