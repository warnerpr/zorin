import sys
import json

from ZODB import FileStorage, DB
from persistent.mapping import PersistentMapping
import transaction
storage = FileStorage.FileStorage('/tmp/zreport2.db')
db = DB(storage)
connection = db.open()
root = connection.root()
with transaction.manager:
    root['visitors'] = PersistentMapping()


class Site(object):

    def __init__(self):
        self.op_events = {}
        self.chats = set()
        self.emails = set()
        self.operators = set()

    def add_operator_event(self, ts, op, state):
        self.op_events[op] = sorted(set(self.op_events.get(op, []) + [(ts, state)]))
        self.operators.add(op)

    def get_state(self, time_stamp):
        states = []
        for op, events in self.op_events.items():
            prev_state = 'offline'
            for ts, state in events:
                if ts > time_stamp:
                    break
                prev_state = state
            states.append(prev_state)
        return 'online' if 'online' in states else 'offline'

    def add_chat(self, time_stamp, visitor, site_id):
        if time_stamp in self.chats or time_stamp in self.emails:
            return
        state = self.get_state(time_stamp)
        if state == 'online':
            self.chats.add(time_stamp)
        else:
            self.emails.add(time_stamp)

        visitors = root['visitors']
	with transaction.manager:
            visitors.setdefault(site_id, PersistentMapping())[visitor] = None  # no persisted set

    def report(self, site_id):
        visitors = root['visitors'][site_id]
        print "{site_id},messages={messages},emails={emails},operators={operators},visitors={visitors}".format(
            site_id=site_id, messages=len(self.chats), emails=len(self.emails),
            operators=len(self.operators), visitors=len(visitors))


def main():
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
                site.add_chat(data['timestamp'], data['from'], site_id)

    for site_id, site in sorted(sites.items(), key=lambda _e: _e[0]):
        site.report(site_id)


if __name__ == '__main__':
    main()
