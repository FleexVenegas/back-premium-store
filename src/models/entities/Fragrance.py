from utilities.DateFormat import DateFormat

class Fragrance:
    def __init__(self, perfumeID, name=None, brand=None, fragrance=None, volumeML=None, 
                price=None, stock=None, creationDate=None, rating=None, gender=None, 
                description=None, imageURL=None, public_id=None ) -> None:
        self.perfumeID = perfumeID
        self.name = name
        self.brand = brand
        self.fragrance = fragrance
        self.volumeML = volumeML
        self.price = price
        self.stock = stock
        self.creationDate = creationDate
        self.rating = rating
        self.gender = gender
        self.description = description
        self.imageURL = imageURL
        self.public_id = public_id


    def to_JSON(self):
        return {
            "perfumeID": self.perfumeID,
            "name": self.name,
            "brand": self.brand, 
            "fragrance": self.fragrance, 
            "volumeML": self.volumeML,
            "price": self.price,
            "stock": self.stock,
            "creationDate": DateFormat.convert_date(self.creationDate),
            "rating": self.rating,
            "gender": self.gender,
            "description": self.description,
            "imageURL": self.imageURL,
            "public_id": self.public_id
        }