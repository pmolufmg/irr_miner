from.collector import rir

class RirList():
    def __init__(self):
        self.rir_list = [object]

    def base_rir(self):
        ripe = rir('ripe', "whois.ripe.net")
        easynet = rir('easynet', 'whois.noc.easynet.net')
        level3 = rir('level3', 'rr.level3.net')
        afrinic = rir('afrinic', 'whois.afrinic.net')
        radb = rir('radb', 'whois.radb.net')
        nttcom = rir('nttcom', 'rr.ntt.net' )
        bell = rir('bell', 'whois.in.bell.ca')
        apnic = rir('apnic', 'whois.apnic.net')
        bboi = rir('bboi', 'irr.bboi.net')
        canarie = rir('canarie', 'whois.canarie.ca')
        ottix = rir('ottix', 'whois.ottix.net')
        host = rir('host', 'rr.host.net')
        tc = rir('tc', 'whois.bgp.net.br')
        panix = rir('panix', 'rrdb.access.net')
        reach = rir('reach', 'rr.telstraglobal.net')
        altdb = rir('altdb', 'whois.altdb.net')
        risq = rir('risq', 'rr.risq.net')
        rgnet = rir('rgnet', 'whois.rg.net')
        nestegg = rir('nesteg', 'whois.nestegg.net')

