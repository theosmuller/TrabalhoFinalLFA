from asyncio.format_helpers import _format_callback_source
from os import stat
from typing import List, NamedTuple, Dict
import re
from glud import GludDefinition, Production

class DeltaInput(NamedTuple):
    currentState: str
    inputSymbol: str

class Delta(NamedTuple):
    input: DeltaInput
    output: str

class FA(NamedTuple):
    states: List[str]
    inputSymbols: List[str]
    programFunction: set[Delta]
    initialState: str

def afd_from_glud(glud):
    afne = afne_from_glud(glud)
    return afne_to_afd(afne.initialState, afne.programFunction, afne.inputSymbols)
    


def afne_from_glud(glud):
    glud.gludDefinition.variables.append("qf")
    return FA(
        states = glud.gludDefinition.variables,
        inputSymbols = glud.gludDefinition.terminals,
        initialState = glud.gludDefinition.initialSymbol,
        programFunction = get_program_function_from_productions(glud.productions)
    )

def get_program_function_from_productions(productions):
    setOfDelta = set()
    for production in productions:
        setOfDelta.add(production_to_delta(production))
    return setOfDelta


def production_to_delta(production):
    if stateIsFinal(production.output[1]):
        return Delta(
        input = DeltaInput(
            currentState = production.input,
            inputSymbol = production.output[0]
        ),
        output = "qf"
    )
    return Delta(
        input = DeltaInput(
            currentState = production.input,
            inputSymbol = production.output[0]
        ),
        output = production.output[1]
    )

def stateIsFinal(outputState):
    if (outputState == "λ"):
        return True
    return False

def empty_closure(states, listofdelta):
    emptyClosure = []
    for state in states:
        emptyClosure.append(state)
        for delta in listofdelta:
            if (delta.input.currentState == state and delta.input.inputSymbol == "λ"):
                if delta.output != "λ":
                    emptyClosure.append(delta.output)
                else:
                    emptyClosure.append("qf")
    return emptyClosure



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

def afd_program_function(states, programFunction, alphabet):
    transitions = []
    newInitialState = empty_closure(states, programFunction)
    for symbol in alphabet: 
        reachedStates = []
        for delta in programFunction:
            if delta.input.currentState in newInitialState and symbol == delta.input.inputSymbol:
                if delta.output not in reachedStates:
                    reachedStates.append(delta.output)
                
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
            
                '''transitions.append(
                    Delta(
                        input = DeltaInput(
                        currentState = "".join(reachedStates),
                        inputSymbol = symbol
                        ),
                        output = empty_closure(reachedStates, programFunction)
                    )
                    
                )'''
                

                #PRIMEIRAS DUAS PRODUÇÕES SÃO INUTEIS
                #TA COLOCANDO DUAS VEZES AS PRODUÇÕES (EXCETO AS PRIMEIRAS DUAS Q SÃO INUTEIS)
                #FALTA SER TRANSITIVO (TODOS OS ESTADOS APONTAREM PRA ALGO PRA TODOS OS SIMBOLOS)


                if reachedStates != states:
                    transitions.extend(afd_program_function(reachedStates, programFunction, alphabet))
    #transitions = list(set(transitions))
    return(transitions)
                
# cria primeiro a função programa do afd
# depois acrescenta as transições faltantes
# para tratar todos os simbolos do alfabeto    
def afne_to_afd(initialState, programFunction, alphabet):
    dirtyAfd = afd_program_function(initialState, programFunction, alphabet)
    return clean_afd(initialState, dirtyAfd, alphabet)

