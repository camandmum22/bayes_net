from copy import deepcopy
from itertools import combinations_with_replacement, permutations
from collections import OrderedDict
"""
This class represents a Bayes Network
"""
class bayes_network:

    def init_net(self):
        '''
        We initialize the net with our first scenario
        '''
        T = True
        F = False
        HAS_PARENTS = -1
        self.batch_permutations = {}
        self.net = {}

        self.net['Travel'] = {
            'parents': [],
            'childs': [],
            'probability': 0.05,
            'cpt': {}
        }

        self.net['OC'] = {
            'parents': [],
            'childs': [],
            'probability': 0.8,
            'cpt': {}
        }

        self.net['Travel']['childs'].append('Fraud')
        self.net['Fraud'] = {
            'parents': ['Travel'],
            'childs': [],
            'probability': HAS_PARENTS,
            'cpt': {}
        }
        self.net['Fraud']['cpt'][(T,)] = 0.01
        self.net['Fraud']['cpt'][(F,)] = 0.004

        self.net['OC']['childs'].append('CRP')
        self.net['CRP'] = {
            'parents': ['OC'],
            'childs': [],
            'probability': HAS_PARENTS,
            'cpt': {}
        }
        self.net['CRP']['cpt'][(T,)] = 0.1
        self.net['CRP']['cpt'][(F,)] = 0.001

        self.net['Travel']['childs'].append('FP')
        self.net['Fraud']['childs'].append('FP')
        self.net['FP'] = {
            'parents': ['Travel', 'Fraud'],
            'childs': [],
            'probability': HAS_PARENTS,
            'cpt': {}
        }
        self.net['FP']['cpt'][(T, T)] = 0.9
        self.net['FP']['cpt'][(T, F)] = 0.9
        self.net['FP']['cpt'][(F, T)] = 0.1
        self.net['FP']['cpt'][(F, F)] = 0.01

        self.net['OC']['childs'].append('IP')
        self.net['Fraud']['childs'].append('IP')
        self.net['IP'] = {
            'parents': ['OC', 'Fraud'],
            'childs': [],
            'probability': HAS_PARENTS,
            'cpt': {}
        }
        self.net['IP']['cpt'][(T, T)] = 0.15
        self.net['IP']['cpt'][(T, F)] = 0.1
        self.net['IP']['cpt'][(F, T)] = 0.051
        self.net['IP']['cpt'][(F, F)] = 0.001

    def init_net_empty_evidence(self):
        '''
        We initialize the net to calculate prior probabilities without evidence given
        '''
        self.batch_permutations = {}
        self.net = {}

        T = True
        F = False
        HAS_PARENTS = -1
        self.batch_permutations = {}
        self.net = {}

        self.net['Travel'] = {
            'parents': [],
            'childs': [],
            'probability': 0.05,
            'cpt': {}
        }

        self.net['Travel']['childs'].append('Fraud')
        self.net['Fraud'] = {
            'parents': ['Travel'],
            'childs': [],
            'probability': HAS_PARENTS,
            'cpt': {}
        }
        self.net['Fraud']['cpt'][(T,)] = 0.01
        self.net['Fraud']['cpt'][(F,)] = 0.004

    # Normalizes a factor, making all its probabilties to sum up to 1
    def normalize(self, factor):
        return tuple(x * 1 / (sum(factor)) for x in factor)

    # Returns the probability of ocurrence for a given variable an evidence
    def get_probability(self, variable, evidence):
        if self.net[variable]['probability'] != -1:
            if evidence[variable]:   # value is True
                p = self.net[variable]['probability']
            else: #value is False
                p = 1 - self.net[variable]['probability']
        else:
            parents = tuple(evidence[p] for p in self.net[variable]['parents'])
            if evidence[variable]:  # value is True
                p = self.net[variable]['cpt'][parents]
            else: #value is False
                p = 1 - self.net[variable]['cpt'][parents]
        print "get_probability( variable --> %s, evidence --> %s)\n\tresult --> %s" \
              % (variable, evidence,p)
        return p

    # Generates all the permutations of n boolean values
    # and stores in memory for future use
    def generate_permutations(self, n):
        if n in self.batch_permutations:
            return self.batch_permutations[n]
        else:
            set_permutations = set()
            for comb in combinations_with_replacement([False, True], n):
                for p in permutations(comb):
                    set_permutations.add(p)
            self.batch_permutations[n] = list(set_permutations)
            return set_permutations

    # Creates a new factor for a given variable, a corresponding net of values
    # and an evidence set
    def restrict_factor(self, variable, mapping, evidence):
        variables = mapping[variable]
        variables.sort()
        map_vars = deepcopy(self.net[variable]['parents'])
        map_vars.append(variable)
        set_permutations = self.generate_permutations(len(map_vars))
        pairs = {}
        values = {}

        for p in set_permutations:
            stop = False
            for entry in zip(map_vars, p):
                if entry[0] in evidence and evidence[entry[0]] != entry[1]:
                    stop = True
                    break
                values[entry[0]] = entry[1]
            if stop:
                continue

            key = tuple(values[v] for v in variables)
            probability = self.get_probability(variable, values)
            pairs[key] = probability

        print "restrict_factor( variable --> %s, net --> %s, evidence --> %s)\n\tresult --> %s" \
              % (variable, mapping, evidence, (variables, pairs))
        return (variables, pairs)

    # Computes the product of two factors
    def product_factor(self, factor_one, factor_two):
        set_vars = []
        set_vars.extend(factor_one[0])
        set_vars.extend(factor_two[0])
        set_vars = list(set(set_vars))
        set_vars.sort()

        set_permutations = self.generate_permutations(len(set_vars))
        mapping = {}
        values = {}
        for p in set_permutations:
            for entry in zip(set_vars, p):
                values[entry[0]] = entry[1]
            set_1 = tuple(values[var] for var in set_vars)
            set_2 = tuple(values[var] for var in factor_one[0])
            set_3 = tuple(values[var] for var in factor_two[0])
            probability = factor_one[1][set_2] * factor_two[1][set_3]
            mapping[set_1] = probability

        print "product_factor( factor_one --> %s, \n\tfactor_two --> %s)\n\tresult --> %s" \
              % (factor_one, factor_two, (set_vars, mapping))
        return (set_vars, mapping)

    # Computes summing out a factor with a given variable
    def sumout_factor(self, variable, factor):
        initial_factor = deepcopy(factor)
        set_factors = []
        pos = []
        for i, sub_factor in enumerate(factor):
            if variable in sub_factor[0]:
                set_factors.append(sub_factor)
                pos.append(i)
        if len(set_factors) > 1:
            for i in reversed(pos):
                del factor[i]
            result = set_factors[0]
            for sub_factor in set_factors[1:]:
                result = self.product_factor(result, sub_factor)
            factor.append(result)

        for i, sub_factor in enumerate(factor):
            for j, var in enumerate(sub_factor[0]):
                if var == variable:
                    set_variables = sub_factor[0][:j] + sub_factor[0][j + 1:]
                    set_pairs = {}
                    for pair in sub_factor[1]:
                        pair = list(pair)
                        key = tuple(pair[:j] + pair[j + 1:])
                        pair[j] = True
                        probability_1 = sub_factor[1][tuple(pair)]
                        pair[j] = False
                        probability_2 = sub_factor[1][tuple(pair)]
                        prob = probability_1 + probability_2
                        set_pairs[key] = prob

                    factor[i] = (set_variables, set_pairs)
                    if len(set_variables) == 0:
                        del factor[i]
        print "sumout_factor( variable --> %s, inital_factor --> %s)\n\tresult --> %s" \
              % (variable, initial_factor, factor)
        return factor

    # Returns the order of exploration defined for the variables
    def order_variables(self):
       return ["Travel", "FP", "Fraud", "IP", "OC", "CRP"]

    # Computes the probability distribution for a given variable with evidence e
    # and using variable elimination
    def variable_elimination_inference(self, variable, evidence):
        set_marked = set()
        set_factors = []
        print "variable_elimination_inference( variable --> %s, evidence --> %s)" \
              % (variable, evidence)
        while len(set_marked) < len(self.net):
            # variables marked
            vars = filter(lambda v: v not in set_marked, list(self.net.keys()))

            # variables with some children that haven't been marked yet
            vars = filter(lambda v: all(c in set_marked for c in self.net[v]['childs']),vars)

            # enumerate the variables in the factor associated with the variable
            sub_factor = {}
            for v in vars:
                sub_factor[v] = [parent for parent in self.net[v]['parents'] if parent not in evidence]  # and p != variable]
                if v not in evidence:  # and v != variable:
                    sub_factor[v].append(v)

            # sort according to the order given in the handout
            selected_var = list(OrderedDict(sorted(sub_factor.items(), key=lambda i: self.order_variables().index(i[0]))).keys())[0]
            if len(sub_factor[selected_var]) > 0:
                set_factors.append(self.restrict_factor(selected_var, sub_factor, evidence))

            if selected_var != variable and selected_var not in evidence:
                set_factors = self.sumout_factor(selected_var, set_factors)
            set_marked.add(selected_var)

            print "selected variable during inference --> %s, set_factors --> \n\t\t%s" \
                  % (selected_var, set_factors)

        if len(set_factors) >= 2:
            product = set_factors[0]
            for factor in set_factors[1:]:
                product = self.product_factor(product, factor)
        else:
            product = set_factors[0]
        return self.normalize((product[1][(False,)], product[1][(True,)]))

