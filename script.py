from trello import TrelloClient as tc
from trello_settings import *
from podio_settings import *
from podio_settings import users
from pypodio2 import api
import json

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

    def get_comments(self, card):
        if card.comments > 1:
            comments = []
            for comment in card.comments:

                comments.append({
                    'date':comment['date'],
                    'text':comment['data']['text'],
                    'username': comment['memberCreator']['username']
                    })
            return comments
        else:
            pass
            #print "No Updates"
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

    def create_project(self, trello_card, trello_list='', tcon = ''):
        """ Create a project with values for 
        title, description (with html), and stage/state

        """
        state_map = {
                'Now': 3,
                'Next': 2,
                'Queued': 1,
                'Done': 4
                }
        c = trello_card
        if c.description == '':
            description = """No description available"""
        else:
            description = c.description
        if trello_list == '':
            state = 1 # 'Placeholder for future project'
        else:
            state = state_map[trello_list]
        if c.name == '':
            title = 'auto-created from trello api'
        else:
            title = c.name
        external_id = c.id
        team = []
        team_values=[]
        comments = []
        for comment in reversed(tcon.get_comments(c)):
            d = comment['date'].split('-')
            date = "%s/%s/%s" % (d[1],d[2][:2], d[0])
            if users.has_key(comment['username']):
                username  = "@[%s](user:%s)" % (comment['username'], users[comment['username']])
                if comment['username'] not in team:
                    team.append(comment['username'])
                    team_values.append({
                        'value': {
                        'id':users[comment['username']],
                        'type': 'user',
                        'user_id': users[comment['username']]}})
                else:
                    pass
            else:
                username = comment['username']
            text = comment['text']
            for user in users:
                richuser = "[%s](user:%s)" % (user, users[user])
                text = text.replace(user, richuser)
            commentdetails = "[trello imported comment]\n %s by %s:\n %s" % (
                    date, username, text)
            comments.append(json.dumps(commentdetails))
        item = {
            'external_id' : external_id,
        'fields': [{
        'external_id': 'project-title',
            'values': [{
                'value': title
        }]},{
        'external_id': 'project-description',
            'values': [{
                'value': description
        }]},{
        'external_id': 'project-team2',
            'values': team_values
            },{
        'external_id': 'link',
            'values': [{
                'url': c.url
        }]},{
        'external_id': 'stage',
            'values': [{
                'value': state
        }]}]}
        print item
        self.con.Item.create(int(app_id), item)
        pitem = self.con.transport.GET('/item/app/%s/external_id/%s' % (app_id, external_id))
        #print 'item %s: %s' % (pitem['item_id'], pitem['title'])
        for item in comments:
            self.create_comment(pitem['item_id'], item)
    def create_comment(self,itemid,comment_text):
        payload = '{"value":%s}' % comment_text
        self.con.transport.POST(url='/comment/item/%s' % 
                itemid, body=payload, type='application/json')
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
    #print '\nBoard: %s - %s' % (b.id, b.name)
    for l in t.get_lists(b):
        for c in t.get_cards(l):
            card_details = t.get_card_details(c)
            p.create_project(c,
                    tcon = t,
                    trello_list = l.name)
            #print c.name
            #TODO add checklist items as subtasks?
            #t.print_checklists(card_details)

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
