from nfa import *
from parse import *

# When parsing the regular expression, the special characters may cause problems
# For this reason, I am replacing the *, $ and # characters in the language given to us with d, e and f
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', '1', '2', '3']

input_string = input("Enter the input string: ")

input_string = input_string.replace('$', 'd')
input_string = input_string.replace('*', 'e')
input_string = input_string.replace('#', 'f')

# print(input_string)

regex1 = "(a+b+c+d+e+f+1+2+3)*123(a+b+c+d+e+f+1+2+3)*" # detecting at least 1 '123' pattern 
regex2 = "(a+b+c+d+e+f+1+2+3)*(d+e+f)(a+b+c+d+e+f+1+2+3)*" # detecting at least 1 special character
regex3 = "(a+b+c+d+e+f+1+2+3)*(1+2+3)(a+b+c+d+e+f+1+2+3)*" # detecting at least 1 numeral
regex4 = "(a+b+c+d+e+f+1+2+3)*(a+b+c)(a+b+c+d+e+f+1+2+3)*" # detecting at least alphabet
# detecing length of at least 6
regex5 = "(a+b+c+d+e+f+1+2+3)(a+b+c+d+e+f+1+2+3)(a+b+c+d+e+f+1+2+3)(a+b+c+d+e+f+1+2+3)(a+b+c+d+e+f+1+2+3)(a+b+c+d+e+f+1+2+3)(a+b+c+d+e+f+1+2+3)*"

#creating NFAs from regexes and running them
tree1 = parse_regex(regex1)
nfa1 = parse_tree_to_nfa(tree1)
x1 = nfa1.run(input_string)

tree2 = parse_regex(regex2)
nfa2 = parse_tree_to_nfa(tree2)
x2 = nfa2.run(input_string)

tree3 = parse_regex(regex3)
nfa3 = parse_tree_to_nfa(tree3)
x3 = nfa3.run(input_string)

tree4 = parse_regex(regex4)
nfa4 = parse_tree_to_nfa(tree4)
x4 = nfa4.run(input_string)

tree5 = parse_regex(regex5)
nfa5 = parse_tree_to_nfa(tree5)
x5 = nfa5.run(input_string)

# if a 123 pattern was detected, we can reject
if x1: 
    print("False")
# if no 123 pattern, we need to check all the other conditions hold (\geq 1 alphabet, number and letter, \geq 6 length)
elif (not x1) and (x2 and x3 and x4 and x5):
    print("True")
else:
    print("False")
