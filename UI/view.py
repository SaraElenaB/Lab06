import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Lab 06"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self._ddAnno = None
        self._ddBrand = None
        self._ddRetailer = None
        self._btnTopVendite = None
        self._btnAnalizzaVendite = None

    def load_interface(self):
        # title
        self._title = ft.Text("Analizza Vendite", color="blue", size=24)

        #row1
        self._ddAnno = ft.Dropdown( label="anno", width=200, expand=True,
                                    options= [ ft.dropdown.Option("Nessun filtro")] )
                                    #inizializzo con una stringa "Nessun filtro"
        self._controller.fillddAnno(self._ddAnno)

        self._ddBrand = ft.Dropdown( label="brand", width=200, expand=True,
                                     options= [ ft.dropdown.Option("Nessun filtro")])
        self._controller.fillddBrand(self._ddBrand)

        self._ddRetailer = ft.Dropdown( label="retailer", width=200, expand=True,
                                        options= [ ft.dropdown.Option("Nessun filtro")])
        self._controller.fillddRetailer(self._ddRetailer)
        row1= ft.Row( [self._ddAnno, self._ddBrand, self._ddRetailer], alignment=ft.MainAxisAlignment.CENTER)


        #row2
        self._btnTopVendite = ft.ElevatedButton( text="Top Vendite", width=300,
                                                 on_click= self._controller.handleTopVendite)
        self._btnAnalizzaVendite = ft.ElevatedButton( text="Analizza Vendite", width=300,
                                                      on_click= self._controller.handleAnalisiVendite)
        row2= ft.Row( [self._btnTopVendite, self._btnAnalizzaVendite], alignment=ft.MainAxisAlignment.CENTER)

        #Output
        self.lvTxtOut = ft.ListView(expand=True)


        #Visualizzare
        self._page.add(self._title, row1, row2, self.lvTxtOut)
        self._page.update()

    #-----------------------------------------------------------------------------------------------------------------------------
    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    # -----------------------------------------------------------------------------------------------------------------------------
    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
