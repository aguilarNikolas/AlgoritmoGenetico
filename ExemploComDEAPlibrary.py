# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 13:33:02 2020

@author: Nikolas N Aguilar
"""


import random
import matplotlib.pyplot as plt
import numpy
from deap import base
from deap import creator
from deap import tools
from deap import algorithms


class Produto():
    #atributos iniciais
        def __init__(self,nome,espaco,valor):
            self.nome = nome
            self.espaco = espaco
            self.valor = valor
            
            
lista_produtos = []           
lista_produtos.append(Produto("Geladeira Dako", 0.751, 999.90))
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
lista_produtos.append(Produto("Notebook Asus", 0.527, 3999.00))     


espacos = []
valores = [] 
nome = []

for produto in lista_produtos:
    espacos.append(produto.espaco)
    valores.append(produto.valor)
    nome.append(produto.nome)
    
    
#3 metros cubicos de volume maximo que cabe no caminhao    
limite = 3 


#inicializacao dos recursos da biblioteca
toolbox = base.Toolbox()
#Criando a funcao de avaliacao entre 0 e 1, proximo de 1 eh melhor
creator.create("FitnessMax", base.Fitness, weights=(1.0, ))
#Criando o individuo  list -> 0 e 1 do cromossomo
creator.create("Individual",list, fitness=creator.FitnessMax)
#registro de como o atributo list vai ser preenchido
toolbox.register("attr_bool", random.randint, 0, 1)
#registro dos individuos
toolbox.register("individual", tools.initRepeat, creator.Individual,   
                 toolbox.attr_bool, n=len(espacos))
#criacao da populacao
toolbox.register("population", tools.initRepeat, list, toolbox.individual)



def avaliacao(individual):
    nota = 0
    soma_espacos = 0
    for i in range(len(individual)):
        if individual[i] == 1:
            nota += valores[i]
            soma_espacos += espacos[i]
    if soma_espacos > limite:
        nota = 1

    return nota / 100000,

#resgistro das metricas
toolbox.register("evaluate", avaliacao)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", tools.mutFlipBit, indpb = 0.01)
toolbox.register("select", tools.selRoulette)




if __name__ == "__main__":
    

    # para inicilizar com a mesma semente aleatoria
    # random.seed(1)    
    populacao = toolbox.population(n = 20)
    probabilidade_crossover = 1.0
    probabilidade_mutacao = 0.01
    numero_geracoes = 100
    
    
    
    estatisticas = tools.Statistics(key = lambda individuo: individuo.fitness.values)
    estatisticas.register("max", numpy.max)
    estatisticas.register("min",numpy.min)
    estatisticas.register("med",numpy.mean)
    estatisticas.register("std", numpy.std)
    
    
    #chamando o algoritmo genetico, as estatisticas estao no INFO
    populacao, info = algorithms.eaSimple(populacao, toolbox, probabilidade_crossover, 
                                          probabilidade_mutacao, numero_geracoes,estatisticas)



    melhores = tools.selBest(populacao, 1)
    for individuo in melhores:
        print(individuo)
        print(individuo.fitness)
        # print(individuo)
        soma  = 0
        for i in range(len(lista_produtos)):
            if individuo[i] == 1:
                soma += valores[i]
                print("Nome : %s R$ %s" % (lista_produtos[i].nome,
                                           lista_produtos[i].valor))
        print("melhor solucao: %s" % soma)

    
    #puxando as estatisticas
    valores_grafico = info.select("max")
    #plotando
    plt.plot(valores_grafico)
    plt.title("acompanhamento dos valores")
    plt.show()
    
    






      