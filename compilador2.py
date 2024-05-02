def isletra(caractere):
    return 'a' <= caractere <= 'z' or 'A' <= caractere <= 'Z'


def is_se(caractere):
    simbolos_especiais = [';', ',', '.', '+', '-', '*', '(', ')', '<', '>', ':', '=', '{', '}', '/', '@']
    return caractere in simbolos_especiais


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
    
    print(f"{cor}Token: {token.ljust(30)} -- Classe Token: {classificacao_token}{reset}")


def classifica_token(estado):
    classificacoes = {
        1: 'Digito',
        2: 'Digito',
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
        18: 'Comentário',
        19: 'Comentário',
        20: 'Comentário',
        21: 'Simbolo Especial'
    }
    
    return classificacoes.get(estado, 'não reconhece')


def compilador(fonte):
    index_linha = 0
    token = ""
    estado = 0
    
    while index_linha < len(fonte):
        index_caractere = 0
        
        while index_caractere < len(fonte[index_linha]):
            caractere_atual = fonte[index_linha][index_caractere]
            token += caractere_atual
            
            # Definição das transições
            transicoes = {
                (0, str.isdigit): 1,
                (0, '-'): 4,
                (0, is_se): 7,
                (0, '!'): 13,
                (0, isletra): 5,
                (0, '_'): 22,
                (1, str.isdigit): 1,
                (1, ','): 2,
                (2, str.isdigit): 3,
                (3, str.isdigit): 3,
                (4, str.isdigit): 1,
                (5, lambda x: str.isdigit(x) or isletra(x)): 6,
                (6, lambda x: str.isdigit(x) or isletra(x) or x == '\n'): 6,
                (8, '='): 9,
                (10, '='): 9,
                (10, '>'): 11,
                (12, '/'): 15,
                (13, '!'): 16,
                (14, '@'): 17,
                (15, '/'): 18,
                (15, '\n'): None,
                (16, '!'): 19,
                (17, '\n'): None,
                (18, '/'): 20,
                (19, '!'): 20,
                (21, lambda x: str.isdigit(x) or isletra(x)): 6,
                (22, lambda x: str.isdigit(x) or isletra(x)): 6
            }
            
            estado = transicoes.get((estado, caractere_atual), 0)
            
            if estado == 0:
                token = token[:-1]
                index_caractere -= 1
            
            classificacao = classifica_token(estado)
            
            if classificacao and token:
                print_colorido(token, classificacao)
                token = ""
            
            index_caractere += 1
        
        index_linha += 1

    classificacao = classifica_token(estado)
    
    if classificacao and token:
        print_colorido(token, classificacao)
