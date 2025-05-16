from websocket_server import WebsocketServer

# 连接建立时的回调函数
def new_client(client, server):
    print("New client connected and was given id %d" % client['id'])
    server.send_message_to_all("Hey all, a new client has joined us")

# 接收到消息时的回调函数
def message_received(client, server, message):
    print("Client(%d) said: %s" % (client['id'], message))
    server.send_message_to_all(message)

# 连接关闭时的回调函数
def client_left(client, server):
    print("Client(%d) disconnected" % client['id'])

# 创建 WebSocket 服务器
server = WebsocketServer(host='0.0.0.0', port=8080)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)

# 启动服务器
server.run_forever()