# Bayesian Network

## Network Design
![Image]
(https://drive.google.com/open?id=0B5-d8KjN9CEvZm9xZDFSUFotM00)

## Transition Model
	### Node Trav
	* P(Trav) = 0.05
	* P(¬Trav) = 0.95
	### Node OC
	* P(OC) = 0.8
	* P(¬OC) = 0.2
	### Node Fraud
	* P(Fraud | Trav) = 0.01
	* P(Fraud | ¬Trav) = 0.004
	* P(¬Fraud | Trav) = 0.99
	* P(¬Fraud | ¬Trav) = 0.996
	### Node CRP
	* P(CRP | OC) = 0.1
	* P(CRP | ¬ OC) = 0.01
	* P(¬CRP | OC) = 0.9
	* P(¬CRP | ¬ OC) = 0.99
	### Node FP
	* P(FP| Trav, Fraud) = 0.9
	* P(FP| Trav, ¬Fraud) = 0.9
	* P(FP| ¬Trav, Fraud) = 0.1
	* P(FP| ¬Trav, ¬Fraud) = 0.01
	* P(¬FP| Trav, Fraud) = 0.1
	* P(¬FP| Trav, ¬Fraud) = 0.1
	* P(¬FP| ¬Trav, Fraud) = 0.9
	* P(¬FP| ¬Trav, ¬Fraud) = 0.99
	### Node IP
	* P(IP| OC, Fraud) = 0.15
	* P(IP | OC, ¬Fraud) = 0.1
	* P(IP | ¬ OC, Fraud) = 0.051
	* P(IP | ¬ OC, ¬Fraud) = 0.001
	* P(¬IP | OC, Fraud) = 0.85
	* P(¬IP | OC, ¬Fraud) = 0.9
	* P(¬IP | ¬ OC, Fraud) = 0.949
	* P(¬IP | ¬ OC, ¬Fraud) = 0.999
  
## Inference Solving
For a query P(Q|e) where Q is our query variable set and e is the evidence we want to found the corresponding probabilities
* Value Iteration Algorithm
