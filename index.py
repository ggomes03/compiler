import compilador as c
import compilador2 as c2

with open("fonte.txt", "r") as arquivo:
    linhas = arquivo.readlines()

c.analisador_lexico(linhas)
