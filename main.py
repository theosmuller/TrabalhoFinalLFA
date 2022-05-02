from distutils.command.clean import clean
from glud import get_GLUD_from_file, read_words_from_file, validate_list, isLanguageInfinite
from afd import afd_from_glud, afne_plus_graph
import os


def main():

    gludFile = input("\nINSIRA O NOME DA GLUD A SER LIDA\n")

    glud = get_GLUD_from_file(gludFile)
    while True:
        operation = input(
            "SELECIONE A OPERACAO DESEJADA\n1 - Transformar GLUD em AUTOMATO FINITO\n2 - Testar lista de palavras\n3 - Determinar se a linguagem gerada é finita\n4 - Ler outra GLUD\n5 - SAIR\n")
        print(operation)
        print
        if operation == '1':
            type = input("\n1 - AFD\n2 - AFNE\n")
            if type == '1':
                print(afd_from_glud(glud))
            if type == '2':
                print(afne_plus_graph(glud))

        if operation == '2':
            wordFile = input(
                "Insira nome do arquivo de texto contendo as palavras a testar\n")
            words = read_words_from_file(wordFile)
            print(words)
            print(validate_list(words, glud))

        if operation == '3':
            print(
                f'\n\n A linguagem é {"infinita" if isLanguageInfinite(glud) else "finita"}')

        if operation == '4':
            gludFile = input("INSIRA O NOME DA GLUD A SER LIDA\n")
            glud = get_GLUD_from_file(gludFile)

        if operation == '5':
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Programa finalizado\n")
            quit()


if __name__ == "__main__":
    main()
