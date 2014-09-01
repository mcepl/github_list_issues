#!/usr/bin/python3
import configparser
import getpass
import json
import logging
import os
from urllib.request import (Request, HTTPSHandler, build_opener,
                            HTTPPasswordMgrWithDefaultRealm)

from urllib2_prior_auth import HTTPBasicPriorAuthHandler


logging.basicConfig(format='%(levelname)s:%(funcName)s:%(message)s',
                    level=logging.INFO)

conf_pars = configparser.SafeConfigParser({
    'user': getpass.getuser(),
    'password': None
})
conf_pars.read(os.path.expanduser("~/.githubrc"))
git_user = conf_pars.get('github', 'user')
git_password = conf_pars.get('github', 'password')
if git_password is None:
    raise ValueError('Missing credentials!')

req = Request("https://api.github.com")

pwd_manager = HTTPPasswordMgrWithDefaultRealm()
pwd_manager.add_password(None, 'https://api.github.com',
                         git_user, git_password)
auth_prior_handler = HTTPBasicPriorAuthHandler(pwd_manager)
verbose_handler = HTTPSHandler(debuglevel=1)

opener = build_opener()
opener.add_handler(verbose_handler)
opener.add_handler(auth_prior_handler)

api_stream = opener.open('https://api.github.com/issues')
iss = json.loads(api_stream.read().decode())

for i in iss:
    title = i['title']
    print("%s // %s:\n%s\n" % (i['repository']['name'], title, i['url']))
