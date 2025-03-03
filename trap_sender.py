# -*- coding: utf-8 -*-
from pysnmp.hlapi import *
from sqlalchemy.orm import sessionmaker
from db_engine import engine, AlarmLog, Parameters, SnmpTraps
import json
import logging
import time

def sendTrap(snmpEngine, object_value_list, trapDestination, trapPort, trapCommunity):
    # object_value_list must be something like this
    # [ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0'), OctetString('my string')),
    # ObjectType(ObjectIdentity('1.3.6.1.2.1.1.3.0'), Integer32(42))]))
    next(sendNotification(snmpEngine,CommunityData(trapCommunity),
                          UdpTransportTarget((trapDestination, trapPort)),
                          ContextData(), 'trap', object_value_list))

def trapCheckingLoop(snmpEngine, displayString):
    logging.basicConfig(filename='/var/www/equalizer-agent/trapLog.log',level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M')
    logging.info("Iniciando monitor de traps")
    # Cria sessão com BD
    Session = sessionmaker(bind=engine)
    session = Session()
    # If the parameters table does not exist, do nothing
    cfg = session.query(Parameters).first()
    if cfg:
        logging.info("Parametros {0} {1} {2}".format(cfg.param4, cfg.param5, cfg.param6))
        # Read the trap counter from file, and if it fails assume we have to send everything
        try:
            with open("/var/www/equalizer-agent/trapCount", "r") as fd:
                alarm_count = int(fd.read())
        except:
            alarm_count = 0

        logging.info("Alarm count iniciando em {}".format(alarm_count))

        # Read the DB, check if there is another registry in the DB and send it as a trap
        traps = session.query(SnmpTraps).all() # Query all trap addresses
        trapPort = int(cfg.param5) # standard trap port
        while True:
            al = session.query(AlarmLog).offset(alarm_count)
            logging.info("{} novas entradas".format(al.count()))
            print al.count()
            if al.count() > 0:
                object_list = []
                for item in al:
                    object_list.append(ObjectType(ObjectIdentity('1.3.6.1.4.1.39178.100.1.10'), displayString(item.descricao)))
                for trap in traps:
                    sendTrap(snmpEngine, object_list, trap.Address, trapPort, trap.Community)

                alarm_count += al.count()
                # Save the number of alarms emmited
                with open("/var/www/equalizer-agent/trapCount", "w") as fd:
                    fd.write(str(alarm_count))

            # Wait some time before checking the table again
            time.sleep(int(cfg.param6))
            traps = session.query(SnmpTraps).all() # Query all trap addresses

if __name__ == "__main__":
    # Set the snmpEngine to enable translation
    snmpEngine = SnmpEngine()
    mibBuilder = snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder
    # This is a tuple containing DisplayString as first element
    DisplayString = mibBuilder.importSymbols("SNMPv2-TC","DisplayString")
    trapCheckingLoop(snmpEngine, DisplayString[0])
