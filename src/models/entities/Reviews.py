from utilities.DateFormat import DateFormat

class Reviews:
    def __init__(self, reviewID, imageUrl=None, name=None, rating=None, comment=None, creationDate=None) -> None:
        self.reviewID = reviewID
        self.imageUrl = imageUrl
        self.name = name
        self.rating = rating
        self.comment = comment
        self.creationDate = creationDate


    def review_to_JSON(self):
        return {
            "reviewID": self.reviewID,
            "imageUrl": self.imageUrl,
            "name": self.name,
            "rating": self.rating,
            "comment": self.comment,
            "creationDate": DateFormat.convert_date(self.creationDate)
        }