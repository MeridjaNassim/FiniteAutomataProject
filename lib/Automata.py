from lib.dfa import DFA
from lib.nfa import NFA
def renameStates(automaton,state_start_char ="Z"):
    count = 0
    letter= state_start_char
    states=set()
    final_states =set()
    initial_state =""
    for state in automaton.states:
        
        if(state in automaton.final_states):
            final_states.add(letter+str(count))
        
        if(state == automaton.initial_state):
             initial_state = letter+str(count);

        states.add(letter+str(count))       
        
        for trans in automaton.transitions:
            dic = automaton.transitions[trans]
            for alpha in automaton.input_symbols:
                if(dic[alpha] == state):
                    dic[alpha] = letter+str(count)
        tra = automaton.transitions[state]
        automaton.transitions[letter+str(count)] = tra
        del automaton.transitions[state]   
        count+=1
    automaton.states = states 
    automaton.final_states = final_states
    automaton.initial_state = initial_state
def mirror(automaton,renamed=False,initial_state_name="start"):
    if not renamed:
        renameStates(automaton)    
    states= automaton.states
    input_symbols = automaton.input_symbols
    final_states = {automaton.initial_state}
    initial_state=initial_state_name
    transitions = mirrorEffect(automaton)
    #epsilon transition from initial state to the new initial states
    transitions[initial_state_name]={}
    transitions[initial_state_name][''] =set()
    states.add(initial_state)
    for state in automaton.final_states:
        transitions[initial_state_name][''].add(state)
    #fixing finale states 
    for state in states:
        if not transitions.get(state,None):
            transitions[state] ={}
            for alpha in input_symbols:
                transitions[state][alpha] =set()
    mir = NFA(
        states=states,
        final_states=final_states,
        initial_state=initial_state,
        transitions=transitions,
        input_symbols=input_symbols
    )
    return mir    


def mirrorEffect(automaton):
    new_trans = {}
    for state in automaton.transitions: # for each state in old transitions
        dic = automaton.transitions[state] # get the row of that trasition
        for alpha in automaton.input_symbols: # for each column(alphabet)
            new_state = dic[alpha] #we get the state transitionned to by old automaton
            if not new_trans.get(new_state,None): # if this state does not exist in our new transition table
                new_trans[new_state] = {alpha :{state}} # add a new entry containing one state
            else: # exists in new trans
                if not new_trans[new_state].get(alpha,None):
                    new_trans[new_state][alpha] = {state}
                else:
                    new_trans[new_state][alpha].add(state) #add the state to existing entry
    return new_trans

def complement(automata,complete=True):
    if not complete : # if the automata is not complete make it complete otherwise you cant complement it 
        automata = completify(automata)
    finals = automata.final_states
    states = automata.states
    newfinals = set() # final states of complement 
    for state in states:
        if state not in finals:
            newfinals.add(state) # adding non final states to finals of complement 
    
    cmplt =  DFA(
            states = states,
            final_states=newfinals,
            transitions=automata.transitions,
            initial_state=automata.initial_state,
            input_symbols=automata.input_symbols
        )
    return cmplt       
def completify(automata):
    if isinstance(automata,NFA):
        complete = NFA.copy(automata)
        complete = DFA.from_nfa(complete)
        return complete
    else :
        complete = DFA.copy(automata)
        return complete
def read_from_file(file_name):
    with open(file_name,"r") as file:
        lines = file.read().splitlines()
        input_symbols = lines[0].split(" ") # reading the alphabet
        input_symbols = set(input_symbols)
        states = lines[1].split(" ") # reading the states
        states = set(states)
        initial_state = lines[2]
        final_states = set(lines[3].split(" "))
        transitions = dict()
        for state in states:
            transitions[state] = dict()
            dic = transitions[state]
            for alpha in input_symbols:
                dic[alpha] = set()

        #reading transitions 
        for i in range(4,len(lines)):
            if(lines[i] ==""):
                break
            transition = lines[i].split(";")
            in_state = transition[0]
            letter = transition[1]
            out_state=transition[2]
            if letter is 'eps':
                letter = ''
                transitions[in_state][letter] = set()
            transitions[in_state][letter].add(out_state)    
        return NFA(
            states=states,
            input_symbols=input_symbols,
            initial_state=initial_state,
            final_states=final_states,
            transitions=transitions
        )
