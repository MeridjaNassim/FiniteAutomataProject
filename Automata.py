from automata.fa.dfa import DFA
from automata.fa.nfa import NFA


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

