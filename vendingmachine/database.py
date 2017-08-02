from pymongo import MongoClient
from bson.objectid import ObjectId
import gridfs
from datetime import datetime
import mimetypes
from pprint import pprint


class Database(object):

    def __init__(self,config=None):

        self.databaseUrl = ''
        self.dbname = ''
        self.dbuser = ''
        self.dbpass = ''


        #get database info from file or parameters
        if config is None:
            self.configFile = 'vendingmachine/config.txt'
            self.loadConfig()
        else:
            self.databaseUrl = config['dburl']
            self.dbname = config['dbname']

        #initialize database client
        uri = 'mongodb://%s:%s@%s/%s?authMechanism=SCRAM-SHA-1'%(self.dbuser,self.dbpass,self.databaseUrl,self.dbname)
        self.dbclient = MongoClient(uri)

        #defind the database name
        self.db = self.dbclient[self.dbname]
        #define the db file system name
        self.fs = gridfs.GridFS(self.db)
        #define the collection names
        self.config = self.db.config
        self.things = self.db.things


    def loadConfig(self):
        print("loading config")
        with open(self.configFile) as config:
            for line in config:

                line = line.replace('\n','')
                line = line.split('::')

                if line[0].upper() == 'DBURL':
                    self.databaseUrl = line[1]
                elif line[0].upper() == 'DBNAME':
                    self.dbname = line[1]
                elif line[0].upper() == 'DBUSER':
                    self.dbuser = line[1]
                elif line[0].upper() == 'DBPASS':
                    self.dbpass = line[1]


    def cleanSku(self,sku):
        sku = sku.upper()
        sku = sku.replace(' ','')
        sku = sku.replace('\n','')
        sku = sku.replace('\t','')
        return sku


    def getSettings(self):
        return self.config.find_one({"_id":"settings"})

    def getLocationsData(self, ins):
        return self.db['locations'].find(ins)

    def insertLocation(self,location):
        self.db.locations.insert_one(location.to_dict())

    def deleteLocation(self,locationID):
        locationID = ObjectId(locationID)
        self.db.locations.delete_one({'_id':locationID})

    def getLocationById(self,locationID):
        locationID = ObjectId(locationID)
        return self.db.locations.find_one({'_id':locationID})

    def updateLocation(self,locationID,location):
        locationID = ObjectId(locationID)
        l = location.to_dict()
        pprint(l)
        self.db.locations.find_one_and_update({'_id':locationID},
            {"$set": {
                       "name": l['name'],
                       "address": l['address'],
                       "contact_number": l['contact_number'],
                       "GPS": l['GPS'],
                       "machine": l['machine'],
                       "history": l['history'],
                       "notes": l['notes'],
                       "contract": l['contract']
                      }})

if __name__ == "__main__":

    db = Database()
    print(db.getSettings())
    input()
