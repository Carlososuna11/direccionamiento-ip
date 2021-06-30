from red import DireccionamientoIP,subRedes, vlsm

if __name__ == "__main__":
    #DireccionamientoIP('192.168.128.0','255.255.248.0')
    #subRedes('192.168.192.0',6,'255.255.240.0')
    vlsm('13.0.0.0',10,[300,260,100,2,2,2,3,40,80,20],8)