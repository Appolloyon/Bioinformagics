#!/usr/bin/env python

class BlastRecord(object):
    """Class to model BLAST results for one Qacc"""

    def __init__(self, ID, Hit, Eval, Title):
        self.ID = ID
        self.hits = []
        self.hits.append([Hit,Eval,Title])

    def print_self(self):
        print self.ID
        for e in self.hits:
            print e

    def get_ID(self):
        return self.ID

    def add(self, Hit, Eval, Title):
        self.hits.append([Hit,Eval,Title])

    def check_hit(self):
        pass

    def return_hit(self):
        pass
