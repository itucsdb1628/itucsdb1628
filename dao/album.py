class Album:
    def __init__(self, name, cover_filepath, albumdate=None, albumid=None):
        self.name = name
        self.cover_filepath = cover_filepath
        self.albumdate = albumdate
        self.albumid = albumid