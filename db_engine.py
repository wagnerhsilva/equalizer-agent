from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

# engine = create_engine('sqlite:////home/prjs/cm_comandos_lineares/equalizer-agent/equalizerdb', echo=False)
engine = create_engine('sqlite:////var/www/equalizer-api/equalizer-api/equalizerdb', echo=False)

Base = declarative_base()

# Database classes, reflect the schema in wiki
class Usuario(Base):
    __tablename__ = "Usuario"

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    sobreNome = Column(String)
    telefone = Column(String)
    email = Column(String)
    senha = Column(String)
    acesso = Column(String)


class Modulo(Base):
    __tablename__ = 'Modulo'

    id = Column(Integer, primary_key=True)
    descricao = Column(String)
    # There is a problem with the base, this value is a String, but the column is defined as Real
    tensao_nominal = Column(Float)
    capacidade_nominal = Column(Integer)
    n_strings = Column(Integer)
    n_baterias_por_strings = Column(Integer)
    contato = Column(String)
    localizacao = Column(String)
    fabricante = Column(String)
    tipo = Column(String)
    data_instalacao = Column(String)

    conf_alarme_id = Column(Integer, ForeignKey('AlarmeConfig.id'))
    alarme_config = relationship("AlarmeConfig")

class AlarmeConfig(Base):
    __tablename__ = "AlarmeConfig"

    id = Column(Integer, primary_key=True)
    tipo_modulo = Column(String)
    nivel_alert_tensao_max = Column(Float)
    nivel_alert_tensao_min = Column(Float)
    nivel_alert_temp_max = Column(Float)
    nivel_alert_temp_min = Column(Float)
    nivel_alert_impedancia_max = Column(Float)
    nivel_alert_impedancia_min = Column(Float)
    nivel_max_tensao_ativo = Column(Integer)
    nivel_max_tensao_val = Column(Float)
    alarme_nivel_tensao_max = Column(Float)
    alarme_nivel_tensao_min = Column(Float)
    alarme_nivel_temp_max = Column(Float)
    alarme_nivel_temp_min = Column(Float)
    alarme_nivel_imped_max = Column(Float)
    alarme_nivel_imped_min = Column(Float)
    alarme_nivel_tensaoBarr_min = Column(Float)
    alarme_nivel_tensaoBarr_max = Column(Float)
    alarme_nivel_target_min = Column(Float)
    alarme_nivel_target_max = Column(Float)

class RedeSeguranca(Base):
    __tablename__ = "RedeSeguranca"

    id = Column(Integer, primary_key=True)
    mac = Column(String)
    velocidadePlacaRede = Column(String)
    localAddress = Column(String)
    gateway = Column(String)
    mascara = Column(String)
    servidorDNS = Column(String)
    nomeDoSistema = Column(String)
    localDoSistema = Column(String)
    contatoDoSistema = Column(String)
    httpPort = Column(Integer)
    useHttps = Column(Integer)
    httpsPort = Column(Integer)
    httpTempoDeAtualizacao = Column(Integer)
    paginaPadraoHttp = Column(String)

class DataLogRT(Base):
    __tablename__ = "DataLogRT"

    id = Column(Integer, primary_key=True)
    dataHora = Column(String)
    string = Column(String)
    bateria = Column(String)
    temperatura = Column(Float)
    impedancia = Column(Float)
    tensao = Column(Float)
    equalizacao = Column(Float)

class DataLog(Base):
    __tablename__ = "DataLog"

    id = Column(Integer, primary_key=True)
    dataHora = Column(String)
    string = Column(String)
    bateria = Column(String)
    temperatura = Column(Float)
    impedancia = Column(Float)
    tensao = Column(Float)
    equalizacao = Column(Float)

class TimeServer(Base):
    __tablename__ = "TimeServer"

    id = Column(Integer, primary_key=True)
    timeServerAddress1 = Column(String)
    timeServerAddress1_complemento = Column(String)
    timeServerAddress2 = Column(String)
    timeServerAddress2_complemento = Column(String)
    timeServerAddress3 = Column(String)
    timeServerAddress3_complemento = Column(String)
    connectionRetries = Column(Integer)
    timeZone = Column(String)
    automAdjustTimeDaylightSavingChanges = Column(Integer)

class EmailServer(Base):
    __tablename__ = "EmailServer"

    id = Column(Integer, primary_key=True)
    server = Column(String)
    portaSMTP = Column(Integer)
    usarCriptografiaTLS = Column(Integer)
    email = Column(String)
    assunto = Column(String)
    usarAutenticacao = Column(Integer)
    login = Column(String)
    senha = Column(String)

class AlarmLog(Base):
    __tablename__ = "AlarmLog"

    id = Column(Integer, primary_key=True)
    dataHora = Column(String)
    descricao = Column(String)
    emailEnviado = Column(Integer)
    n_ocorrencias = Column(Integer)

class Parameters(Base):
    __tablename__ = "Parameters"

    id = Column(Integer, primary_key=True)
    avg_last = Column(String)
    duty_min = Column(String)
    duty_max = Column(String)
    cte_index = Column(String)
    delay = Column(String)
    num_cycles_var_read = Column(String)
    bus_voltage = Column(String)
    save_log_time = Column(String)
    disk_capacity = Column(String)
    param1 = Column(String)
    param2 = Column(String)
    param3 = Column(String)
    param4 = Column(String)
    param5 = Column(String)
    param6 = Column(String)
    param7 = Column(String)
    param8 = Column(String)
    param9 = Column(String)
    param10 = Column(String)

class ApelidoString(Base):
    __tablename__ = "ApelidoString"

    string = Column(String, primary_key=True)
    apelido = Column(String)
