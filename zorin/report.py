

class Site(object):

    def __init__(self):
        self.op_events = []
        self.chats = {}
        self.emails = {}
        self.operators = set()
        self.visitors = set()

    def add_operator_event(self, ts, op, state):
        self.transitions = \
            sorted(set(self.op_events + [(ts, op, state)]))
        self.operators.add(op)
    
    def get_state(self, time_stamp):
        op_count = 0
        for ts, op, state in self.transitions:
            if time_stamp >= ts:
                break
            change = 1 if state == 'online' else -1
            op_count += change
        return 'online' if op_count else 'offline'

    def add_chat(self, time_stamp, visitor):
        if time_stamp in self.chats or time_stamp in self.emails:
            return
        state = self.get_state(time_stamp)
        if state == 'online':
            self.chats[time_stamp] = visitor
        else:
            self.emails[time_stamp] = visitor
        self.visitors.add(visitor)

    def report(self, site_id):
        print "{site_id},messages={messages},emails={emails},operators={operators},visitors={visitors}".format(
            site_id=site_id, messages=len(self.chats), emails=len(self.emails), 
            operators=len(self.operators), visitors=len(self.visitors))

def main():
    import sys
    import json
    fname = sys.argv[1]

    sites = {}
    
    with open(fname) as f:
       for line in f.readlines():
           data = json.loads(line)
           site_id = data['site_id']
           site = sites.setdefault(site_id, Site())
           if data['type'] == 'status':
               site.add_operator_event(data['timestamp'], data['from'], data['data']['status'])
          
    with open(fname) as f:
        for line in f.readlines():
            data = json.loads(line.strip())
            site_id = data['site_id']
            site = sites[site_id]
            if data['type'] == 'message':
                site.add_chat(data['timestamp'], data['from'])

    for site_id, site in sites.items():
       site.report(site_id)


if __name__ == '__main__':
    main()
