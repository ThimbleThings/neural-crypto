# Neural cryptography protocol for key exchange

Implementation of the key exchange protocol described in Neural Synchronization and Cryptography, Ruttor 2006.
(Corrected two severe implementation errors found in the original git repo)

## Idea of this repository

This repository is meant to provide a tool that allows testing the synchronization behaviour of two Tree Parity Machines
for different configurations of the Parameters K, N, and L and the success rate of a simple attacker.
Data for the simulations run by me is provided in the data folder.
To plot this data the bubblePlot.py and boxPlot.py scripts can be used, requiring plotly and matplotlib respectively
(bubblePlot is meant to process the collectedDataSyncXXX.csv files, boxPlot to process the collectedDataXXX.csv files).

If you are interested in using this repo for further research feel free to send pull requests or contact me.

Interesting topics might be to implement the Query Mechanism proposed by Ruttor instead of using the random input
vectors in this implementation. Also of interest might be the implementation of more sophisticated attacks
(genetic attack, geometric attack, majority attack).


### Important Note:

Contrary to the statement in the original git by exced, neural cryptography is not secure against a MITM Attack.
What neural cryptography provides is an alternative to the Diffie-Hellman key exchange without needing a trapdoor
functionality like the modulo operation and integer factorization.


## Simulation Example

To generate your own data execute the run.py file with the configurations you want to investigate, for example:
```bash
python3 run.py -r hebbian -K 3.4.5 -N 3.4 -L 3.4 -n 10 -t 10.0
```

From the generated CSV file you can extract interesting data using the extractCSVData.py script.
On the two generated CSV files you can then use the plot scripts.

The parameters to the simulation are:
- r: the learning rule to use [hebbian, anti_hebbian, random_walk]
- K: point separated integers for the numbers of neurons to test
- N: point separated integers for the numbers of inputs per neuron to test
- L: point separated integers for the maximum weight values to test
- n: number of simulations to run per configuration of K, N, and L
- t: time in seconds before a simulation terminates (default 20.0, stop simulation for unsuccessful synchronizations)


[Example Plot](https://github.com/ThimbleThings/neural-crypto/blob/master/example/exampleData.html)
