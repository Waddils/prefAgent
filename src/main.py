import os
import random
from itertools import product

print("Welcome to PrefAgent!")
print()

while(True):
    attribute_file = input("Enter Attributes File Name: ")

    if os.path.exists(attribute_file):
        print()
        break
    
    print("File does not exist... Enter another file")
    print()

while(True):
    hard_constr = input("Enter Hard Constraints File Name: ")

    if os.path.exists(hard_constr):
        print()
        break
    
    print("File does not exist... Enter another file")
    print()

    

###################################################
#                                                 #
#           Functions to gather information       #
#                                                 #
###################################################

def read_attr(attribute_file):
    attributes = {}
    
    with open(attribute_file, 'r') as file:
        for line in file:
            name, values = line.strip().split(': ')
            attributes[name] = values.split(', ')
            
    return attributes



def read_pref(pref_file):
    conditions = []
    scores = []
    
    with open(pref_file, 'r') as file:
        for line in file:
            logic, score = line.strip().split(', ')
            conditions.append(logic)
            scores.append(int(score))
            
    return conditions, scores



def read_qual_pref(pref_file):
    rules = []
    
    with open(pref_file, 'r') as file:
        for line in file:
            logic_rule = ''
            current_word = ''

            for char in line:
                if char.isupper():
                    if current_word:
                        logic_rule += current_word + ' '
                        current_word = ''
                        
                    logic_rule += char
                else:
                    current_word += char
            
            if current_word:
                logic_rule += current_word
            
            rules.append(logic_rule.strip())
    
    return rules



# Reads the file, "splits" the attribute name and its values into vars
# "name" and "values" respectively, separates the values, and gets all the combinations
# with the objects and spits it out in the desired format
def encode_obj(attribute_file):
    attributes = read_attr(attribute_file)
    combinations = list(product(*attributes.values()))
    combinations.reverse()
    
    for i, combo in enumerate(combinations):
        print(f"o{i} - {', '.join(combo)}")



def feas_check(attribute_file):
    objects = 0
    
    with open(attribute_file, 'r') as file:
        for line in file:
            objects += 2
    
    if (objects != 0):
        print(f"Yes, there are {objects} feasible objects.")
    else:
        print("No, there are no feasible objects.")



def calc_pen_scores(combinations, conditions, scores):
    penalty_scores = []

    # Iterates through all combinations
    for combination in combinations:
        indiv_penalty = []
        
        # Calculates the penalty score for each condition in the combination
        for condition, score in zip(conditions, scores):
            words = condition.split() # ex: "fish" "AND" "wine"
            
            if "AND" in words:
                if all(word in combination for word in words[::2]): # If all of the words (items) in combination are in "words"
                    indiv_penalty.append(0)
                else:
                    indiv_penalty.append(score)
                    
            elif "OR" in words:
                if any(word in combination for word in words[::2]): # Checks if any item in combination contains "words"
                    indiv_penalty.append(0)
                else:
                    indiv_penalty.append(score)
                    
            elif "AND NOT" in words:
                if any(word in combination for word in words[::2]):
                    indiv_penalty.append(score)
                else:
                    indiv_penalty.append(0)
        
        # Calculate the total penalty for this combination
        total_penalty = sum(indiv_penalty)
        penalty_scores.append((indiv_penalty, total_penalty))
    
    return penalty_scores



def calc_qual_pen_scores(combinations, conditions):  
    return



def show_table(attribute_file, pref_file):
    conditions, scores = read_pref(pref_file)
    attributes = read_attr(attribute_file)
    combinations = list(product(*attributes.values()))
    combinations.reverse()

    # Calculates penalty scores using the provided function
    penalty_scores = calc_pen_scores(combinations, conditions, scores)
    
    # Printing table header
    print("+----------+---------------+--------------+---------------+")
    print(f"| encoding | {' | '.join(conditions)} | total penalty |")
    print("+----------+---------------+--------------+---------------+")
        
    for i, (indiv_penalty, total_penalty) in enumerate(penalty_scores):
        row = (f"| o{i:<7} |            {' | '.join(str(penalty) for penalty in indiv_penalty):<17} | {total_penalty:<13} |")
        print(row)
            
    print("+----------+---------------+--------------+---------------+")