def write_to_file(automaton,filename):
    dummy = DFA.copy(automaton)
    with open(filename,"w") as file:
        lines =[]
        input_symbols = dummy.input_symbols
        input_symbols = " ".join(input_symbols)
        states = dummy.states
        states = " ".join(states)
        lines.append(input_symbols+"\n")
        lines.append(states+"\n")
        lines.append(dummy.initial_state+"\n")
        lines.append(" ".join(dummy.final_states)+"\n")
        for state in dummy.transitions:
            dic = dummy.transitions[state]
            for alpha in dummy.input_symbols:
                trans=state+";"+alpha+";"+dic[alpha]
                lines.append(trans+"\n")
        file.writelines(lines)        
def union(automaton1,automaton2):
    initial_state = "s0"
    finial_states ={"sf"}
    input_symbols = automaton1.input_symbols.union(automaton2.input_symbols)
    if(isinstance(automaton1,NFA)):
        automaton1 = DFA.from_nfa(automaton1)
    if(isinstance(automaton2,NFA)):
        automaton2 = DFA.from_nfa(automaton2)    
    renameStates(automaton1,state_start_char="X")
    renameStates(automaton2,state_start_char="Z")
    states = finial_states.union({initial_state},automaton1.states,automaton2.states,finial_states)
    transitions =dict()
    transitions[initial_state] = dict()
    transitions[initial_state][''] = set([automaton1.initial_state,automaton2.initial_state])
    
    for state in automaton1.states:
        transitions[state] = dict()
        for alpha in input_symbols:
            transitions[state][alpha] = set()
        for alpha in automaton1.input_symbols:
            transitions[state][alpha].add(automaton1.transitions[state][alpha])
    for state in automaton2.states:
        transitions[state] = dict()
        for alpha in input_symbols:
            transitions[state][alpha] = set()
        for alpha in automaton2.input_symbols:
            transitions[state][alpha].add(automaton2.transitions[state][alpha])    

    for state in automaton1.final_states:
        transitions[state][''] = finial_states
    for state in automaton2.final_states:
        transitions[state][''] = finial_states
    
    transitions["sf"]=dict()
    for alpha in input_symbols:
        transitions["sf"][alpha] = set()
    
    return NFA(
        states = states,
        transitions = transitions,
        final_states=finial_states,
        initial_state=initial_state,
        input_symbols=input_symbols
    )
def concat(automaton1,automaton2):
    initial_state = "s0"
    finial_states ={"sf"}
    input_symbols = automaton1.input_symbols.union(automaton2.input_symbols)
    if(isinstance(automaton1,NFA)):
        automaton1 = DFA.from_nfa(automaton1)
    if(isinstance(automaton2,NFA)):
        automaton2 = DFA.from_nfa(automaton2)    
    renameStates(automaton1,state_start_char="X")
    renameStates(automaton2,state_start_char="Z")
    states = finial_states.union({initial_state},automaton1.states,automaton2.states,finial_states)
    transitions =dict()
    transitions[initial_state] = dict()
    transitions[initial_state][''] = {automaton1.initial_state}
    
    for state in automaton1.states:
        transitions[state] = dict()
        for alpha in input_symbols:
            transitions[state][alpha] = set()
        for alpha in automaton1.input_symbols:
            transitions[state][alpha].add(automaton1.transitions[state][alpha])
    for state in automaton2.states:
        transitions[state] = dict()
        for alpha in input_symbols:
            transitions[state][alpha] = set()
        for alpha in automaton2.input_symbols:
            transitions[state][alpha].add(automaton2.transitions[state][alpha])

    for state in automaton1.final_states:
        transitions[state]['']={automaton2.initial_state} 
    for state in automaton2.final_states:
        transitions[state][''] = finial_states
    transitions["sf"]=dict()
    for alpha in input_symbols:
        transitions["sf"][alpha] = set()
    return NFA(
        states = states,
        transitions = transitions,
        final_states=finial_states,
        initial_state=initial_state,
        input_symbols=input_symbols
    )
def iteration(automaton):
      final_states ={"sf"}
      states = automaton.states.union(final_states)
      if(isinstance(automaton,NFA)):
        automaton = DFA.from_nfa(automaton)
      renameStates(automaton,state_start_char="I")
      states = automaton.states.union(final_states)  
      transitions = dict()
      for state in automaton.states:
          transitions[state] = dict()
          for alpha in automaton.input_symbols:
              transitions[state][alpha] = {automaton.transitions[state][alpha]}

      
      for state in automaton.final_states:
            transitions[state]['']=final_states
      transitions["sf"]=dict()
      transitions["sf"][''] ={automaton.initial_state}

      return NFA(
          states=states,
          final_states= final_states,
          initial_state=automaton.initial_state,
          transitions=transitions,
          input_symbols=automaton.input_symbols
      )    