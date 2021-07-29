# Curso Algoritmos geneticos em python (Udemy)
"""
Created on Thu Apr  9 12:15:56 2020

Nikolas N Aguilar
"""
from random import random
import matplotlib.pyplot as plt
import pymysql



# criacao da classe de produto
class Produto():
    #atributos iniciais
        def __init__(self,nome,espaco,valor):
            self.nome = nome
            self.espaco = espaco
            self.valor = valor
            
#  criacao da classe individuo
class Individuo():
    #atributos iniciais
    def __init__(self,espacos,valores, limite_espacos, geracao=0):
        self.espacos = espacos
        self.valores = valores
        self.limite_espacos = limite_espacos
        self.nota_avaliacao = 0
        self.espaco_ussado = 0
        self.geracao = geracao
        self.cromossomo = []
        for i in range (len(espacos)):  
            if random() < 0.5:
                self.cromossomo.append("0")
            else:
                self.cromossomo.append("1")
    # funcao de avaliacao do individuo            
    def avaliacao(self):
        nota = 0
        soma_espacos = 0
        for i in range(len(self.cromossomo)):
            if self.cromossomo[i] == '1':
                nota += self.valores[i]
                soma_espacos += self.espacos[i]
                
        if soma_espacos > self.limite_espacos:    
             nota = 1
        
        # atribuicao da nota-> valor em R$
        self.nota_avaliacao = nota
        
        #atribuicao do volume ocupado
        self.espaco_usado = soma_espacos
          
    # funcao de reproducao, combinacao de dois individuos
    def crossover(self,outro_individuo):    
        corte = round(random() * len(self.cromossomo))
        
        #criacao dos filhos de acordo com os cortes dos cromossomos
        filho1 = outro_individuo.cromossomo[0:corte] + self.cromossomo[corte::]
        filho2 = self.cromossomo[0:corte] + outro_individuo.cromossomo[corte::]
        
        filhos = [Individuo(self.espacos, self.valores, self.limite_espacos, self.geracao+1),
                  Individuo(self.espacos, self.valores, self.limite_espacos,self.geracao+1)]
        
        filhos[0].cromossomo = filho1
        filhos[1].cromossomo = filho2
        return filhos
        
        
     # funcao de mutacao dos genes, inversão de bits (mutacao binaria)
    def mutacao(self,taxa_mutacao):
        # print("antes %s " % self.cromossomo)
        for i in range(len(self.cromossomo)):
            if random() < taxa_mutacao:   
                if self.cromossomo[i] == '1':
                    self.cromossomo[i] = '0'
                else:
                    self.cromossomo[i] = '1'
         
        # print("Depois %s " % self.cromossomo)    
        return self    
            
            

