#convert bpmn to tpn
import os
os.chdir("/Users/elianatschang/Desktop/Business-Process-Technology-Management")

import xml.dom
from xml.dom import minidom

file = minidom.parse('Assignment1.bpmn')

root = file.getroot()
for child in root:
 testing  = child.get('id')
 if testing == 'sid-D9F3C396-BE0D-4992-819D-9C76BE04AA90':
    print (child.tag, child.attrib)
    print (child.find('name').text)

import xml.etree.ElementTree as ET
root_node = ET.parse('Assignment1.bpmn').getroot()
print(root_node)


from xml.dom import minidom

doc = minidom.parse("Assignment1.bpmn")

# doc.getElementsByTagName returns NodeList
name = doc.getElementsByTagName("name")[0]
print(name.firstChild.data)

Elements = doc.getElementsByTagName("extensionElements")
for extensionElements in Elements:
        sid = extensionElements.getAttribute("id")
        name = extensionElements.getElementsByTagName("name")[0]
        in = extensionElements.getElementsByTagName("incoming")[0]
        out = extensionElements.getElementsByTagName("outgoing")[0]
        print("id:%s, name:%s, in:%s, out:%s" %
              (sid, name.firstChild.data, in.firstChild.data, out.firstChild.data))