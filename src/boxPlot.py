import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

csv_in_file = input("Path to the CSV Data File: ")
k_vals = input("Integer Values for K (separated by a '.'): ")
n_vals = input("Integer Values for N (separated by a '.'): ")
l_vals = input("Integer Values for L (separated by a '.'): ")

k_set = [int(x) for x in k_vals.split(".")]
n_set = [int(x) for x in n_vals.split(".")]
l_set = [int(x) for x in l_vals.split(".")]

# Load the data
df = pd.read_csv(csv_in_file)

# Remove uninteresting data
del df["KeyA"]
del df["KeyB"]
del df["KeyE"]

data = pd.DataFrame()

for k in k_set:
    for n in n_set:
        for l in l_set:
            # Create the selection vectors for the current configuration
            k_rows = df["K"] == k
            n_rows = df["N"] == n
            l_rows = df["L"] == l
            AB_rows = df["SyncAB"] == 100.0
            AE_rows = df["SyncAE"] == 100.0

            # Select all rows for the configuration where A & B synchronize and of this matrix the columns for ABUpdates
            data = pd.concat([data, pd.DataFrame(df[k_rows & n_rows & l_rows & AB_rows].ABUpdates.values,
                                                 columns=["K" + str(k) + ", N" + str(n) + ", L" + str(l)])], axis=1)

# Calculate the boxplot data for the ABUpdates columns
boxplot = data.boxplot()
boxplot.set_xlabel("TPM Parameters")
boxplot.set_ylabel("t_sync")

# Show the boxplot
plt.show()
