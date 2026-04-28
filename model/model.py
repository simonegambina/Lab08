from database.DAO import DAO


class Model:
    def __init__(self):
        self._solBest = []
        self._listNerc = None
        self._listEvents = None
        self.loadNerc()


    def worstCase(self, nerc, maxY, maxH):
        self.loadEvents(nerc)
        self._listEvents.sort(key=lambda e: e.date_event_began)
        self._solBest = []

        self.ricorsione([], maxY, maxH, 0)

        return self._solBest, self._totCustomers(self._solBest), self._totHours(self._solBest)


    def ricorsione(self, parziale, maxY, maxH, pos):
        if self._totCustomers(parziale) > self._totCustomers(self._solBest):
            self._solBest = list(parziale)

        for i in range(pos, len(self._listEvents)):
            evento = self._listEvents[i]
            parziale.append(evento)

            if self.isValid(parziale, maxY, maxH):
                self.ricorsione(parziale, maxY, maxH, i + 1)

            parziale.pop()


    def isValid(self, parziale, maxY, maxH):
        if self._totHours(parziale) > maxH:
            return False

        if len(parziale) <= 1:
            return True

        anno_min = parziale[0].date_event_began.year
        anno_max = parziale[-1].date_event_began.year

        if anno_max - anno_min > maxY:
            return False

        return True


    def _totCustomers(self, eventi):
        return sum(e.customers_affected for e in eventi)


    def _totHours(self, eventi):
        return sum(self._eventHours(e) for e in eventi)


    def _eventHours(self, evento):
        delta = evento.date_event_finished - evento.date_event_began
        return delta.total_seconds() / 3600


    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc)


    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()


    @property
    def listNerc(self):
        return self._listNerc