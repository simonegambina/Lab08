from database.DB_connect import DBConnect
from model.nerc import Nerc
from model.powerOutages import Event


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllNerc():
        conn = DBConnect.get_connection()

        result = []

        if conn is None:
            return result

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT n.id, n.value
                    FROM Nerc n
                    ORDER BY n.value """

        cursor.execute(query)

        for row in cursor:
            result.append(Nerc(row["id"], row["value"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEvents(nerc):
        conn = DBConnect.get_connection()

        result = []

        if conn is None:
            return result

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT p.id,
                   p.event_type_id,
                   p.tag_id,
                   p.area_id,
                   p.nerc_id,
                   p.responsible_id,
                   COALESCE(p.customers_affected, 0) AS customers_affected,
                   p.date_event_began,
                   p.date_event_finished,
                   COALESCE(p.demand_loss, 0) AS demand_loss
            FROM PowerOutages p
            WHERE p.nerc_id = %s
            ORDER BY p.date_event_began """

        cursor.execute(query, (nerc.id,))

        for row in cursor:
            result.append(
                Event(row["id"], row["event_type_id"],
                      row["tag_id"], row["area_id"],
                      row["nerc_id"], row["responsible_id"],
                      row["customers_affected"], row["date_event_began"],
                      row["date_event_finished"], row["demand_loss"]))

        cursor.close()
        conn.close()
        return result