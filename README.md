# Neural cryptography protocol for key exchange

Implementation of the key exchange protocol described in International Journal of Advanced Research in
Computer Science and Software Engineering.

Contrary to the statement in the original git, neural cryptography is not secure against a MITM Attack.
What neural cryptography provides is an alternative to the Diffie-Hellman key exchange without needing a trapdoor functionality like the modulo operation and integer factorization.

## openSSL
Require openSSL to encyrpt with AES cipher.

## Generate key and IV for AES encryption
```bash
python3 run.py -r hebbian -i <input file> -o <output file> -K <nb hidden neurons> -N <nb input neurons> -L <range of weight> -k <key length> -v <iv length>
```
r : update rules : 'hebbian', 'anti_hebbian' or 'random_walk'
key length options : 128, 192, 256
iv length : [0:256]
if inputfile is read, aes encryption is executed.

## Use with openSSL
if inputfile option not set, use openSSL to encrypt file.
### Cipher with AES
```bash
openssl enc -aes128 -K <key> -iv <init vector> -in <inputfile> -out <outputfile>
openssl enc -aes192 -K <key> -iv <init vector> -in <inputfile> -out <outputfile>
openssl enc -aes256 -K <key> -iv <init vector> -in <inputfile> -out <outputfile>
```
### Decipher with AES
```bash
openssl enc -aes128 -K <key> -iv <init vector> -in <inputfile(enc)> -out <outputfile> -d
openssl enc -aes192 -K <key> -iv <init vector> -in <inputfile(enc)> -out <outputfile> -d
openssl enc -aes256 -K <key> -iv <init vector> -in <inputfile(enc)> -out <outputfile> -d
```
## Examples
```bash
echo "hello world" > hello.txt
python3 run.py -i hello.txt -k 256 -K 20 -N 50 -L 6
cat out.enc
cat decipher.txt
```

![example1 synchronization of Alice and Bob](https://github.com/ThimbleThings/neural-crypto/blob/master/extras/ex1.png)
