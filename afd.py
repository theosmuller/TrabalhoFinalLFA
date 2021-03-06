from graphviz import Digraph
from glud import GludDefinition, Production
from pyparsing import empty
from asyncio.format_helpers import _format_callback_source
from audioop import tostereo
from os import stat
from pickle import TRUE
from typing import List, NamedTuple, Dict
import re
import os


class FA():
    def __init__(self, stateCount, states, alphabetCount, alphabet, initialState,
                 finalState, transitionCount, transitions):
        self.stateCount = stateCount
        self.states = states
        self.alphabetCount = alphabetCount
        self.alphabet = alphabet

        self.alphabet.append('λ')
        self.alphabetCount += 1
        self.initialState = initialState
        self.finalState = finalState
        self.transitionCount = transitionCount
        self.transitions = transitions
        self.graph = Digraph()
        self.states_dict = dict()
        for i in range(self.stateCount):
            self.states_dict[self.states[i]] = i
        self.alphabet_dict = dict()
        for i in range(self.alphabetCount):
            self.alphabet_dict[self.alphabet[i]] = i

        self.transition_table = dict()
        for i in range(self.stateCount):
            for j in range(self.alphabetCount):
                self.transition_table[str(i)+str(j)] = []
        for i in range(self.transitionCount):
            self.transition_table[str(self.states_dict[self.transitions[i][0]])
                                  + str(self.alphabet_dict[
                                      self.transitions[i][1]])].append(
                                          self.states_dict[self.transitions[i][2]])

    @classmethod
    def isFinalAFD(self, stateList):
        for x in stateList:
            if (x == 'q'):
                return True
        return False

    def getStateName(self, stateList):
        name = ''
        for x in stateList:
            name += self.states[x]
        return name

    def empty_closure(self, state):
        emptyClosure = dict()
        emptyClosure[self.states_dict[state]] = 0
        emptyClosureStack = [self.states_dict[state]]

        while(len(emptyClosureStack) > 0):
            current = emptyClosureStack.pop(0)
            for transition in self.transition_table[str(current)+str(self.alphabet_dict['λ'])]:
                if transition not in emptyClosure.keys():
                    emptyClosure[transition] = 0
                    emptyClosureStack.append(transition)
            emptyClosure[current] = 1
        return emptyClosure.keys()


def afd_from_glud(glud):
    afne = afne_from_glud(glud)
    return afne_to_afd(afne)


def afne_plus_graph(glud):
    afne = afne_from_glud(glud)
    return show_afne_graph(afne)


def afne_from_glud(glud):
    glud.gludDefinition.variables.append("qf")
    return FA(
        finalState='qf',
        states=glud.gludDefinition.variables,
        stateCount=len(glud.gludDefinition.variables),
        alphabet=glud.gludDefinition.terminals,
        alphabetCount=len(glud.gludDefinition.terminals),
        initialState=glud.gludDefinition.initialSymbol,
        transitions=get_program_function_from_productions(glud.productions),
        transitionCount=len(
            get_program_function_from_productions(glud.productions))
    )


def get_program_function_from_productions(productions):
    listOfDelta = []
    for production in productions:
        listOfDelta.append(production_to_delta(production))
    return listOfDelta


def production_to_delta(production):
    if stateIsFinal(production.output[1]):
        return[production.input, production.output[0], 'qf']
    return [production.input, production.output[0], production.output[1]]


def stateIsFinal(outputState):
    if (outputState == "λ"):
        return True
    return False


# recebe:
# lista de estados (vai ser chamado com o estado inicial do AFV)
# função programa (todas as transições do AFV)
# alfabeto (simbolos)
#
# faz:
# fazer o fecho fazio do estado
# para cada simbolo do alfabeto :
# encontrar as transições desse fecho vazio
# se não tem transições adiciona à lista de transições do AFD esse fecho vazio indo para o novo qf
# se tem, faz tudo isso pro novo conjunto de estados atingidos por essas transições
# adiciona à lista essa transição
# quando n tem transições retorna a lista do afd

def afd_convert_and_graph(afne):

    ec_program_function = dict()

    afdGraph = Digraph()

    # faz o fecho vazio de todos os estados para não ter que refazer durante a construçõa do afd
    for state in afne.states:
        ec_program_function[state] = list(afne.empty_closure(state))

    afdStack = list()
    afdStack.append(ec_program_function[afne.initialState])

    # Adiciona o estado inicial ao grafo com uma seta vazia para indicar que é inicial
    afdGraph.attr('node', shape='circle')
    afdGraph.node(afne.getStateName(afdStack[0]))
    afdGraph.attr('node', shape='none')
    afdGraph.node('')
    afdGraph.edge('', afne.getStateName(afdStack[0]))

    afdStates = list()
    afdStates.append(ec_program_function[afne.initialState])

    while (len(afdStack) > 0):
        currentState = afdStack.pop(0)

        for symbol in range((afne.alphabetCount)-1):
            fromClosure = set()
            for x in currentState:
                fromClosure.update(
                    set(afne.transition_table[str(x)+str(symbol)]))

            if (len(fromClosure) > 0):
                toState = set()
                for x in list(fromClosure):
                    toState.update(set(ec_program_function[afne.states[x]]))

                if list(toState) not in afdStates:
                    afdStack.append(list(toState))
                    afdStates.append(list(toState))

                    isFinal = (afne.getStateName(list(toState)))
                    if (afne.isFinalAFD(isFinal)):
                        afdGraph.attr('node', shape='doublecircle')
                    else:
                        afdGraph.attr('node', shape='circle')
                    afdGraph.node(afne.getStateName(list(toState)))

                afdGraph.edge(afne.getStateName(currentState),
                              afne.getStateName(list(toState)),
                              label=afne.alphabet[symbol])
            else:
                if (-1) not in afdStates:
                    afdGraph.attr('node', shape='circle')
                    afdGraph.node('ϕ')

                    # For new dead state, add all transitions to itself,
                    # so that machine cannot leave the dead state
                    for symbol2 in range(afne.alphabetCount - 1):
                        afdGraph.edge('ϕ', 'ϕ', afne.alphabet[symbol2])

                    # Adding -1 to list to mark that dead state is present
                    afdStates.append(-1)

                # Adding transition to dead state
                afdGraph.edge(afne.getStateName(currentState,),
                              'ϕ', label=afne.alphabet[symbol])
    afdGraph.render('AFD', view=True)


def show_afne_graph(afne):
    afne.graph = Digraph()

    # Adding states/nodes in afne diagram
    for x in afne.states:
        # If state is not a final state, then border shape is single circle
        # Else it is double circle
        if (x != afne.finalState):
            afne.graph.attr('node', shape='circle')
            afne.graph.node(x)
        else:
            afne.graph.attr('node', shape='doublecircle')
            afne.graph.node(x)

    # Adding start state arrow in afne diagram
    afne.graph.attr('node', shape='none')
    afne.graph.node('')
    afne.graph.edge('', afne.initialState)

    # Adding edge between states in afne from the transitions array
    for x in afne.transitions:
        afne.graph.edge(x[0], x[2], label=('ε', x[1])[x[1] != 'λ'])

    # Makes a pdf with name afne.graph.pdf and views the pdf
    afne.graph.render('AFNE', view=True)


# cria primeiro a função programa do afd
# depois acrescenta as transições faltantes
# para tratar todos os simbolos do alfabeto
def afne_to_afd(afne):
    afd_convert_and_graph(afne)
