import os
import configparser
import time
import nipyapi
import asyncio

config_ini = configparser.ConfigParser()
config_ini.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),"config.ini"), encoding='utf-8')

def stopAllProcessors(root_pg_id):
    # get all processors
    all_proc = nipyapi.canvas.list_all_processors(root_pg_id)

    # stop all_processors
    for proc in all_proc:
        nipyapi.canvas.schedule_processor(proc, False)

    return True

async def asyncStopAllProcessors(root_pg_id):
    while True:
        try :
            ret = stopAllProcessors(root_pg_id)
            if(ret==True): break
            await asyncio.sleep(2)
        except:
            pass

def deleteAllProcessors(root_pg_id):
    # get all processors
    all_proc = nipyapi.canvas.list_all_processors(root_pg_id)

    # delete all_processors
    for processor in all_proc:
        nipyapi.canvas.delete_processor(processor)

    return True

async def asyncDeleteAllProcessors(root_pg_id):
    while True:
        try :
            ret = deleteAllProcessors(root_pg_id)
            if(ret==True): break
            await asyncio.sleep(2)
        except:
            pass

def deleteAllProcessGroup(root_pg_id):
    # get all process groups
    all_pg = nipyapi.canvas.list_all_process_groups(root_pg_id)

    # delete all_processors
    for pg in all_pg:
        if(pg.id==root_pg_id):continue
        nipyapi.canvas.delete_process_group(pg)
    return True

async def asyncDeleteAllProcessGroup(root_pg_id):
    while True:
        try :
            ret = deleteAllProcessGroup(root_pg_id)
            if(ret==True): break
            await asyncio.sleep(2)
        except:
            pass

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

    stopAllProcessors(root_pg_id),
    myTasks = {
        asyncStopAllProcessors(root_pg_id),
        asyncDeleteAllProcessors(root_pg_id),
        asyncDeleteAllProcessGroup(root_pg_id)
    }
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(asyncio.gather(*myTasks))


if __name__=='__main__':
    main()
