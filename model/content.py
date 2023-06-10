class Content:
    def __init__(self, type, title_kr, title_origin, attribute1, attribute2, attribute3, file=None, highlights=None):
        self.type = type
        self.title_kr = title_kr
        self.title_origin = title_origin
        self.attribute1 = attribute1
        self.attribute2 = attribute2
        self.attribute3 = attribute3

        if self.type == "노래":
            self.file = file
            self.highlights = highlights

    def to_dict(self):
        content_dict = {
            "type": self.type,
            "title_kr": self.title_kr,
            "title_origin": self.title_origin,
            "attribute1": self.attribute1,
            "attribute2": self.attribute2,
            "attribute3": self.attribute3,
        }

        if self.type == "노래":
            content_dict["file"] = self.file
            content_dict["highlights"] = self.highlights

        return content_dict
