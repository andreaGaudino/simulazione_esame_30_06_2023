from database.DB_connect import DBConnect



class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllTeams():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct name 
                    from lahmansbaseballdb.teams 
                    order by name"""

        cursor.execute(query, ())

        for row in cursor:
            result.append(row["name"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNodes(team):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select `year` 
                    from lahmansbaseballdb.teams 
                    where name = %s
                    order by name, `year` """

        cursor.execute(query, (team,))

        for row in cursor:
            result.append(row["year"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges(team):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select a1.`year` as y1, a.`year` as y2, count(a.playerID) as tot
                    from lahmansbaseballdb.appearances a1, lahmansbaseballdb.appearances a, lahmansbaseballdb.teams t 
                    where a1.`year` < a.`year` 
                    and t.name = %s
                    and t.`year` = a.`year` 
                    and a1.teamCode = t.teamCode 
                    and a.teamCode = a1.teamCode 
                    and a.teamCode = t.teamCode 
                    and a.ID != a1.ID 
                    and a.playerID = a1.playerID
                    group by a1.`year`, a.`year`
                    order by a1.`year` 
                    """

        cursor.execute(query, (team,))

        for row in cursor:
            result.append([row["y1"], row["y2"], row["tot"]])

        cursor.close()
        conn.close()
        return result
