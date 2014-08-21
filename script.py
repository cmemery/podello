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

    def create_project(self, title='', trello_list='', description=''):
        """ Create a project with values for 
        title, description (with html), and stage/state

        """
        state_map = {
                'Now': 3,
                'Next': 2,
                'Queued': 1,
                'Done': 4
                }

        if description == '':
            description = """No description available"""

        if trello_list == '':
            state = 1 # 'Placeholder for future project'
        else:
            state = state_map[trello_list]

        if title == '':
            title = 'auto-created from trello api'

        #TODO: update Team members on project
        #TODO: add tasks to a project
        #TODO: Add comments/updates to a project

        item = {'fields': [{
            'external_id': 'project-title',
                'values': [{
                    'value': title
            }]},{
            'external_id': 'project-description',
                'values': [{
                    'value': description
            }]},{
            'external_id': 'stage',
                'values': [{
                    'value': state
            }]}]}
        self.con.Item.create(int(app_id), item)

def get_board(trellocon, board):
    for b in trellocon.get_boards():
        if b.name == board:
            return b

def get_list(trellocon, board, listname):
    for l in trellocon.get_lists(board):
        if l.name == listname:
            return l

def import_trello():
    t = TrelloCon()
    p = PodioCon()
    b = get_board(t, board_name)
    print '\nBoard: %s - %s' % (b.id, b.name)
    for l in t.get_lists(b):
        for c in t.get_cards(l):
            p.create_project(title = c.name,
                    trello_list = l.name,
                    description = c.description)
            #card_details = t.get_card_details(c)
            #TODO add checklist items as subtasks?
            #t.print_checklists(card_details)
            #TODO add comments as updates
            #t.print_comments(card_details)
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
        print "  %s - %s" % (project, "")
    return projects['items'][0]
    print "End Podio output"

if __name__ == "__main__":
    pass
    #Debug actions
    #import_trello()
    #output_podio()
