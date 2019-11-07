#!/usr/bin/python
# -*- coding: utf-8 -*-
# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from graphviz import Digraph
from sys import argv, exit
from Parser import Parser

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
    a = Parser(f.read())
    imprime_arvore(a.ast)
    w = Digraph('G', filename='./Expressoes')
    printTreeText(a.ast, w, i=0)
    w.view()