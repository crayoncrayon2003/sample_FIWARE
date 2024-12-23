import socket
import time

HOST = 'localhost'  # サーバーのホスト名
PORT = 9001         # サーバーのポート番号

# サンプルデータ（JSON形式）
data = [
    '{"id": "urn:ngsi-ld:Sensor:001", "type": "Sensor", "name": {"type": "Text", "value": "Sensor", "metadata": {}}, "temperature": {"type": "Integer", "value": 20, "metadata": {}}, "humidity": {"type": "Integer", "value": 20, "metadata": {}}}',
    '{"id": "urn:ngsi-ld:Sensor:002", "type": "Sensor", "name": {"type": "Text", "value": "Sensor", "metadata": {}}, "temperature": {"type": "Integer", "value": 22, "metadata": {}}, "humidity": {"type": "Integer", "value": 21, "metadata": {}}}'
]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    for item in data:
        s.sendall(item.encode('utf-8'))
        time.sleep(1)  # データ送信間隔
