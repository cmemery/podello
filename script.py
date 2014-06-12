from trello import TrelloClient as tc
from trello_settings import *
from podio_settings import *
from pypodio2 import api

class TrelloCon(object):
    def __init__(self, k = KEY, t = TOKEN):
        self.con = tc(k, token=t)

    def get_boards(self):
        return self.con.list_boards()

    def get_lists(self, board):
        return board.all_lists()

    def get_cards(self, list):
        return list.list_cards()

    def get_card_details(self, card):
        card.fetch()
        return card
        #print c.comments

    def get_checklists(self, card):
        if card.checklists > 1:
            for checklist in card.checklists:
                print 'CHECKLIST:%s' % checklist.name
                for item in checklist.items:
                    print 'ITEM: %s' % item
        else:
            print 'no checklists'

class PodioCon(object):
    def __init__(self, cid=client_id, cs=client_secret, uname=username, passwd=password):
        self.con = api.OAuthClient(cid,cs,uname,password)

    def examples(self):
        pass
        #To create an item
        #item = {
        #	"fields":[
        #		{"external_id":"org-name", "values":[{"value":"The Items API sucks"}]}
        #	]
        #}
        #print c.Application.find(179652)
        #c.Item.create(app_id, item)
        #Undefined and created at runtime example
        #print c.transport.GET.user.status()

        # Other methods are:
        # c.transport.PUT.#{uri}.#{divided}.{by_slashes}()
        # c.transport.DELETE.#{uri}.#{divided}.{by_slashes}()
        # c.transport.POST.#{uri}.#{divided}.{by_slashes}(body=paramDict))
        # For POST and PUT you can pass "type" as a kwarg and register the type as either
        # application/x-www-form-urlencoded or application/json to match what API expects.

        #items[0]['fields'][2]['values'][0]['value']['file_id']
