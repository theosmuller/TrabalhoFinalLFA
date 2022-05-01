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
    for state in afne.states[:-1] :
        empty_closure(state, afne.programFunction)
    return afne


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

def empty_closure(state, listofdelta):
    emptyClosure = [state]
    for delta in listofdelta:
        if (delta.input.currentState == state and delta.input.inputSymbol == "λ"):
            if delta.output != "λ":
                emptyClosure.append(delta.output)
            else:
                emptyClosure.append("qf")
    print(emptyClosure)
    return emptyClosure
