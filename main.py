from automata.fa.dfa import DFA
from automata.fa.nfa import NFA

import Automata as aut
nf = NFA(states ={"s0","s1"},
    initial_state="s0",
    input_symbols={"a","b"},
    transitions={
        "s0": {
            "a" :{"s0","s1"},
            "b" :{"s1"}
        },
        "s1" : {
            "a" :{"s0","s1"},
            
        }
    },
    final_states={"s0"}
)
df= DFA.from_nfa(nf)
print(DFA.from_nfa(nf).transitions)



print("the word : baa is recognized by automate" , df.accepts_input("baaba"))
aut.renameStates(df,state_start_char="")


mir = aut.mirror(df,renamed=True)

dfa2 = DFA.from_nfa(mir)
aut.renameStates(dfa2,state_start_char="Z")
print("the word : aab is recognized by mirror" , dfa2.accepts_input("abaab"))


