from flask import Flask, send_from_directory
from flask import Flask, request, jsonify
import json
import socket


testJsonData=[{"id": "node1", "name": "板卡1", "children": [{"id": 1, "text": "server1"}]}, {"id": "node2", "name": "板卡2", "children": []}, {"id": "node3", "name": "板卡3", "children": []}, {"id": "node4", "name": "板卡4", "children": []}]
testJsonData2=[{"id": "node1", "name": "板卡1", "children": [{"id": 1, "text": "server1"}, {"id": 3, "text": "server3"}, {"id": 4, "text": "server4"}, {"id": 2, "text": "server2"}]}, {"id": "node2", "name": "板卡2", "children": []}, {"id": "node3", "name": "板卡3", "children": []}, {"id": "node4", "name": "板卡4", "children": []}]
testJsonData3=[{"id": "node1", "name": "板卡1", "children": [{"id": 1, "text": "atomic_service_fwwz"}, {"id": 3, "text": "atomic_service_dds"}]}, {"id": "node2", "name": "板卡2", "children": [{"id": 4, "text": "atomic_service_gdwz"}, {"id": 2, "text": "atomic_service_fwgz"}]}, {"id": "node3", "name": "板卡3", "children": []}, {"id": "node4", "name": "板卡4", "children": []}]

node1={'ip':'192.168.0.106','port':6666}
node0={'ip':'192.168.0.105','port':6666}

def sendJson(node,data):
    udp_addr = (node['ip'], node['port'])
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.sendto(json.dumps(data).encode('utf-8') , udp_addr)

sendJson(node0,testJsonData3)
sendJson(node1,testJsonData3)

