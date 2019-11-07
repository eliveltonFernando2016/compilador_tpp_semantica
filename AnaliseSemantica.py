import pprint
import sys
from   Parser import Parser
from   ply    import yacc

class Semantica():
    def __init__(self, code):
        self.simbolos = {}
        self.escopo = "global"
        self.tree = Parser(code).ast

        self.programa(self.tree)
        #self.check_main(self.simbolos)
        #self.check_utilizadas(self.simbolos)
        #self.check_functions(self.simbolos)
    
    def programa(self,node):
        self.lista_declaracoes(node.child[0])

    def lista_declaracoes(self, node):
        if(len(node.child) == 1):
            self.declaracao(node.child[0])
        else:
            self.lista_declaracoes(node.child[0])
            self.declaracao(node.child[1])

    def declaracao(self,node):
        if(node.child[0].type == "declaracao_variaveis"):
            self.declaracao_variaveis(node.child[0])
        elif(node.child[0].type == "inicializacao_variaveis"):
            self.inicializacao_variaveis(node.child[0])
        else:
            if(len(node.child[0].child) == 1):
                self.escopo = node.child[0].child[0].value
            else:
                self.escopo = node.child[0].child[1].value

            self.declaracao_funcao(node.child[0])
            self.escopo = "global"

    def declaracao_variaveis(self, node):
        tipo = node.child[0].type
        arr_name = ""

        for son in self.lista_variaveis(node.child[1]):
            if("[" in son):
                arr_name = son.split('[')[0]
                son = arr_name
            if(self.escopo + '-' + son in self.simbolos.keys()):
                print("Erro: A variável '" + son + "' já foi declarada anteriormente.")
            if("global-" + son in self.simbolos.keys()):
                print("Erro: A variável '" + son + "' já foi declarada anteriormente.")
            if(son in self.simbolos.keys()):
                print("Erro: Já existe uma função com o nome '" + son + "'")
            self.simbolos[self.escopo + "-" + son] = ["variavel", son, False, False, tipo, 0]
        return "void"

    def inicializacao_variaveis(self,node):
        self.atribuicao(node.child[0])

    def lista_variaveis(self, node):
        ret_args = []		

        if(len(node.child) == 1):
            if(len(node.child[0].child) == 1):
                ret_args.append(node.child[0].value + self.indice(node.child[0].child[0]))
            else:
                ret_args.append(node.child[0].value)
            return ret_args
        else:
            ret_args = self.lista_variaveis(node.child[0])
            if(len(node.child[1].child) == 1):
                ret_args.append(node.child[1].value+self.indice(node.child[1].child[0]))
            else:
                ret_args.append(node.child[1].value)
            return ret_args
    
    def declaracao_funcao(self, node):
        if(len(node.child) == 1):
            tipo = "void"
            if node.child[0].value in self.simbolos.keys():
                print ("Erro: Função " + node.child[0].value + " já foi declarada.")
            elif "global-" + node.child[0].value in self.simbolos.keys():
                print ("Erro: Uso duplicado do nome '" + node.child[0].value  + "'")
            self.simbolos[node.child[0].value] = ["funcao", node.child[0].value, [], False, tipo, 0]	
            self.cabecalho(node.child[0])
        else:
            tipo = self.tipo(node.child[0])
            self.simbolos[node.child[1].value] = ["funcao", node.child[1].value, [], False, tipo, 0]
            self.cabecalho(node.child[1])

    def atribuicao(self, node):
        nome = self.escopo + "-" + node.child[0].value
        if(self.escopo + "-" + node.child[0].value not in self.simbolos.keys()):
            nome = "global" + "-" + node.child[0].value
            if("global" + "-" + node.child[0].value not in self.simbolos.keys()):
                print ("Erro: A variável '" + node.child[0].value + "' não foi declarada.")
        tipo_esperado  = self.simbolos[nome][4]
        tipo_recebido =  self.expressao(node.child[1])
        self.simbolos[nome][2]=True
        self.simbolos[nome][3]=True
        if(tipo_esperado != tipo_recebido):
            print ("Warning: Coerção implícita de tipos! Tipo esperado: " + tipo_esperado + ", tipo recebido: " + tipo_recebido +".")
        return "void"

    def indice(self, node):
        if(len(node.child) == 1):
            tipo = self.expressao(node.child[0])
            if(node.child[0].value == "" or tipo != "inteiro"):
                print("Erro: index invalido, permitido somente inteiro")
            return("[]")
        else:
            variavel=self.indice(node.child[0])
            tipo=self.expressao(node.child[1])
            if(tipo != "inteiro"):
                print("Erro: index invalido, permitido sómente inteiro")
            return ("[]"+variavel)

    def cabecalho(self,node):
        lista_par = self.lista_parametros(node.child[0])

        self.simbolos[node.value][2] = lista_par
        tipo_corpo = self.corpo(node.child[1])
        tipo_fun = self.simbolos[node.value][4]
        if tipo_corpo != tipo_fun:
            if(node.value == "principal"):
                print("Warning: a função '"+node.value+"' deveria retornar: '"+tipo_fun+"' mas retorna '"+tipo_corpo+"'")
            else:	
                print("Erro: a função '"+node.value+"' deveria retornar: '"+tipo_fun+"' mas retorna '"+tipo_corpo+"'")

    def tipo(self,node):
        if(node.type == "inteiro" or node.type == "flutuante"):
            return node.type
        else:
            print("Erro: Somente tipos inteiros e flutuantes são aceitos. Tipo entrado: " + node.type)

    def expressao(self, node):
        if(node.child[0].type ==  "expressao_simples"):
            return self.expressao_simples(node.child[0])   
        else:
            return self.atribuicao(node.child[0])

    def lista_parametros(self, node):
        lista_param = []
        if(len(node.child) == 1):
            if(node.child[0] == None):
                return self.vazio(node.child[0])
            else:
                lista_param.append(self.parametro(node.child[0]))
                return lista_param
        else:
            lista_param = self.lista_parametros(node.child[0])
            lista_param.append(self.parametro(node.child[1]))
            return lista_param

    def corpo(self, node):
        if(node.child != None):
            if(len(node.child) == 1):
                return self.vazio(node.child[0])		
            else:
                #tipo1c = self.corpo(node.child[0])
                tipo2c = self.acao(node.child[1])
                if(tipo2c != None):
                    return tipo2c

    def expressao_simples(self, node):     
        if len(node.child) ==  1:
            return self.expressao_aditiva(node.child[0])   
        else:
            tipo1 = self.expressao_simples(node.child[0])
            self.operador_relacional(node.child[1])
            tipo2 = self.expressao_aditiva(node.child[2])
            if(tipo1 != tipo2):
                print("Warning: Operação com tipos diferentes '" + tipo1 + "' e '" + tipo2)
            return "logico"

    def vazio(self, node):
        return "void"

    def parametro(self, node):
        if(node.child[0].type == "parametro"):
            return self.parametro(node.child[0]) + "[]"
        else:
            self.simbolos[self.escopo + "-" + node.value] = ["variavel", node.value, False, False, node.child[0].type, 0]
            return self.tipo(node.child[0])

    def acao(self, node):
        #tipo_ret_acao = "void"
        if(node.child[0].type == "expressao"):
            return self.expressao(node.child[0])
        elif(node.child[0].type == "declaracao_variaveis"):
            return self.declaracao_variaveis(node.child[0])
        elif(node.child[0].type == "se"):
            return self.se(node.child[0])
        elif(node.child[0].type == "repita"):
            return self.repita(node.child[0])
        elif(node.child[0].type == "leia"):
            return self.leia(node.child[0])
        elif(node.child[0].type == "escreva"):
            return self.escreva(node.child[0])
        elif(node.child[0].type=="retorna"):
            return self.retorna(node.child[0])
        elif(node.child[0].type == "error"):
            return self.error(node.child[0])

    def expressao_aditiva(self, node):
        if(len(node.child) ==  1):
            return self.expressao_multiplicativa(node.child[0])
        else:
            tipo1 = self.expressao_aditiva(node.child[0])
            self.operador_soma(node.child[1])
            tipo2 = self.expressao_multiplicativa(node.child[2])

            if(tipo1 != tipo2):
                print("Warning: Operação com tipos diferentes '" + tipo1 + "' e '" + tipo2)
            if((tipo1 ==  "flutuante") or (tipo2 ==  "flutuante")):
                return "flutuante"
            else:
                return "inteiro"

    def operador_relacional(self, node):
        return None

if __name__ == '__main__':
	code = open(sys.argv[1])
	s = Semantica(code.read())
	#print_tree(s.tree)
	#pprint.pprint(s.simbolos, depth=3, width=300)