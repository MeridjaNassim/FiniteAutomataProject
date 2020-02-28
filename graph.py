from graphviz import Digraph
from automata.fa.dfa import DFA
f = Digraph('finite_state_machine', filename='fsm.gv')
f.attr(rankdir='LR', size='8,5')
""" 
f.attr('node', shape='doublecircle')
f.node('LR_0')
f.node('LR_3')
f.node('LR_4')
f.node('LR_8')

f.attr('node', shape='circle')
f.edge('LR_0', 'LR_2', label='SS(B)')
f.edge('LR_0', 'LR_1', label='SS(S)')
f.edge('LR_1', 'LR_3', label='S($end)')
f.edge('LR_2', 'LR_6', label='SS(b)')
f.edge('LR_2', 'LR_5', label='SS(a)')
f.edge('LR_2', 'LR_4', label='S(A)')
f.edge('LR_5', 'LR_7', label='S(b)')
f.edge('LR_5', 'LR_5', label='S(a)')
f.edge('LR_6', 'LR_6', label='S(b)')
f.edge('LR_6', 'LR_5', label='S(a)')
f.edge('LR_7', 'LR_8', label='S(b)')
f.edge('LR_7', 'LR_5', label='S(a)')
f.edge('LR_8', 'LR_6', label='S(b)')
f.edge('LR_8', 'LR_5', label='S(a)') """

#f.view()

def graph(automaton,graph_name="finite_state_machine",file_name="finite_state_machine.gv"):
    """Function that helps in drowing the automaton and saving it to a draw file ".gv"
        -automaton : the desired automaton to be drawn (DFA, NFA) all states must be renamed and complete
        -graph_name : the name of the graph
        -file_name : the name of the saved file must be of extension .gv
        """
    letter =  next(iter(automaton.states))[0]
    grph = Digraph(graph_name,filename=file_name)
    grph.attr(rankdir=letter, size='8,5')
    #specifying final nodes 
    grph.attr('node', shape='doublecircle')
    for state in automaton.final_states:
        grph.node(state)
    #creating edges
    
    grph.attr('node', shape='circle')
    if(isinstance(automaton,DFA)):
        grph =addEdgesDFA(grph,automaton)
        grph.edge("",automaton.initial_state,"")
        grph.edge("",automaton.initial_state,"")
    else:
       grph =addEdgesNFA(grph,automaton)    
    return grph


def addEdgesDFA(graph,automaton):
    for state in automaton.transitions:
        tail = state
        trans = automaton.transitions[state]
        for alpha in automaton.input_symbols:
            label =alpha
            if(alpha==''):
                label ="epsilon"
            graph.edge(tail,trans[alpha],label)
    return graph

def addEdgesNFA(graph,automaton):
    return graph    