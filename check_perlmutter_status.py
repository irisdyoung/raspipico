# note: run this at sparse enough intervals to avoid getting our IP address blocked. Should be at least 10 seconds.
from urllib.request import urlopen, Request

def check_perlmutter_status():
    url = Request('https://www.nersc.gov/live-status/motd/',
	    headers={'User-Agent': 'Mozilla/5.0'})

    try:
        contents =  urlopen(url).read()
        splitlines = contents.splitlines()
        perl_line = [splitlines[i] for i in range(len(splitlines)) if splitlines[i].rfind(b'<b>Perlmutter</b>:') > 0][0]
        perl_is_down = perl_line.rfind(b'color:red') > 0
        if perl_is_down:
	        return 'Perlmutter is down or degraded.'
        else:
            return 'Perlmutter is OK.'
    except Exception as e:
        print('Encountered exception when checking Perlmutter status: {}'.format(e))
        return 'Could not check Perlmutter status.'

