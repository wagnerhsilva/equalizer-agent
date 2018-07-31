from sqlalchemy.orm import sessionmaker
from db_engine import engine, SnmpCfgs

Session = sessionmaker(bind=engine)
session = Session()
configs = session.query(SnmpCfgs).all()[0]

Content  = "view   systemonly  included   .1.3.6.1.2.1.1\n"
Content += "view   systemonly  included   .1.3.6.1.2.1.25.1\n"
Content += "agentAddress udp:161,udp6:[::1]:161\n"
if configs.Security == 0:
    Content += "createUser " + configs.User + "\n"
    Content += "rouser " + configs.User + " noauth\n"
elif configs.Security == 1:
    Content += "createUser " + configs.User + " MD5 " + configs.Pass + "\n"
    Content += "rwuser " + configs.User + " auth\n"
elif configs.Security == 2:
    Content += "createUser " + configs.User + " MD5 " + configs.Pass + " DES " + configs.Pass + "\n"
    Content += "rwuser " + configs.User + " priv\n"

Content += "pass_persist .1.3.6.1.4.1.39178.100.1 /usr/bin/python -u /var/www/equalizer-agent/agent_extension.py"

with open("/etc/snmp/snmpd.conf", "w") as fd:
    fd.write(Content)
