def chop(message):  # chopet -> chop
    print(message)

def qosh(x, y):
    return x + y

def ayir(x, y):
    return x - y

def kopayt(x, y):  # kopaytir -> kopayt
    return x * y

def bol(x, y):
    return x / y

def max_qiymat(x):  # yuqori -> max_qiymat
    return max(x)

def min_qiymat(x):  # past -> min_qiymat
    return min(x)

def uzun(x):
    return len(x)

def format_raqam(x):  # formatla -> format_raqam
    return f"{x:.2f}"

def matnga_otkaz(x):  # qatorga_ol -> matnga_otkaz
    return str(x)

def butun_qiymat(x):  # butun -> butun_qiymat
    return int(x)

def haqiqiy_qiymat(x):  # haqiqiy -> haqiqiy_qiymat
    return float(x)

def kvadrat(x):
    return x ** 2

def kub(x):
    return x ** 3

def ildiz_ol(x):  # ildiz -> ildiz_ol
    from math import sqrt
    return sqrt(x)

def qoldiq(x, y):
    return x % y

def ulush_ol(x, y):  # ulush -> ulush_ol
    return x // y

def tartibla(x):  # tartib -> tartibla
    return sorted(x)

def avvalgi_qismini_ol(x):  # avvalgi -> avvalgi_qismini_ol
    return x[1:]

def oxirgi_qismini_ol(x):  # orqa -> oxirgi_qismini_ol
    return x[:-1]

def listdan_qidir(x, y):  # qidir -> listdan_qidir
    return x.find(y)

def mavjudmi(x, y):  # mavjud -> mavjudmi
    return y in x

def havola_parsela(x):  # havola -> havola_parsela
    import urllib.parse
    return urllib.parse.urlparse(x)

def fayl_oqish(x):  # oqish -> fayl_oqish
    with open(x, 'r') as file:
        return file.read()

def fayl_yozish(x, data):  # yozish -> fayl_yozish
    with open(x, 'w') as file:
        file.write(data)

def fayl_qatorlar_ol(x):  # faylni_qaytar -> fayl_qatorlar_ol
    with open(x, 'r') as file:
        return file.readlines()

def vaqt_ol():  # vaqtni_ol -> vaqt_ol
    from datetime import datetime
    return datetime.now()

def vaqt_formatlash(x):  # vaqtni_belgila -> vaqt_formatlash
    from datetime import datetime
    return datetime.strptime(x, '%Y-%m-%d %H:%M:%S')

def ipni_top(x):  # boglan -> ipni_top
    import socket
    return socket.gethostbyname(x)

def formatla(x, y):  # format -> formatla
    return f"{x:{y}}"
