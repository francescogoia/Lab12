from database.DB_connect import DBConnect
from model.retailer import Retailer


class DAO():
    def __init__(self):
        pass
    @staticmethod
    def get_all_countries():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary = True)
        result = []
        query = """
            select distinct gr.Country 
            from go_retailers gr 
        """
        cursor.execute(query)
        for row in cursor:
            result.append(row["Country"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_reatiler_country(country):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []
        query = """
                    select *
                    from go_retailers gr 
                    where gr.Country = %s
                """
        cursor.execute(query, (country, ))
        for row in cursor:
            result.append(Retailer(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_archi(r1, r2, anno):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []
        query = """
                select gds1.Retailer_code as R1,  gds2.Retailer_code as R2, count( distinct gds1.Product_number) as NumProdInComune
                from go_daily_sales gds1, go_daily_sales gds2
                where gds1.Retailer_code = %s and gds2.Retailer_code = %s and gds2.Product_number = gds1.Product_number
                        and year (gds2.`Date`) = %s and year (gds1.`Date`) = year (gds2.`Date`)
                        """
        cursor.execute(query, (r1, r2, anno,))
        for row in cursor:
            if (row["R1"] != None):
                result.append(row)
                #print(row)
        cursor.close()
        conn.close()
        return result


if __name__ == "__main__":
    d = DAO()
    #print(d.get_all_countries())
    print(d.get_reatiler_country("France"))