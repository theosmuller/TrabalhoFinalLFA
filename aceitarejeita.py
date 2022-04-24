from typing import List, NamedTuple

class AceitaRejeita(NamedTuple):
    aceita: List[str]
    rejeita: List[str]

def nojeira():
    
    return AceitaRejeita(
        aceita = [  
            "v2ss+u1c*|.",
            "u3skm.",
            "w1c*|*||.",
            "v1k(p+v1k(p.",
            "u1m(((+v1s****."
        ],
        rejeita = [
            "vp.",
            "|||.",
            "2ll.",
            "v2ss+u1c+|.",
            "+."
        ]
    )
    '''
    with open("Palavras aceita e rejeita.txt", 'r', encoding='utf8') as aceitaRejeita:
        aceita = []
        rejeita = []
        aceitaRejeita.readline()
        for line in aceitaRejeita:
            if line == "REJEITA":
                aceitaRejeita.readline()
                break
            aceita.append(line)
        for line in aceitaRejeita:
            rejeita.append(line)

        return AceitaRejeita(
            aceita = aceita,
            rejeita = rejeita
        )'''