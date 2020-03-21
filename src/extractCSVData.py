import pandas as pd
import numpy as np

k_set = [3, 4, 5]
n_set = [4, 6, 8, 10]
l_set = [4, 6, 8, 10]

# Load the data
df = pd.read_csv("../data/collectedData.csv")

# Remove uninteresting data
del df["KeyA"]
del df["KeyB"]
del df["KeyE"]

data = list()

for k in k_set:
    for n in n_set:
        for l in l_set:
            # Create the selection vectors for the current configuration
            k_rows = df["K"] == k
            n_rows = df["N"] == n
            l_rows = df["L"] == l
            AB_rows = df["SyncAB"] == 100.0
            AE_rows = df["SyncAE"] == 100.0

            # Select all rows for the configuration where A & B synchronize
            configuration_sync = np.array(df[k_rows & n_rows & l_rows & AB_rows].values)
            # Select all rows for the configuration where A & B & E synchronize
            configuration_attack = np.array(df[k_rows & n_rows & l_rows & AB_rows & AE_rows].values)

            data.append(
                # Calculate the mean for all fields, put the resulting vector into a list and turn it into a string
                str(list(configuration_sync.mean(axis=0))).replace("[", "").replace("]", "").replace(" ", "") + "," +
                # Append the minimal and maximal number of rounds needed for synchronization
                str(configuration_sync[:, 3].min()) + "," + str(configuration_sync[:, 3].max()) + "," +
                # Append the success rate for the simple attack
                str(configuration_attack.shape[0] / configuration_sync.shape[0]) + "," +
                # Append the sample size to understand relevance of the success rate of the simple attack
                str(configuration_sync.shape[0])
            )

with open('../data/collectedDataSync.csv', 'w') as f:
    f.write("K,N,L,ABUpdates,EUpdates,SyncAB,SyncAE,UpdatesABmin,UpdatesABmax,SyncAESuccess,SampleSize\n")
    for line in data:
        f.write(line + "\n")
