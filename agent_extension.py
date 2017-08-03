#!/usr/bin/python -u
import snmp_passpersist as snmp

element_list = {"0": "batStatus",
                "1": "nBatBank"}
value_list = {"batStatus": 1,
              "nBatBank": 2}

def main_update():
    for element in element_list:
        pp.add_cnt_64bit(element, value_list[element_list[element]])

pp = snmp.PassPersist('.1.3.6.1.4.1.39178.100.1.1.1.2')
pp.start(main_update, 10)
