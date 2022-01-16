from itertools import product
from timeit import default_timer


def loadWords():
    with open("words.txt", "r") as f:
        words = f.read().splitlines()
    return words


def genRandomWordsPasswords(nums):
    words = loadWords()
    passwords = [""]
    for _ in range(nums):
        p = ["".join(x) for x in list(product(passwords, words))]
        passwords = p
    return passwords


start = default_timer()
genRandomWordsPasswords(2)
end = default_timer()
print("Runtime: {}".format(end - start))
