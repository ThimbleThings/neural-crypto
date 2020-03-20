import subprocess
import time

data = list()

"""
We want to test for different K, N, and L to empirically analyze the data
"""

k_set = [2, 3, 4, 5, 6, 7, 8]
n_set = [2, 4, 8]
l_set = [2, 4, 8, 16, 32, 64, 128, 256]

with open('collectedData.txt', 'w') as f:
    for k in k_set:
        for n in n_set:
            for l in l_set:
                # clean out the data to be less memory hungry
                data = list()

                start_time = time.time()
                for i in range(1000):
                    cmd = "python3 run.py -K" + str(k) + " -N" + str(n) + " -L" + str(l) + " -k256 -v0"
                    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
                    output, error = process.communicate()
                    data.append(output.decode())

                end_time = time.time()
                time_taken = end_time - start_time

                # after a configuration was run for 1000 times write out the data
                for item in data:
                    f.write("{}\n".format(item))
