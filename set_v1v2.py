from sqlalchemy.orm import sessionmaker
from db_engine import engine, SnmpCommunities

Session = sessionmaker(bind=engine)
session = Session()
communities = session.query(SnmpCommunities).all()

Content  = "view   systemonly  included   .1.3.6.1.2.1.1\n"
Content += "view   systemonly  included   .1.3.6.1.2.1.25.1\n"
Content += "agentAddress udp:161,udp6:[::1]:161\n"
Content += "rocommunity public\n"

for community in communities:
    if community.Permission == 0:
        Content += "rocommunity " + community.Community + " " + community.Address + "\n"
    else:
        Content += "rwcommunity " + community.Community + " " + community.Address + "\n"

Content += "pass_persist .1.3.6.1.4.1.39178.100.1 /usr/bin/python -u /var/www/equalizer-agent/agent_extension.py"

with open("/etc/snmp/snmpd.conf", "w") as fd:
    fd.write(Content)
