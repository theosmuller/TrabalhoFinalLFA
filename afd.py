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

class Afd(NamedTuple):
    states: List[str]
    inputSymbols: List[str]
    programFunction: List[Delta]
    initialState: str

def afd_from_glud(glud):
    return Afd(
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
        output = production.input
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
