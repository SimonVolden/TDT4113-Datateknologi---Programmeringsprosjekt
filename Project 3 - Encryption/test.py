import ascii
import crypto_utils as crypto
from numpy import power
text = "HEMMELIGHET"

key = "PIZZA"
#alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
                    #"N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
alphabet = [chr(i) for i in range(127)][32:126]
encrypted_string = ""

length_of_text = len(text)
length_of_key = len(key)

#print((length_of_text//length_of_key) + 1)
extended_list = list(key)*(length_of_text//length_of_key + 1)
print(extended_list)
matched_list = extended_list[:len(text)]
print(matched_list)
for i in matched_list:
    matched_list[matched_list.index(i)] = alphabet.index(i)
print(matched_list)

for i in range(len(text)):
            encrypted_string = encrypted_string + \
                               alphabet[(alphabet.index(str(text[i])) + matched_list[i]) % 95]

print(encrypted_string)

text = ""

for i in range(len(encrypted_string)):
            text = text + \
                               alphabet[(alphabet.index(str(encrypted_string[i])) - matched_list[i]) % 95]
print(text)

asciiList = [chr(i) for i in range(127)]
print(asciiList[32:126])

alphabet = [chr(i) for i in range(127)][32:126]
print(alphabet)
print(len(alphabet))

encrypted_code = crypto.blocks_from_text("Hello", 1)
print("Encrypted")
print(encrypted_code[0])
print(encrypted_code[0]*2 % 2)
code = crypto.text_from_blocks(encrypted_code, 1)
print(code)
counter = 0
with open("english_words.txt", 'r') as words:
    for line in words.readlines():
        counter += 1
        if line.strip() == "dog":
            print(line)
            print(counter)

with open("english_words.txt", 'r') as words:
    if "dog" in words.read():
        print("dogs")






