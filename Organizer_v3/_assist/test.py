import socket
  
client = socket.socket()
# подключаемся по адресу www.python.org и порту 80
client.connect(("e9226605.beget.tech", 80))
# данные для отправки - стандартные заголовки протокола http
message = "test"
print("Connecting...")
client.send(message.encode())       # отправляем данные серверу
data = client.recv(1024)            # получаем данные с сервера
print("Server sent: ", data.decode())    # выводим данные на консоль
client.close()                      # закрываем подключение
