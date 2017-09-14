#!/usr/bin/python -u
# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker
from db_engine import engine, Usuario, Modulo, AlarmeConfig, RedeSeguranca, DataLogRT
from db_engine import TimeServer, EmailServer, AlarmLog, Parameters, ApelidoString, DataLog
import json
import sys
import logging

import snmp_passpersist as snmp

# logging.basicConfig(filename='/home/prjs/cm_comandos_lineares/equalizer-agent/log.log',level=logging.DEBUG,
logging.basicConfig(filename='/var/www/equalizer-agent/log.log',level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')
logging.info("Iniciando agente extra")

# Create DB sessionmaker, every request will have open and close a new session
Session = sessionmaker(bind=engine)

# Load json
# with open("/home/prjs/cm_comandos_lineares/equalizer-agent/element_mib.json", "r") as fd:
with open("/var/www/equalizer-agent/element_mib.json", "r") as fd:
    element_dic = json.loads(fd.read())
    # Set up inverted lookup
    element_dic_inv = {}
    for e in element_dic:
        element_dic_inv[element_dic[e]] = e

logging.info("Carregado arquivo de elmentos/OID")

def addParametersToOIDs(parameter, pp):
    logging.info("Adiciona parameter nos OIDs")
    pp.add_str(element_dic_inv["avg_last"], parameter.avg_last)
    pp.add_str(element_dic_inv["duty_min"], parameter.duty_min)
    pp.add_str(element_dic_inv["duty_max"], parameter.duty_max)
    pp.add_str(element_dic_inv["cte_index"], parameter.cte_index)
    pp.add_str(element_dic_inv["delay"], parameter.delay)
    pp.add_str(element_dic_inv["num_cycles_var_read"], parameter.num_cycles_var_read)
    pp.add_str(element_dic_inv["bus_voltage"], parameter.bus_voltage)
    pp.add_str(element_dic_inv["save_log_time"], parameter.save_log_time)
    pp.add_str(element_dic_inv["disk_capacity"], parameter.disk_capacity)
    pp.add_str(element_dic_inv["param1"], parameter.param1)
    pp.add_str(element_dic_inv["param2"], parameter.param2)
    pp.add_str(element_dic_inv["param3"], parameter.param3)
    pp.add_str(element_dic_inv["param4"], parameter.param4)
    pp.add_str(element_dic_inv["param5"], parameter.param5)
    pp.add_str(element_dic_inv["param6"], parameter.param6)
    pp.add_str(element_dic_inv["param7"], parameter.param7)
    pp.add_str(element_dic_inv["param8"], parameter.param8)
    pp.add_str(element_dic_inv["param9"], parameter.param9)
    pp.add_str(element_dic_inv["param10"], parameter.param10)

def addModultoToOIDs(modulo, pp):
    logging.info("Adiciona modulo nos OIDs")
    pp.add_str(element_dic_inv["descricao"], modulo.descricao)
    # There is a problem with the DB, this value is a String, but the column is defined as Real
    pp.add_str(element_dic_inv["tensao_nominal"], str(modulo.tensao_nominal))
    pp.add_int(element_dic_inv["capacidade_nominal"], modulo.capacidade_nominal)
    pp.add_int(element_dic_inv["n_strings"], modulo.n_strings)
    pp.add_int(element_dic_inv["n_baterias_por_strings"], modulo.n_baterias_por_strings)
    pp.add_str(element_dic_inv["contato"], modulo.contato)
    pp.add_str(element_dic_inv["localizacao"], modulo.localizacao)
    pp.add_str(element_dic_inv["fabricante"], modulo.fabricante)
    pp.add_str(element_dic_inv["tipo"], modulo.tipo)
    pp.add_str(element_dic_inv["data_instalacao"], modulo.data_instalacao)
    pp.add_int(element_dic_inv["conf_alarme_id"], modulo.conf_alarme_id)

def addUsuarioToOIDs(user, pp):
    logging.info("Adiciona usuario nos OIDs")
    i = 1
    for item in user:
        pp.add_str(element_dic_inv["nome"] + "." + str(i), item.nome)
        pp.add_str(element_dic_inv["sobreNome"] + "." + str(i), item.sobreNome)
        pp.add_str(element_dic_inv["telefone"] + "." + str(i), item.telefone)
        pp.add_str(element_dic_inv["email"] + "." + str(i), item.email)
        # pp.add_str(element_dic_inv["senha"], item.senha)
        pp.add_str(element_dic_inv["acesso"] + "." + str(i), item.acesso)
        i += 1

def addRedeToOIDs(rede, pp):
    logging.info("Adiciona rede nos OIDs")
    pp.add_str(element_dic_inv["mac"], rede.mac)
    pp.add_str(element_dic_inv["velocidadePlacaRede"], rede.velocidadePlacaRede)
    pp.add_str(element_dic_inv["localAddress"], rede.localAddress)
    pp.add_str(element_dic_inv["gateway"], rede.gateway)
    pp.add_str(element_dic_inv["mascara"], rede.mascara)
    pp.add_str(element_dic_inv["servidorDNS"], rede.servidorDNS)
    pp.add_str(element_dic_inv["nomeDoSistema"], rede.nomeDoSistema)
    pp.add_str(element_dic_inv["localDoSistema"], rede.localDoSistema)
    pp.add_str(element_dic_inv["contatoDoSistema"], rede.contatoDoSistema)
    pp.add_int(element_dic_inv["httpPort"], rede.httpPort)
    pp.add_int(element_dic_inv["useHttps"], rede.useHttps)
    pp.add_int(element_dic_inv["httpsPort"], rede.httpsPort)
    pp.add_int(element_dic_inv["httpTempoDeAtualizacao"], rede.httpTempoDeAtualizacao)
    pp.add_str(element_dic_inv["paginaPadraoHttp"], rede.paginaPadraoHttp)

def addEmailServerToOIDs(email, pp):
    logging.info("Adiciona EmailServer nos OIDs")
    pp.add_str(element_dic_inv["server"], email.server)
    pp.add_int(element_dic_inv["portaSMTP"], email.portaSMTP)
    pp.add_int(element_dic_inv["usarCriptografiaTLS"], email.usarCriptografiaTLS)
    pp.add_str(element_dic_inv["emailAdmin"], email.email)
    pp.add_str(element_dic_inv["assunto"], email.assunto)
    pp.add_int(element_dic_inv["usarAutenticacao"], email.usarAutenticacao)
    pp.add_str(element_dic_inv["login"], email.login)
    # pp.add_str(element_dic_inv["senha"], email.senha)

def addTimeServerToOIDs(timeserver, pp):
    logging.info("Adiciona timeServer nos OIDs")
    pp.add_str(element_dic_inv["timeServerAddress1"], timeserver.timeServerAddress1)
    pp.add_str(element_dic_inv["timeServerAddress1_complemento"], timeserver.timeServerAddress1_complemento)
    pp.add_str(element_dic_inv["timeServerAddress2"], timeserver.timeServerAddress2)
    pp.add_str(element_dic_inv["timeServerAddress2_complemento"], timeserver.timeServerAddress2_complemento)
    pp.add_str(element_dic_inv["timeServerAddress3"], timeserver.timeServerAddress3)
    pp.add_str(element_dic_inv["timeServerAddress3_complemento"], timeserver.timeServerAddress3_complemento)
    pp.add_int(element_dic_inv["connectionRetries"], timeserver.connectionRetries)
    pp.add_str(element_dic_inv["timeZone"], timeserver.timeZone)
    pp.add_int(element_dic_inv["automAdjustTimeDaylightSavingChanges"], timeserver.automAdjustTimeDaylightSavingChanges)

def addAlarmeConfigToOIDs(ac, pp):
    logging.info("Adiciona alarmeConfig nos OIDs")
    pp.add_str(element_dic_inv["tipo_modulo"], ac.tipo_modulo)
    pp.add_str(element_dic_inv["nivel_alert_tensao_max"], str(ac.nivel_alert_tensao_max))
    pp.add_str(element_dic_inv["nivel_alert_tensao_min"], str(ac.nivel_alert_tensao_min))
    pp.add_str(element_dic_inv["nivel_alert_temp_max"], str(ac.nivel_alert_temp_max))
    pp.add_str(element_dic_inv["nivel_alert_temp_min"], str(ac.nivel_alert_temp_min))
    pp.add_str(element_dic_inv["nivel_alert_impedancia_max"], str(ac.nivel_alert_impedancia_max))
    pp.add_str(element_dic_inv["nivel_alert_impedancia_min"], str(ac.nivel_alert_impedancia_min))
    pp.add_str(element_dic_inv["nivel_max_tensao_ativo"], str(ac.nivel_max_tensao_ativo))
    pp.add_str(element_dic_inv["nivel_max_tensao_val"], str(ac.nivel_max_tensao_val))
    pp.add_str(element_dic_inv["alarme_nivel_tensao_max"], str(ac.alarme_nivel_tensao_max))
    pp.add_str(element_dic_inv["alarme_nivel_tensao_min"], str(ac.alarme_nivel_tensao_min))
    pp.add_str(element_dic_inv["alarme_nivel_temp_max"], str(ac.alarme_nivel_temp_max))
    pp.add_str(element_dic_inv["alarme_nivel_temp_min"], str(ac.alarme_nivel_temp_min))
    pp.add_str(element_dic_inv["alarme_nivel_imped_max"], str(ac.alarme_nivel_imped_max))
    pp.add_str(element_dic_inv["alarme_nivel_imped_min"], str(ac.alarme_nivel_imped_min))
    pp.add_str(element_dic_inv["alarme_nivel_tensaoBarr_min"], str(ac.alarme_nivel_tensaoBarr_min))
    pp.add_str(element_dic_inv["alarme_nivel_tensaoBarr_max"], str(ac.alarme_nivel_tensaoBarr_max))
    pp.add_str(element_dic_inv["alarme_nivel_target_min"], str(ac.alarme_nivel_target_min))
    pp.add_str(element_dic_inv["alarme_nivel_target_max"], str(ac.alarme_nivel_target_max))

def addApelidoStringToOIDs(ap_list, pp):
    logging.info("Adiciona apelidos nos OIDs")
    i = 1
    for item in ap_list:
        pp.add_str(element_dic_inv["ap_string"] + "." + str(i), item.string)
        pp.add_str(element_dic_inv["apelido"] + "." + str(i), item.apelido)
        i += 1

def addBateriaToOIDs(bat_list, pp, n_bat, n_string):
    # Add table lines to "bateria"
    i = 1
    target = 0
    for item in bat_list:
        logging.info("Adiciona bateria {} nos OIDs".format(i))
        pp.add_str(element_dic_inv["bateria_index"] + "." + str(i), item.id)
        pp.add_str(element_dic_inv["string"] + "." + str(i), item.string)
        pp.add_str(element_dic_inv["bateria"] + "." + str(i), item.bateria)
        pp.add_str(element_dic_inv["tensao"] + "." + str(i), str(item.tensao/1000))
        pp.add_str(element_dic_inv["temperatura"] + "." + str(i), str(item.temperatura/10))
        pp.add_str(element_dic_inv["impedancia"] + "." + str(i), str(item.impedancia/100))
        pp.add_str(element_dic_inv["equalizacao"] + "." + str(i), str(item.equalizacao/1000))
        # Sum values to get target and tensBarr
        target += item.tensao
        i += 1
    pp.add_str(element_dic_inv["target"], str(target/(1000*n_bat*n_string)))
    pp.add_str(element_dic_inv["tensBarr"], str(target/(1000*n_string)))

def addBateriaLogToOIDs(bat_list, pp):
    # Add table lines to "bateria"
    i = 1
    for item in bat_list:
        logging.info("Adiciona bateria {} nos OIDs".format(i))
        pp.add_str(element_dic_inv["bateria_index_log"] + "." + str(i), item.id)
        pp.add_str(element_dic_inv["string_log"] + "." + str(i), item.string)
        pp.add_str(element_dic_inv["bateria_log"] + "." + str(i), item.bateria)
        pp.add_str(element_dic_inv["tensao_log"] + "." + str(i), str(item.tensao/1000))
        pp.add_str(element_dic_inv["temperatura_log"] + "." + str(i), str(item.temperatura/10))
        pp.add_str(element_dic_inv["impedancia_log"] + "." + str(i), str(item.impedancia/100))
        pp.add_str(element_dic_inv["equalizacao_log"] + "." + str(i), str(item.equalizacao/1000))
        i += 1

def addAlarmToOIDs(alarms, pp):
    # Add table lines to "bateria"
    i = 1
    for item in alarms:
        logging.info("Adiciona alarme {} nos OIDs".format(i))
        pp.add_str(element_dic_inv["alarm_index"] + "." + str(i), item.id)
        pp.add_str(element_dic_inv["descricaoAlarm"] + "." + str(i), item.descricao)
        pp.add_int(element_dic_inv["emailEnviado"] + "." + str(i), item.emailEnviado)
        pp.add_int(element_dic_inv["n_ocorrencias"] + "." + str(i), item.n_ocorrencias)
        i += 1

def main_update():
    logging.info("Main update")
    session = Session()
    logging.info("Aberta sessao com o BD")
    # Query parameters from database, one object at a time
    # These go to the "settings" object
    p = session.query(Parameters).first()
    # Post parameters related to that object
    addParametersToOIDs(p, pp)
    m = session.query(Modulo).first()
    addModultoToOIDs(m, pp)
    u = session.query(Usuario)
    addUsuarioToOIDs(u, pp)
    r = session.query(RedeSeguranca).first()
    addRedeToOIDs(r, pp)
    e = session.query(EmailServer).first()
    addEmailServerToOIDs(e, pp)
    t = session.query(TimeServer).first()
    addTimeServerToOIDs(t, pp)
    ac = session.query(AlarmeConfig).first()
    addAlarmeConfigToOIDs(ac, pp)
    ap = session.query(ApelidoString)
    addApelidoStringToOIDs(ap, pp)

    # These should go to the "alarmes" object
    # Check alarm table, and return the last 15 entries
    a = session.query(AlarmLog).order_by(AlarmLog.dataHora.desc()).limit(15)
    addAlarmToOIDs(a, pp)

    # These should go to the "bateria" object
    # "DatalogRT" e "Datalog".
    dlogRt = session.query(DataLogRT).limit(int(m.n_baterias_por_strings * m.n_strings))
    addBateriaToOIDs(dlogRt, pp, m.n_baterias_por_strings, m.n_strings)

    dlog = session.query(DataLog).limit(15)
    addBateriaLogToOIDs(dlog, pp)

    session.close()

logging.info("Registra OID")
pp = snmp.PassPersist('.1.3.6.1.4.1.39178.100.1')
# If the configuration table does not exist, create entry
cfgsession = Session()
cfg = cfgsession.query(Parameters).first()
if cfg:
    logging.info("Agente com periodicidade {}s".format(cfg.param7))
    pp.start(main_update, int(cfg.param7))
else:
    logging.info("Periodicidade (param7) inacessível, usando padrão(60s)")
    pp.start(main_update, 60)
