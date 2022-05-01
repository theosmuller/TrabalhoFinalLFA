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
    programFunction: List[Delta]
    initialState: str

def afd_from_glud(glud):
    afne = afne_from_glud(glud)
    print(afne_to_afd(afne.initialState, afne.programFunction, afne.inputSymbols))
    


def afne_from_glud(glud):
    glud.gludDefinition.variables.append("qf")
    return FA(
        states = glud.gludDefinition.variables,
        inputSymbols = glud.gludDefinition.terminals,
        initialState = glud.gludDefinition.initialSymbol,
        programFunction = get_program_function_from_productions(glud.productions)
    )

def get_program_function_from_productions(productions):
    listOfDelta = []
    for production in productions:
        listOfDelta.append(production_to_delta(production))
    return listOfDelta


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
def afne_to_afd(states, programFunction, alphabet):
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
                return transitions
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
                if reachedStates != states:
                    transitions.extend(afne_to_afd(reachedStates, programFunction, alphabet))
                
    return(transitions)
                
    

