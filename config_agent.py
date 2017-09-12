# -*- coding: utf-8 -*-
import json
import logging
from db_engine import engine, SNMPConfig
from sqlalchemy.orm import sessionmaker
from subprocess import call


def read_config():
    with open("/var/www/equalizer-agent/agent_config.json") as fd:
        #The file format is
        config = json.loads(fd.read())
        return config
    return None

def stop_services():
    logging.info("Stopping services")
    call(["/etc/init.d/equalizer-traps", "stop"])
    call(["/etc/init.d/snmpd", "stop"])

def start_trap_service():
    logging.info("Starting trap service")
    call(["/etc/init.d/equalizer-traps", "start"])

def start_snmpd_service():
    logging.info("Starting snmpd service")
    call(["/etc/init.d/snmpd", "start"])

def main_cli():
    """Enable SNMP agent parametrization"""
    Session = sessionmaker(bind=engine)
    session = Session()
    config = read_config()

    # Log new configuration parameters
    # for k in config:
    #     print("K", k, "VAL", config[k])

    if config:
        db_config = session.query(SNMPConfig).first()
        if db_config:
            # Log Configuration changes
            logging.info("Modificando destino das traps de {0} para {1}".format(db_config.trapDestination, config["trapDestination"]))
            logging.info("Modificando porta de envio de traps de {0} para {1}".format(db_config.trapPort, config["trapPort"]))
            logging.info("Modificando periodicidade de envio de traps de {0} s para {1} s".format(db_config.trapSendPeriod, config["trapSendPeriod"]))
            logging.info("Modificando periodicidade de atualização SNMP de {0} s para {1} s".format(db_config.agentUpdatePeriod, config["agentUpdatePeriod"]))
            db_config.trapDestination = config["trapDestination"]
            db_config.trapPort = config["trapPort"]
            db_config.trapSendPeriod = config["trapSendPeriod"]
            db_config.agentUpdatePeriod = config["agentUpdatePeriod"]
            session.add(db_config)
            session.commit()
        if config["trapSender"] == "on":
            start_trap_service()
        if config["snmpAgent"] == "on":
            start_snmpd_service()
    else:
        logging.info("Não há arquivo de configuração disponível")

if __name__ == "__main__":
    logging.basicConfig(filename='/var/www/equalizer-agent/configuration.log',level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M')
    logging.info("Iniciando configurador do SNMP")
    stop_services()
    main_cli()