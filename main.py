from lib.dfa import DFA
from lib.nfa import NFA
from graphviz import Digraph
import lib.Automata as aut
import lib.graph as graph

def createAutomaton():
    print("Automaton Creation : ")
    print("======================")
    hasInitial = False
    states=set()
    final_states=set()
    initial_state=""
    transitions=dict()
    input_symbols=set()
    print("Phase 1 : Entering Input Symbols")
    while True:
        alpha = input("Enter a letter of the input symbols recognized by this Automaton (a , 0 ,! ...) 'exit' to stop->>>")
        if alpha == 'exit':
            break
        else:
            if(len(alpha)==1):
                input_symbols.add(alpha)
            else:
                print("Please enter one letter ( lenght == 1 )")
                continue

    print("Input_symbols ==",input_symbols)
    print("======================")    
    print("Phase 2 : Entering States ...")
    while True:
        inp=input("Enter a state name (exp : S0,state1) 'exit' to stop entering states-->>>")
        if(inp=='exit'):
            break
        else:
            states.add(inp)
            if not hasInitial:
                booll = input("Is this state initial for the Automaton (y/n) -->>>")
                if booll is "y":
                    hasInitial = True
                    initial_state=inp
            booll =input("Is this state final for the Automaton (y/n)-->>>")
            if booll is "y":
                final_states.add(inp)
    print("states ==>" ,states)
    print("initial state==>",initial_state)
    print("final states==>",final_states)
    print("======================")
    for state in states:
        transitions[state] = dict()
        dic = transitions[state]
        for alpha in input_symbols:
            dic[alpha] =set()

    print("Phase 3 : Entering Transitions")
    stop = False
    for state in states:
        print("Transitions for state: ",state)
        print("======================")   
        for alpha in input_symbols:
            finished_alpha = False 
            while not finished_alpha:  
                print("Current input symbol ->>> ",alpha)
                if finished_alpha :
                    break; 
                outstate = input("Enter a existing ending state name ,'exit' to stop entering transitions-->>>")
                if outstate =="exit":
                    finished_alpha=True
                    continue
        
                while outstate not in states:
                    outstate = input("Enter a existing ending state name ,'exit' to stop entering transitions-->>>")
                    if outstate =="exit":
                        finished_alpha=True
                        break
                if finished_alpha :
                    break

                if outstate == state: # transition boucle
                    transitions[state][alpha].add(state)
                else:
                    eps = input("Is this spontanious/epsilon transition (y/n)->>>")
                    if eps is 'y':
                            if not transitions[state].get('',None):
                                transitions[state][''] = set()
                            transitions[state][''].add(outstate)
                    else:
                        transitions[state][alpha].add(outstate)    
        
    print("Transitions ==",transitions)
    nfa = NFA(
        states = states,
        input_symbols=input_symbols,
        transitions=transitions,
        final_states= final_states,
        initial_state= initial_state
    ) 
    print("======================")   
    print("Automate créé avec succée")
    print("Adress :",nfa)
    print("states ==>" ,nfa.states)
    print("input symbols==>",nfa.input_symbols)
    print("initial state==>",nfa.initial_state)
    print("final states==>",nfa.final_states)
    print("transitions==>",nfa.transitions)
    print("======================")
    return nfa
def determinize(automaton):
    print("Automaton Determinization : ")
    if(isinstance(automaton,NFA)):
        automaton = DFA.from_nfa(automaton)
    aut.renameStates(automaton,state_start_char="D")   
    print("======================")   
    print("Automate Determinized with success")
    print("Adress :",automaton)
    print("states ==>" ,automaton.states)
    print("input symbols==>",automaton.input_symbols)
    print("initial state==>",automaton.initial_state)
    print("final states==>",automaton.final_states)
    print("transitions==>",automaton.transitions)
    print("======================")    
    return automaton

def complement(automaton):
    print("Automaton Complementation : ")
    automaton = aut.complement(automaton,complete=False)
    print("======================")   
    print("Automate Complemented with success")
    print("Adress :",automaton)
    print("states ==>" ,automaton.states)
    print("input symbols==>",automaton.input_symbols)
    print("initial state==>",automaton.initial_state)
    print("final states==>",automaton.final_states)
    print("transitions==>",automaton.transitions)
    print("======================")    
    
    return automaton
def minify(automaton):
    print("Automaton Minification : ")
    if(isinstance(automaton,NFA)):
        automaton = DFA.from_nfa(automaton)

    aut.renameStates(automaton,state_start_char="M")   
    automaton.minify()
    print("======================")   
    print("Automate Minimised with success")
    print("Adress :",automaton)
    print("states ==>" ,automaton.states)
    print("input symbols==>",automaton.input_symbols)
    print("initial state==>",automaton.initial_state)
    print("final states==>",automaton.final_states)
    print("transitions==>",automaton.transitions)
    print("======================")    
    return automaton
def mirror(automaton):
    print("Automaton Mirror: ")
    if isinstance(automaton,NFA):
        automaton = DFA.from_nfa(automaton)
        automaton.minify()
    aut.renameStates(automaton,state_start_char="MRS")
    automaton = aut.mirror(automaton,renamed=True)
    if isinstance(automaton,NFA):
        automaton = DFA.from_nfa(automaton).minify()
        aut.renameStates(automaton,state_start_char="MR")
    print("======================")   
    print("Automate Mirrored with success")
    print("Adress :",automaton)
    print("states ==>" ,automaton.states)
    print("input symbols==>",automaton.input_symbols)
    print("initial state==>",automaton.initial_state)
    print("final states==>",automaton.final_states)
    print("transitions==>",automaton.transitions)
    print("======================")    
    return automaton
def accept_word(automaton):
    print("Word Acceptance : ")
    print("=================")
    word = input("Enter the word you want to test ->>>")
    accept = automaton.accepts_input(word)
    if accept :
        print("the word :",word,"is recognized by this automaton")
    else : 
        print("the word :",word,"is not recognized by this automaton")
    
    return automaton
def save(automaton):
    print("Automaton Saving : ")
    if(isinstance(automaton,NFA)):
        automaton = DFA.from_nfa(automaton)
        
    automaton.minify()
    letter =input("How do you want to name the states ,one word->>>")
    aut.renameStates(automaton,state_start_char=letter) 
    filename = input("Enter output path (if you add extension add .gr) ->>>")
    viz = graph.graph(automaton,graph_name="automaton",file_name=filename)   
    viz.view()
    return automaton

operations = {
    "1" :createAutomaton,
    "2" :determinize,
    "3" :complement,
    "4" :minify,
    "5" :mirror,
    "6" :accept_word,
    "7" :save,    
}
keys = {"1","2","3","4","5","6","7","E"}
while True:
    print("Hello to Automata Simulator by Meridja Nassim")
    inp = input("enter any key to continue... (E) to exit-->>>")
    if(inp =="E"):
        exit(0)
    else :
        automate = None
        while True:
            print("Available operations : ")
            print("1-Create Automata")
            print("2-Determinization")
            print("3-Complement")
            print("4-Minification")
            print("5-Mirror")
            print("6-Accepts Word")
            print("7-save automaton")
            inp=input("Enter desired operation key...(E) to exit-->>>")
            while(inp not in keys):
                print("Please enter correct key :)")
                inp=input("Enter desired operation key...(E) to exit-->>>")
            if inp is "E":
                print("Thank you !!")
                exit(0)
            operation = operations[inp]    
            if inp is "1":
                automate = createAutomaton()
                
            else :
                if(automate is None):
                    automate = createAutomaton()
                automate =operation(automate)



