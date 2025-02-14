import json
from graphviz import Digraph

# Function to calculate vector clocks for the given DAG
def calculate_vector_clocks(dag):
    branches = list(dag.keys())
    # Initialize vector clocks for each commit in each branch as a list of zeros
    vector_clocks = {}
    for branch in branches:
        for commit in dag[branch]:
            vector_clocks[commit] = [0] * len(branches) # for our case, size of 3
    
    for branch_index, branch in enumerate(branches): # gets the index and name of each branch in the DAG
        for commit in dag[branch]:
            parents = dag[branch][commit]
            
            # Start from the initial commit
            if not parents:
                vector_clocks[commit][branch_index] = 1 # need to get the parents (branch 1 is [1, 0, 0])
            else:
                # Update the vector clock based on parent clocks
                for parent in parents:
                    parent_clock = vector_clocks[parent].copy() # create a copy
                    parent_clock[branch_index] += 1 # increment parent
                    # Merge the clocks by taking the max value for each element
                    updated_clock = []
                    for vc, pc in zip(vector_clocks[commit], parent_clock):
                        updated_clock.append(max(vc, pc))
                    vector_clocks[commit] = updated_clock
    
    return vector_clocks



# Test DAG (Git DAG example file)
with open('DAG.json') as dag_json:
    dag = json.load(dag_json)

# Calculate vector clocks
vector_clocks = calculate_vector_clocks(dag)

# Save the output in JSON format
output_file = 'vector_clocks.json'
with open(output_file, 'w') as f:
    json.dump(vector_clocks, f, indent=4)

print(f"Vector clocks saved to {output_file}")




# Function to check if vector clock a causally precedes b
def causally_precedes(a, b):
    all_less_equal = True
    any_strictly_less = False
    for x, y in zip(a, b):
        if x > y: # If any component of the vc a is greater, than it does not causally precede b
            all_less_equal = False
            break
        if x < y: # Ensure at least one component in vc a is less than b
            any_strictly_less = True
    return all_less_equal and any_strictly_less


# Function to generate causal graph based on vector clocks
def generate_causal_graph(vector_clocks):
    dot = Digraph(comment='Causal Graph')

    # Add nodes (commits)
    for commit, clock in vector_clocks.items():
        dot.node(commit, f"{commit}: {clock}")

    # Add edges (causal relations)
    commits = list(vector_clocks.keys())
    for i in range(len(commits)):
        for j in range(i + 1, len(commits)):
            if causally_precedes(vector_clocks[commits[i]], vector_clocks[commits[j]]):
                dot.edge(commits[i], commits[j])

    return dot

# Generate and save the graph
dot = generate_causal_graph(vector_clocks)
dot.render('causal_graph', format='png')
print("Causal graph saved as causal_graph.png")






# Function to generate a graph with minimal causal edges (removing redundant ones)
def generate_minimal_causal_graph(vector_clocks):
    dot = Digraph(comment='Minimal Causal Graph')

    # Add nodes (commits)
    for commit, clock in vector_clocks.items():
        dot.node(commit, f"{commit}: {clock}")

    # Add minimal edges
    commits = list(vector_clocks.keys())
    for i in range(len(commits)):
        for j in range(i + 1, len(commits)):
            if causally_precedes(vector_clocks[commits[i]], vector_clocks[commits[j]]):
                # Check if the edge is redundant (i.e., there's a transitive path)
                transitive = False
                for k in range(i + 1, j):
                    if causally_precedes(vector_clocks[commits[i]], vector_clocks[commits[k]]) and \
                       causally_precedes(vector_clocks[commits[k]], vector_clocks[commits[j]]):
                        transitive = True
                        break
                if not transitive:
                    dot.edge(commits[i], commits[j])

    return dot

# Generate and save the minimal graph
minimal_dot = generate_minimal_causal_graph(vector_clocks)
minimal_dot.render('minimal_causal_graph', format='png')
print("Minimal causal graph saved as minimal_causal_graph.png")