def exemp(attribute_file, pref_file):
    conditions, scores = read_pref(pref_file)
    attributes = read_attr(attribute_file)
    combinations = list(product(*attributes.values()))
    combinations.reverse()
    penalty_scores = calc_pen_scores(combinations, conditions, scores)
    
    # Gather/Compare the two variables
    x, y = random.sample(combinations, 2)
        
    x_index = combinations.index(x)
    y_index = combinations.index(y)
    
    x_total_score = penalty_scores[x_index][1]
    y_total_score = penalty_scores[y_index][1]
    
    if x_total_score < y_total_score:
        print(f"Two randomly selected feasible objects are o{x_index} and o{y_index}, and o{x_index} is strictly preferred over o{y_index}.")
    elif x_total_score > y_total_score:
        print(f"Two randomly selected feasible objects are o{x_index} and o{y_index}, and o{y_index} is strictly preferred over o{x_index}.")
    else:
        print(f"Two randomly selected feasible objects are o{x_index} and o{y_index}, and o{x_index} and o{y_index} are equal.")



def qual_exemp(attribute_file, pref_file):
    return


def omni_opti(attribute_file, pref_file):
    optimal_combinations = []
    conditions, scores = read_pref(pref_file)
    attributes = read_attr(attribute_file)
    combinations = list(product(*attributes.values()))
    combinations.reverse()
    penalty_scores = calc_pen_scores(combinations, conditions, scores)
    
    for i, (indiv_penalty, total_penalty) in enumerate(penalty_scores):
        if total_penalty == 0:
            optimal_combinations.append(i)

    print(f"All optimal objects: {', '.join(f'o{i}' for i in optimal_combinations)}.")



def qual_omni_opti(attribute_file, pref_file):
    return

    
    
#---------------------------------------------------------------------------------------------------
    

    
user_choice = 0
while (user_choice != 3):
    print("Choose the preference logic to use: \n1. Penalty Logic \n2. Qualitative Choice Logic \n3. Exit")
    print()
    
    user_choice = input("Your Choice: ")
    print()
    
    match(user_choice):
        case "1": # Penalty Logic
            print("You picked Penalty Logic")
            
            while(True):
                pref_file = input("Enter Preferences File Name: ")

                if os.path.exists(pref_file):
                    print()
                    break
                else: 
                    print("File does not exist... Enter another file")
                    print()
            
            while(True):
                print("Choose the reasoning task to perform: \n1. Encoding \n2. Feasibility Checking \n3. Show the Table \n4. Exemplification \n5. Omni-optimization \n6. Back to previous menu")
                print()
                
                command_choice = input("Your Choice: ")
                print()
                
                match(command_choice):
                    case "1":
                        encode_obj(attribute_file)
                        print()
                        
                    case "2":
                        feas_check(attribute_file)
                        print()
                        
                    case "3":
                        show_table(attribute_file, pref_file)
                        print()
                        
                    case "4":
                        exemp(attribute_file, pref_file)
                        print()
                    
                    case "5":
                        omni_opti(attribute_file, pref_file)
                        print()
                    
                    case "6":
                        print("Going back to previous menu...")
                        print()
                        break
                    
                    case _:
                        print("Please choose a valid option")
                        print()
        
        case "2": # Qualitative Choice Logic
            print("You picked Qualitative Choice Logic")
            
            while(True):
                pref_file = input("Enter Preferences File Name: ")

                if os.path.exists(pref_file):
                    print()
                    break
                else: 
                    print("File does not exist... Enter another file")
                    print()
            
            while(True):
                print("Choose the reasoning task to perform: \n1. Encoding \n2. Feasibility Checking \n3. Show the Table \n4. Exemplification \n5. Omni-optimization \n6. Back to previous menu")
                print()
                
                command_choice = input("Your Choice: ")
                print()
                
                match(command_choice):
                    case "1":
                        encode_obj(attribute_file)
                        print()
                        
                    case "2":
                        feas_check(attribute_file)
                        print()
                        
                    case "3":
                        print("There is no table")
                        print()
                        
                    case "4":
                        print("Not working...")
                        #qual_exemp(attribute_file, pref_file)
                        print()
                    
                    case "5":
                        print("Not working...")
                        #qual_omni_opti(attribute_file, pref_file)
                        print()
                    
                    case "6":
                        print("Going back to previous menu...")
                        print()
                        break
                    
                    case _:
                        print("Please choose a valid option")
                        print()
            
        
        case "3":
            print("Exiting...")
            break
        
        case _:
            print("Please choose a valid option")
            print()