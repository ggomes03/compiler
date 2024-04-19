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
    
    print(f"{cor}Token:{token.ljust(20)} -- Classe Token:{classificacao_token}{reset}")


def classifica_token(estado):
  if estado in [4,7,8,9,10,11,12,14,21]:
    return "Simbolo Especial"
  elif estado in [1,3]:
    return "Digito"
  elif estado in [13,15,16,17,20]:
    return "Comentário"
  elif estado in [5,6,21]:
    return "Identificador"
  elif estado in [2,22]:
    return "não reconhece"


def compilador(fonte):
  index_linha = 0

  while (index_linha < len(fonte)):
    estado              = 0
    index_caractere     = 0
    token               = ""
    classificacao_token = ""
    while (index_caractere < len(fonte[index_linha])):
      caractere_atual = fonte[index_linha][index_caractere]
      
      if not caractere_atual.isspace():
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
            elif caractere_atual == ".":
              estado = 21 
            elif caractere_atual == "/":
              estado = 12
            elif caractere_atual == "@":
              estado = 14
          elif isletra(caractere_atual):
            estado = 5
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
            if not caractere_atual.isspace():
              classificacao_token = classifica_token(estado)
              token = token[:-1]
              index_caractere -= 1
            else:
              classificacao_token = classifica_token(estado)
    
        case 4:
          if caractere_atual.isdigit():
            estado = 1
          else:
            classificacao_token = classifica_token(estado)
            
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
              classifica_token(estado)
          else:
            if caractere_atual.isspace():
              classificacao_token = classifica_token(estado)
            else:
              classificacao_token = classifica_token(estado)
              token = token[:-1]
              index_caractere -= 1


        case 12:
          if caractere_atual == "/":
            estado = 15
          if caractere_atual.isspace():
            classificacao_token = classifica_token(estado)
          else:
            classificacao_token = classifica_token(estado)
            token = token[:-1]
            index_caractere -= 1
        
        case 14: 
          if caractere_atual == "@":
            estado = 17
          else:
            classificacao_token = classifica_token(estado)
            token = token[:-1]
            index_caractere -= 1
        
        case 21:
          if caractere_atual.isdigit() or isletra(caractere_atual):
            estado = 6
          else:
            if caractere_atual.isspace():
              classificacao_token = classifica_token(estado)
            else:
              classificacao_token = classifica_token(estado)
              token = token[:-1]
              index_caractere -= 1
        case 22:
          if caractere_atual.isdigit() or isletra(caractere_atual):
            estado = 6
          else:
            classificacao_token = classifica_token(estado)
            token = token[:-1]
            index_caractere -= 1
        
      if classificacao_token and token:
        print_colorido(token, classificacao_token)
        token               = ""
        classificacao_token = ""
        estado              = 0
      index_caractere += 1

    index_linha += 1

    classificacao_token = classifica_token(estado) #classfica o ultimo token
    if classifica_token and token:
      print_colorido(token, classificacao_token)