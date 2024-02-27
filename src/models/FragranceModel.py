from database.database import get_connection
from .entities.Fragrance import Fragrance
import cloudinary.uploader

class PerfumeRegistry:

    @classmethod
    def add_perfume(self, perfume):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("""INSERT INTO Perfumes (PerfumeID, Name, Brand, Fragrance, 
                               VolumeML, Price, Stock, Rating, Gender, description, ImageURL, Public_id) 
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                               (perfume.perfumeID, perfume.name, perfume.brand, perfume.fragrance, perfume.volumeML, 
                                perfume.price, perfume.stock, perfume.rating, perfume.gender, perfume.description, perfume.imageURL, perfume.public_id))
                affected_row = cursor.rowcount
                connection.commit()
            
            connection.close()
            return affected_row

        except Exception as ex:
          return str(ex)
    

        
    @classmethod
    def get_perfume(self, id):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Perfumes WHERE PerfumeID = %s", id)
                row = cursor.fetchone()

                register = None
                if row != None:
                    register = Fragrance(*row)
                    register = register.to_JSON()
                
            connection.close()
            return [register]

        except Exception as ex:
            return str(ex)
        

    @classmethod
    def get_perfume_gender(self, gender):
        try:
            connection = get_connection()
            perfumes = []

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Perfumes WHERE Gender = %s ORDER BY Rating DESC", gender)
                results = cursor.fetchall()

                for row in results:
                    register = Fragrance(*row)
                    perfumes.append(register.to_JSON())
                
            connection.close()
            return perfumes

        except Exception as ex:
            return str(ex)
        

    @classmethod
    def get_perfumes(self):
        try:
            connection = get_connection()
            perfumes = []

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Perfumes ORDER BY name ASC")
                results = cursor.fetchall()

                for row in results:
                    register = Fragrance(*row)
                    perfumes.append(register.to_JSON())

            connection.close()
            return perfumes

        except Exception as ex:
            return str(ex)
        


    @classmethod
    def get_perfumes_top(self):
        try:
            connection = get_connection()
            perfumes = []

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Perfumes ORDER BY COALESCE(Rating, 0) DESC LIMIT 5")
                results = cursor.fetchall()

                for row in results:
                    register = Fragrance(*row)
                    perfumes.append(register.to_JSON())

            connection.close()
            return perfumes

        except Exception as ex:
            return str(ex)
        

    @classmethod
    def delete_perfume(self, id):
        try:
            connection = get_connection()

            # Obtnemos el id de la imagen de cloudinary
            with connection.cursor() as cursor:
                cursor.execute("SELECT Public_id FROM Perfumes WHERE PerfumeID = %s", id)
                result = cursor.fetchone()
                public_id = result[0] if result else None

            if public_id:
                # Eliminamos la imagen de cloudinary
                image_delete_result = cloudinary.uploader.destroy(public_id)

                if 'result' not in image_delete_result or image_delete_result['result'] != 'ok':
                    return 'Error al eliminar la imagen en Cloudinary'


                # Eliminamos el registro de la base de datos
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM Perfumes WHERE PerfumeID = %s", id)
                    affected_row = cursor.rowcount
                    connection.commit()
                
                connection.close()
                return affected_row
            
            else:
                connection.close()
                return "No se encontró el public_id para el PerfumeID proporcionado."

        except Exception as ex:
            return str(ex)



    @classmethod
    def update_perfume(self, perfume, file=None):
        try:
            connection = get_connection()

            # Verificar si se proporcionó un archivo para la actualización de la imagen
            if file:

                # Eliminamos la imagen de cloudinary
                image_delete_result = cloudinary.uploader.destroy(perfume.public_id)

                if 'result' not in image_delete_result or image_delete_result['result'] != 'ok':
                    return 'Error al actualizar la imagen en Cloudinary'
                
                # Subir la nueva imagen a Cloudinary y obtener su public_id
                new_image_result = cloudinary.uploader.upload(file, folder='uploads')
                new_public_id = new_image_result.get('public_id')

                if new_public_id:
                    # Actualizar la base de datos con la nueva información, incluido el nuevo public_id
                    with connection.cursor() as cursor:
                        cursor.execute("""
                            UPDATE Perfumes SET 
                                Name = %s, 
                                Brand = %s, 
                                Fragrance = %s, 
                                VolumeML = %s, 
                                Price = %s, 
                                Stock = %s, 
                                Rating = %s, 
                                Gender = %s, 
                                Description = %s, 
                                ImageURL = %s, 
                                Public_id = %s
                            WHERE PerfumeID = %s""",
                            (perfume.name, perfume.brand, perfume.fragrance, perfume.volumeML, 
                            perfume.price, perfume.stock, perfume.rating, perfume.gender, 
                            perfume.description, new_image_result['secure_url'], new_public_id, perfume.perfumeID))
                        
                        affected_row = cursor.rowcount
                        connection.commit()

                    connection.close()
                    return affected_row
                
                else:
                    connection.close()
                    return 'Error al actualizar la imagen en Cloudinary.'
                
            else:
                # Actualizar la base de datos sin cambiar la imagen
                with connection.cursor() as cursor:
                    cursor.execute("""
                        UPDATE Perfumes SET 
                            Name = %s, 
                            Brand = %s, 
                            Fragrance = %s, 
                            VolumeML = %s, 
                            Price = %s, 
                            Stock = %s, 
                            Rating = %s, 
                            Gender = %s, 
                            Description = %s 
                            WHERE PerfumeID = %s""",
                        (perfume.name, perfume.brand, perfume.fragrance, perfume.volumeML, 
                        perfume.price, perfume.stock, perfume.rating, perfume.gender, 
                        perfume.description, perfume.perfumeID))
                    affected_row = cursor.rowcount
                    connection.commit()

                connection.close()
                return affected_row

        except Exception as ex:
            return str(ex)
