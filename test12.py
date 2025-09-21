import socket

def send_data_to_server(data, server_ip='localhost', server_port=7777):
    # 创建一个socket对象
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # 连接到服务器
        client_socket.connect((server_ip, server_port))
        print(f"Connected to server {server_ip}:{server_port}")

        # 发送数据，并添加换行符
        client_socket.sendall((data + "\n").encode('utf-8'))
        print(f"Data sent: {data}")

        # 接收服务器的响应（如果有）
        response = client_socket.recv(1024)
        print(f"Received response from server: {response.decode('utf-8')}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # 关闭连接
        client_socket.close()
        print("Connection closed")

if __name__ == "__main__":
    # 需要发送的数据
    data_list = ["103121 12", "104521 45"]
    for data in data_list:
        send_data_to_server(data)
