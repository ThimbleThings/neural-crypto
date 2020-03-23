from tpm import TPM
import numpy as np
import time, sys, getopt


# import matplotlib.pyplot as plt


def random(K, N):
    '''random
    return a random vector input for TPM
    '''

    """
    Inputs to the Tree Parity Machine should always be binary from the set {-1, +1}.
    
    For reference see: Neural Synchronization and Cryptography, Ruttor 2006, Page 14.
    """
    return np.random.choice(np.array([-1, 1]), [K, N])


def sync_score(TPM1, TPM2, L):
    '''sync_score
    Synchronize the score of 2 tree parity machines
    TPM1 - Tree Parity Machine 1
    TPM2 - Tree Parity Machine 2
    '''

    return 1.0 - np.average(1.0 * np.abs(TPM1.W - TPM2.W) / (2 * L))


def run(K, N, L, key_length, iv_length, update_rule, time_threshold):
    # Create TPM for Alice, Bob and Eve. Eve eavesdrops communication of Alice and Bob
    Alice = TPM(K, N, L, update_rule)
    Bob = TPM(K, N, L, update_rule)
    Eve = TPM(K, N, L, update_rule)

    # Synchronize weights
    nb_updates = 0
    nb_eve_updates = 0
    start_time = time.time()  # Start time
    sync_history = []  # plot purpose
    sync_history_eve = []  # plot purpose
    score = 0  # synchronisation score of Alice and Bob

    while score < 100:

        X = random(K, N)  # Create random vector [K, N]

        # compute outputs of TPMs
        tauA = Alice.get_output(X)
        tauB = Bob.get_output(X)
        tauE = Eve.get_output(X)

        # Alice and Bob would update only if tauA == tauB
        if tauA == tauB:
            Alice.update()
            Bob.update()
            nb_updates += 1

        # Eve would update only if tauA = tauB = tauE
        if tauA == tauB == tauE:
            Eve.update()
            nb_eve_updates += 1

        # sync of Alice and Bob
        score = 100 * sync_score(Alice, Bob, L)  # Calculate the synchronization of Alice and Bob
        sync_history.append(score)  # plot purpose
        # sync of Alice and Eve
        score_eve = 100 * sync_score(Alice, Eve, L)  # Calculate the synchronization of Alice and Eve
        sync_history_eve.append(score_eve)  # plot purpose

        # When the networks take longer than 15 seconds to synchronize terminate
        if time.time() - start_time > time_threshold:
            break

    # results
    Alice_key, Alice_iv = Alice.makeKey(key_length, iv_length)
    Bob_key, Bob_iv = Bob.makeKey(key_length, iv_length)
    Eve_key, Eve_iv = Eve.makeKey(key_length, iv_length)

    # Directly create the data for the CSV
    #           K              N              L              ABUpdates               EUpdates
    #           SyncAB                             SyncAE                             KeyA              KeyB
    #             KeyE
    data = str(K) + "," + str(N) + "," + str(L) + "," + str(nb_updates) + "," + str(nb_eve_updates) + "," + \
           str(int(sync_history[-1])) + "," + str(int(sync_history_eve[-1])) + "," + Alice_key + "," + Bob_key + \
           "," + Eve_key

    return data


def print_opts():
    print('run.py -r hebbian -K 2.3.4 -N 2.3.4 -L 2.3.4 -n 100 -t 20.0')
    print('update rule: hebbian, anti_hebbian, random_walk')
    print('Default update rule: random_walk')
    print('K number of neurons to test')
    print('N number of inputs to test per neuron')
    print('L maximum value to test for weights')
    print('n the number of simulations per configuration of K, N, and L')
    print('t the time in seconds before the simulation terminates (default 20.0)')
    print('(stop simulation for unsuccessful synchronizations)')


def main():
    """
    From testing and Neural Synchronization and Cryptography, Ruttor 2006 it was found, that values of K > 2
    are beneficial to ensure a smaller amount of repulsive moves.
    Ruttor also shows on pages 38-39, that the synchronization time is strictly dependent on m = 2 * L + 1,
    with the standard deviation increasing drastically with larger m.
    Page 42 shows, that the average synchronization time increases linearly with N.
    On page 57 can be seen, that for the geometric attack (not the here employed simlpe attack) the success probability
    for Eve decreases exponentially for K >=3 with L.
    
    Further testing revealed, that the runtime for networks with K > 5, N > 10 and L > 10 is really bad (10-30 seconds),
    thus the reduced test values are used, feel free to test on your own.
    """

    # Default values to use
    k_set = [2, 3, 4]
    n_set = [2, 3, 4]
    l_set = [2, 3, 4]
    time_threshold = 20.0
    nb_simulations = 100  # The simulations to run for the given configuration
    update_rule = 2  # Use random walk as learning rule, has highest relative entropy
    key_length = 256  # bits
    iv_length = 0  # bits

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hK:N:L:t:r:n:", ["K=", "N=", "L=", "t=", "r=", "n="])
    except getopt.GetoptError:
        print('unknown options')
        print_opts()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print_opts()
            sys.exit()
        if opt in ("-r", "--r"):
            if arg not in ['hebbian', 'anti_hebbian', 'random_walk']:
                print('unknown update rule: ' + arg)
                print('available options:')
                print('hebbian, anti_hebbian, random_walk (default)')
                sys.exit()
            else:
                if str(arg) == 'hebbian':
                    update_rule = 0
                elif str(arg) == 'anti_hebbian':
                    update_rule = 1
                else:
                    update_rule = 2
        elif opt in ("-K", "--K"):
            k_set = [int(x) for x in arg.split(".")]
        elif opt in ("-N", "--N"):
            n_set = [int(x) for x in arg.split(".")]
        elif opt in ("-L", "--L"):
            l_set = [int(x) for x in arg.split(".")]
        elif opt in ("-t", "--t"):
            time_threshold = float(arg)
        elif opt in ("-n", "--n"):
            nb_simulations = int(arg)

    with open('../data/collectedData.csv', 'w') as f:
        # Write the CSV header
        f.write("K,N,L,ABUpdates,EUpdates,SyncAB,SyncAE,KeyA,KeyB,KeyE\n")

        for k in k_set:
            for n in n_set:
                for l in l_set:
                    # clean out the data to be less memory hungry
                    data = list()

                    print("{} {} {}:".format(k, n, l))
                    start_time = time.time()

                    for i in range(nb_simulations):
                        # Measure time for one run
                        s_time = time.time()

                        data.append(run(k, n, l, key_length, iv_length, update_rule, time_threshold))

                        # print the time the run took
                        e_time = time.time()
                        print(e_time - s_time)

                    # after a configuration was run for 100 times write out the data
                    for item in data:
                        f.write("{}\n".format(item))

                    print(time.time() - start_time)


if __name__ == "__main__":
    main()
