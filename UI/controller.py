import flet as ft

from model.nerc import Nerc


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._idMap = {}
        self.fillIDMap()

    def handleWorstCase(self, e):
        #print("CLICK su Worst Case")

        self._view._txtOut.controls.clear()
        self._view._txtOut.update()

        if self._view._ddNerc.value is None:
            self._view.create_alert("Selezionare un NERC")
            return

        if self._view._txtYears.value is None or self._view._txtYears.value == "" :
            self._view.create_alert("Inserire il numero massimo di anni")
            return

        if self._view._txtHours.value is None or self._view._txtHours.value == "" :
            self._view.create_alert("Inserire il numero massimo di ore")
            return

        try:
            maxY = int(self._view._txtYears.value)
            maxH = int(self._view._txtHours.value)
        except ValueError:
            self._view.create_alert("Anni e ore devono essere interi")
            return

        print("Input letti:", self._view._ddNerc.value, maxY, maxH)

        if maxY < 0 or maxH <= 0:
            self._view.create_alert("Inserire valori validi")
            return

        nerc = self._idMap[self._view._ddNerc.value]
        print("NERC selezionato:", nerc)

        #print("PRIMA di worstCase")
        soluzione, clienti, ore = self._model.worstCase(nerc, maxY, maxH)
        #print("DOPO worstCase")
        print("Risultato:", len(soluzione), clienti, ore)

        self._view._txtOut.controls.append(ft.Text(f"Tot people affected: {clienti}"))
        self._view._txtOut.controls.append(ft.Text(f"Tot hours of outages: {ore}"))
        self._view._txtOut.controls.append(ft.Text(""))

        for ev in soluzione:
            self._view._txtOut.controls.append(ft.Text(str(ev)))

        self._view.update_page()


    def fillDD(self):
        nercList = self._model.listNerc

        for n in nercList:
            self._view._ddNerc.options.append(
                ft.dropdown.Option(key=n.value, text=n.value))
        self._view.update_page()

    def fillIDMap(self):
        values = self._model.listNerc
        for v in values:
            self._idMap[v.value] = v
