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
                    order by `year` """

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
                    and t.`year` = a1.`year` 
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

    @staticmethod
    def getPlayers(team, anno):
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """select a.`year` as anno, a.playerID as player
                    from lahmansbaseballdb.appearances a, lahmansbaseballdb.teams t 
                    where t.name = %s
                    and t.teamCode = a.teamCode 
                    and t.`year`= a.`year`
                    and t.`year`>= %s"""

        cursor.execute(query, (team,anno))

        for row in cursor:
            year = row['anno']
            giocatore = row['player']
            if year not in result:
                result[year] = [giocatore]
            else:
                result[year].append(giocatore)


        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNamePlayers():
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """select p.playerID as ID, p.nameFirst as Nome, p.nameLast as Cognome
                    from lahmansbaseballdb.people p 
                    order by p.nameLast 
                    """

        cursor.execute(query, ())

        for row in cursor:
            id = row['ID']
            if row['Nome'] is not None:
                cognome_nome = row['Cognome']+" "+row['Nome']
            else:
                cognome_nome = row['Cognome']
            result[id] = cognome_nome

        cursor.close()
        conn.close()
        return result
