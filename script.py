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

    def get_spaces(self, org_id):
        return self.con.Space.find_all_for_org(org_id)

    def get_space(self, urlfragment):
        url = "%s/%s" % (url_root, urlfragment)
        return self.con.Space.find_by_url(url)

    def get_apps(self, space_id):
        return self.con.Application.list_in_space(space_id)

    def get_items(self, app_id):
        items = self.con.Application.get_items(app_id)
        for project in items['items']:
            print project['title']

        #To create an item
        #item = {
        #	"fields":[
        #		{"external_id":"org-name", "values":[{"value":"The Items API sucks"}]}
        #	]
        #}
        #print c.Application.find()
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

if __name__ == "__main__":
    def output_trello():
        t = TrelloCon()
        print 'Trello card data: \n'
        for b in t.get_boards():
            print ' Board: %s \n' % b.name
            for l in t.get_lists(b):
                print '   List: %s \n' % l.name
                for c in t.get_cards(l):
                    print '     Card: %s \n' % c.name
        print 'Trello output complete'

    def print_space(space):
        print "%s \n" % space['name']
        for k,v in space.iteritems():
            print "%s: %s" % (k, v)

    def output_podio():
        p = PodioCon()
        #spaces = p.get_spaces(org_id)
        #for space in spaces:
        #    print space
        workspace_id = p.get_space(space_name)
        apps = p.get_apps(workspace_id)
        for app in apps:
            if app['config']['name'] == 'Projects':
                print "%d: %s" % (app['app_id'], app['config']['name'])

    #output_trello()
    output_podio()
