from asyncio.format_helpers import _format_callback_source
from audioop import tostereo
from os import stat
from pickle import TRUE
from typing import List, NamedTuple, Dict
import re
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'

from pyparsing import empty
from glud import GludDefinition, Production
from graphviz import Digraph



class FA():
    def __init__(self, stateCount, states, alphabetCount, alphabet, initialState,
                 transitionCount, transitions):
        self.stateCount = stateCount
        self.states = states
        self.alphabetCount = alphabetCount
        self.alphabet = alphabet
         
        self.alphabet.append('λ')
        self.alphabetCount += 1
        self.initialState = initialState
        self.finalState = ('qf')
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
            if (x == 'qf'):
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

        while(len(emptyClosureStack)>0):
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
    


def afne_from_glud(glud):
    glud.gludDefinition.variables.append("qf")
    return FA(
        states = glud.gludDefinition.variables,
        stateCount = len(glud.gludDefinition.variables),
        alphabet = glud.gludDefinition.terminals,
        alphabetCount = len(glud.gludDefinition.terminals),
        initialState = glud.gludDefinition.initialSymbol,
        transitions = get_program_function_from_productions(glud.productions),
        transitionCount = len(get_program_function_from_productions(glud.productions))
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


'''
def clean_afd(afnInitialState, transitions, alphabet):
    states = []
    states.append("qf")
    for transition in transitions:
        if transition.output == afnInitialState:
            transitions = list(filter(lambda val: val != transition, transitions))
        if transition.input.currentState not in states:
            states.append(transition.input.currentState)
    for state in states:
        for symbol in alphabet:
            if not any(transition.input.inputSymbol == symbol and transition.input.currentState == state for transition in transitions):
                transitions.append(
                    Delta(
                        input =  DeltaInput(
                            currentState = state,
                            inputSymbol = symbol
                        ),
                        output = state
                    )
                )
    cleanTransitions = set()
    cleanTransitions.update(transitions)
    return FA(
        states = states,
        inputSymbols = alphabet,
        programFunction = sorted(cleanTransitions),
        initialState = empty_closure(afnInitialState, transitions)
    )

'''
# recebe: 
# lista de estados (vai ser chamado com o estado inicial do AFV)
# função programa (todas as transições do AFV)
# alfabeto (simbolos)
#  
# DEVERIA:
# fazer o fecho fazio do estado 
# para cada simbolo do alfabeto :
# encontrar as transições desse fecho vazio
# se não tem transições adiciona à lista de transições do AFD esse fecho vazio indo para o novo qf
# se tem, faz tudo isso pro novo conjunto de estados atingidos por essas transições
# adiciona à lista essa transição
# quando n tem transições retorna a lista do afd

def afd_convert_and_graph(afne):
    '''transitions = []
    newInitialState = empty_closure(states, programFunction) 
    reachedStatesAndSymbols = []
    reachedStates = []'''
    ec_program_function = dict()

    afdGraph = Digraph()


    for state in afne.states:
        ec_program_function[state] = afne.empty_closure(state)
    
    afdStack = []
    afdStack.append(afne.empty_closure(afne.initialState))
    afdStates = []
    afdStates.append(afne.empty_closure(afne.initialState))

    if (afne.isFinalAFD(afdStack[0])):
        afdGraph.attr('node', shape='doublecircle')
    else:
        afdGraph.attr('node', shape='circle')
    afdGraph.node(afne.getStateName(afdStack[0]))

    afdGraph.attr('node', shape='none')
    afdGraph.node('')
    afdGraph.edge('', afne.getStateName(afdStack[0]))



    while(len(afdStack) > 0):
        currentState = afdStack.pop(0)

        for symbol in range (afne.alphabetCount):
            fromClosure = set()
            for x in currentState:
                fromClosure.update(set(afne.transition_table[str(x)+str(symbol)]))

            if (len(fromClosure) > 0):
                toState = set()
                for x in list(fromClosure):
                    toState.update(set(ec_program_function[afne.states[x]]))
                
                if list(toState) not in afdStates:
                    afdStack.append(list(toState))
                    afdStates.append(list(toState))

                    if (afne.isFinalAFD(list(toState))):
                        afdGraph.attr('node', shape='doublecircle')
                    else:
                        afdGraph.attr('node', shape='circle')
                    afdGraph.node(afne.getStateName(list(toState)))
    
                # Adding edge between from state and to state
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
                        'ϕ', label = afne.alphabet[symbol])
    afdGraph.render('AFD', view = True)

            



    '''for delta in programFunction:
        if delta.input.currentState in newInitialState and any(s == delta.input.inputSymbol for s in alphabet):
            if delta.output not in reachedStates:
                reachedStates.append(delta.output)
                reachedStatesAndSymbols.append(StateSymbol(
                    state = delta.output,
                    symbol = delta.input.inputSymbol
                ))
                
            
    if reachedStates != newInitialState:
        if reachedStates == []:
            if ("qf" in newInitialState):
                newInitialState.remove("qf")
            transitions.append(
                Delta(
                    input = DeltaInput(
                        currentState = "".join(newInitialState),
                        inputSymbol = symbol
                        ),
                        output = "qf"
                )

            )

        else:
            transitions.append(
                Delta(
                    input = DeltaInput(
                    currentState = "".join(newInitialState),
                    inputSymbol = symbol
                    ),
                    output = "".join(reachedStates)
                )
                
            )
        
            ''transitions.append(
                Delta(
                    input = DeltaInput(
                    currentState = "".join(reachedStates),
                    inputSymbol = symbol
                    ),
                    output = empty_closure(reachedStates, programFunction)
                )
                
            )''
            

            #PRIMEIRAS DUAS PRODUÇÕES SÃO INUTEIS
            #TA COLOCANDO DUAS VEZES AS PRODUÇÕES (EXCETO AS PRIMEIRAS DUAS Q SÃO INUTEIS)
            #FALTA SER TRANSITIVO (TODOS OS ESTADOS APONTAREM PRA ALGO PRA TODOS OS SIMBOLOS)


            if reachedStates != states:
                transitions.extend(afd_program_function(reachedStates, programFunction, alphabet))
    #transitions = list(set(transitions))
    return(transitions)'''
                
# cria primeiro a função programa do afd
# depois acrescenta as transições faltantes
# para tratar todos os simbolos do alfabeto    
def afne_to_afd(afne):
    afd = afd_convert_and_graph(afne)

