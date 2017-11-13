import socket


def log(*args, **kwargs):
    print('log', *args, **kwargs)


def route_index():
    # 主页的处理函数，返回主页的响应
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = '<h1>Hello World</h1><img src="/doge.gif"/>'
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_image():
    # 图片的处理函数，读取图片并生成响应返回
    with open('doge.gif', 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n'
        img = header + b'\r\n' + f.read()
        return img


def error(code=404):
    # 根据code返回不同的错误响应
    e = {
        404: b'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def response_for_path(path):
    # 根据path调用响应处理函数，没有处理的path会返回404
    r = {
        '/': route_index,
        '/doge.gif': route_image,
    }
    response = r.get(path, error)
    return response()


def run(host='', port=3000):
    # 启动服务器
    with socket.socket() as s:
        s.bind((host, port))
    # 无限循环处理请求
    while True:
        s.listen(5)
        connection, address = s.accept()
        request = connection.recv(1024)
        request = request.decode('utf-8')
        log('ip and request, {}\n{}'.format(address, request))
        try:
            # chrome会发送空请求导致split得到空list，用try防止崩溃
            path = request.split()[1]
            # 用response_for_path得到path对应的相应内容
            response = response_for_path(path)
            # 把响应发给客户端
            connection.sendall(response)
        except Exception as e:
            log('error', e)


def main():
    config = {
        'host': '',
        'port': 3000,
    }
    run(**config)


if __name__ == '__main__':
    main()
