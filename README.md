# Equalizer SNMP Agent Extension

## Introdução

O agente do net-snmp pode ser estendido para responder a OIDs específicos de um fabricante e utilizamos tal mecanismo para prover os OIDs da MIB CM_COMANDOS.
A extensão do agente é feita por um script em Python, que é executado periodicamente pelo próprio net-snmp e coleta os dados da base de dados do Equalizer.

## Configuração do Net-SNMP

A imagem do Equalizer já está configurada pra conter as alterações relacionadas à chamada do script, mas para referência a parte principal é a seguinte:

`pass_persist <OID base> /usr/bin/python -u /home/root/agent_extension.py`

Esta linha deve ser adicionada ao arquivo "snmpd.conf" e o script estará no caminho "/home/root"

## Módulo snmp_passpersist

Este projeto utiliza como base de funcionalidade o módulo python "snmp_passpersist" na versão 1.3.0, que pode ser baixado neste [link](https://github.com/nagius/snmp_passpersist.git)
