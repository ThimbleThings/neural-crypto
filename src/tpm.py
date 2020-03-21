import numpy as np
import hashlib


def theta(t1, t2):
    return t1 == t2


class TPM:
    '''TPM
    Tree Parity Machine is a special type of multi-layer feed-forward neural network.
    K - number of hidden neurons
    N - number of input neurons connected to each hidden neuron
    L - range of each weight ({-L,..,0,..,+L })
    W - weight matrix between input and hidden layers. Dimensions : [K, N]
    tau - output score
    '''

    def __init__(self, K=8, N=12, L=4, update_rule=0):
        '''
        Initialize TPM
        :param K: number of hidden neurons
        :param N: number of inputs per neuron
        :param L: range of discrete weights
        :param update_rule: Update rule for TPM weights
        '''

        self.K = K
        self.N = N
        self.L = L
        self.W = np.random.randint(-L, L + 1, [K, N])
        self.sigma = np.ndarray
        self.tau = 0

        # Use a function pointer instead of if/else construct to select update function
        if update_rule == 0:
            self.update_rule = self.hebbian
        elif update_rule == 1:
            self.update_rule = self.anti_hebbian
        else:
            self.update_rule = self.random_walk

    def get_output(self, X):
        '''
        Returns a binary digit tau for a given random vector.
        X - Input random vector
        '''

        X = X.reshape([self.K, self.N])

        '''
        np.sign() is defined as:
        np.sign(x) = -1 if x < 0, 0 if x = 0, 1 if x > 0
        But research papers suggest using a sign() defined as:
        sign(x) = -1, if x <= 0, and 1 if x > 0
        
        For reference see: Neural Synchronization and Cryptography, Ruttor 2006, Page 14.
        
        We know that the sum over the weighted inputs is always a whole integer.
        Thus we can subtract 0.5 and force the results of the calculation to always be
        either -1 or +1.
        The resulting sigma vector would be of type float, but we force it to be int.
        '''
        sigma = np.sign(np.sum(X * self.W, axis=1) - 0.5).astype(int)
        tau = np.prod(sigma)

        self.X = X
        self.sigma = sigma
        self.tau = tau

        return tau

    def hebbian(self):
        '''
        hebbian update rule
        '''

        for (i, j), _ in np.ndenumerate(self.W):
            self.W[i, j] += self.X[i, j] * self.tau * theta(self.sigma[i], self.tau)
            self.W[i, j] = np.clip(self.W[i, j], -self.L, self.L)

    def anti_hebbian(self):
        '''
        anti-hebbian update rule
        '''

        for (i, j), _ in np.ndenumerate(self.W):
            self.W[i, j] -= self.X[i, j] * self.tau * theta(self.sigma[i], self.tau)
            self.W[i, j] = np.clip(self.W[i, j], -self.L, self.L)

    def random_walk(self):
        '''
        random walk update rule
        '''

        for (i, j), _ in np.ndenumerate(self.W):
            self.W[i, j] += self.X[i, j] * theta(self.sigma[i], self.tau)
            self.W[i, j] = np.clip(self.W[i, j], -self.L, self.L)

    def update(self):
        '''
        Updates the weights according to the specified update rule.
        '''

        self.update_rule()

    # make key from weight matrix
    def makeKey(self, key_length, iv_length):
        '''makeKey
        weight matrix to key and iv : use sha256 on concatenated weights 
        '''

        key = ''
        iv = ''

        # generate key
        for (i, j), _ in np.ndenumerate(self.W):
            if i == j:
                iv += str(self.W[i, j])
            key += str(self.W[i, j])

        # sha256 iv
        hash_object_iv = hashlib.sha256(iv.encode("ascii"))
        hex_dig_iv = hash_object_iv.hexdigest()

        # sha256 key
        hash_object_key = hashlib.sha256(key.encode("ascii"))
        hex_dig_key = hash_object_key.hexdigest()

        # key & iv lengths are given in bits, divide by 4 to get number of chars in hex string
        return (hex_dig_key[0:int(key_length / 4)], hex_dig_iv[0:int(iv_length / 4)])
