import pandas as pd
import matplotlib

matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import numpy as np

# csv_in_file = "../data/collectedDataSync 100 K3.4 N4.16.32 L4.6.8.10.12.csv"  # input("Path to the CSV Data File: ")
csv_in_file = "../data/collectedDataSync 100 K3.4.5 N4.6.8.10 L4.6.8.10.csv"  # input("Path to the CSV Data File: ")
# k_vals = "3.4"  # input("Integer Values for K (separated by a '.'): ")
k_vals = "3.4.5"  # input("Integer Values for K (separated by a '.'): ")
# n_vals = "4.16.32"  # input("Integer Values for N (separated by a '.'): ")
n_vals = "4.6.8.10"  # input("Integer Values for N (separated by a '.'): ")
# l_vals = "4.6.8.10.12"  # input("Integer Values for L (separated by a '.'): ")
l_vals = "4.6.8.10"  # input("Integer Values for L (separated by a '.'): ")

k_set = [int(x) for x in k_vals.split(".")]
n_set = [int(x) for x in n_vals.split(".")]
l_set = [int(x) for x in l_vals.split(".")]

# Load the data
df = pd.read_csv(csv_in_file)

# Remove uninteresting data
del df["EUpdates"]
del df["SyncAB"]
del df["SyncAE"]
del df["UpdatesABmin"]
del df["UpdatesABmax"]
del df["SyncAESuccess"]

data = pd.DataFrame()

# Extract the column of L values
k_rows = df["K"] == k_set[0]
n_rows = df["N"] == n_set[0]
data = pd.concat([data, pd.DataFrame(df[k_rows & n_rows].L.values, columns=["L"])], axis=1)

for k in k_set:
    for n in n_set:
        # Create the selection vectors for the current configuration
        k_rows = df["K"] == k
        n_rows = df["N"] == n

        # Select all rows for the configuration where A & B synchronize and of this matrix the columns for ABUpdates
        data = pd.concat([data, pd.DataFrame(df[k_rows & n_rows].ABUpdates.values,
                                             columns=["K" + str(k) + ", N" + str(n)])], axis=1)

# Sort the columns based on the values in the last row
data = data.sort_values(by=3, axis=1)

# Make data easily addressable for plotting
data_np = data.to_numpy()

colors = cm.jet(np.linspace(0, 1, data.shape[1] - 1))

for i in range(data.shape[1] - 1):
    plt.plot(data_np[:, 0], data_np[:, 1 + i], 'o', label=list(data.columns)[1 + i], color=colors[i])

plt.xticks(l_set)

# Make sure the label of each plot is shown
plt.legend()

# set the axis labels
plt.xlabel("Value of L")
plt.ylabel("Average t_sync")

# Show the boxplot
plt.show()
