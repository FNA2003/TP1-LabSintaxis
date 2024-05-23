from AFDs import *

tipos_de_tokens_con_sus_automatas = [("if",afd_if), ("then",afd_then), ("call",afd_call), ("begin",afd_begin), 
    ("end",afd_end), ("while",afd_while), ("do",afd_do), ("odd",afd_odd), 
    ("const",afd_const), ("var",afd_var), ("comparation",afd_comparation), ("assign", afd_asignation),
    ("procedure", afd_procedure),("id",afd_id), ("operation",afd_operation),  
    ("#", afd_end_program), ("numbers",afd_numbers),  ("coma", afd_coma), (";",afd_punto_y_coma), 
    ("(",afd_parentesis_inicial), (")",afd_parentesis_final), ("blanckSpace", afd_white_space)]

def lexer(codigoFuente):

    contador = 1
    inicio_del_token = 0
    fin_del_token = 0
    token = ''

    nuevos_tipos_de_tokens_posibles = []
    antiguos_tipos_de_tokens_posibles = []

    lista_final_de_tokens_con_sus_tipos = []
    
    # Recorro el codigo fuente del prg, formando un token 1 caracter mas largo por cada iteracion hasta hallarle una clasificacion
    # Una vez hallada la clasificacion, paso a recorrer lo que resta del codigo fuente aplicando el mismo procedimiento
    while contador <= len(codigoFuente):
        fin_del_token += contador
        token = codigoFuente[inicio_del_token:fin_del_token]
        
        # A cada nuevo token extraido del codigo fuente (cadena del codigo fuente desde la posicion 'inicio_del_token' 
        # hasta la posicion anterior a 'fin_del_token') lo evaluo con todos los automatas de los tipos de tokens 
        # anteriormente definidos.
        for tipo_de_token, afd_del_token in tipos_de_tokens_con_sus_automatas:
            
            # Si el token corresponde a algun tipo, agrego ese tipo a la lista de 'nuevos_tipos_de_tokens_posibles'
            if afd_del_token(token) == 'aceptado':
                nuevos_tipos_de_tokens_posibles.append(tipo_de_token)
        
        # Si la lista de 'nuevos_tipos_de_tokens_posibles' no esta vacia, quiere decir que puedo agregar un caracter mas al token 
        # extraido del codigo fuente evaluado actualmente, y verificar si el nuevo token resultante pertenece a algun tipo de token
        if len(nuevos_tipos_de_tokens_posibles) >= 1:
            antiguos_tipos_de_tokens_posibles = nuevos_tipos_de_tokens_posibles
            contador += 1

        # Si la lista de 'nuevos_tipos_de_tokens_posibles' esta vacia y la lista de 'antiguos_tipos_de_tokens_posibles' no esta vacia, 
        # quiere decir que debo quitarle un caracter al token extraido del codigo fuente evaluado actualmente y clasificar al nuevo token 
        # resultante con el tipo de token que tenga mayor prioridad dentro de la lista de 'antiguos_tipos_de_tokens_posibles'
        elif len(nuevos_tipos_de_tokens_posibles == 0) and len(antiguos_tipos_de_tokens_posibles >= 1):
            token = token[:-1]

            tipo_de_token_definitivo = antiguos_tipos_de_tokens_posibles[0] # El tipo de token con mayor prioridad esta en la posicion 0

            # Agrego el token ya clasificado, junto con su clasificacion, a la 'lista_final_de_tokens_con_sus_tipos'
            lista_final_de_tokens_con_sus_tipos.append((tipo_de_token_definitivo, token)) 

            # como ya clasifique el token extraido del codigo fuente desde la posicion 'inicio_del_token' hasta la posicion
            # anterior a 'fin_del_token' ahora analizo el token que comienza en la posicion anterior a 'fin_del_token'
            inicio_del_token = fin_del_token - 1

            # Vacio las listas con los tipos de tokens posibles antiguos y nuevos para analizar el siguiente token
            nuevos_tipos_de_tokens_posibles = []
            antiguos_tipos_de_tokens_posibles = []
        
        elif len(nuevos_tipos_de_tokens_posibles == 0) and len(antiguos_tipos_de_tokens_posibles == 0): 
            print('Error: Caracter o expresion invalida')
    
    return lista_final_de_tokens_con_sus_tipos