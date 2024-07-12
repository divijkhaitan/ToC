from nfa import *
from parse import *

def main(string, regex, draw = False, name = False):
    tree = parse_regex(regex)
    if draw:
        draw_tree(tree, name)
    nfa = parse_tree_to_nfa(tree)
    if (nfa.run(string)):
        print(f"String {string} is in the language generated by regex {regex}")
        return True
    else:
        print(f"String {string} is not in the language generated by regex {regex}")
        return False

regex = input("Enter regex to test against (no spaces, no special characters as terminals): ")
string = input("Enter input string (no spaces, no special characters as terminals): ")

main(string, regex)
# main("00000","((0|1)1)*|((0|1)1)*(0|1)")
# main("11111","((0|1)1)*|((0|1)1)*(0|1)")
# main("01110","((0|1)1)*|((0|1)1)*(0|1)")
# main("10101","((0|1)1)*|((0|1)1)*(0|1)")
# main("11110","((0|1)1)*|((0|1)1)*(0|1)")
# main("000", "0*")