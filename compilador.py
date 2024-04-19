def isletra(caractere):
  if 'a' <= caractere <= 'z' or 'A' <= caractere <= 'Z':
    return True
  
  return False


def is_se(caractere):
  simbolos_especiais = [';', ',', '.', '+', '-', '*', '(', ')', '<','>', ':', '=','{', '}', '/', '@']
  
  if caractere in simbolos_especiais:
    return True
  
  return False

def classifica_token(estado):
  if estado in [4,7]:
    return "Simbolo Especial"
  elif estado in [1,3]:
    return "Digito"
  elif estado in [0,2]:
    return "não reconhece"

def compilador(fonte):
  index_linha     = 0
  
  
  
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
          elif caractere_atual == ",":
            estado = 7
            classificacao_token = classifica_token(estado)

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
            
      if classificacao_token and token:
        print(f"Token:{token} -- Classe Token:{classificacao_token}")
        
        token               = ""
        classificacao_token = ""
        estado              = 0
      index_caractere += 1

    index_linha += 1