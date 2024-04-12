
#13.)
# Teil a
def pad_key(plaintext, key):
    return (key * (len(plaintext) // len(key) + 1))[:len(plaintext)]

def xor_encrypt(plaintext, key):
    padded_key = pad_key(plaintext, key)
    ciphertext = bytes([a ^ b for (a, b) in zip(plaintext.encode(), padded_key.encode())])
    return ciphertext

def xor_decrypt(ciphertext, key):
    padded_key = pad_key(ciphertext.decode(), key)
    decrypted_text = bytes([a ^ b for (a, b) in zip(ciphertext, padded_key.encode())])
    return decrypted_text.decode()

# Teil b
def count_coincidences(ciphertext, shift):
    count = 0
    for i in range(len(ciphertext) - shift):
        if (ciphertext[i] ^ ciphertext[i + shift]) == 0:
            count += 1
    return count

def determine_key_length(ciphertext, threshold=0.0665):
    n = len(ciphertext)
    percentages = []
    for shift in range(1, len(ciphertext)):
        coincidence_count = count_coincidences(ciphertext, shift)
        percentage = coincidence_count / (n - shift)
        percentages.append((shift, percentage))

        if percentage > threshold:
            return shift, percentage, percentages
    return None, None, percentages

# 14.)
def hamming_distance(bytes1, bytes2):
    return sum(bin(b1 ^ b2).count('1') for b1, b2 in zip(bytes1, bytes2))

def normalized_hamming_distance(ciphertext, key_size):
    blocks = [ciphertext[i:i + key_size] for i in range(0, len(ciphertext), key_size)]
    distances = []
    for i in range(0, len(blocks) - 1):
        if len(blocks[i]) == key_size and len(blocks[i+1]) == key_size:
            distance = hamming_distance(blocks[i], blocks[i+1])
            distances.append(distance / key_size)
    return sum(distances) / len(distances) if distances else float('inf')

def find_key_length(ciphertext):
    key_sizes = range(1, len(ciphertext))
    normalized_distances = [(key_size, normalized_hamming_distance(ciphertext, key_size)) for key_size in key_sizes]
    return min(normalized_distances, key=lambda x: x[1])

plaintext = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam nec odio et odio fermentum fermentum."
key = "thisisakey"
ciphertext = xor_encrypt(plaintext, key)

key_length= find_key_length(ciphertext)

if key_length:
    print(key_length)