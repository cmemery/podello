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

    def print_comments(self, card):
        if card.comments > 1:
            for comment in card.comments:
                print "Update: %s" % comment['data']['text']
        else:
            print "No Updates"
    def print_checklists(self, card):
        if card.checklists > 1:
            for checklist in card.checklists:
                complete_tasks = []
                incomplete_tasks = []
                print 'CHECKLIST:%s' % checklist.name
                for item in checklist.items:
                    if item['checked'] == False:
                        incomplete_tasks.append(item['name'])
                    else: 
                        complete_tasks.append(item['name'])
                print 'Incomplete tasks: %s' % incomplete_tasks
                print 'Complete tasks: %s' % complete_tasks
        else:
            print 'No checklists'

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

    def get_items(self, app):
        return self.con.Application.get_items(app)

    def create_project(self):
        """ Create a project with values for 
        title, description (with html), and stage/state
        """
        #TODO: Add args to this function to set values
        #TODO: update Team members on project
        #TODO: add tasks to a project
        #TODO: Add comments/updates to a project
        item = {'fields': [{
            'external_id': 'project-title',
            'values': [{
                'value': 'New test project created via API'
                }]},{
            'external_id': 'project-description',
            'values': [{
                'value': """<p>Long description of the project.</p>
                    <p> This project was created via api, and the 
                    description supports limited html</p><ul><li>
                    bullet item 1</li><li>bullet item 2</li></ul>"""
                }]},{
            'external_id': 'stage', 
            'values': [{'value': 3}]}]}
        self.con.Application.create(app_id, item, silent=quiet)

if __name__ == "__main__":
    def output_trello():
        t = TrelloCon()
        for b in t.get_boards():
            if b.name == board_name:
                print '\nBoard: %s - %s' % (b.id, b.name)
                for l in t.get_lists(b):
                    print ' List: %s' % l.name
                    for c in t.get_cards(l):
                        print '  Card: %s' % c.name
                        card_details = t.get_card_details(c)
                        t.print_checklists(card_details)
                        t.print_comments(card_details)
        print 'End Trello output'

    def print_space(space):
        print "%s \n" % space['name']
        for k,v in space.iteritems():
            print "%s: %s" % (k, v)

    def output_podio():
        p = PodioCon()
        print "Begin Podio output"
        print " Projects for %s" % space_name
        projects = p.get_items(app_id)
        for project in projects['items']:
            print "  %s" % project['title']
        return projects['items'][0]
        print "End Podio output"
    #Debug actions
    output_trello()
    output_podio()
