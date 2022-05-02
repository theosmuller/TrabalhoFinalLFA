from encodings import utf_8
from threading import currentThread
from typing import List, NamedTuple
import re

class GludDefinition(NamedTuple):
    name: str
    variables: List[str]
    terminals: List[str]
    initialSymbol: str

class Production(NamedTuple):
    input: str
    output: List[str]

class Glud(NamedTuple):
    gludDefinition: GludDefinition
    productions: List[Production]

def get_GLUD_from_file(filename):
    try:
        with open(filename, 'r', encoding='utf8') as input:
        #primeira linha é a definição da glud
            firstLine = input.readline()

            '''segunda linha é o prod, ignora'''
            prod = input.readline()

            productions = []
            '''pega o conteúdo da primeira linha e encaixa no GludDefinition'''
            definition = parse_first_line(firstLine)

            for line in input:
                productions.append(get_production(line, definition.variables))


            return Glud(
                definition,
                productions
                )
    except:
        print("Failed to read glud from file")
    

'''
PARSE da definição da GLUD
pega primeiro o nome dela (tudo antes do =)
depois as variáveis (tudo entre chaves)
depois os terminais (tudo entre chaves mas com uma virgula antes, aka segunda chaves)
depois o simbolo inicial ()
'''
def parse_first_line(line):
    line = line.replace(' ', '')

    gludName = line.split('=')[0]

    variables = re.search('{(.*?)}', line)[0].replace('{','').replace('}','').split(',')

    terminals = re.search(',{(.*?)}', line)[0].replace(',{','').replace('}','').split(',')

    initialSymbol = re.search(',(.1?)\)', line)[0].replace(',','').replace(')','')

    return GludDefinition(
            name = gludName,
            variables = variables,
            terminals = terminals,
            initialSymbol = initialSymbol
        )

def get_production(line, variables):
    '''
    production = {
        "input" : line[0],
        "output" : line.replace(' ','').replace('\n','').split('>')[1]
        }
    '''
    return Production(
        input = line[0],
        output = replace_empty(line.replace(' ','').replace('\n','').split('>')[1], variables)
    )

def replace_empty(productionOutput, variables):
    if len(productionOutput) < 2:
        if len(productionOutput) < 1:
            return ('λ'+'λ')
        if (productionOutput in variables):
            return (("λ")+productionOutput)
        return (productionOutput+("λ"))
    return productionOutput
        


def validate_word(word, glud):
    initialState = glud.gludDefinition.initialSymbol
    return(word_validation_recursive(word, glud, initialState))


'''
EXPLICAÇÃO
para cada letra da word ele vai:
tentar para cada produção achar uma que tenha o estado atual e a letra da palavra 
se tiver ele avança pro estado resultante e chama pra próxima letra a função
se alguma dessas chamadas for a ultima letra e o resultado for um vazio
retorna TRUE
se não avançar o suficiente vai retornar false
'''
def word_validation_recursive(word, glud, currentState):
    for production in glud.productions:
        if ((word == '' and production.output[1] == "λ" and production.input == currentState)
            or(word == '' and production.output[1] == currentState and production.output[0] == "λ")):
            return True
        if (not(word == '')):
            if (production.input == currentState and production.output[0] == word[0]):
                if (production.output[1] == "λ"):
                    currentState = production.input
                else:
                    currentState = production.output[1]
                if(word_validation_recursive(word[1:], glud, currentState)):
                    return True
    return False
        

def validate_list(words, glud):
    acceptedwords = []
    for word in words:
        if validate_word(word, glud):
            acceptedwords.append(word)
    return acceptedwords

def read_words_from_file(file):
    words = []
    try:
        with open(file, 'r', encoding='utf_8') as input:
            words = input.read().splitlines()
        return words
    except:
        print("failed reading word file")
