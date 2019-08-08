from socket import gethostname
from popen2 import popen2
from lxml import etree

VALID_HOSTS = ["g2.hpc.swin.edu.au"]

class InvalidHost(Exception):
    def __init__(self):
        msg = "\n".join(("Current host %s not in list of valid hosts."%gethostname(),
                         "Host must be one of:",
                         "\n".join(VALID_HOSTS)))
        super(InvalidHost,self).__init__(msg)

class QueueParser(object):
    __ACTIVE_ID = 2
    __ELIGIBLE_ID = 3
    __BLOCKED_ID = 4
    def __init__(self,user):
        """A class to capture information about a given users gstar jobs.

        Args: 
        user -- gstar username

        Note: When instantiated this object will have three attributes of note:
        QueueParser.active
        QueueParser.eligible
        QueueParser.blocked

        These contain lists of dictionaries containing information about each queue. 
        In turn each queue contains information about each job

        Example:
        
        import queue_parser as qp
        x = qp.QueueParser('bekiaris')
        print x.active
        ...
        [{'sstar': [{'AWDuration': '7892',
        'Account': 'p001_swin',
        'Class': 'sstar',
        'DRMJID': '2877151.pbs.hpc.swin.edu.au',
        'EEDuration': '63459',
        'Group': 'cas',
        'JobID': '2877151',
        'JobName': 'mock_fit_single',
        'MasterHost': 'sstar128',
        'PAL': 'sstar',
        'QOS': 'sstar',
        'ReqAWDuration': '43200',
        'ReqNodes': '1',
        'ReqProcs': '1',
        'RsvStartTime': '1432507622',
        'RunPriority': '1',
        'StartPriority': '1587',
        'StartTime': '1432507622',
        'StatPSDed': '7891.560000',
        'StatPSUtl': '7802.781900',
        'State': 'Running',
        'SubmissionTime': '1432442628',
        'SuspendDuration': '0',
        'User': 'bekiaris'},...

        # This would print the 6th active job on the sstar queue
        print x.active["sstar"][5]
        """
        self.user = user
        if gethostname() not in VALID_HOSTS:
            raise InvalidHost
        self.update()

    def _set_by_queue(self,elements):
        output = {}
        for element in elements:
            info = dict(element.items())
            if not info["QOS"] in output.keys():
                output[info["QOS"]] = []
            output[info["QOS"]].append(info)
        return output

    def update(self):
        o,i = popen2("showq -v -n -w user=%s --format=xml"%(self.user))
        self.qstring = o.read().strip()
        self.xml = etree.fromstring(self.qstring)
        self.active   = self._set_by_queue(self.xml[self.__ACTIVE_ID])
        self.eligible = self._set_by_queue(self.xml[self.__ELIGIBLE_ID])
        self.blocked  = self._set_by_queue(self.xml[self.__BLOCKED_ID])

if __name__ == "__main__":
    import sys
    if len(sys.argv)<=1:
        print "Command line usage: python %s <username>"%(sys.argv[0])
        print "Note: This is designed to be used inside scripts."
        print "Import using: import queue_parser"
    else:
        x = QueueParser(sys.argv[1])
        print "Active Jobs"
        print x.active
        print
        print "Eligible Jobs"
        print x.eligible
        print
        print "Blocked Jobs"
        print x.blocked
