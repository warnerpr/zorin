

class Site(object):

    def __init__(self):
        self.op_events = {}
        self.chats = set()
        self.emails = set()
        self.operators = set()
        self.visitors = set()

    def add_operator_event(self, ts, op, state):
        self.op_events[op] =  sorted(set(self.op_events.get(op, []) + [(ts, state)]))
        self.operators.add(op)
    
    def get_state(self, time_stamp):
#        import pdb; pdb.set_trace()
        states = []
        for op, events in self.op_events.items():
            prev_state = 'offline'# if events[0][1] == 'online' else 'online'
            for ts, state in events:
                if ts > time_stamp:
                    break
                prev_state = state
            states.append(prev_state)
        #print time_stamp, states
        return 'online' if 'online' in states  else 'offline'

    def add_chat(self, time_stamp, visitor):
        if time_stamp in self.chats or time_stamp in self.emails:
            return
        state = self.get_state(time_stamp)
        if state == 'online':
            self.chats.add(time_stamp)
        else:
            self.emails.add(time_stamp)
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
    
    i = 0
    with open(fname) as f:
       for line in f.readlines():
#           if i % 10000 == 0: print 'first pass {}'.format(i)
           i+=1
           data = json.loads(line)
           site_id = data['site_id']
           site = sites.setdefault(site_id, Site())
           if data['type'] == 'status':
               site.add_operator_event(data['timestamp'], data['from'], data['data']['status'])
 
#    from pprint import pprint
#    pprint(sites.values()[0].op_events)
         
    i = 0
    with open(fname) as f:
        for line in f.readlines():
#            if i % 10000 == 0: print 'second pass {}'.format(i)
            i+=1
            data = json.loads(line.strip())
            site_id = data['site_id']
            site = sites[site_id]
            if data['type'] == 'message':
                #print data['timestamp']
                site.add_chat(data['timestamp'], data['from'])

    for site_id, site in sorted(sites.items(), key=lambda _e: _e[0]):
       site.report(site_id)


if __name__ == '__main__':
    main()
