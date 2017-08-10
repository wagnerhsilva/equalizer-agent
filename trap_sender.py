# -*- coding: utf-8 -*-
from pysnmp.hlapi import *
from sqlalchemy.orm import sessionmaker
from db_engine import engine, AlarmLog
import json
import logging
import time

# Set the snmpEngine to enable translation
snmpEngine = SnmpEngine()
mibBuilder = snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder
# This is a tuple containing DisplayString as first element
DisplayString = mibBuilder.importSymbols("SNMPv2-TC","DisplayString")

def sendTrap(object_value_list):
    global snmpEngine
    # object_value_list must be something like this
    # [ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0'), OctetString('my string')),
    # ObjectType(ObjectIdentity('1.3.6.1.2.1.1.3.0'), Integer32(42))]))
    next(sendNotification(snmpEngine,CommunityData('public'),
                          UdpTransportTarget(('192.168.1.149', 162)),
                          ContextData(), 'trap', object_value_list))

def trapCheckingLoop():
    logging.basicConfig(filename='/home/root/equalizer-agent/trapLog.log',level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M')
    logging.info("Iniciando monitor de traps")
    # Cria sessão com BD
    Session = sessionmaker(bind=engine)
    session = Session()
    # Read the trap counter from file, and if it fails assume we have to send everything
    try:
        with open("/home/root/equalizer-agent/trapCount", "r") as fd:
            alarm_count = int(fd.read())
    except:
        alarm_count = 0

    logging.info("Alarm count iniciando em {}".format(alarm_count))

    # Read the DB, check if there is another registry in the DB and send it as a trap
    while True:
        al = session.query(AlarmLog).offset(alarm_count)
        logging.info("{} novas entradas".format(al.count()))
        if al.count() > 0:
            object_list = []
            for item in al:
                object_list.append(ObjectType(ObjectIdentity('1.3.6.1.4.1.39178.100.1.10'), DisplayString[0](item.descricao)))
            sendTrap(object_list)

            alarm_count += al.count()
            # Save the number of alarms emmited
            with open("/home/root/equalizer-agent/trapCount", "w") as fd:
                fd.write(str(alarm_count))

        # Wait some time before checking the table again
        time.sleep(30)

if __name__ == "__main__":
    trapCheckingLoop()
