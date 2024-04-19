import compilador as c

with open("fonte.txt", "r") as arquivo:
    linhas = arquivo.readlines()
    
c.compilador(linhas)