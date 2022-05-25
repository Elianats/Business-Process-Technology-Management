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




