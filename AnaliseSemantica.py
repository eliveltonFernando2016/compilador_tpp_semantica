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
        self.check_main(self.simbolos)
        self.check_utilizadas(self.simbolos)
        self.check_functions(self.simbolos)

    def programa(self,node):
        self.lista_declaracoes(node.child[0], "global")

    def lista_declaracoes(self, node, scope):
        if node is not None:
            self.escopo = scope
            self.declaracao(node)

        if(node is not None and len(node.child) > 0):
            old_scope = scope
            if(len(node.child) > 1):
                if(node.type == "declaracao_funcao"):
                    scope = node.child[1].value
                self.lista_declaracoes(node.child[1], scope)

            self.lista_declaracoes(node.child[0], scope)
            scope = old_scope

    def declaracao(self,node):
        if(node is not None and len(node.child) >= 1):
            if(node.type == "declaracao_variaveis"):
                self.declaracao_variaveis(node)
            elif(node.type == "atribuicao"):
                self.inicializacao_variaveis(node)
            elif(node.type == "declaracao_funcao"):
                self.declaracao_funcao(node)
                self.escopo = "global"
            #else:
            #    print("[",node, node.type, node.value,"]")

    def declaracao_variaveis(self, node):
        if(len(node.child) >= 1):
            tipo = node.child[0].value
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
        self.atribuicao(node)

    def lista_variaveis(self, node):
        ret_args = []		

        if(len(node.child) == 1):
            if(len(node.child[0].child) == 1):
                ret_args.append(node.child[0].value + self.indice(node.child[0].child[0]))
            else:
                ret_args.append(node.child[0].value)
            return ret_args
        else:
            if(len(node.child) > 0):
                ret_args = self.lista_variaveis(node.child[0])

                if(len(node.child[1].child) == 1):
                    ret_args.append(node.child[1].value+self.indice(node.child[1].child[0]))
                else:
                    ret_args.append(node.child[1].value)
            return ret_args
    
    def declaracao_funcao(self, node):
        if(node is not None):
            if(len(node.child) == 1 and node.child[0] is not None):
                nome_funcao = node.child[0].value
                cabecalho = node.child[0]
                tipo = "void"
            elif(len(node.child) == 2):
                tipo = node.child[0].value

                nome_funcao = node.child[1].value
                cabecalho = node.child[1]

            if node.child[0] in self.simbolos.keys():
                print ("Erro: Função " + node.child[0].value + " já foi declarada.")
            elif "global-" + str(node.child[0]) in self.simbolos.keys():
                print ("Erro: Uso duplicado do nome '" + node.child[0].value  + "'")

            self.simbolos[nome_funcao] = ["funcao", nome_funcao, [], False, tipo, 0]
            self.cabecalho(cabecalho)

    def atribuicao(self, node):
        if(len(node.child) >= 1):
            nome = self.escopo + "-" + node.child[0].value

            if(nome not in self.simbolos.keys()):
                print ("Erro: A variável '" + node.child[0].value + "' não foi declarada.")
                return

            tipo_esperado  = self.simbolos[nome][4]
            tipo_recebido =  self.expressao(node.child[1])

            self.simbolos[nome][2]=True
            self.simbolos[nome][3]=True

            if(tipo_esperado != tipo_recebido):
                print ("Warning: Coerção implícita de tipos! Tipo esperado: " + tipo_esperado + ", tipo recebido: " + tipo_recebido +".")
            
        return

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
                print("Erro: index invalido, permitido somente inteiro")
            return ("[]"+variavel)

    def cabecalho(self,node):
        if(node is not None and len(node.child) >= 1):
            lista_par = self.lista_parametros(node.child[0])

            if(lista_par is not "void"):
                self.simbolos[node.value][2] = lista_par

        if(node is not None and len(node.child) >= 2):
            tipo_corpo = self.corpo(node.child[1])
            tipo_fun = self.simbolos[node.value][4]
        
            if tipo_corpo != tipo_fun:
                if(node.value == "principal"):
                    print("Warning: a função '"+str(node.value)+"' deveria retornar: '"+str(tipo_fun)+"' mas retorna '"+str(tipo_corpo)+"'")
                else:
                    print("Erro: a função '"+str(node.value)+"' deveria retornar: '"+str(tipo_fun)+"' mas retorna '"+str(tipo_corpo)+"'")

    def tipo(self,node):
        if(node is not None):
            if(node.value == "inteiro" or node.value == "flutuante"):
                return node.value

    def expressao(self, node):
        if(node.child[0].type ==  "expressao_simples"):
            return self.expressao_simples(node.child[0])   
        else:
            return self.atribuicao(node.child[0])

    def lista_parametros(self, node):
        lista_param = []

        if(node is not None):
            if(len(node.child) == 1):
                if(node.child[0] == None):
                    return self.vazio()
                else:
                    lista_param.append(self.parametro(node.child[0]))
            elif(len(node.child) == 2):
                lista_param = self.lista_parametros(node.child[0])
                lista_param.append(self.parametro(node.child[1]))
        
        return lista_param

    def corpo(self, node):
        if(node.child != None):
            if(len(node.child) == 1):
                return self.vazio()		
            else:
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

    def vazio(self):
        return "void"

    def parametro(self, node):
        if(node is not None and len(node.child) >= 1):
            if(node.child[0].type == "parametro"):
                return self.parametro(node.child[0]) + "[]"
            else:
                self.simbolos[self.escopo + "-" + node.value] = ["variavel", node.value, False, False, node.child[0].type, 0]
                return self.tipo(node.child[0])

    def acao(self, node):
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
        #elif(node.child[0].type == "error"):
            #return self.error(node.child[0])

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

    def se(self, node):
        tipo_se = self.expressao(node.child[0])
        if tipo_se != "logico":
            print("Erro: Era esperado uma expressão logica para a condição, foi dado uma expressão do tipo: " + tipo_se)

        if(len(node.child) == 2):
            return self.corpo(node.child[1])
        else:
            tipo_c1 = self.corpo(node.child[1])
            tipo_c2 = self.corpo(node.child[2])
            if tipo_c1 != tipo_c2:
                if(tipo_c1 == "void"):
                    return tipo_c2
                else:
                    return tipo_c1
            return tipo_c1

    def repita(self, node):
        tipo_se = self.expressao(node.child[1])
        if tipo_se != "logico":
            print("Erro: Espera-se uma expressão logica para o SE, foi dado: " + tipo_se)

        return self.corpo(node.child[0])

    def leia(self, node):
        if self.escopo + "-" + node.value not in self.simbolos.keys():
            if "global-" + node.value not in self.simbolos.keys():
                print("Erro: " + node.value + " não declarada")
        return "void"

    def escreva(self, node):
        tipo_exp = self.expressao(node.child[0])
		
        if tipo_exp == "logico":
            print("Erro: expressao inválida!")
		
        return "void"

    def retorna(self, node):
        tipo_exp = self.expressao(node.child[0])

        if(tipo_exp == "logico"):
            print("Erro: expressao inválida!")
        return tipo_exp

    def expressao_multiplicativa(self, node):
        if(len(node.child) == 1):
            return self.expressao_unaria(node.child[0])
        else:
            tipo1 = self.expressao_multiplicativa(node.child[0])
            self.operador_multiplicacao(node.child[1])
            tipo2 = self.expressao_unaria(node.child[2])
            if(tipo1 != tipo2):
                print("Warning: Operação com tipos diferentes '" + tipo1 + "' e '" + tipo2)
            if((tipo1 ==  "flutuante")or(tipo2 ==  "flutuante")):
                return "flutuante"
            else:
                return "inteiro"

    def operador_soma(self, node):
        return None

    def expressao_unaria(self, node):
        if(len(node.child) ==  1):
            return self.fator(node.child[0])
        else:
            self.operador_soma(node.child[0])
            return self.fator(node.child[1])

    def operador_multiplicacao(self, node):
        return None

    def fator(self, node):
        if(node.child[0].type ==  "var"):   
            return self.var(node.child[0])
        if(node.child[0].type ==  "chamada_funcao"):
            return self.chamada_funcao(node.child[0])
        if(node.child[0].type ==  "numero"):
            return self.numero(node.child[0])
        else:
            return self.expressao(node.child[0])

    def var(self,node):
        nome = self.escopo + "-" + node.value
        
        if(len(node.child) == 1):
            if(nome not in self.simbolos):
                nome = "global-" + node.value
                
                if(nome not in self.simbolos):
                    print("Erro: A váriavel '" + node.value + "' não foi declarada")

            if(self.simbolos[nome][3] == False):
                print("Erro: váriavel '" + nome + "' não foi inicializada")
            
            var = self.indice(node.child[0])			
            
            self.simbolos[nome][4] = self.simbolos[nome][4] + var
            self.simbolos[nome][2] = True
            
            return self.simbolos[nome][4]
        else:
            if(nome not in self.simbolos):
                print(self.simbolos[nome][2])
                nome = "global-" + node.value
                if(nome not in self.simbolos):
                    print("Erro: A váriavel '" + node.value + "' não foi declarada")

            if(self.simbolos[nome][3] == False):
                print("Erro: A váriavel '" + nome + "' não foi inicializada.")

            self.simbolos[nome][2] = True 
            
            return self.simbolos[nome][4]

    def chamada_funcao(self, node):
        if(node.value == "principal" and self.escopo == "principal"):
            print("Erro: Chamada recursiva para a função principal")
        
        if(node.value == "principal" and self.escopo != "principal"):
            print("Erro: A função '" + self.escopo + "' realiza uma chamada para a função principal.")
        
        if node.value not in self.simbolos.keys():
            print ("Erro: Função " + node.value + " não declarada")
            return
		
        self.simbolos[node.value][5] = 1
        argslista = []
        argslista.append(self.lista_argumentos(node.child[0]))
        
        if(argslista[0] == None):
            argslista=[]
        elif(not(type(argslista[0]) is str)):
            argslista = argslista[0]

        args_esperados = self.simbolos[node.value][2]
        if(type(args_esperados) is str):
            args_esperados = []		
        if(len(argslista) != len(args_esperados)):
            lesperados = (len(args_esperados))
            lrecebidos = (len(argslista))
            print("Erro: Numero de argumentos esperados em '" + node.value + "': " + str(lesperados) + ", quantidade de argumentos recebidos: " + str(lrecebidos))

        for i in range(len(argslista)):
            if(argslista[i] != args_esperados[i]):
                print("Erro: Argumento " + str(i) + ", tipo esperado " + args_esperados[i] + ", tipo recebido " +  argslista[i])
        
        self.simbolos[node.value][3]=True
        return self.simbolos[node.value][4]

    def numero(self, node):
        string = repr(node.value)
        if "."in string:
            return "flutuante"
        else:
            return "inteiro"

    def lista_argumentos(self, node):
        if(len(node.child) == 1):
            if(node.child[0] == None):
                return 
            if(node.child[0].type == "expressao"):
                return (self.expressao(node.child[0]))
            else:
                return []
        else:
            ret_args = []
            ret_args.append(self.lista_argumentos(node.child[0]))
            
            if(not(type(ret_args[0]) is str)):
                ret_args = ret_args[0]

            ret_args.append(self.expressao(node.child[1]))
            return ret_args

    def check_main(self, simbolos):
        if("principal" not in simbolos.keys()):
            print("Erro: função principal não declarada")

    def check_utilizadas(self, simbolos):
        for k,v in simbolos.items():
            if(v[0] == "variavel"):
                if(v[2] == False):
                    escopo=k.split("-")
                    
                    if(escopo[0]!= "global"):
                        print("Warning: Variavel '" + v[1] + "' da função '" + escopo[0] + "' nunca é utilizada")
                    else:
                        print("Warning: Variavel '" + v[1] + "' nunca é utilizada")

    def check_functions(self, simbolos):
        for key, value in simbolos.items():
            if(value[0] == "funcao" and key != "principal"):					
                if(value[5] != 1):
                    print("Warning: Função '" + key + "' nunca utilizada.")

if __name__ == '__main__':
	code = open(sys.argv[1])
	s = Semantica(code.read())
	pprint.pprint(s.simbolos, depth=3, width=300)