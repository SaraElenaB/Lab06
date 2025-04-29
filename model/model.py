from database.DAO import DAO


class Model:
    def __init__(self):
        pass

    def getAnni(self):
        return DAO.getAnni()

    def getBrand(self):
        return DAO.getBrand()

    def getRetailer(self):
        retailer= DAO.getRetailer()
        retailer.sort(key=lambda r: r.Retailer_name)
        #sorted --> NON modifica l'originale e ritorna direttamente una lista nuova ordinata --> retailer.sorted(retailer, key=lambda r: r.Retailer_name)
        #sort -->ordina la lista in-place e restituisce None --> retailer.sort(key=lambda r: r.Retailer_name)
        return retailer

    def getTopVendite(self, anno, brandCodice, retailerCodice):
        return DAO.getTopVendite(anno, brandCodice, retailerCodice)
        #topVendita= DAO.getTopVendite(anno, brandNome, retailerNome)
        #return topVendite[:5]
        #capisci bene il concetto di tuple

    def getAnalisiVendite(self, anno, brandName, retailerName):
        return DAO.getAnalisiVendite(anno, brandName, retailerName)