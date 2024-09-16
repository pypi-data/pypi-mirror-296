def chopet(message):
    print(message)

def qosh(x, y):
    return x + y

def ayir(x, y):
    return x - y

def kopaytir(x, y):
    return x * y

def bol(x, y):
    return x / y

def yuqori(x):
    return max(x)

def past(x):
    return min(x)

def uzunlik(x):
    return len(x)

def formatla(x):
    return f"{x:.2f}"

def qator_bul(x):
    return str(x)

def butun(x):
    return int(x)

def haqiqiy(x):
    return float(x)

def kvadrat(x):
    return x ** 2

def kub(x):
    return x ** 3

def ildiz(x):
    from math import sqrt
    return sqrt(x)

def qoldiq(x, y):
    return x % y

def ulush(x, y):
    return x // y

def tartib(x):
    return sorted(x)

def avvalgi(x):
    return x[1:]

def orqa(x):
    return x[:-1]

def qidir(x, y):
    return x.find(y)

def mavjud(x, y):
    return y in x

def havola(x):
    import urllib.parse
    return urllib.parse.urlparse(x)

def oqish(x):
    with open(x, 'r') as file:
        return file.read()

def yozish(x, data):
    with open(x, 'w') as file:
        file.write(data)

def faylni_qaytar(x):
    with open(x, 'r') as file:
        return file.readlines()

def vaqtni_ol():
    from datetime import datetime
    return datetime.now()

def vaqtni_belgila(x):
    from datetime import datetime
    return datetime.strptime(x, '%Y-%m-%d %H:%M:%S')

def boglan(x):
    import socket
    return socket.gethostbyname(x)

def format(x, y):
    return f"{x:{y}}"
