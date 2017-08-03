from vendingmachine.machine import Machine
import datetime
from pprint import pprint
from vendingmachine.database import Database
from re import search
class Location(object):

    def __init__(self,name='TEST', contact_number='000-000-0000', address='0', GPS={'lat':0,'lon':0}, contract={}):
        self.name = name
        self.contact_number = contact_number
        self.address = address
        self.GPS = GPS
        self.machine = Machine()
        #history is a dictionary
        self.history = {}
        #notes is a list of dictionaries (user,note,time)
        self.notes = list()
        #contract is a dict
        self.contract = contract

    def set_history(self, history):
        self.history = history

    def set_notes(self, notes):
        self.notes = notes

    def update_history(self,note,user):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        historyDate = {}
        try:
            historyDate = self.history[now]
            historyDate['note'] = note
        except KeyError:
            historyDate = {}
            historyDate['note'] = ''
        historyDate['user'] = user
        if historyDate['note'] == '':
            historyDate['note'] = note
        else:
            historyDate['note'] = historyDate['note'] + ", " + note
        self.history[now] = historyDate

    def set_name(self,name,user):
        if self.name != name:
            self.update_history("Name updated from " + self.name + " to " + name,user)
            self.name = name

    def set_contact_number(self,number,user):
        if self.contact_number != number:
            self.update_history("contact_number updated from " + self.contact_number + " to " + number,user)
            self.contact_number = number

    def set_address(self,address,user):
        if self.address != address:
            self.update_history("address updated from " + self.address + " to " + address,user)
            self.address = address

    def set_GPS(self,GPS,user):
        if self.GPS['lat'] != GPS['lat'] and self.GPS['lon'] != self.GPS['lon']:
            self.update_history("GPS updated from " + self.GPS['lat'] + "," + self.GPS['lon'] + " to " + GPS['lat'] + "," + GPS['lon'],user)
            self.GPS = GPS

    def update_machine(self,machine,user):
        #self.update_history("machine updated ",user)
        self.machine = machine

    def add_note(self,note,user):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dictionary = {'date':now, 'user':user, 'note':note}
        self.notes.append(dictionary)

    def to_dict(self):
        t = {}
        t['name'] = self.name
        t['contact_number'] = self.contact_number
        t['address'] = self.address
        t['GPS'] = self.GPS
        t['machine'] = self.machine.to_dict()
        t['history'] = self.history
        t['notes'] = self.notes
        t['contract'] = self.contract
        return t

    def set_contract(self,contract,user):
        #self.update_history("contract updated ",user)
        self.contract = contract

    def update_all(self, updates):
        #In order: name,number,address,lat,lon,machine,contract
        user = updates[5].get_user()
        self.set_name(updates[0],user)
        self.set_contact_number(updates[1],user)
        self.set_address(updates[2],user)
        self.set_GPS({"lat":updates[3],"lon":updates[4]},user)
        self.set_contract(updates[6],user)
        self.update_machine(updates[5],user)


if __name__ == "__main__":
    l = Location()
    l.set_name("TEST","USER")
    l.set_contact_number('123-456-6780',"USER")
    pprint.pprint(l.to_dict(),width=1)
    #db = Database()
    #db.db.locations.insert_one(l.to_dict())
    input()