class AlgoritmoGenetico():
    #atributos iniciais
    def __init__(self, tamanho_populacao):
        self.tamanho_populacao = tamanho_populacao
        self.populacao = []
        self.geracao = 0
        self.melhor_solucao = 0
        self.lista_solucoes = []
        
    def inicializa_populacao(self, espacos, valores, limite_espacos):
        for i in range(self.tamanho_populacao):
            self.populacao.append(Individuo(espacos, valores, limite_espacos))
        self.melhor_solucao = self.populacao[0]        


    def ordena_populacao(self):
        self.populacao = sorted(self.populacao,
                                key = lambda populacao: populacao.nota_avaliacao,
                                reverse = True)

    def melhor_individuo(self, individuo):
        #atualiza o melhor individuo
        if individuo.nota_avaliacao > self.melhor_solucao.nota_avaliacao:
            self.melhor_solucao = individuo
         
        
    def soma_avaliacoes(self):    
        soma = 0
        for individuo in self.populacao:
            soma += individuo.nota_avaliacao
        return soma
    
    
    def seleciona_pai(self, soma_avaliacao):
        #seleciona o indice do pai
        pai = -1
        valor_sorteado = random()* soma_avaliacao
        soma = 0
        i = 0
        while i< len(self.populacao) and soma < valor_sorteado:
            soma += self.populacao[i].nota_avaliacao
            pai += 1
            i += 1
        return pai    
  
    
    def visualiza_geracao(self):
        melhor = self.populacao[0]
        print("G: %s  > valor: %s  Espaco: %s  Cromossomo: %s" % (self.populacao[0].geracao,
                                                                  melhor.nota_avaliacao,
                                                                  melhor.espaco_usado,
                                                                  melhor.cromossomo))
    
    
    def resolver(self, taxa_mutacao, numero_geracoes, espacos, valores, limite_espacos):
        self.inicializa_populacao(espacos,valores,limite_espacos)
        
        for individuo in self.populacao:
            individuo.avaliacao()
            
        self.ordena_populacao()
        #é usado o index 0 pois a populacao ja foi ordenada
        self.melhor_solucao = self.populacao[0]
        self.lista_solucoes.append(self.melhor_solucao.nota_avaliacao)
        
        self.visualiza_geracao()
        
        for geracao in range(numero_geracoes):
            soma_avaliacao = self.soma_avaliacoes()
            nova_populacao = []
            
            for individuos_gerados in range(0, self.tamanho_populacao, 2):
                pai1 = self.seleciona_pai(soma_avaliacao)
                pai2 = self.seleciona_pai(soma_avaliacao)
                
                filhos = self.populacao[pai1].crossover(self.populacao[pai2])
                
                nova_populacao.append(filhos[0].mutacao(taxa_mutacao))
                nova_populacao.append(filhos[1].mutacao(taxa_mutacao))
    
    
            self.populacao = list(nova_populacao)
            
            for individuo in self.populacao:
                individuo.avaliacao()
                
            self.ordena_populacao()
            
            self.visualiza_geracao()
            
            melhor = self.populacao[0]
            self.lista_solucoes.append(melhor.nota_avaliacao)
            
            self.melhor_individuo(melhor)
            
        print("\n Melhor solucao -> G: %s Valor: %s Espaco: %s Cromossomo: %s" %
              (self.melhor_solucao.geracao,self.melhor_solucao.nota_avaliacao,
               self.melhor_solucao.espaco_usado, self.melhor_solucao.cromossomo))
    
    
        return self.melhor_solucao.cromossomo
    
    
    
    
            
if __name__ == '__main__':   


       
#    p1 = Produto("Iphone6", 0.0000899, 2199.12)
    lista_produtos = []
    
    #estabelece a conexao com o SQL, 'localhost' eh a minha propria maquina
    conexao = pymysql.connect(host='localhost', user='root', passwd='*********', db='produtos')
    cursor = conexao.cursor()
    # vai trazer um vetor com os parametros nos indices indicados [0]-> nome
    cursor.execute('select nome, espaco, valor, quantidade from produtos')
    for produto in cursor:
        # print (produto[0])
        for i in range(produto[3]):
            lista_produtos.append(Produto(produto[0], produto[1], produto[2]))
    
    #para liberar memoria
    cursor.close()
    conexao.close()
    
    
    # a lista de produtos ser construida no MySQL
    '''lista_produtos.append(Produto("Geladeira Dako", 0.751, 999.90))
    lista_produtos.append(Produto("Iphone 6", 0.0000899, 2911.12))
    lista_produtos.append(Produto("TV 55' ", 0.400, 4346.99))
    lista_produtos.append(Produto("TV 50' ", 0.290, 3999.90))
    lista_produtos.append(Produto("TV 42' ", 0.200, 2999.00))
    lista_produtos.append(Produto("Notebook Dell", 0.00350, 2499.90))
    lista_produtos.append(Produto("Ventilador Panasonic", 0.496, 199.90))
    lista_produtos.append(Produto("Microondas Electrolux", 0.0424, 308.66))
    lista_produtos.append(Produto("Microondas LG", 0.0544, 429.90))
    lista_produtos.append(Produto("Microondas Panasonic", 0.0319, 299.29))
    lista_produtos.append(Produto("Geladeira Brastemp", 0.635, 849.00))
    lista_produtos.append(Produto("Geladeira Consul", 0.870, 1199.89))
    lista_produtos.append(Produto("Notebook Lenovo", 0.498, 1999.90))
    lista_produtos.append(Produto("Notebook Asus", 0.527, 3999.00))'''
    
    
