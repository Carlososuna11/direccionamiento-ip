from red import DireccionamientoIP,subRedes, vlsm

if __name__ == "__main__":
    #DireccionamientoIP('192.168.128.0','255.255.248.0')
    #subRedes('192.168.192.0',6,'255.255.240.0')
    vlsm('150.15.128.0',8,[20,3,2,40,600,100,300,60],18)