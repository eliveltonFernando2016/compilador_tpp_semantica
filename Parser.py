from Lexer import Lexer
from ply import yacc
from Tree import Tree

class Parser:
    def __init__(self, code):
        lex = Lexer()
        self.tokens = lex.tokens
        self.precedence = (
                            ('left', 'IGUAL', 'MAIOR', 'MENOR', 'MAIORIGUAL', 'MENORIGUAL', 'DIFERENTE'),
                            ('left', 'SOMA', 'SUBR'),
                            ('left', 'VEZES', 'DIVIDE')
                           )
        parser = yacc.yacc(debug=False, module=self, optimize=False)
        self.ast = parser.parse(code)

    def p_programa(self, p):
        '''
        programa : lista_declaracoes 
        '''        
        p[0] = Tree('programa', [p[1]])

    def p_lista_declaracoes(self, p):
        '''
        lista_declaracoes : lista_declaracoes declaracao
        '''
        
        p[0] = Tree('lista_declaracoes', [p[1], p[2]])

    def p_lista_declaracoes1(self,p):
        '''
            lista_declaracoes : declaracao
        '''
        p[0] = Tree('lista_declaracoes1', [p[1]])

    def p_lista_declaracoes_error(self, p):
        '''
            lista_declaracoes : error error
                              | error
        '''
        
        raise SyntaxError("Erro: declaração \n")

    def p_declaracao(self, p):
        '''
        declaracao : declaracao_variaveis
        		   | inicializacao_variaveis
        		   | declaracao_funcao
        '''
        p[0] = Tree('declaracao', [p[1]])

    def p_declaracao_error(self, p):
        '''
            declaracao : error
        '''
		
        raise SyntaxError("Erro: declaração \n")

    def p_declaracao_variaveis(self, p):
        'declaracao_variaveis : tipo DOISPONTOS lista_variaveis'
        p[0] = Tree('declaracao_variaveis', [p[1],p[3]])

    def p_declaracao_variaveis_error(self, p):
        '''
            declaracao_variaveis : error DOISPONTOS error 	
        '''
		
        raise SyntaxError("Erro: declaração variaveis \n")

    def p_inicializacao_variaveis(self, p):
    	'inicializacao_variaveis : atribuicao'
    	p[0] = Tree('inicializacao_variaveis', [p[1]])

    def p_inicializacao_variaveis_error(self, p):
        '''
            inicializacao_variaveis : error
        '''
        
        raise SyntaxError("Erro: inicialização variaveis \n")

    def p_lista_variaveis(self, p):
        '''
        lista_variaveis : lista_variaveis VIRGULA var
        '''
        
        p[0] = Tree('lista_variaveis',[p[1],p[3]])

    def p_lista_variaveis1(self, p):
        '''
            lista_variaveis : var
        '''

        p[0] = Tree('lista_variaveis1', [p[1]])

    def p_lista_variaveis_error(self, p):
        '''
            lista_variaveis : error VIRGULA error
                            | error
        '''

        raise SyntaxError("Erro: variável \n")

    def p_var(self, p):
        '''
            var : ID
        '''

        p[0] = Tree('var',[],p[1])

    def p_var1(self, p):
        '''
	        var : ID indice
        '''

        p[0] = Tree('var1', [p[2]], p[1])

    def p_var_error(self, p):
        '''
            var : ID error
        '''

        raise SyntaxError("Erro: variavel \n")

    def p_indice(self, p):
        '''
        indice : indice ABRECOLCH expressao FECHACOLCH
        '''

        p[0] = Tree('indice',[p[1],p[3]])

    def p_indice1(self, p):
        '''
	 	    indice : ABRECOLCH expressao FECHACOLCH
	 	'''

        p[0] = Tree('indice1',[p[2]])

    def p_indice_error(self, p):
        '''
            indice : indice ABRECOLCH error FECHACOLCH
                   | ABRECOLCH error FECHACOLCH
        '''

        raise SyntaxError("Erro: sintaxe de indexação \n")

    def p_tipo(self, p):
        '''
            tipo : INTEIRO
        '''

        p[0] = Tree('tipo', [], p[1])

    def p_tipo1(self, p):
        '''
            tipo : FLUTUANTE
        '''
		
        p[0] = Tree('tipo1',[], p[1])

    def p_tipo_error(self, p):
        '''
            tipo : error
        '''

        raise SyntaxError("Erro: tipo de variável \n")

    def p_declaracao_funcao(self ,p):
        '''
            declaracao_funcao : tipo cabecalho
        '''
        
        p[0] = Tree('declaracao_funcao',[p[1],p[2]])

    def declaracao_funcao1(self, p):
        '''
            declaracao _funcao : cabecalho
        '''

        p[0] = Tree('declaracao_funcao', [p[1]])

    def p_declaracao_funcao_error(self, p):
        '''
            declaracao_funcao : error error
                              | error
        '''

        raise SyntaxError("Erro: declaração de função \n")

    def p_cabecalho(self, p):
    	'''
            cabecalho : ID ABREPAR lista_parametros FECHAPAR corpo FIM
        '''
    	p[0] = Tree('cabecalho',[p[3],p[5]],p[1])

    def p_cabecalho_error(self, p):
        '''
            cabecalho : ID ABREPAR error FECHAPAR error FIM
        '''

        raise SyntaxError("Erro: cabeçalho \n")

    def p_lista_parametros(self, p):
        '''
            lista_parametros : lista_parametros VIRGULA lista_parametros
                             | parametro
        '''
        
        if len(p) == 4:
            p[0] = Tree('lista_parametros', [p[1], p[3]])
        elif len(p) == 2:
            p[0] = Tree('lista_parametros', [p[1]])

    def p_lista_parametros1(self, p):
        '''
            lista_parametros : vazio
        '''

    def p_lista_parametros_error(self, p):
        '''
            lista_parametros : error VIRGULA error
        '''

        raise SyntaxError("Erro: parâmetro \n")

    def p_parametro(self, p):
    	'''
            parametro : tipo DOISPONTOS ID
        '''
    	p[0] = Tree('parametro', [p[1]], p[3])

    def p_parametro1_error(self, p):
        '''
            parametro : error DOISPONTOS ID
        '''

        raise SyntaxError("Erro: parâmetro \n")

    def p_parametro1(self, p):
    	'''
            parametro : parametro ABRECOLCH FECHACOLCH
        '''
    	p[0] = Tree('parametro', [p[1]])

    def p_corpo(self, p):
        '''
            corpo : corpo acao
        '''
        
        if len(p) == 3:
            p[0] = Tree('corpo', [p[1], p[2]])
        elif len(p) == 2:
            p[0] = Tree('corpo', [p[1]])

    def p_corpo1(self, p):
        '''
            corpo : vazio
        '''

        #p[0] = Tree('corpo', [p[1]])

    def p_corpo_error(self, p):
        '''
            corpo : error error
                  | error
        '''

        raise SyntaxError("Erro: corpo de função \n")

    def p_acao(self ,p):
    	'''
        acao : expressao
             | declaracao_variaveis
             | se
             | repita
             | leia
             | escreva
             | retorna
    	''' 
    	p[0] = Tree('acao', [p[1]])

    def p_acao_error(self, p):
        '''
            acao : error
        '''
        
        raise SyntaxError("Erro: ação \n")

    def p_se(self, p):
        '''
            se : SE expressao ENTAO corpo FIM
            | SE expressao ENTAO corpo SENAO corpo FIM
            | SE ABREPAR expressao FECHAPAR ENTAO corpo SENAO corpo FIM
        '''

        if len(p) == 6:
            p[0] = Tree('se', [p[2], p[4]])
        elif len(p) == 8:
            p[0] = Tree('se', [p[2], p[4], p[6]])
        elif len(p) == 10:
            p[0] = Tree('se', [p[3], p[6], p[8]])

    def p_se1(self, p):
        '''
            se : SE ABREPAR expressao FECHAPAR ENTAO corpo FIM
        '''

        p[0] = Tree('se', [p[3], p[6]])

    def p_se_error(self, p):
        '''
            se : SE error ENTAO error FIM
               | SE error ENTAO error SENAO error FIM
        '''

        raise SyntaxError("Erro: expressão se \n")

    def p_repita(self, p):
        '''
            repita : REPITA corpo ATE expressao
                   | REPITA corpo ATE ABREPAR expressao FECHAPAR
        '''
    	
        if len(p) == 5:
            p[0] = Tree('repita', [p[2], p[4]])
        elif len(p) == 7:
            p[0] = Tree('repita', [p[2], p[5]])

    def p_repita_error(self, p):
        '''
            repita : REPITA error ATE error
        '''
        
        raise SyntaxError("Erro: expressão repita \n")

    def p_atribuicao(self, p):
        '''
            atribuicao : var ATRIBUICAO expressao
        '''
        
        if len(p):
            p[0] = Tree('atribuicao', [p[1], p[3]], p[2])

    def p_atribuicao_error(self, p):
        '''
            atribuicao : error ATRIBUICAO error
        '''
		
        raise SyntaxError("Erro: atribuição \n")

    def p_leia(self, p):
    	'''
            leia : LEIA ABREPAR ID FECHAPAR
        '''
    	p[0] = Tree('leia',[],p[3])

    def p_leia_error(self, p):
        '''
            leia : error error error error
        '''

        raise SyntaxError("Erro: expressão LEIA \n")

    def p_escreva(self, p):
    	'''
            escreva : ESCREVA ABREPAR expressao FECHAPAR
        '''
    	p[0] = Tree('escreva',[p[3]])

    def p_escreva_error(self, p):
        '''
            escreva : ESCREVA ABREPAR error FECHAPAR
        '''

        raise SyntaxError("Erro: expressão ESCREVA \n")

    def p_retorna(self, p):
    	'''
            retorna : RETORNA ABREPAR expressao FECHAPAR
        '''
    	p[0] = Tree('retorna',[p[3]])

    def p_retorna_error(self, p):
        '''
            retorna : RETORNA ABREPAR error FECHAPAR
        '''

        raise SyntaxError("Erro: expressão RETORNA \n")

    def p_expressao(self, p):
    	'''
            expressao : expressao_simples
                    | atribuicao
    	'''
    	p[0] = Tree('expressao',[p[1]])

    def p_expressao_error(self, p):
        '''
            expressao : error
        '''

        raise SyntaxError("Erro: expressão \n")

    def p_expressao_simples(self, p):
        '''
            expressao_simples : expressao_aditiva
        '''
        
        p[0] = Tree('expressao_simples', [p[1]])

    def p_expressao_simples1(self, p):
        '''
            expressao_simples : expressao_simples operador_relacional expressao_aditiva
        '''

        p[0] = Tree('expressao_simples', [p[1], p[2], p[3]])

    def p_expressao_simples_error(self, p):
        '''
            expressao_simples : error
                              | error error error
        '''

        raise SyntaxError("Erro: expressão simples \n")

    def p_expressao_aditiva(self, p):
        '''
            expressao_aditiva : expressao_multiplicativa
        '''
        
        p[0] = Tree('expressao_aditiva',[p[1]])

    def p_expressao_aditiva_error(self, p):
        '''
            expressao_aditiva : error
                              | error error error
        '''

        raise SyntaxError("Erro: expressão aditiva \n")

    def p_expressao_aditiva1(self, p):
        '''
            expressao_aditiva : expressao_aditiva operador_multiplicacao expressao_unaria
        '''

        p[0] = Tree('expressao_aditiva1', [p[1], p[2], p[3]])

    def p_expressao_multiplicativa(self, p):
        '''
            expressao_multiplicativa : expressao_unaria
        '''

        p[0] = Tree('expressao_multiplicativa', [p[1]])
    
    def p_expressao_multiplicativa1(self, p):
        '''
            expressao_multiplicativa : expressao_aditiva operador_soma expressao_multiplicativa
        '''

        p[0] = Tree('expressao_multiplicativa', [p[1], p[2], p[3]])

    def p_expressao_unaria(self, p):
        '''
            expressao_unaria : fator
        '''
        
        p[0] = Tree('expressao_unaria', [p[1]])
    
    def p_expressao_unaria1(self, p):
        '''
            expressao_unaria : operador_soma fator
        '''
        
        p[0] = Tree('expressao_unaria', [p[1], p[2]])

    def p_operador_relacional(self, p):
    	'''
            operador_relacional : MENOR
                                | MAIOR
                                | IGUAL
                                | DIFERENTE
                                | MENORIGUAL
                                | MAIORIGUAL
                                | ELOGICO
                                | OULOGICO
                                | NEGACAO
    	'''
    	p[0] = Tree('operador_relacional',[])

    def p_operador_soma(self, p):
        '''
            operador_soma : SOMA
                            | SUBR
        '''

        p[0] = Tree('operador_soma',[], str(p[1]))

    def p_operador_multiplicacao(self, p):
        '''
            operador_multiplicacao : VEZES
                                   | DIVIDE
        '''

        p[0] = Tree('operador_multiplicacao',[], str(p[1]))

    def p_fator(self, p):
        '''
            fator : ABREPAR expressao FECHAPAR
    	'''
        
        p[0] = Tree('fator', [p[2]])

    def p_fator1(self, p):
        '''
            fator : var
                  | chamada_funcao
                  | numero
        '''

        p[0] = Tree('fator1', [p[1]])

    def p_numero(self, p):
        '''
            numero : INTEIRO
                | FLUTUANTE
        '''
        p[0] = Tree('numero',[], p[1])

    def p_chamada_funcao(self, p):
        '''
            chamada_funcao : ID ABREPAR lista_argumentos FECHAPAR
        '''
    	
        p[0] = Tree('chamada_funcao',[p[3]],p[1])

    def p_lista_argumentos(self, p):
        '''
            lista_argumentos : lista_argumentos VIRGULA expressao
                             | expressao
        '''
        
        if len(p) == 4:
            p[0] = Tree('lista_argumentos', [p[1], p[3]])
        else:
            p[0] = Tree('lista_argumentos', [p[1]])

    def p_lista_argumentos1(self, p):
        '''
            lista_argumentos : vazio
        '''

        #p[0] = Tree('lista_argumentos1', [p[1]])

    def p_vazio(self, p):
        '''
            vazio :
        '''

    def p_error(self, p):
        if p:
            raise SyntaxError(" '%s', linha %d" % (p.value, p.lineno))
        else:
            raise SyntaxError(" definições incompletas!")
            exit(1)