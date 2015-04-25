import sys
import json

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
        states = []
        for op, events in self.op_events.items():
            prev_state = False
            for ts, state in events:
                if ts > time_stamp:
                    break
                prev_state = state
            states.append(prev_state)
        return True if True in states else False

    def add_chat(self, time_stamp, visitor):
        if time_stamp in self.chats or time_stamp in self.emails:
            return
        state = self.get_state(time_stamp)
        if state:
            self.chats.add(time_stamp)
        else:
            self.emails.add(time_stamp)
        self.visitors.add(visitor)

    def report(self, site_id):
        print "{site_id},messages={messages},emails={emails},operators={operators},visitors={visitors}".format(
            site_id=site_id, messages=len(self.chats), emails=len(self.emails), 
            operators=len(self.operators), visitors=len(self.visitors))

def main():
  fname = sys.argv[1]

  iterations = []

  for iter in range(0,15): 

    sites = {}
    iterations.append(sites)
    
    with open(fname) as f:
       for line in f.readlines():
           data = json.loads(line)
           site_id = data['site_id']
           site = sites.setdefault(site_id, Site())
           if data['type'] == 'status':
               status = True if data['data']['status'] == 'online' else False
               site.add_operator_event(int(data['timestamp']), intern(str(data['from'])), status)
 
    with open(fname) as f:
        for line in f.readlines():
            data = json.loads(line.strip())
            site_id = data['site_id']
            site = sites[site_id]
            if data['type'] == 'message':
                site.add_chat(int(data['timestamp']), intern(str(data['from'])))

#    for site_id, site in sorted(sites.items(), key=lambda _e: _e[0]):
#       site.report(site_id)
  raw_input("Press Enter to continue...")

  print iterations

if __name__ == '__main__':
    main()

