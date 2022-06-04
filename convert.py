#type in #python3 convert.py --input ./Assignment_new.bpmn --output ./output.tpn #to convert
import xml.etree.ElementTree as ET


def main(input:str, output:str):
    datapath = input
    outputpath = output
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
        
    #init all Nodes
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
            
            newSequenceFlow = SequenceFlow(name=tmp_name, id=tmp_id , sourceRef=[],targetRef=[])
            newSequenceFlow.incoming.append(tmp_sourceRef)
            newSequenceFlow.outgoing.append(tmp_targetRef)
            sequenceFlows.append(newSequenceFlow)
            
        elif ChildName == "endEvent":
            EndPoint = TaskNode(type="endpoint", name = childofProcess.attrib["name"], id=childofProcess.attrib["id"],outgoing=[], incoming=[])
            for childofEndEvent in childofProcess:
                if get_correctTag(childofEndEvent)=="incoming":
                    EndPoint.incoming.append(childofEndEvent.text)
            
            Tasks.append(EndPoint)
            
            
        elif ChildName == "startEvent":
            StartPoint = TaskNode(type="startpoint", name=childofProcess.attrib["name"], id=childofProcess.attrib["id"],outgoing=[],incoming=[])
            for childofStartEvent in childofProcess:
                if get_correctTag(childofStartEvent)=="outgoing":
                    
                    StartPoint.outgoing.append(childofStartEvent.text)
            
            Tasks.append(StartPoint)
            
    for Task in Tasks:
        for index, inComeing in enumerate(Task.incoming):
            for seq in sequenceFlows:
                if seq.id == inComeing:
                    Task.incoming[index] = seq
        for index, outGoing in enumerate(Task.outgoing):
            for seq in sequenceFlows:
                if seq.id == outGoing:
                    Task.outgoing[index] = seq
    for seq in sequenceFlows:
        for Task in Tasks:
            if seq.incoming[0] == Task.id:
                seq.incoming[0]=Task
            if seq.outgoing[0] == Task.id:
                seq.outgoing[0]= Task
    delList = list()        
    for seq in sequenceFlows:
        if seq.outgoing[0].type == "exclusiveGateway" or seq.outgoing[0].type == "parallelGateway":
            gateway = seq.outgoing[0]
            parentNode = seq.incoming[0]
            for index,outgoing in enumerate(parentNode.outgoing):
                if outgoing == seq:
                    parentNode.outgoing[index] = gateway
                    gateway.incoming.remove(seq)
                    gateway.incoming.append(parentNode)
            delList.append(seq)
                    
        if seq.incoming[0].type == "exclusiveGateway" or seq.incoming[0].type == "parallelGateway":
            parentNode = seq.outgoing[0]
            gateway = seq.incoming[0]
                
            for index,outgoing in enumerate(gateway.outgoing):
                if outgoing == seq:
                    gateway.outgoing[index] = parentNode
                    parentNode.incoming.remove(seq)
                    parentNode.incoming.append(gateway)
            delList.append(seq)
    
    for each in delList:
        sequenceFlows.remove(each)
    newTask = list()
    for task in Tasks:
        if task.type != "exclusiveGateway" and task.type != "parallelGateway":
            newTask.append(task)
        else:
            sequenceFlows.append(task)
    Places = list()
    Places.append(StartPoint.name)
    Places.append(EndPoint.name)
    for each in sequenceFlows:
        Places.append(each.name)
            
    Tasks = newTask
    
    transDict = {}
    TraverseSet = set()
    
    
    with open(outputpath, 'w') as tpnfile:
        Pending = [StartPoint]
        flag = 0
        while 1:
            if flag == 1:
                break
            for eachPending in Pending:
                if eachPending == EndPoint:
                    flag = 1
                    break

                if isinstance(eachPending,SequenceFlow) or eachPending.type == "exclusiveGateway" or eachPending.type == "parallelGateway":
                    for Task in Tasks:
                        if Task in eachPending.outgoing :
                            if Task.name not in transDict:
                                transDict[Task.name] = {
                                "in":set(),
                                "out":set()
                            }
                            transDict[Task.name]["in"].add(eachPending.name)
                    
                            if Task not in TraverseSet:
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
                            if eachOutgoing == eachSequenceFlow:
                                transDict[eachPending.name]["out"].add(eachSequenceFlow.name)
                                if eachSequenceFlow not in TraverseSet:
                                    Pending.append(eachSequenceFlow)
                    TraverseSet.add(eachPending)
        
        deletePending = []
        for eachSequenceFlow in sequenceFlows:            
            if StartPoint.outgoing[0].id == eachSequenceFlow.id:
                deletePending.append(eachSequenceFlow.name)
                for eachTask in Tasks:
                    if eachSequenceFlow.outgoing == eachTask.id:
                        transDict[eachTask.name]["in"] = set()
                        transDict[eachTask.name]["in"].add(StartPoint.name)
                        
        for eachSequenceFlow in sequenceFlows:            
            if EndPoint.incoming[0].id == eachSequenceFlow.id:
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
                        if value == deletePending[0]:
                            value = StartPoint.name
                        if value == deletePending[1]:
                            value == EndPoint.name
                        if len(values) == 1:
                            tpnfile.write(value)
                        else:
                            if index == len(values)-1:
                                tpnfile.write(value)
                            else:
                                tpnfile.write("{}, ".format(value))
            
                    
                    
                else:
                    tpnfile.write("  out  ")
                    for index, value in enumerate(values):
                        if value in deletePending:
                            value = EndPoint.name
                        if len(values) == 1:
                            tpnfile.write(value+";")
                        else:
                            if index == len(values)-1:
                                tpnfile.write(value+";")
                            else:
                                tpnfile.write("{}, ".format(value))
                    tpnfile.write("\n")
                
                tpnfile.write("\n")
    
    # for k,v in transDict.items():
    #     print("{}:".format(k))
    #     print(v)

                
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
        
    def __repr__(self):
        return "class TN "+ self.name

class SequenceFlow:
    """_summary_
        Define instance of sequenceflow.
        Only keeps the infomation we need.
    """
    StatusNumber = 1
    
    def __init__(self, name="", id="", sourceRef=[], targetRef=[]):
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
    def __repr__(self):
        return "class SF "+ self.name

        



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(prog='argparse_template.py', description='Tutorial') 
    parser.add_argument('--input', '-in', default='./data/Assignment1.xml', type=str, required=True,  help='[type:string]Input Directory')
    parser.add_argument('--output', '-out', default='./output/output.tpn', type=str, required=True,  help='[type:string]Output Directory')
    args = parser.parse_args()
    main(input=args.input, output=args.output)
    
    