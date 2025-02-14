import string
import threading
import time
import random
import numpy as np
from datetime import datetime

nodes = []
buffer = {} # items are in the form 'node_id': [(msg_type, value)]

# TODO: Figure out how to have nodes detect they aren't receiving heartbeats.
# TODO: Figure out how to have nodes timeout of elections
# TODO: Figure out how to isolate nodes

class Node:
    def __init__(self,id):
        buffer[id] = []
        self.id = id
        self.silent_period = 0
        self.state = 'follower'
        self.started_election = False
        self.has_voted = False
        self.leader_present = False
        self.notify_once = False
        self.leader = -1
        self.got_heartbeat = False
        self.votes = list()

    def start(self):
        print(f'node {self.id} started')
        threading.Thread(target=self.run).start()

    def isolate(self,secs):
        self.__init__(self.id)
        self.silent_period = secs
        self.state = 'isolate'

    def run(self):
        while True:
            while buffer[self.id]:
                msg_type, value = buffer[self.id].pop(0)
                self.deliver(msg_type,value)

            if self.state == 'isolate':
                time.sleep(self.silent_period)
                print(f"node {self.id} timed out of election")
                self.state = 'follower'
                self.leader_present = False
                self.votes.clear()
                self.leader = -1

            if self.state == 'leader':
                self.broadcast('heartbeat', self.id)
                time.sleep(0.9)
                continue

            if self.state == 'follower':
                if self.got_heartbeat:
                    self.got_heartbeat = False
                    time.sleep(0.9)
                elif not self.leader_present:
                    self.state = 'candidate'
                elif not self.notify_once:
                    print(f"node {self.id} did not receive heartbeat from node {self.leader}")
                    self.notify_once = True
                    self.leader_present = False
                    self.has_voted = False
                    self.started_election = False
                    self.votes.clear()
                    self.leader = -1

            # Count the votes if at least half have voted
            if len(self.votes) >= (len(nodes) / 2.0) and not self.leader_present:
                self.leader_present = True
                self.leader = self.count_votes()
                if self.id == self.leader:
                    self.state = 'leader'
                else:
                    self.state = 'follower'
                    time.sleep(2.0)
                print(f"node {self.id} detected node {self.leader} as leader")

            if self.state == 'candidate' and not self.started_election:
                time.sleep(random.randint(1, 3))
                self.broadcast('candidacy', self.id)
                self.started_election = True
                print(f"node {self.id} is starting an election")

            time.sleep(0.1)

    def broadcast(self, msg_type, value):
        for node in nodes:
            buffer[node.id].append((msg_type,value))
    
    def deliver(self, msg_type, value):
        if msg_type == 'candidacy' and not self.has_voted:
            self.broadcast(f'vote{value}', self.id) # voting for node with id 'value'
            self.has_voted = True
            print(f"node {self.id} voted for node {value}")

        if 'vote' in msg_type:
            candidate = int(msg_type.strip(string.ascii_letters))
            self.votes.append(candidate)

        if msg_type == 'heartbeat':
            self.got_heartbeat = True
            self.notify_once = False
            if self.state == 'candidate':
                self.leader_present = True
                self.leader = value
                self.state = 'follower'
                print(f"node {self.id} got a heartbeat and followed node {value} as leader")

        pass

    def count_votes(self):
        max = 0
        winner = 0
        for i in self.votes:
            freq = self.votes.count(i)
            if freq > max:
                max = freq
                winner = i
        return winner

def main():
    global nodes
    nodes = [Node(i) for i in range(3)]
    for node in nodes:
        node.start()

    time.sleep(10)

    while True:
        act = input('state or isolate > ')
        if act == 'isolate' : 
            id = int(input('node id >'))
            secs = int(input('how many seconds >'))
            nodes[id].isolate(secs)
        elif act == 'state':
            for node in nodes:
                print(f'state of node {node.id}: {node.state}')

if __name__ == "__main__":
    main()