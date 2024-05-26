from database.DB_connect import DBConnect
from model.product import Product
from model.sale import Sale


class DAO:
    @staticmethod
    def get_all_colors():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select distinct gp.Product_color 
                    from go_products gp
                    order by gp.Product_color"""
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row['Product_color'])
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def get_products_by_color(color):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select * 
                    from go_products gp
                    where gp.Product_color = %s"""
        cursor.execute(query, (color,))
        result = []
        for row in cursor:
            result.append(Product(**row))
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def get_n_sales(p1, p2, year):
        """
        Restituisce il numero di vendite in giorni diversi di una coppia di prodotti per lo stesso retailer
        """
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select count(distinct gds2.`Date`) vendite
        from go_daily_sales gds, go_daily_sales gds2 
        where gds.Product_number = %s and gds2.Product_number = %s and gds.Retailer_code = gds2.Retailer_code and 
        gds.Date = gds2.`Date` and year(gds.Date) = %s"""
        cursor.execute(query, (p1.Product_number, p2.Product_number, year))
        result = None
        for row in cursor:
            result = row["vendite"]
        cursor.close()
        cnx.close()
        return result

