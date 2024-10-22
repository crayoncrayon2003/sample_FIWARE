import os
import configparser
import json
import nipyapi
import dataclasses

config_ini = configparser.ConfigParser()
config_ini.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),"config.ini"), encoding='utf-8')

#ORION1 = 'http://{}:8081'.format(config_ini['DEFAULT']['HOST_IP'])
ORION1 = 'http://{}:1026'.format(config_ini['DEFAULT']['HOST_IP'])

SERVICE = 'service1'            # multi-tenant name
SERVICEPATH = '/servicepath1'   # data storage path

URN  = "urn:ngsi-ld:Sensor:001" # data identifier
TYPE = "Sensor"                 # data type


@dataclasses.dataclass
class ProcessorInfo:
    processor_type : str
    location       : set
    name           : str
    config         : dict
    period         : str
    properties     : dict

# CREATE ENTITIES INFO
CREATE_ENTITIES_BODY = {
    "id"         : URN,
    "type"       : TYPE,
    "name"       : {"type": "Text",    "value": "SensorName",                   "metadata": {}},
    "temperature": {"type": "Integer", "value": "${random():mod(100):plus(1)}", "metadata": {}},
    "humidity"   : {"type": "Integer", "value": "${random():mod(100):plus(1)}", "metadata": {}}
}
CREATE_ENTITIES_GENERATEFLOWFFILE = {}
CREATE_ENTITIES_UPDATEATTRIBUTE   = {
    'messagebody' : json.dumps(CREATE_ENTITIES_BODY)
}
CREATE_ENTITIES_REPLACETEXT = {
    'Replacement Value': '${messagebody}',
    'Evaluation Mode' : 'Entire text'
}
CREATE_ENTITIES_INVOKE_HTTP = {
    'Remote URL'        : ORION1+"/v2/entities/",
    'HTTP Method'       : 'POST',
    'Content-Type'      : 'application/json',
    'Fiware-Service'    : SERVICE,
    'Fiware-ServicePath': SERVICEPATH,
}
CREATE_ENTITIES_PROCESSOR_INFOS = [
    ProcessorInfo("org.apache.nifi.processors.standard.GenerateFlowFile" ,(200,200),"GenerateFlowFile",{"autoTerminatedRelationships":["success"]},                                          '5s',CREATE_ENTITIES_GENERATEFLOWFFILE),
    ProcessorInfo("org.apache.nifi.processors.attributes.UpdateAttribute",(200,400),"UpdateAttribute" ,{"autoTerminatedRelationships":["success"]},                                          '0s',CREATE_ENTITIES_UPDATEATTRIBUTE),
    ProcessorInfo("org.apache.nifi.processors.standard.ReplaceText",      (200,600),"ReplaceText"     ,{"autoTerminatedRelationships":["failure","success"]},                                '0s',CREATE_ENTITIES_REPLACETEXT),
    ProcessorInfo("org.apache.nifi.processors.standard.InvokeHTTP",       (200,800),"InvokeHTTP"      ,{"autoTerminatedRelationships":["Failure","No Retry","Original","Response","Retry"]}, '0s',CREATE_ENTITIES_INVOKE_HTTP),
]

