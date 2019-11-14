#!/usr/bin/python
# -*- coding: utf-8 -*-
# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from graphviz import Digraph
from sys import argv, exit
from Parser import Parser

class Imprimir():
	def __init__(self):
		self.j = 1
		
	def mostra_tree(self, node, strson, father, w, i):
		if node != None :
			i = i + 1
			father = str(node) + " " + str(i-1)+ " " + str(self.j-1)
			for son in node.child:
				strson = str(son) + " " + str(i) + " " + str(self.j)
				w.edge(father, strson)
				self.j = self.j + 1
				self.mostra_tree(son, strson, father, w, i)

#Imprime no terminal
def imprime_arvore(raiz, level="-"):
    if raiz != None and raiz.child != None:
        print(level + "Tipo: " + raiz.type + " Valor: " + raiz.value)
        for son in raiz.child:
            imprime_arvore(son, level + "-")

def printTreeText(node, w, i):
    if node != None and node.child != None:
        value1 = node.type + str(i)
        i += 1
        for son in node.child:
            w.edge(value1, str(son) + str(i))
            printTreeText(son, w, i)

if __name__ == '__main__':
    f = open(argv[1])

    '''a = Parser(f.read())
    imprime_arvore(a.ast)
    w = Digraph('G', filename='./Expressoes')
    printTreeText(a.ast, w, i=0)
    w.view()'''

    try:
        arvore = Parser(f.read())
        w = Digraph('G', filename='Saidas/Saida')
        tree = Imprimir().mostra_tree(arvore.ast,'','', w, i=0)

        w.view()

    except IOError:
        print("Erro: Arquivo não encontrado. Verifique se o nome ou diretório está correto.")