def isletra(caractere):
  if 'a' <= caractere <= 'z' or 'A' <= caractere <= 'Z':
    return True
  
  return False


def classe_token(estado):
    classificacoes = {
        1: 'Digito',
        3: 'Digito',
        4: 'Simbolo Especial',
        5: 'Identificador',
        6: 'Identificador',
        7: 'Simbolo Especial',
        8: 'Simbolo Especial',
        9: 'Simbolo Especial',
        10: 'Simbolo Especial',
        11: 'Simbolo Especial',
        12: 'Simbolo Especial',
        13: 'Comentário de uma linha',
        14: 'Simbolo Especial',
        15: 'Comentário de várias linhas',
        16: 'Comentário de várias linhas',
        17: 'Comentário de uma linha',
        20: 'Comentário',
        21: 'Simbolo Especial',
        23: 'Identificador'
    }
    
    return classificacoes.get(estado, -1)

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


def houve_mudanca_estado(estado_ant, estado_atual):
  return True if estado_ant != estado_atual else False

def estado_loop(estado):
  estados_loop = [1,3,6,23,15,16,17]  
  return True if estado in estados_loop else False    

def compilador1(estado, caractere):
  match estado:
    case 0:
      if caractere.isdigit():
        estado = 1
      elif caractere == "-":
        estado = 4
      elif is_se(caractere):
        if caractere in ['{', '}', ',', '*', '(', ')', '=', ';']:
          estado = 7
        elif caractere in ["+", ":", ">"]:
          estado = 8
        elif caractere == ".":
          estado = 21 
        elif caractere == "/":
          estado = 12
        elif caractere == "@":
          estado = 14
        elif caractere == "<":
          estado = 10
        else: 
          estado = -1
      elif caractere == "!":
        estado = 13
      elif isletra(caractere):
        estado = 23
      elif caractere == "_":
        estado = 22
      else: 
        estado = -1 
    case 1:
      if caractere.isdigit():
        estado = 1
      elif caractere == ",":
        estado = 2
      else: 
          estado = -1
    case 2:
      if caractere.isdigit():
        estado = 3
      else: 
          estado = -1
    case 3: 
      if caractere.isdigit():
        estado = 3
      else: 
          estado = -1
    case 4:
      if caractere.isdigit():
        estado = 1
      else: 
          estado = -1
    case 5:
      if caractere.isdigit() or isletra(caractere):
        estado = 6
      else: 
          estado = -1
    case 6:
      if caractere.isdigit() or isletra(caractere) or caractere == "\n":
        estado = 6
      else: 
          estado = -1
    case 7:
      estado = -1
    case 8:
      if caractere == "=":
        estado = 9 
      else: 
          estado = -1
    case 10:
      if caractere == "=":
        estado = 9
      elif caractere == ">":
        estado = 11
      else: 
          estado = -1
    case 11: 
      estado = -1
    case 12:
      if caractere == "/":
        estado = 15
      else: 
          estado = -1
    case 13:
      if caractere == "!":
        estado = 16
      else:
        estado = 17
    case 14: 
      if caractere == "@":
        estado = 17
      else: 
          estado = -1
    case 15:
      if caractere == "/":
        estado = 18 
      else: 
          estado = -1
    case 16:
      if caractere == "!":
        estado = 19
      else: 
          estado = 16
    case 17:
      if caractere == "\n":
        estado = 20
      else: 
          estado = -1
    case 18:
      if caractere == "/":
        estado = 20
      else:
        estado = 15
    case 19:
      if caractere == "!":
        estado = 20
      else:
        estado = 16
    case 20:
      estado = -1
    case 21:
      if isletra(caractere):
        estado = 6
      else: 
          estado = -1
    case 22:
      if isletra(caractere):
        estado = 6
      else: 
          estado = -1
    case 23: 
      if isletra(caractere):
        estado = 23
      elif caractere == "." or caractere == "_":
        estado = 5
      else: 
          estado = -1
  return estado

def analisador_lexico(linhas):
  indice_linha    = 0
  estado          = 0
  estado_ant      = 0
  
  token = {
    'token': '',
    'classe': '',
  }

  while(indice_linha < len(linhas)):
    indice_caractere = 0

    while(indice_caractere < len(linhas[indice_linha])):
      caractere = linhas[indice_linha][indice_caractere]
      
      estado = compilador1(estado, caractere)
      
      
      token['token'] += caractere
      
      if estado == -1 and classe_token(estado) == -1:
        token['classe'] = classe_token(estado_ant)
        token['token'] = token['token'][:-1]
        
        print_colorido(token['token'], token['classe'])
        token['token'] = ''
        token['classe'] = ''
        
        estado = 0
        estado_ant = 0
        if caractere != '\n':
          indice_caractere -= 1
      elif houve_mudanca_estado(estado_ant, estado) or (not houve_mudanca_estado(estado_ant, estado) and estado_loop(estado)):
        estado_ant = estado
      else:
        print_colorido(token['token'], token['classe'])
        token['token'] = ''
        token['classe'] = ''
        
        estado = 0
        estado_ant = 0
        
        indice_caractere -= 1
          
      indice_caractere += 1
      
    indice_linha += 1
  
  

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