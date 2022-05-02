from distutils.command.clean import clean
from glud import get_GLUD_from_file, read_words_from_file, validate_list, validate_word
from afd import afd_from_glud
from aceitarejeita import nojeira
import os
'''f = open("input.txt", "r")
nomeGLUD = ""
print(f.read())
for line in f:
    for character in line:
        nomeGLUD + character
        if character == '=':        
'''

def main():

    gludFile = input("INSIRA O NOME DA GLUD A SER LIDA")

    glud = get_GLUD_from_file(gludFile)
    print(glud)
    while True:
        operation = input("SELECIONE A OPERACAO DESEJADA\n1 - Transformar GLUD em AFD\n2 - Testar lista de palavras\n3 - Determinar se a linguagem gerada é finita\n4 - SAIR")
        print(operation)
        print
        if operation == '1' :
            print(afd_from_glud(glud))

        if operation == '2' :
            wordFile = input("Insira nome do arquivo de texto contendo as palavras a testar")
            words = read_words_from_file(wordFile)
            print(words)
            print(validate_list(words, glud))
        
        if operation == '3' :
            print("Ainda não foi implementado")
        
        if operation == '4' :
            os.system('cls' if os.name == 'nt' else 'clear')    
            print("Programa finalizado")       
            quit()
            


    #glud = get_GLUD_from_file("input.txt")
    #print (glud)
    #afn = afd_from_glud(glud)
    #print(afn)
    #gludtest = get_GLUD_from_file("test.txt")
    #print("\n\n\n RESULTADO DA CONVERSÃO DE AFV PARA AFD:\n\n\n")
    afd = afd_from_glud(gludtest)
    print("STATES:")
    print(afd.states)
    print("\nTRANSITIONS")

    for delta in afd.programFunction:
        print (delta)


    words = ["ab", "abb", "abcb", "baba"]

    print(validate_list(words, glud))

    icecreammachine = get_GLUD_from_file("GLUD formato de entrada definido.txt")
    print(icecreammachine.gludDefinition.initialSymbol)
    aceitaRejeitaIceCream = nojeira()
    for aceita in aceitaRejeitaIceCream.aceita:
        print(validate_word(aceita, icecreammachine))
    print("EXPECTED: tudo true")

    for rejeita in aceitaRejeitaIceCream.rejeita:
        print(validate_word(rejeita, icecreammachine))
    print("EXPECTED: tudo false")


if __name__ == "__main__":
    main()


