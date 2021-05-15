import psycopg2
import json
import queries 

class Connection:

    def __init__(self, path_to_json):
        self.connection = None
        self.path = path_to_json

    def openConnection(self):
        try:
            with open(self.path, "r") as handler:
                cred = json.load(handler)

            print(cred)

            self.connection = psycopg2.connect(user = cred["user"],
                                               password = cred["password"] ,
                                               database = cred["database"],
                                               host = cred["host"], 
                                               port = cred["port"])


        except Exception as e:
            print (e)

    def closeConnection(self):
        self.connection.close()
