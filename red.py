from tabulate import tabulate
clase = {
            127: {'clase':'A','mask':'255.0.0.0','broadcast':'x.255.255.255'},
            192: {'clase':'B','mask':'255.255.0.0','broadcast':'x.x.255.255'},
            224: {'clase':'C','mask':'255.255.255.0','broadcast':'x.x.x.255'},
            240: {'clase':'D'},
            256: {'clase':'E'}
        }

def direccionRed(ip,mask=None):
    claseip = claseIp(ip)
    ip = convertirBinario(ip)
    if not(mask):
        mask = claseip['mask']
    mask = convertirBinario(mask)
    red = ''
    for index,value in enumerate(ip):
        if mask[index] in ['1','.']:
            red+=value
        else:
            red+='0'
    broasd = broadcast(red,mask)
    rangoDirecciones = rango(red,broasd)
    return {'IP':ip,'MASCARA':mask,'RED':red,'BROADCAST':broasd,'INICIO':rangoDirecciones[0],'FIN':rangoDirecciones[1]}

def claseIp(direccion):
    valor = int(direccion.split('.')[0])
    for i in clase:
        if valor<i:
            return clase[i]
        
def convertirBinario(direccion):
    direccion = list(map(lambda x: f'{int(x):08b}',direccion.split('.')))
    return '.'.join(direccion)

def convertirDecimal(direccion):
    direccion = list(map(lambda x: str(int(f'0b{x}',2)),direccion.split('.')))
    return '.'.join(direccion)

def broadcast(direccion,mask):
    host=0
    if '1' in mask:
        host = len(mask) - mask[::-1].index('1')
    last = ''
    for index,value in enumerate(direccion):
        if value!='.':
            last+= value if index<host else '1'
        else:
            last+='.'
    return last

def rango(red,broadcast):
    first0 = len(red) - red[::-1].index('0') -1 
    last1 = len(broadcast) - broadcast[::-1].index('1') -1 
    begin = red[:first0] + '1' + red[first0+1:]
    final = broadcast[:last1] + '0' + broadcast[last1+1:0]
    return [begin,final]

def encrypt(string, length):
    return '.'.join(string[i:i+length] for i in range(0,len(string),length))

def es_potencia_de_dos(numero):
    if numero < 1:
        return False
    if numero <= 2:
        return [True,1]
    i = 2
    count =1
    while True:
        i *= 2
        count+=1
        if i == numero:
            return [True,count]
        if i > numero:
            return False

def maskBarra(mask):
    a = 32-mask
    mask = '1'*mask + '0'*a
    out = ''
    for i in range(32):
        out+=mask[i]
        if i%8==7 and i>0:
            out+='.'
    return convertirDecimal(out[:-1])

def DireccionamientoIP(ip,mask=None):
    data = direccionRed(ip,mask)
    print(tabulate(list(map(lambda x: [x[0],x[1],convertirDecimal(x[1])],data.items())),tablefmt="fancy_grid"))

def subRedes(ip:str,cantidad:int,mask:str=None,maskbarra:int=None):
    """
    :params ip: Direccion IP
    :param  cantidad: Cantidad de redes
    :param mask: mascara a usar
    :param maskbarra: mascara en formato barra ej: 22
    """
    if maskbarra:
        mask = maskBarra(maskbarra)
    data = direccionRed(ip,mask)
    red = data['RED']
    mask = data['MASCARA']
    while not(es_potencia_de_dos(cantidad)):
        cantidad+=1
    pos = es_potencia_de_dos(cantidad)[1]
    numeros = [format(x,f'0{pos}b') for x in range(cantidad)]
    host=0
    direcciones = []
    if '1' in mask:
        host = len(mask.replace('.','')) - mask[::-1].replace('.','').index('1')
    dir_mask_dec = convertirDecimal(encrypt(mask.replace('.','')[:host]+ numeros[-1] + mask.replace('.','')[host+pos:],8))
    for index,value in enumerate(numeros):
        direcciones.append(convertirDecimal(encrypt(red.replace('.','')[:host]+ value + red.replace('.','')[host+pos:],8)))
    host = 0
    if '1' in convertirBinario(dir_mask_dec):
        host = len(convertirBinario(dir_mask_dec).split('.')) -(len(convertirBinario(dir_mask_dec).split('.')) - convertirBinario(dir_mask_dec).replace('.','')[::-1].index('1'))
    print(f'Hosts: 2^{host}-2 = {(2**(host))-2}\n')
    print(tabulate({'DIRECCIONES':direcciones},headers="keys",tablefmt="fancy_grid"))
    for index,value in enumerate(direcciones):
        print(f'\nDireccion {index+1}\n')
        DireccionamientoIP(value,dir_mask_dec)
        



