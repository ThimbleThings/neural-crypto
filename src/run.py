from tpm import TPM
import numpy as np
import time, sys, getopt
import matplotlib.pyplot as plt


def random(K, N, L):
    '''random
    return a random vector input for TPM
    '''

    return np.random.randint(-L, L + 1, [K, N])


def sync_score(TPM1, TPM2, L):
    '''sync_score
    Synchronize the score of 2 tree parity machines
    TPM1 - Tree Parity Machine 1
    TPM2 - Tree Parity Machine 2
    '''

    return 1.0 - np.average(1.0 * np.abs(TPM1.W - TPM2.W) / (2 * L))


def main(argv):
    # default Tree Parity Machine parameters
    K = 8
    N = 12
    L = 4
    key_length = 128  # bits
    iv_length = 128  # bits
    update_rules = ['hebbian', 'anti_hebbian', 'random_walk']
    update_rule = 'hebbian'
    input_file = ''
    output_file = 'out.enc'
    has_input_file = False
    try:
        opts, args = getopt.getopt(argv, "hK:N:L:k:v:i:o:r:", ["K=", "N=", "L=", "k=", "v=", "i=", "o=", "r="])
    except getopt.GetoptError:
        print('unknown options')
        print('run.py -r hebbian -i <input file> -o <output file> -K <nb hidden neurons> -N' +
              ' <nb input neurons> -L <range of weight> -k <key length> -v <iv length>')
        print('update rule : hebbian, anti_hebbian, random_walk')
        print('key length options : 128, 192, 256')
        print('iv length : [0:256] multiple of 4')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('run.py -r hebbian -i <input file> -o <output file> -K <nb hidden neurons> -N' +
                  ' <nb input neurons> -L <range of weight> -k <key length> -v <iv length>')
            print('update rule : hebbian, anti_hebbian, random_walk')
            print('default values : K=8, N=12, L=4')
            print('key length options : 128, 192, 256 bit')
            print('iv length : [0:256] bit')
            sys.exit()
        elif opt in ("-i", "--i"):
            has_input_file = True
            input_file = arg
        elif opt in ("-o", "--o"):
            output_file = int(arg)
        elif opt in ("-K", "--K"):
            K = int(arg)
        elif opt in ("-N", "--N"):
            N = int(arg)
        elif opt in ("-L", "--L"):
            L = int(arg)
        elif opt in ("-v", "--v"):
            iv_length = int(arg)
        elif opt in ("-r", "--r"):
            update_rule = str(arg)
            if update_rule not in update_rules:
                print('unknown update rule: ' + update_rule)
                print('available options:')
                print(update_rules)
                sys.exit()
        elif opt in ("-k", "--k"):
            if arg == "128" or arg == "192" or arg == "256":
                key_length = int(arg)
            else:
                print('non available key options')
                print('key length options : 128, 192, 256')
                sys.exit()

    # Create TPM for Alice, Bob and Eve. Eve eavesdrops communication of Alice and Bob
    print("Parameters: K=" + str(K) + ", N=" + str(N) + ", L=" +
          str(L) + ", k=" + str(key_length) + ", v=" + str(iv_length))
    Alice = TPM(K, N, L)
    Bob = TPM(K, N, L)
    Eve = TPM(K, N, L)

    # Synchronize weights
    nb_updates = 0
    nb_eve_updates = 0
    start_time = time.time()  # Start time
    sync_history = []  # plot purpose
    sync_history_eve = []  # plot purpose
    score = 0  # synchronisation score of Alice and Bob

    while score < 100:

        X = random(K, N, L)  # Create random vector [K, N]

        # compute outputs of TPMs
        tauA = Alice.get_output(X)
        tauB = Bob.get_output(X)
        tauE = Eve.get_output(X)

        # Alice and Bob would update only if tauA == tauB
        if tauA == tauB:
            Alice.update(update_rule)
            Bob.update(update_rule)
            nb_updates += 1

        # Eve would update only if tauA = tauB = tauE
        if tauA == tauB == tauE:
            Eve.update(update_rule)
            nb_eve_updates += 1


        # sync of Alice and Bob
        score = 100 * sync_score(Alice, Bob, L)  # Calculate the synchronization of Alice and Bob
        sync_history.append(score)  # plot purpose
        # sync of Alice and Eve
        score_eve = 100 * sync_score(Alice, Eve, L)  # Calculate the synchronization of Alice and Eve
        sync_history_eve.append(score_eve)  # plot purpose

        # When the networks take longer than 30 seconds to synchronize terminate
        if time.time() - start_time > 30.0:
            break

        # sys.stdout.write("\r" + "Synchronization = " + str(int(score)) + "%   /  Updates = " + str(
        #    nb_updates) + " / Eve's updates = " + str(nb_eve_updates))

    print("ABUpdates: " + str(nb_updates) + " EUpdates: " + str(nb_eve_updates))
    print("Sync AB: " + str(int(sync_history[-1])) + " AE: " + str(int(sync_history_eve[-1])))

    end_time = time.time()
    time_taken = end_time - start_time

    # results
    # print("\nTime taken = " + str(time_taken) + " seconds.")
    Alice_key, Alice_iv = Alice.makeKey(key_length, iv_length)
    Bob_key, Bob_iv = Bob.makeKey(key_length, iv_length)
    Eve_key, Eve_iv = Eve.makeKey(key_length, iv_length)

    # The key is a string of hex values, thus the length has to be divided by 2 to get the number of bytes.
    # Or multiplied by 4 to get the number of bits.
    print("Alice's key & iv length = " + str(int(len(Alice_key) / 2)) + "byte (" + str(len(Alice_key) * 4) +
          "bit), key: " + Alice_key + " iv: " + Alice_iv)
    print("Bob's   key & iv length = " + str(int(len(Bob_key) / 2)) + "byte (" + str(len(Bob_key) * 4) +
          "bit), key: " + Bob_key + " iv: " + Bob_iv)
    print("Eve's   key & iv length = " + str(int(len(Eve_key) / 2)) + "byte (" + str(len(Eve_key) * 4) +
          "bit), key: " + Eve_key + " iv: " + Eve_iv)

    if Alice_key == Bob_key and Alice_iv == Bob_iv:
        if has_input_file:
            import subprocess
            # cipher with AES 
            bashCommand = "openssl enc -aes" + str(key_length) + " -K " + Alice_key + " -iv " + Alice_iv + " -in " + \
                          input_file + " -out " + output_file
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            # decipher with AES
            bashCommand = "openssl enc -aes" + str(key_length) + " -K " + Alice_key + " -iv " + Alice_iv + " -in " + \
                          output_file + " -out " + "decipher.txt" + " -d"
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            print("encryption and decryption with aes" + str(key_length) + " done.")

    #else:
    #    print("error, Alice and Bob have different key or iv : cipher impossible")

    '''
    # Plot graph
    plt.figure(1)
    plt.title('Synchronisation')
    plt.ylabel('sync %')
    plt.xlabel('nb iterations')
    sync_AB, = plt.plot(sync_history)
    sync_Eve, = plt.plot(sync_history_eve)
    plt.legend([sync_AB, sync_Eve], ["sync Alice Bob", "sync Alice Eve"])
    plt.show()
    '''


if __name__ == "__main__":
    main(sys.argv[1:])