#    for produto in lista_produtos:
#        print(produto.nome) 
    
    espacos = []
    valores = [] 
    nome = []
    
    for produto in lista_produtos:
        espacos.append(produto.espaco)
        valores.append(produto.valor)
        nome.append(produto.nome)
        
    
    # individuo1 = Individuo(espacos,valores,limite)  
    # print("\nIndividuo1")
    # for i in range(len(lista_produtos)):
    #     if individuo1.cromossomo[i] == '1':
    #         print("Nome: %s R$ %s" % (lista_produtos[i].nome, lista_produtos[i].valor))
    # individuo1.avaliacao()
    # print("Nota = %s" % individuo1.nota_avaliacao)
    # print("espaco usado %s" % individuo1.espaco_usado)        
        
    
    
    
    # individuo2 = Individuo(espacos,valores,limite)  
    # print("\nIndividuo2")
    # for i in range(len(lista_produtos)):
    #     if individuo2.cromossomo[i] == '1':
    #         print("Nome: %s R$ %s" % (lista_produtos[i].nome, lista_produtos[i].valor))
    # individuo2.avaliacao()
    # print("Nota = %s" % individuo2.nota_avaliacao)
    # print("espaco usado %s" % individuo2.espaco_usado)      
        
                
    # individuo1.crossover(individuo2)
        
    # individuo1.mutacao(0.05)
    # individuo2.mutacao(0.05)
        
    #3 metros cubicos de volume maximo que cabe no caminhao    
    limite = 10  
    #populacao de 20 individuos          
    tamanho_populacao = 40
    #1 % de chance de ocorrer mutacao
    taxa_mutacao = 0.01
    #numero de geracoes que serao avaliadas
    numero_geracoes = 100
    ag = AlgoritmoGenetico(tamanho_populacao)
    
    #chama o metodo RESOLVER que fica basicamente iterando o algoritmo
    resultado = ag.resolver(taxa_mutacao,numero_geracoes,espacos,valores,limite)
    
    for i in range(len(lista_produtos)):
        # se o produto estiver contido (1 == True) ele aparece
        if resultado[i] == "1":
            print("Nome %s  R$ %s " % (lista_produtos[i].nome,
                                       lista_produtos[i].valor))
    
    #plotar os melhores valores obtidos na evolucao do algoritmo
    # for valor in ag.lista_solucoes:
    #     print(valor)
    
    plt.plot(ag.lista_solucoes)
    plt.title("acompanhamento dos valores")
    plt.show()
    

    
 #codigo debug para criacao do algoritmo genetico
    
    # ag.inicializa_populacao(espacos, valores, limite)
    # for individuo in ag.populacao:
    #     individuo.avaliacao()
    # ag.ordena_populacao()
    # ag.melhor_individuo(ag.populacao[0])
    # soma = ag.soma_avaliacoes()
    # # print("Soma das avaliacoes:  %s \n" % soma)
    
    # # print("melhor solucao para o problema: %s" % ag.melhor_solucao.cromossomo,
    # #       "Nota = %s \n " % ag.melhor_solucao.nota_avaliacao)
    
    # # for i in range(ag.tamanho_populacao):
    # #     print("*** Individuo %s ****\n" % i,
    # #           "Espacos = %s \n" % str(ag.populacao[i].espacos),
    # #           "Valores = %s \n" % str(ag.populacao[i].valores),
    # #           "Cromossomo %s \n " % str(ag.populacao[i].cromossomo),
    # #           "Nota = %s\n " % ag.populacao[i].nota_avaliacao)
        
    # nova_populacao = []
    
    
    # probabilidade_mutacao = 0.01
    
    # for individuos_gerados in range(0, ag.tamanho_populacao,2):
    #     pai1 = ag.seleciona_pai(soma)
    #     pai2 = ag.seleciona_pai(soma)
        
    #     filhos = ag.populacao[pai1].crossover(ag.populacao[pai2])
        
    #     #adicionando os novos filhos a nova populacao
    #     nova_populacao.append(filhos[0].mutacao(probabilidade_mutacao))
    #     nova_populacao.append(filhos[1].mutacao(probabilidade_mutacao))
        
        
    # ag.populacao = list(nova_populacao)
    # for individuo in ag.populacao:
    #     individuo.avaliacao()
        
    # ag.ordena_populacao()
    # ag.melhor_individuo(ag.populacao[0])
    # soma = ag.soma_avaliacoes()

    # print("melhor : %s" % ag.melhor_solucao.cromossomo, "valor %s\n" % ag.melhor_solucao.nota_avaliacao)        
        
      






