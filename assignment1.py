from asyncore import write
from tkinter import E
import xml.etree.ElementTree as ET


def main():
    tree = ET.parse('./data/Assignment1.xml');
    root = tree.getroot();
    reduntantString = root.tag.split("}")[0] + "}";

    ProcessNode= None;
    
    Places = list();
    Tasks = list();
    sequenceFlows = list();
    StartPoint = str();
    EndPoint = str();

    TaskNumber = 1
    
    def get_correctTag(node):
        return node.tag.replace(reduntantString, "")
    
    for childofRoot in root:
        ChildName = get_correctTag(childofRoot)
        if ChildName == "process":
            ProcessNode = childofRoot;
            break
        
    

    for childofProcess in ProcessNode:
        ChildName = get_correctTag(childofProcess)
        if ChildName == "userTask" or ChildName == "serviceTask":
            tmp_name = childofProcess.attrib['name']
            tmp_id = childofProcess.attrib['id']  
            for childofTask in childofProcess:
                ChildofTaskName = get_correctTag(childofTask)
                if ChildofTaskName == "incoming":
                    tmp_incoming = childofTask.text
                elif ChildofTaskName == "outgoing":
                    tmp_outgoing = childofTask.text
            newTask = TaskNode(type = ChildName, name=tmp_name, id=tmp_id, outgoing=tmp_outgoing, incoming=tmp_incoming)
            Tasks.append(newTask)
            Places.append(newTask.name)
            
                    
        elif ChildName == "sequenceFlow":
            tmp_name = childofProcess.attrib['name']
            tmp_id = childofProcess.attrib['id']
            tmp_sourceRef = childofProcess.attrib['sourceRef']
            tmp_targetRef = childofProcess.attrib['targetRef']
            
            newSequenceFlow = SequenceFlow(name=tmp_name, id=tmp_id, sourceRef=tmp_sourceRef, targetRef=tmp_targetRef)
            sequenceFlows.append(newSequenceFlow)
            Places.append(newSequenceFlow.name)
            
        elif ChildName == "endEvent":
            tmp_name = childofProcess.attrib["name"]
            tmp_id = childofProcess.attrib["id"]
            for childofEndEvent in childofProcess:
                if get_correctTag(childofEndEvent)=="incoming":
                    tmp_incoming = childofEndEvent.text
            EndPoint = TaskNode(type="endpoint", name=tmp_name, id=tmp_id, outgoing=None, incoming=tmp_incoming )
            
            Places.append(EndPoint.name)
            
            
        elif ChildName == "startEvent":
            tmp_name = childofProcess.attrib["name"]
            tmp_id = childofProcess.attrib["id"]
            for childofStartEvent in childofProcess:
                if get_correctTag(childofStartEvent)=="outgoing":
                    tmp_outgoing = childofStartEvent.text
            StartPoint = TaskNode(type="startpoint", name=tmp_name, id=tmp_id, outgoing=tmp_outgoing, incoming=None )
            Places.append(StartPoint.name)
            
    Tasks = [StartPoint] + Tasks    
    Tasks = Tasks + [EndPoint]

    print(Places)
    for task in Tasks:
        print(task.name)
    # print("Example Task : ")
    # print(props(Tasks[0]))
    # print("type :", Tasks[0].type)
    # print("name :", Tasks[0].name)
    # print("id :", Tasks[0].id)
    # print("outgoing :", Tasks[0].outgoing)
    # print("incoming :", Tasks[0].incoming)
    # print("--"*50)

    # print("Example sequenceflow : ")
    # print(props(sequenceFlows[0]))
    # print("name : ",sequenceFlows[0].name)
    # print("id : ",sequenceFlows[0].id)
    # print("sourceRef : ", sequenceFlows[0].sourceRef)
    # print("targetRef : ", sequenceFlows[0].targetRef)
    # print("--"*50)

    # print("StartPoing : ")
    # print(props(StartPoint))
    # print("name : ",StartPoint.name)
    # print("id : ",StartPoint.id)
    # print("--"*50)

    # print("EndPoint : ")
    # print(props(EndPoint))
    # print("name : ", EndPoint.name)
    # print("id : ", EndPoint.id)
    # print(Places)
    path = "./output/output.tpn"
    with open(path, 'w') as tpnfile:
        for eachTask in Tasks:
            outgoing = eachTask.outgoing
            incoming = eachTask.incoming
            for eachSequenceFlow in sequenceFlows:
                if eachSequenceFlow.id == outgoing:
                    tpnfile.write(eachSequenceFlow.name+"\n")
                if eachSequenceFlow.id == incoming:
                    tpnfile.write(eachSequenceFlow.name+"\n")
                    
    tpnfile.close()
    




def props(cls):   
  return [i for i in cls.__dict__.keys() if i[:1] != '_']

class TaskNode:
    """_summary_
        Define instance of serviceTask/userTask
        Only keeps the infomation we need.
    """
    def __init__(self, type="",name="", id="", outgoing="", incoming=""):
        self.type = type
        self.name = name
        self.id = id
        self.outgoing = outgoing
        self.incoming = incoming

class SequenceFlow:
    """_summary_
        Define instance of sequenceflow.
        Only keeps the infomation we need.
    """
    StatusNumber = 1
    
    def __init__(self, name="", id="", sourceRef="", targetRef=""):
        self.name = self.getName(name)
        self.id = id
        self.sourceRef = sourceRef
        self.targetRef = targetRef
    def getName(self,name):
        """_summary_
            Generates a new name if it is empty.
        Args:
            name (string): name parsed from the xml file.
        Returns:
            (string): newName
        """
        if name == "":
            newName = "Status_{}".format(SequenceFlow.StatusNumber)
            SequenceFlow.StatusNumber +=1
            return newName
        else:
            return name

class AnchorPoint:
    """
    Starting Point Or End Point
    """
    def __init__(self,name,id):
        self.name = name
        self.id = id
        



if __name__ == "__main__":
    main()