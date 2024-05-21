from database.DB_connect import DBConnect
from model.product import Product
from model.sale import Sale


class DAO:
    @staticmethod
    def get_all_products():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select * 
                    from go_products gp"""
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(Product(**row))
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def get_all_sales():
        """
        Restituisce il codice prodotto e il numero di retailer che l'hanno venduto per ogni data
        """
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select *
                    from go_daily_sales gds"""
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(Sale(**row))
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def get_n_sales(p1, p2, year):
        """
        Restituisce il codice prodotto e il numero di retailer che l'hanno venduto per ogni data
        """
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select count(distinct gds2.`Date`) from go_daily_sales gds, go_daily_sales gds2 where 
        gds.Product_number = %s and gds2.Product_number = %s and gds.Retailer_code = gds2.Retailer_code and 
        gds.Date = gds2.`Date` and year(gds.Date) = %s"""
        cursor.execute(query, (p1.Product_number, p2.Product_number, year))
        result = []
        for row in cursor:
            result.append(Sale(**row))
        cursor.close()
        cnx.close()
        return result

