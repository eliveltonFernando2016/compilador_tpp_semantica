#!/usr/bin/python
# -*- coding: utf-8 -*-

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
        parser = yacc.yacc(debug=True, module=self, optimize=False)
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

    def p_declaracao(self, p):
        '''
        declaracao : declaracao_variaveis
        		   | inicializacao_variaveis
        		   | declaracao_funcao
        '''
        p[0] = Tree('declaracao', [p[1]])

    def p_declaracao_variaveis(self, p):
        'declaracao_variaveis : tipo DOISPONTOS lista_variaveis'
        p[0] = Tree('declaracao_variaveis', [p[1],p[3]])

    def p_inicializacao_variaveis(self, p):
    	'inicializacao_variaveis : atribuicao'
    	p[0] = Tree('inicializacao_variaveis', [p[1]])

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

    def p_cabecalho(self, p):
    	'''
        cabecalho : ID ABREPAR lista_parametros FECHAPAR corpo FIM
        '''
    	p[0] = Tree('cabecalho',[p[3],p[5]],p[1])

    def p_lista_parametros(self, p):
        '''
        lista_parametros : lista_parametros VIRGULA lista_parametros
        '''
        p[0] = Tree('lista_parametros',[p[1],p[3]])

    def p_lista_parametros1(self, p):
        '''
            lista_parametros : parametro
                                | vazio
        '''
        
        p[0] = Tree('lista_parametros',[p[1]])

    def p_parametro(self, p):
    	'''
        parametro : tipo DOISPONTOS ID
        '''
    	p[0] = Tree('parametro', [p[1]], p[3])

    def p_parametro1(self, p):
    	'''
            parametro : parametro ABRECOLCH FECHACOLCH
        '''
    	p[0] = Tree('parametro', [p[1]])

    def p_corpo(self, p):
        '''
            corpo : corpo acao
        '''
        
        p[0] = Tree('corpo',[p[1],p[2]])

    def p_corpo1(self, p):
        '''
            corpo : vazio
        '''

        p[0] = Tree('corpo', [p[1]])

    def p_acao(self ,p):
    	'''
        acao : expressao
             | declaracao_variaveis
             | se
             | repita
             | leia
             | escreva
             | retorna
             | error
    	''' 
    	p[0] = Tree('acao', [p[1]])

    def p_se(self, p):
        '''
            se : SE expressao ENTAO corpo FIM
        '''
        
        p[0] = Tree('se', [p[2],p[4]])

    def p_se1(self, p):
        '''
            se : SE expressao ENTAO corpo SENAO corpo FIM
        '''

        p[0] = Tree('se', [p[2], p[4], p[6]])

    def p_repita(self, p):
    	'''
            repita : REPITA corpo ATE expressao
        '''
    	p[0] = Tree('repita',[p[2],p[4]])

    def p_atribuicao(self, p):
    	'''
            atribuicao : var ATRIBUICAO expressao
        '''
    	p[0] = Tree('atribuicao',[p[1],p[3]])

    def p_leia(self, p):
    	'''
            leia : LEIA ABREPAR ID FECHAPAR
        '''
    	p[0] = Tree('leia',[],p[3])

    def p_escreva(self, p):
    	'''
            escreva : ESCREVA ABREPAR expressao FECHAPAR
        '''
    	p[0] = Tree('escreva',[p[3]])

    def p_retorna(self, p):
    	'''
            retorna : RETORNA ABREPAR expressao FECHAPAR
        '''
    	p[0] = Tree('retorna',[p[3]])

    def p_expressao(self, p):
    	'''
            expressao : expressao_simples
                    | atribuicao
    	'''
    	p[0] = Tree('expressao',[p[1]])

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

    def p_expressao_aditiva(self, p):
        '''
            expressao_aditiva : expressao_multiplicativa
        '''
        
        p[0] = Tree('expressao_aditiva',[p[1]])

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
            expressao_multiplicativa : expressao_multiplicativa operador_multiplicacao expressao_unaria
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
        '''
        
        p[0] = Tree('lista_argumentos',[p[1],p[3]])

    def p_lista_argumentos1(self, p):
        '''
            lista_argumentos : expressao
                             | vazio
        '''

        p[0] = Tree('lista_argumentos1', [p[1]])

    def p_vazio(self, p):
        '''
            vazio :
        '''

    def p_error(self, p):
        if p is None:
            print("Sintax Error")
            exit(1)
        else:
            print("Erro sintático: '%s', linha %d" % (p.value, p.lineno))