def vlsm(ip:str,cantidad:int,hosts:list,maskbarra:int=None):
    octeto = {
        9:1,
        17:2,
        25:3,
        32:4
    }
    abecedario = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    """
    :params ip: Direccion IP
    :param  cantidad: Cantidad de redes
    :param hosts: hosts de cada subred
    :param maskbarra: mascara en formato barra ej: 22
    """
    if len(hosts)!=cantidad:
        print('ERROR, La cantidad de hosts no coincide con la de subredes')
        exit()
    if maskbarra:
        mask = maskBarra(maskbarra)
    data = direccionRed(ip,mask)
    red = data['RED']
    mask = data['MASCARA']
    canthost = [2**(32-i)-2 for i in range(maskbarra+1,32)]
    hosts.sort(reverse=True)
    value =[]
    masks = []
    direcciones = []
    sumador = 0
    sumador2 = 0
    for index,host in enumerate(hosts):
        n = 0
        for index2,pos in enumerate(canthost):
            if host>pos:
                break
            n=index2
        if index==0:
            value.append(format(0,f'0{n+1}b'))
        else:
            val = int(value[-1],base=2)
            val = format(val+1,f'0{len(value[-1])}b')
            value.append(val+'0'*(n+1-len(value[-1])))
        masks.append(value[-1].replace('0','1'))
        if index==0:
            for key,val in octeto.items():
                if  maskbarra+n+1 < key:
                    sumador=val
                    break
        for key,val in octeto.items():
                if  maskbarra+n+1 < key:
                    sumador2=val
                    break
        a = encrypt(red.replace('.','')[:maskbarra]+ value[-1] + red.replace('.','')[maskbarra+n+1:],8)
        b = convertirDecimal(encrypt(red.replace('.','')[:(sumador-1)*8],8))
        #print(len(encrypt(red.replace('.','')[:(sumador-1)*8],8)))
        #a= a[:maskbarra+n+sumador] + ' | ' + a[maskbarra+n+sumador:]
        dir_mask_dec = convertirDecimal(encrypt(mask.replace('.','')[:maskbarra]+ masks[-1] + mask.replace('.','')[maskbarra+n+1:],8))
        dir = convertirDecimal(encrypt(red.replace('.','')[:maskbarra]+ value[-1] + red.replace('.','')[maskbarra+n+1:],8))
        print(f"{b}.{a[(sumador-1)*8:maskbarra+n+sumador2]} | {a[maskbarra+n+sumador2:]} ------> {dir}/{maskbarra+n+1}")
        data = dict(map(lambda x: (x[0],convertirDecimal(x[1])), direccionRed(dir,dir_mask_dec).items()))
        direcciones.append([f"RED {abecedario[index].upper()}\n ({host} hosts)",canthost[n],dir,data['INICIO'],data['FIN'],data['BROADCAST'],data['MASCARA'],f"/{maskbarra+n+1}"])
    print("\n")
    print(tabulate(direcciones,headers=["RED","MAXIMO DE HOSTS","DIRECCION","PRIMER HOST","ULTIMO HOST","BROADCAST","MASCARA","FORMATO BARRA"],tablefmt="fancy_grid"))
