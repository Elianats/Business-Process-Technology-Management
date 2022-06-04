
import xml.etree.ElementTree as ET
import os
os.chdir('/Users/elianatschang/Desktop/Business-Process-Technology-Management');

def main():
    datapath = './Assignment1-9.bpmn'
    tree = ET.parse(datapath);
    root = tree.getroot();
    reduntantString = root.tag.split("}")[0] + "}";

    ProcessNode= None;
    
    Places = list();
    Tasks = list();
    sequenceFlows = list();
    StartPoint = None;
    EndPoint = None;
    
    def get_correctTag(node):
        return node.tag.replace(reduntantString, "")
    
    for childofRoot in root:
        ChildName = get_correctTag(childofRoot)
        if ChildName == "process":
            ProcessNode = childofRoot;
            break
        
    
    TaskType = ["userTask","serviceTask","exclusiveGateway","parallelGateway"]
    for childofProcess in ProcessNode:
        ChildName = get_correctTag(childofProcess)
        if ChildName in TaskType:
            newTask = TaskNode(name=childofProcess.attrib['name'], id=childofProcess.attrib['id'], type = ChildName, outgoing=[], incoming=[] )
            for childofTask in childofProcess:
                ChildofTaskName = get_correctTag(childofTask)
                if ChildofTaskName == "incoming":
                    newTask.incoming.append(childofTask.text)
                elif ChildofTaskName == "outgoing":
                    newTask.outgoing.append(childofTask.text)
            Tasks.append(newTask)
        
                    
        elif ChildName == "sequenceFlow":
            tmp_name = childofProcess.attrib['name']
            tmp_id = childofProcess.attrib['id']
            tmp_sourceRef = childofProcess.attrib['sourceRef']
            tmp_targetRef = childofProcess.attrib['targetRef']
            
            newSequenceFlow = SequenceFlow(name=tmp_name, id=tmp_id, sourceRef=tmp_sourceRef, targetRef=tmp_targetRef)
            sequenceFlows.append(newSequenceFlow)
            Places.append(newSequenceFlow.name)
            
        elif ChildName == "endEvent":
            EndPoint = TaskNode(type="endpoint", name = childofProcess.attrib["name"], id=childofProcess.attrib["id"],outgoing=[], incoming=[])
            for childofEndEvent in childofProcess:
                if get_correctTag(childofEndEvent)=="incoming":
                    EndPoint.incoming.append(childofEndEvent.text)
            
            Tasks.append(EndPoint)
            Places.append(EndPoint.name)
            
            
        elif ChildName == "startEvent":
            StartPoint = TaskNode(type="startpoint", name=childofProcess.attrib["name"], id=childofProcess.attrib["id"],outgoing=[],incoming=[])
            for childofStartEvent in childofProcess:
                if get_correctTag(childofStartEvent)=="outgoing":
                    childofStartEvent.text
                    
                    StartPoint.outgoing.append(childofStartEvent.text)
            
            Tasks.append(StartPoint)
            Places.append(StartPoint.name)
            

    transDict = {}
    TraverseSet = set()
    
    path = "./output/output.tpn"
    with open(path, 'w') as tpnfile:

        Pending = [StartPoint]
        flag = 0
        while 1:
            if flag == 1:
                break
            for eachPending in Pending:
                if eachPending == EndPoint:
                    flag = 1
                    break

                if isinstance(eachPending,SequenceFlow):
                    for Task in Tasks:
                        if eachPending.outgoing == Task.id :
                            if Task.name not in transDict:
                                transDict[Task.name] = {
                                "in":set(),
                                "out":set()
                            }
                            transDict[Task.name]["in"].add(eachPending.name)
                    
                            if (Task) not in TraverseSet:
                                Pending.append(Task)
                        
                else:
                    #trans
                    if eachPending.name not in transDict:
                        transDict[eachPending.name] = {
                            "in":set(),
                            "out":set()
                        }

                    for eachOutgoing in eachPending.outgoing:
                        for eachSequenceFlow in sequenceFlows: #比對每個status
                            if eachOutgoing == eachSequenceFlow.id:
                                transDict[eachPending.name]["out"].add(eachSequenceFlow.name)
                                if eachSequenceFlow not in TraverseSet:
                                    Pending.append(eachSequenceFlow)
                    TraverseSet.add(eachPending)
        
        deletePending = []
        for eachSequenceFlow in sequenceFlows:            
            if StartPoint.outgoing[0] == eachSequenceFlow.id:
                deletePending.append(eachSequenceFlow.name)
                for eachTask in Tasks:
                    if eachSequenceFlow.outgoing == eachTask.id:
                        transDict[eachTask.name]["in"] = set()
                        transDict[eachTask.name]["in"].add(StartPoint.name)
                        
        for eachSequenceFlow in sequenceFlows:            
            if EndPoint.incoming[0] == eachSequenceFlow.id:
                deletePending.append(eachSequenceFlow.name)
                for eachTask in Tasks:
                    if eachSequenceFlow.incoming == eachTask.id:
                        transDict[eachTask.name]["out"] = set()
                        transDict[eachTask.name]["out"].add(EndPoint.name)
        
        
        
        for eachPlace in Places:
            if eachPlace in deletePending:
                continue
            if eachPlace == StartPoint.name:
                tpnfile.write("place "+eachPlace+" init 1;\n")
            else:
                tpnfile.write("place "+eachPlace+";\n")
        
        tpnfile.write("\n\n")
                    
        for k,v in transDict.items():
            if k == StartPoint.name or k == EndPoint.name:
                continue
            tpnfile.write("trans {}\n".format(k))
            for key, values in v.items():
                if key == "in":
                    tpnfile.write('  in  ')
                    for index, value in enumerate(values):
                        if len(values) == 1:
                            tpnfile.write(value)
                        else:
                            if index == len(values)-1:
                                tpnfile.write(value)
                            else:
                                tpnfile.write("{}, ".format(value))
            
                    
                    
                else:
                    tpnfile.write("  out ")
                    for index, value in enumerate(values):
                        if len(values) == 1:
                            tpnfile.write(value+";")
                        else:
                            if index == len(values)-1:
                                tpnfile.write(value+";")
                            else:
                                tpnfile.write("{}, ".format(value))
                    tpnfile.write("\n")
                
                tpnfile.write("\n")
    
    for k,v in transDict.items():
        print("{}:".format(k))
        print(v)
        
    for eachTask in Tasks:
        if eachTask.name == "T_4":
            print(eachTask.id)
                
    tpnfile.close()
    




def props(cls):   
  return [i for i in cls.__dict__.keys() if i[:1] != '_']

class TaskNode:
    """_summary_
        Define instance of serviceTask/userTask
        Only keeps the infomation we need.
    """
    T = 1
    def __init__(self, type="",name="", id="", outgoing=[], incoming=[]):
        self.type = type
        self.name = self.getName(name)
        self.id = id
        self.outgoing = outgoing
        self.incoming = incoming
    def getName(self,name):
        if name == "":
            newName = "T_{}".format(TaskNode.T)
            TaskNode.T +=1
            return newName
        else:
            return name

class SequenceFlow:
    """_summary_
        Define instance of sequenceflow.
        Only keeps the infomation we need.
    """
    StatusNumber = 1
    
    def __init__(self, name="", id="", sourceRef="", targetRef=""):
        self.name = self.getName(name)
        self.id = id
        self.incoming = sourceRef
        self.outgoing = targetRef
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

        



if __name__ == "__main__":
    main()
    
    