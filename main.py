from glud import get_GLUD_from_file, validate_word
from afd import afd_from_glud
from aceitarejeita import nojeira
'''f = open("input.txt", "r")
nomeGLUD = ""
print(f.read())
for line in f:
    for character in line:
        nomeGLUD + character
        if character == '=':        
'''

def main():
    glud = get_GLUD_from_file("input.txt")
    print (glud)
    afn = afd_from_glud(glud)
    print(afn)

    print(validate_word("ab", glud)) 
    print(validate_word("abb", glud))
    print("EXPECTED: true, false")

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


