def get_single_run():
    """
    Generator Function returning the data for a single run, such that it can be processed
    :return:
    """
    with open('collectedData.txt', 'r') as f:
        # Create an empty list
        data = []
        for line in f:
            # Line == "\n" once we have data for a single run
            if line == "\n":
                # Append the data
                yield data
                data = []
            else:
                data.append(line.strip())


def extract_relevant_data(data):
    """
    Extracts the data we are interested in and returns it as a comma separated string
    :param data: a list of strings
    :return: comma separated string of values
    """
    string = ""

    # Extract the parameters K, N, and L
    parameters = data[0].replace(",", "").replace("K=", "").replace("N=", "").replace("L=", "").split()[1:4]
    string += parameters[0] + "," + parameters[1] + "," + parameters[2]

    # Extract the number of Updates for Alice & Bob as well as for Eve
    string += data[1].replace("ABUpdates: ", ",").replace(" EUpdates: ", ",")

    # Extract the sync success for AB and AE
    string += data[2].replace("Sync AB: ", ",").replace(" AE: ", ",")

    # Extract the generated keys
    string += data[3].replace("Alice's key & iv length = 32byte (256bit), key: ", ",").replace(" iv:", ",")
    string += data[4].replace("Bob's   key & iv length = 32byte (256bit), key: ", "").replace(" iv:", ",")
    string += data[5].replace("Eve's   key & iv length = 32byte (256bit), key: ", "").replace(" iv:", "\n")

    return string


def main():
    with open('collectedData.csv', 'w') as f:
        # Write the CSV header
        f.write("K,N,L,ABUpdates,EUpdates,SyncAB,SyncAE,KeyA,KeyB,KeyE\n")

        # Write the comma separated values to the file
        for i, tmp in enumerate(get_single_run()):
            f.write(extract_relevant_data(tmp))


if __name__ == '__main__':
    main()
