import json
import uuid
import pandas as pd
import multiprocessing

def readConfigInfo(configType:str, configFile:str)->list:
    csvFile = pd.read_csv(configFile, encoding='cp1252',delimiter=';')
    csvFile.dropna(inplace=True)
    return csvFile[configType].values.tolist()


def createCodeSysVarConfigs(configList)->list:

    jsonConfigList = []
    for config in configList:

        devicePathSplitted = config.split(" ")
        dataType = devicePathSplitted[-1].strip("()")
        path = devicePathSplitted[2].split(".")

        _uuid = str(uuid.uuid4())

        eachConfigInJSON = {
        "@IO.CODESYS.Variable": {
            "id": f"{path[-2]}.{path[-1]}",
            "uuid": f"{_uuid}",
            "path": f"{'.'.join(path)}",
            "dataType": f"{dataType}",
            "access": "readWrite",
            "readCommand": "PLC Handler.Read Values"
        }
        }
        jsonConfigList.append(eachConfigInJSON)

    return jsonConfigList

def createInfluxDBConfigInfo(configList:list)->list:
    jsonConfigList = {}

    for config in configList:

        linieName = config
        configNameSplitted = config.split(".")
        uniquePartOfName = configNameSplitted[3:]
        plcName = "PLC Handler." + ".".join(uniquePartOfName)

        jsonConfigList[linieName] = plcName

    return jsonConfigList

#use this for Influx DB and CodeSys by passing list
def writeJsonConfigToFile(jsonConfigList,fileName):
    with open(f"{fileName}.json", "a") as outfile:
        json_object = json.dumps(jsonConfigList, indent=4, ensure_ascii=False)
        outfile.write(json_object)

def main(configFile:str):
   # create Code SYS Variable Configuration 
    configList = readConfigInfo("PLC",configFile)
    jsonConfigList = createCodeSysVarConfigs(configList)
    writeJsonConfigToFile(jsonConfigList,"jsonConfigs/CodeSysVarConfig")

    # create Influx DB microservice configuration
    influxDBConfigList = readConfigInfo("InfluxDBVar",configFile)
    influxDBJSONConfigList = createInfluxDBConfigInfo(influxDBConfigList)
    writeJsonConfigToFile(influxDBJSONConfigList,"jsonConfigs/influxDBConfig")
    

if __name__=="__main__":
   main()