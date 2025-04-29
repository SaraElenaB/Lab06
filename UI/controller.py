import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._retailerValue = None
        self._brandValue = None

        self._brandMap= {}
        self._retailerMap = {}

    #-----------------------------------------------------------------------------------------------------------------------------
    def fillddAnno(self, dd: ft.Dropdown):
        #parametro dd: deve comportarsi come un oggetto di tipo ft.Dropdown

        anni= self._model.getAnni() #lista di str
        for a in anni:
            dd.options.append( ft.dropdown.Option(a) ) #oggetto Option contenente str

    # -----------------------------------------------------------------------------------------------------------------------------
    def fillddBrand(self, dd: ft.Dropdown):

        #Io voglio salvare tutti gli oggetti brand che ricavo dal db, ma al tempo stesso
        # avere nel dd solo i nomi dei brand non ripetuti

        all_brands= self._model.getBrand()

        for b in all_brands:
            if b.Product_brand not in self._brandMap:
                self._brandMap[b.Product_brand] = b
                dd.options.append( ft.dropdown.Option( key= b.Product_brand,
                                                       data=b,
                                                       on_click=self.choiceDDbrand
                                                       ))

    def choiceDDbrand(self, e):
        self._brandValue = e.control.data

    # .items() --> restituisce una tupla (chiave, valore) --> (nome_brand, ogg_Brand)
    # for nome_brand, ogg_Brand in brandMap2.items():
    #     dd.options.append( ft.dropdown.Option( key= nome_brand,
    #                                            data= ogg_Brand,   #devo salvare l'oggetto brand come data
    #                                            on_click= self.choiceDDbrand
    #                                            ) )

    # -----------------------------------------------------------------------------------------------------------------------------
    def fillddRetailer(self, dd: ft.Dropdown):

        retailer= self._model.getRetailer()
        for r in retailer:
            if r.Retailer_name not in self._retailerMap:
                self._retailerMap[r.Retailer_name] = r
                dd.options.append( ft.dropdown.Option( key= r.Retailer_name,
                                                       data= r,
                                                       on_click = self.choiceDDretailer))

    def choiceDDretailer(self, e):
        self._retailerValue = e.control.data

    # -----------------------------------------------------------------------------------------------------------------------------
    def handleTopVendite(self, e):

        self._view.lvTxtOut.controls.clear()
        anno= self._view._ddAnno.value
        brandNome= self._view._ddBrand.value
        retailerNome= self._view._ddRetailer.value

        if anno=="Nessun filtro":
            anno=None
        if brandNome=="Nessun filtro":
            brandNome=None
        if retailerNome=="Nessun filtro":
            retailerNome=None

        brand= self._brandMap.get(brandNome)
        retailer= self._retailerMap.get(retailerNome)

        #ATTENZIONE: devi passare il nome del Brand: 1 brand + prodotti
        topVendite = self._model.getTopVendite(anno, brandNome, retailer.Retailer_code )

        if len(topVendite) == 0:
            self._view.lvTxtOut.controls.append( ft.Text(f"Non è stato venduto nessun pezzo per l'anno {anno} del brand {brandNome} dal retailer {retailerNome}"))
            self._view.update_page()
            return

        self._view.lvTxtOut.controls.append( ft.Text( f"Top vendite: "))
        # essendo topVendite una lista di dizionari (fetchmany(5) ) usi for --> lista
        for t in topVendite:
            self._view.lvTxtOut.controls.append( ft.Text( f"Data: {t["Data"]}; Ricavo:{t["Ricavo"]}; Retailer:{t["Retailer"]}; Product:{t["Prodotto"]}\n"))

        self._view.update_page()


    # -----------------------------------------------------------------------------------------------------------------------------
    def handleAnalisiVendite(self, e):

        self._view.lvTxtOut.controls.clear()

        anno = self._view._ddAnno.value
        brandNome = self._view._ddBrand.value
        retailerNome = self._view._ddRetailer.value

        if anno == "Nessun filtro":
            anno = None
        if brandNome == "Nessun filtro":
            brandNome = None
        if retailerNome == "Nessun filtro":
            retailerNome = None

        analizzaVendite = self._model.getAnalisiVendite(anno, brandNome, retailerNome)
        if len(analizzaVendite)==0:
            self._view.lvTxtOut.controls.append( ft.Text( f"Non ci sono statistiche vendite per i valori selezionati, riprovare!"))
            self._view.update_page()
            return

        self._view.lvTxtOut.controls.append( ft.Text( "Statistiche vendite: "))
        # essendo analizzaVendite un singolo dizionario (fetchone() ) non usi for (no lista) ma direttamente append
        a=analizzaVendite
        self._view.lvTxtOut.controls.append(ft.Text(f"Giro d'affari: {a["Affari"]} \n Numero vendite: {a["Vendite"]} \nNumero retailers coinvolti: {a["Retailers"]} \nNumero prodotti coinvolti: {a["Prodotti"]} "))

        self._view.update_page()
    # -----------------------------------------------------------------------------------------------------------------------------









    def handle_hello(self, e):
        name = self._view.txt_name.value
        if name is None or name == "":
            self._view.create_alert("Inserire il nome")
            return
        self._view.txt_result.controls.append(ft.Text(f"Hello, {name}!"))
        self._view.update_page()
