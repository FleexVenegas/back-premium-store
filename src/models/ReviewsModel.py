import cloudinary.uploader
from .entities.Reviews import Reviews
from cloud.Cloud import CloudConfig
from database.database import get_connection


class ReviewsModel:

    @classmethod
    def add_review(self, review, file):
        try:

            CloudConfig.get_connection_cloud()
            cloud_path = cloudinary.uploader.upload(file, folder='upload_reviews')

            if 'secure_url' not in cloud_path:
                return "Error en subir los datos a Claudinary"
            
            pathImage = cloud_path.get('secure_url')
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("""INSERT INTO Reviews (reviewID, imageUrl, name, rating, comment)
                                VALUES (%s, %s, %s, %s, %s)""", (review.reviewID, pathImage, 
                                                                 review.name, review.rating, review.comment))
                affected_row = cursor.rowcount
                connection.commit()
            
            connection.close()
            return affected_row

        except Exception as ex:
            return str(ex)



    @classmethod
    def get_reviews(self):
        try:

            connection = get_connection()
            reviews = []

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Reviews")
                results = cursor.fetchall()

                if results:
                    for row in results:
                        result = Reviews(*row)
                        reviews.append(result.review_to_JSON())
                
            connection.close()
            return reviews

        except Exception as ex:
            return str(ex)
