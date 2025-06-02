import sys
import json
import os
from lib import common

# Cli Arguments to dict
a = common.parseArgs(sys.argv)
here = os.path.realpath(__file__).replace("main.py", "")
ioRawData = common.bash("{}usb-info.sh".format(here))
ioJSONData = json.loads(ioRawData)
deviceListLocation = "{}devices.json".format(here)
oldDeviceList = json.loads(common.fileToString(deviceListLocation))
newDeviceList = {}
for device in ioJSONData["IORegistryEntryChildren"]:
    parentDevice = ioJSONData["IORegistryEntryName"]
    if "IORegistryEntryChildren" in device.keys():
        for child in device["IORegistryEntryChildren"]:
            parentDevice = device["IORegistryEntryName"]
            newDevice = {}
            newDevice["parentDevice"] = parentDevice
            newDevice["class"] = child["IOObjectClass"]
            newDevice["name"] = child["IORegistryEntryName"]
            newDeviceList[child["IORegistryEntryName"]] = newDevice
            if a["v"]:
                print("{} connected to {}".format(child["IORegistryEntryName"], parentDevice))
            if "IORegistryEntryChildren" in child.keys():
                for grandchild in child["IORegistryEntryChildren"]:
                    parentDevice = child["IORegistryEntryName"]
                    newDevice = {}
                    newDevice["parentDevice"] = parentDevice
                    newDevice["class"] = grandchild["IOObjectClass"]
                    newDevice["name"] = grandchild["IORegistryEntryName"]
                    newDeviceList[grandchild["IORegistryEntryName"]] = newDevice
                    if a["v"]:
                        print("{} connected to {}".format(grandchild["IORegistryEntryName"], parentDevice))
                    if "IORegistryEntryChildren" in grandchild.keys():
                        for greatgrandchild in grandchild["IORegistryEntryChildren"]:
                            parentDevice = grandchild["IORegistryEntryName"]
                            newDevice = {}
                            newDevice["parentDevice"] = parentDevice
                            newDevice["class"] = greatgrandchild["IOObjectClass"]
                            newDevice["name"] = greatgrandchild["IORegistryEntryName"]
                            newDeviceList[greatgrandchild["IORegistryEntryName"]] = newDevice
                            if a["v"]:
                                print("{} connected to {}".format(greatgrandchild["IORegistryEntryName"], parentDevice))
                            if "IORegistryEntryChildren" in greatgrandchild.keys():
                                for greatgreatgrandchild in greatgrandchild["IORegistryEntryChildren"]:
                                    parentDevice = greatgrandchild["IORegistryEntryName"]
                                    newDevice = {}
                                    newDevice["parentDevice"] = parentDevice
                                    newDevice["class"] = greatgreatgrandchild["IOObjectClass"]
                                    newDevice["name"] = greatgreatgrandchild["IORegistryEntryName"]
                                    newDeviceList[greatgreatgrandchild["IORegistryEntryName"]] = newDevice
                                    if "IORegistryEntryChildren" in greatgreatgrandchild.keys():
                                        print("{} has other devices".format(greatgreatgrandchild["IORegistryEntryName"]))
                                
nothingNew = True
for deviceKey in newDeviceList.keys():
    if deviceKey not in oldDeviceList.keys():
        nothingNew = False
        device = newDeviceList[deviceKey]
        title = "New USB Device Connected"
        message = "{} connected via {}".format(device["name"], device["parentDevice"])
        print("New device: {}".format(message))
        common.desktopNotify(title, message)
common.stringToFile(deviceListLocation, json.dumps(newDeviceList))
if nothingNew:
    print("No new USB devices found")