# -------------------------------------------------------------------

def main():
    net_v1 = bayes_network()

    empty_evidence = {}
    evidence_1 = {'FP': True, 'IP': False, 'CRP': True}
    evidence_2 = {'FP': True, 'IP': False, 'CRP': True, 'Travel': True}
    evidence_3_1 = {'IP': True, 'FP': True, 'CRP': True}
    evidence_3_2 = {'IP': True, 'FP': True, 'CRP': False}
    evidence_3_3 = {'IP': True, 'FP': False, 'CRP': True}
    evidence_3_4 = {'IP': True, 'FP': False, 'CRP': False}

    print "---------------------------------- Printout for 2b_prior ----------------------------------"
    net_v1.init_net_empty_evidence()
    ans_2b_1 = net_v1.variable_elimination_inference('Fraud', empty_evidence)
    net_v1.init_net()
    print "\n\n---------------------------------- Printout for 2b ----------------------------------"
    ans_2b_2 = net_v1.variable_elimination_inference('Fraud', evidence_1)
    print "\n\n---------------------------------- Printout for 2c ----------------------------------"
    ans_2c = net_v1.variable_elimination_inference('Fraud', evidence_2)
    print "\n\n---------------------------------- Printout for 2d ----------------------------------"
    print "-------------- Option 1 --------------"
    ans_2d_1 = net_v1.variable_elimination_inference('Fraud', evidence_3_1)
    print "\n-------------- Option 2 --------------"
    ans_2d_2 = net_v1.variable_elimination_inference('Fraud', evidence_3_2)
    print "\n-------------- Option 3 --------------"
    ans_2d_3 = net_v1.variable_elimination_inference('Fraud', evidence_3_3)
    print "\n-------------- Option 4 --------------"
    ans_2d_4 = net_v1.variable_elimination_inference('Fraud', evidence_3_4)

if __name__ == "__main__":
    main()