from database.DB_connect import DBConnect
from model import retailer
from model.brand import Brand
from model.retailer import Retailer


class DAO():

    @staticmethod
    def getAnni():

        cnx= DBConnect.get_connection()
        ris=[]
        if cnx is None:
            print("Connessione fallita")
            return ris
        else:
            cursor = cnx.cursor() #lascio tupla per comodità
            query= """select distinct YEAR(Date) as anno
                      from go_daily_sales gds 
                      order by anno ASC """
            cursor.execute(query)

            for row in cursor:
                ris.append(row[0])

            cursor.close()
            cnx.close()
            return ris


    #--------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def getBrand():

        cnx = DBConnect.get_connection()
        ris = []
        if cnx is None:
            print("Connessione fallita")
            return ris
        else:
            cursor = cnx.cursor( dictionary=True )
            query = """select distinct Product_number, Product_line, Product_type, Product, Product_brand, Product_color, Unit_cost, Unit_price
                       from go_products gp  """
            cursor.execute(query)

            for row in cursor:
                ris.append( Brand( row["Product_number"], row["Product_line"], row["Product_type"], row["Product"], row["Product_brand"], row["Product_color"], row["Unit_cost"], row["Unit_price"] ))

            cursor.close()
            cnx.close()
            return ris

    # --------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def getRetailer():
        #popolare con oggetti

        cnx = DBConnect.get_connection()
        ris = []
        if cnx is None:
            print("Connessione fallita")
            return ris
        else:
            cursor = cnx.cursor( dictionary=True)
            query = """select distinct Retailer_code, Retailer_name, Type, Country
                       from go_retailers gr """
            cursor.execute(query)

            for row in cursor:
                ris.append( Retailer( row["Retailer_code"], row["Retailer_name"], row["Type"], row["Country"]) )

            cursor.close()
            cnx.close()
            return ris

    # --------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def getTopVendite(anno, brandNumero, retailerCodice):

        cnx = DBConnect.get_connection()
        ris = []
        if cnx is None:
            print("Connessione fallita")
            return ris
        else:
            cursor = cnx.cursor( dictionary=True)
            query = """select distinct gds.Date as Data, (gds.Unit_sale_price * gds.Quantity) as Ricavo, gds.Retailer_code as Retailer, gds.Product_number as Prodotto
                       from go_daily_sales gds, go_products gp 
                       where gds.Product_number = gp.Product_number 
                       and YEAR(gds.Date) = COALESCE (%s, YEAR(gds.Date))
                       and gp.Product_brand= COALESCE (%s, gp.Product_brand)
                       and gds.Retailer_code= COALESCE (%s, gds.Retailer_code)
                       order by Ricavo desc"""
                        #i doppioni li elimini dai join
            cursor.execute(query, (anno, brandNumero, retailerCodice))
            rows= cursor.fetchmany(5)
            for row in rows:
                ris.append(row)

            random=cursor.fetchall()
            cursor.close()
            cnx.close()
            return ris

    # --------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def getAnalisiVendite(anno, brand, retailer):

        cnx = DBConnect.get_connection()
        ris = []
        if cnx is None:
            print("Connessione fallita")
            return ris
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select SUM(gds.Unit_sale_price * gds.Quantity) as Affari, COUNT(*) as Vendite, COUNT( distinct gds.Retailer_code) as Retailers, COUNT( distinct gds.Product_number) as Prodotti
                       from go_daily_sales gds, go_products gp, go_retailers gr 
                       where gds.Product_number = gp.Product_number
                       and gds.Retailer_code = gr.Retailer_code 
                       and  YEAR(gds.Date) = COALESCE (%s, YEAR(gds.Date))
                       and gp.Product_brand = COALESCE (%s, gp.Product_brand)
                       and gr.Retailer_name = COALESCE (%s, gr.Retailer_name)"""
         
            cursor.execute(query, (anno, brand, retailer))
            ris = cursor.fetchone()
            cursor.close()
            cnx.close()
            return ris

if __name__ == "__main__":
    vendite = DAO.getAnalisiVendite(2017, "Star", "Connor Department Store")
    print(vendite)