# UPDATE ENTITIES INFO
UPDATE_ENTITIES_BODY = {
    "temperature": {"type": "Integer", "value": "${random():mod(100):plus(1)}", "metadata": {}},
    "humidity"   : {"type": "Integer", "value": "${random():mod(100):plus(1)}", "metadata": {}}
}
UPDATE_ENTITIES_GENERATEFLOWFFILE = {}
UPDATE_ENTITIES_UPDATEATTRIBUTE   = {
    'messagebody' : json.dumps(UPDATE_ENTITIES_BODY)
}
UPDATE_ENTITIES_REPLACETEXT = {
    'Replacement Value': '${messagebody}',
    'Evaluation Mode' : 'Entire text'
}
UPDATE_ENTITIES_INVOKE_HTTP = {
    'Remote URL'        : ORION1+"/v2/entities/"+URN+"/attrs/",
    'HTTP Method'       : 'PATCH',
    'Content-Type'      : 'application/json',
    'Fiware-Service'    : SERVICE,
    'Fiware-ServicePath': SERVICEPATH,
}
UPDATE_ENTITIES_PROCESSOR_INFOS=[
    ProcessorInfo("org.apache.nifi.processors.standard.GenerateFlowFile" ,(600,200),"GenerateFlowFile",{"autoTerminatedRelationships":["success"]},                                          '5s',UPDATE_ENTITIES_GENERATEFLOWFFILE),
    ProcessorInfo("org.apache.nifi.processors.attributes.UpdateAttribute",(600,400),"UpdateAttribute" ,{"autoTerminatedRelationships":["success"]},                                          '0s',UPDATE_ENTITIES_UPDATEATTRIBUTE),
    ProcessorInfo("org.apache.nifi.processors.standard.ReplaceText",      (600,600),"ReplaceText"     ,{"autoTerminatedRelationships":["failure","success"]},                                '0s',UPDATE_ENTITIES_REPLACETEXT),
    ProcessorInfo("org.apache.nifi.processors.standard.InvokeHTTP",       (600,800),"InvokeHTTP"      ,{"autoTerminatedRelationships":["Failure","No Retry","Original","Response","Retry"]}, '0s',UPDATE_ENTITIES_INVOKE_HTTP),
]

def createProcessor(pg, info:ProcessorInfo):
    # get processor type
    proc_type = nipyapi.canvas.get_processor_type(info.processor_type)
    if proc_type is None:
        raise ValueError("error : get_processor_type")

    if type(proc_type) == list:
        for tmp in proc_type:
            if(tmp.type == info.processor_type):
                proc_type=tmp
                break

    # create processor
    proc = nipyapi.canvas.create_processor(
        parent_pg= pg,
        processor= proc_type,
        location = info.location,
        name     = info.name,
        config   = info.config,
    )

    # setting processor
    nipyapi.canvas.update_processor(
        processor=proc,
        update=nipyapi.nifi.ProcessorConfigDTO(
            scheduling_period =info.period,
            properties        =info.properties,
        )
    )

    # return processor
    return proc


def createflow(pg, ProcessorInfos):
    procs=[]
    # create Processor
    for info in ProcessorInfos:
        proc = createProcessor(pg, info)
        procs.append(proc)

    # connection Processor
    for idx, (source, target) in enumerate(zip(procs[:-1], procs[1:])):
        nipyapi.canvas.create_connection(
            source=source,
            target=target,
            relationships = ['success'] if idx!=(len(procs)-2) else ['success','failure']
        )

    return procs

def scheduleflow(procs,bool=True):
    for proc in procs:
        nipyapi.canvas.schedule_processor(proc, bool)

def scheduleflowOnece(procs):
    scheduleflow(procs,True)

    scheduleflow(procs,False)

def main():
    # setting nifi endpoint
    nipyapi.config.nifi_config.host = "http://localhost:8080/nifi-api"
    nipyapi.config.registry_config.host = "http://localhost:18080/nifi-registry-api"

    # setting nifi authentication
    username = "admin"
    password = "admin"
    nipyapi.config.nifi_config.auth = (username, password)

    # get Root Process Group ID
    root_pg_id = nipyapi.canvas.get_root_pg_id()

    # get Root Process Group
    root_pg    = nipyapi.canvas.get_process_group(root_pg_id, 'id')

    # create New Process Group
    test_pg     = nipyapi.canvas.create_process_group(root_pg, 'test_process_group', (200, 200), 'this is a test')

    # create flow
    procs_create_entities = createflow(test_pg, CREATE_ENTITIES_PROCESSOR_INFOS)
    procs_update_entities = createflow(test_pg, UPDATE_ENTITIES_PROCESSOR_INFOS)

    # run flow
    scheduleflowOnece(procs_create_entities)
    scheduleflow(procs_update_entities)

if __name__=='__main__':
    main()
