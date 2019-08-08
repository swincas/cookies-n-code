from popen2 import popen3
from lxml import etree

class NvidiaStats(dict):
    """Get the stats of the available nvidia devices via the nvidia-smi tool.
    
    In [1]: import gpu_info_parser as gip

    In [2]: info = gip.NvidiaStats()

    In [3]: print info
    {'driver': '340.32',
    'ngpus': 2,
    'serials': ['0322211078822', '0322211078739'],
    'types': ['Tesla C2070', 'Tesla C2070']}
    """
    def __init__(self):
        super(NvidiaStats,self).__init__({})
        self._xml = None
        self._read_info()

    def _read_info(self):
        o,i,e = popen3("nvidia-smi -q -x")
        error = e.read()
        if error:
            raise Exception(error)
        _xml = etree.fromstring(o.read())
        self["driver"] = _xml.find("driver_version").text
        gpus = _xml.findall("gpu")
        self["ngpus"] = len(gpus)
        self["types"]  = [i.find("product_name").text for i in gpus]
        self["serials"] = [i.find("serial").text for i in gpus]
        self._xml = _xml

if __name__ == "__main__":
    print NvidiaStats()
