class Post:
    def __init__(self, blog):
        self.number = int(blog["id"]) - 1
        self.title = blog["title"]
        self.subtitle = blog["subtitle"]
        self.body = blog["body"]

