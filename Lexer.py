# -*- coding: utf-8 -*-

import ply.lex as lex
import sys

class Lexer:
	def __init__(self):
		self.lexer = lex.lex(debug=False, module=self, optimize=False)

	#palavras reservadas
	keywords = {
		'repita'    : 'REPITA',
		'fim'       : 'FIM',
		'se'        : 'SE',
		'então'     : 'ENTAO',
		'senão'     : 'SENAO',
		'flutuante' : 'FLUTUANTE',
		'retorna'   : 'RETORNA',
		'até'       : 'ATE',
		'leia'      : 'LEIA',
		'escreva'   : 'ESCREVA',
		'inteiro'   : 'INTEIRO',
	}

	tokens = [
		'ID',
		'VIRGULA',
		'ATRIBUICAO',
		'SOMA',
		'SUBR',
		'VEZES',
		'DIVIDE',
		'IGUAL',
		'MENOR',
		'MAIOR',
		'MENORIGUAL',
		'MAIORIGUAL',
		'ELOGICO',
		'OULOGICO',
		'NEGACAO',
		'DIFERENTE',
		'ABREPAR',
		'FECHAPAR',
		'DOISPONTOS',
		'ABRECOLCH',
		'FECHACOLCH'] + list(keywords.values())

	t_SOMA       = r'\+'
	t_SUBR       = r'\-'
	t_VEZES      = r'\*'
	t_DIVIDE     = r'\/'
	t_IGUAL      = r'\='
	t_VIRGULA    = r'\,'
	t_ATRIBUICAO = r'\:\='
	t_MENOR      = r'\<'
	t_MAIOR      = r'\>'
	t_MENORIGUAL = r'\<\='
	t_MAIORIGUAL = r'\>\='
	t_ABREPAR    = r'\('
	t_FECHAPAR   = r'\)'
	t_DOISPONTOS = r'\:'
	t_ABRECOLCH  = r'\['
	t_FECHACOLCH = r'\]'
	t_ELOGICO    = r'\&\&'
	t_OULOGICO   = r'\|\|'
	t_DIFERENTE  = r'\!\='
	t_INTEIRO    = r'[0-9]+'
	t_FLUTUANTE  = r'[0-9]+[\.][0-9]*' 
                
	def t_ID(self, t):
		r'[a-zA-Zá-ñÁ-Ñà-źÀ-Ź][a-zA-Zá-ñÁ-Ñà-źÀ-Ź0-9_à-ú]*'
		t.type = self.keywords.get(t.value, 'ID')
		return t

	def t_COMMENT(self, t):
		r'\{[\s]*[^}]*[\s]*[^{]*\}'
		for x in range(0, len(t.value)):
			if t.value[x] == '\n':
				t.lexer.lineno += 1

	def t_NEWLINE(self, t):
		r'\n+'
		t.lexer.lineno += len(t.value)

	t_ignore = ' \t'

	def t_error(self, t):
		if t.value[0] == '{':
			print("Comentario incompleto")
		
		if t.value[0] == '}':
			print("Comentario não inicializado")

		print("Character illegal: "+ t.value[0])

		t.lexer.skip(1)
		#return None

	def test(self, code):
		lex.input(code)
		while True:
			t = lex.token()
			if not t:
				break
			print(f'Tipo: {t.type:10} Valor: {t.value:14} Linha: {t.lineno:<3} Posicao: {t.lexpos}')