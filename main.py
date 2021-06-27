from red import DireccionamientoIP,subRedes, vlsm

if __name__ == "__main__":
    #DireccionamientoIP('192.168.128.0','255.255.248.0')
    #subRedes('192.168.192.0',6,'255.255.240.0')
    vlsm('192.168.1.0',7,[15,30,45,8,22,3,2],24)