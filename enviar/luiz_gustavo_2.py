def isletra(caractere):
  if 'a' <= caractere <= 'z' or 'A' <= caractere <= 'Z':
    return True
  
  return False


def is_se(caractere):
  simbolos_especiais = [';', ',', '.', '+', '-', '*', '(', ')', '<','>', ':', '=','{', '}', '/', '@']
  
  if caractere in simbolos_especiais:
    return True
  
  return False

def print_colorido(token, classificacao_token):
    cores = {
        "Simbolo Especial": "\033[30m",  # Vermelho
        "Digito": "\033[94m",             # Azul
        "Comentário": "\033[93m",         # Amarelo
        "Identificador": "\033[92m",      # Verde
        "não reconhece": "\033[91m"       # Vermelho
    }
    
    reset = "\033[0m"
    
    cor = cores.get(classificacao_token, reset)
    
    print(f"{cor}Token: {token.ljust(30)} -- Classe Token:{classificacao_token}{reset}")


def classifica_token(estado):
  if estado in [4,7,8,9,10,11,12,14,21]:
    return "Simbolo Especial"
  elif estado in [1,3]:
    return "Digito"
  elif estado in [13,15,16,17,20]:
    return "Comentário"
  elif estado in [6,23]:
    return "Identificador"
  elif estado in [2,5,22]:
    return "não reconhece"





def compilador(fonte):
  index_linha         = 0
  estado              = 0
  token               = ""
  while (index_linha < len(fonte)):
    index_caractere     = 0
    classificacao_token = ""
    while (index_caractere < len(fonte[index_linha])):
      caractere_atual = fonte[index_linha][index_caractere]
      
      if caractere_atual != "\n":
        token += caractere_atual
      
      match estado:
        case 0:
          if caractere_atual.isdigit():
            estado = 1
          elif caractere_atual == "-":
            estado = 4
          elif is_se(caractere_atual):
            if caractere_atual in ['{', '}', ',', '*', '(', ')', '=', ';']:
              estado = 7
              classificacao_token = classifica_token(estado)
            elif caractere_atual in ["+", ":", ">"]:
              estado = 8
            elif caractere_atual == ".":
              estado = 21 
            elif caractere_atual == "/":
              estado = 12
            elif caractere_atual == "@":
              estado = 14
            elif caractere_atual == "<":
              estado = 10
          elif caractere_atual == "!":
            estado = 13
          elif isletra(caractere_atual):
            estado = 23
          elif caractere_atual == "_":
            estado = 22 
        case 1:
          if caractere_atual.isdigit():
            estado = 1
          elif caractere_atual == ",":
            estado = 2
          else: 
            classificacao_token = classifica_token(estado)
        case 2:
          if caractere_atual.isdigit():
            estado = 3
          else:
            classificacao_token = classifica_token(estado)
        case 3: 
          if caractere_atual.isdigit():
            estado = 3
          else: 
            classificacao_token = classifica_token(estado)
            token = token[:-1]
            index_caractere -= 1
        case 4:
          if caractere_atual.isdigit():
            estado = 1
          else:
            classificacao_token = classifica_token(estado)
            token = token[:-1]
            index_caractere -= 1
        case 5:
          if caractere_atual.isdigit() or isletra(caractere_atual):
            estado = 6
          else:
            classificacao_token = classifica_token(estado)
            token = token[:-1]
            index_caractere -= 1
        case 6:
          if caractere_atual.isdigit() or isletra(caractere_atual) or caractere_atual == "\n":
            estado = 6
            if caractere_atual == "\n":
              classificacao_token = classifica_token(estado)
          else:
            classificacao_token = classifica_token(estado)
            token = token[:-1]
            index_caractere -= 1
        case 8:
          if caractere_atual == "=":
            estado = 9 
          else:
              classificacao_token = classifica_token(estado)
              token = token[:-1]
              index_caractere -= 1
        case 9:
          if caractere_atual != "\n":
            token = token[:-1]
          classificacao_token = classifica_token(estado)
          index_caractere -= 1
        case 10:
          if caractere_atual == "=":
            estado = 9
          elif caractere_atual == ">":
            estado = 11
          else:
            classificacao_token = classifica_token(estado)
            token = token[:-1]
            index_caractere -= 1
        case 11:
          classificacao_token = classifica_token(estado)
          token = token[:-1]
          index_caractere -= 1
        case 12:
          if caractere_atual == "/":
            estado = 15
          else:
            classificacao_token = classifica_token(estado)
            token = token[:-1]
            index_caractere -= 1
        case 13:
          if caractere_atual == "!":
            estado = 16
          else:
            if caractere_atual == "\n":
              estado = 17
              index_caractere -= 1
        case 14: 
          if caractere_atual == "@":
            estado = 17
          else:
            classificacao_token = classifica_token(estado)
            token = token[:-1]
            index_caractere -= 1
        case 15:
          if caractere_atual == "/":
            estado = 18 
          elif caractere_atual == "\n":
            break
        case 16:
          if caractere_atual == "!":
            estado = 19
        case 17:
          if caractere_atual == "\n":
            estado = 20
            classificacao_token = classifica_token(estado)
        case 18:
          if caractere_atual == "/":
            estado = 20
            classificacao_token = classifica_token(estado)
          else:
            estado = 15
        case 19:
          if caractere_atual == "!":
            estado = 20
          else:
            estado = 16
        case 20:
          if caractere_atual != "\n":
            token = token[:-1]
          classificacao_token = classifica_token(estado)
          index_caractere -= 1
        case 21:
          if caractere_atual.isdigit() or isletra(caractere_atual):
            estado = 6
          else:
            classificacao_token = classifica_token(estado)
            # token = token[:-1]
            # index_caractere -= 1
        case 22:
          if caractere_atual.isdigit() or isletra(caractere_atual):
            estado = 6
          else:
            classificacao_token = classifica_token(estado)
            token = token[:-1]
            index_caractere -= 1
        case 23:
          if caractere_atual == "." or caractere_atual == "_":
            estado = 5
          elif caractere_atual.isdigit() or isletra(caractere_atual):
            estado = 23
          else:
            classificacao_token = classifica_token(estado)
            # token = token[:-1]
            # index_caractere -= 1
            
      if classificacao_token and token:
        if classificacao_token != "Comentário":
          token = token.replace(" ","")
        print_colorido(token, classificacao_token)
        token               = ""
        classificacao_token = ""
        estado              = 0
      index_caractere += 1

    index_linha += 1

  classificacao_token = classifica_token(estado)
  if classifica_token and token:
    print_colorido(token, classificacao_token)