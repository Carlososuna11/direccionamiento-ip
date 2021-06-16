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



def DireccionamientoIP(ip,mask=None):
    data = direccionRed(ip,mask)
    print(tabulate(list(map(lambda x: [x[0],x[1],convertirDecimal(x[1])],data.items())),tablefmt="fancy_grid"))
