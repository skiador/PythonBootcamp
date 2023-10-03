class Post:
    def __init__(self, entry):
        self.id = entry["id"]
        self.body = entry["body"]
        self.date = entry["date"]
        self.title = entry["title"]
        self.author = entry["author"]
        self.subtitle = entry["subtitle"]
        self.image_url = entry["image_url"]
        self.image_alt = entry["image_alt"]
