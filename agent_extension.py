#!/usr/bin/python -u
from sqlalchemy.orm import sessionmaker
from db_engine import engine, Usuario, Modulo, AlarmeConfig, RedeSeguranca, DataLog
from db_engine import TimeServer, EmailServer, AlarmLog, Parameters
import json
import sys
import logging

import snmp_passpersist as snmp

# logging.basicConfig(filename='/home/prjs/cm_comandos_lineares/equalizer-agent/log.log',level=logging.DEBUG,
logging.basicConfig(filename='/home/root/equalizer-agent/log.log',level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')
logging.info("Iniciando agente extra")

# Create DB sessionmaker, every request will have open and close a new session
Session = sessionmaker(bind=engine)

# Load json
# with open("/home/prjs/cm_comandos_lineares/equalizer-agent/element_mib.json", "r") as fd:
with open("/home/root/equalizer-agent/element_mib.json", "r") as fd:
    element_dic = json.loads(fd.read())
    # Set up inverted lookup
    element_dic_inv = {}
    for e in element_dic:
        element_dic_inv[element_dic[e]] = e

logging.info("Carregado arquivo de elmentos/OID")

def addParametersToOIDs(parameter, pp):
    logging.info("Adiciona parameter nos OIDs")
    pp.add_str(element_dic_inv["avg_max"], parameter.avg_last)
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
    pp.add_str(element_dic_inv["nome"], user.nome)
    pp.add_str(element_dic_inv["sobreNome"], user.sobreNome)
    pp.add_str(element_dic_inv["telefone"], user.telefone)
    pp.add_str(element_dic_inv["email"], user.email)
    pp.add_str(element_dic_inv["senha"], user.senha)
    pp.add_str(element_dic_inv["acesso"], user.acesso)

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

def main_update():
    logging.info("Main update")
    session = Session()
    logging.info("Aberta sessao com o BD")
    # Query parameters from database, one object at a time
    p = session.query(Parameters).first()
    # Post parameters related to that object
    addParametersToOIDs(p, pp)

    m = session.query(Modulo).first()
    addModultoToOIDs(m, pp)

    u = session.query(Usuario).first()
    addUsuarioToOIDs(u, pp)

    r = session.query(RedeSeguranca).first()
    addRedeToOIDs(r, pp)
    session.close()

logging.info("Registra OID")
pp = snmp.PassPersist('.1.3.6.1.4.1.39178.100.1.1.1.2')
pp.start(main_update, 10)
