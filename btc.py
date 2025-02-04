# -*- coding: utf-8 -*-
import random
import hashlib

IS_RAND_DICE = True
IS_TEST = False
IS_PRINT_WORD = True
DICE_COUNT = 100 
MAX_LEN = 256
VALUE_CNT = 11
BIP_0039 = []
with open("./bip_0039", "r") as rf:
	for line in rf.readlines():
		BIP_0039.append(line.strip())

# INPUT -----------
dice_list = [1,2,3]
binary_list = []
binary_list_str = ""

if IS_RAND_DICE:
	dice_list = [random.randint(1, 8)-1 for _ in range(DICE_COUNT)]
print("dice_list:", dice_list)

for x in dice_list:
	for i in range(3):
		if len(binary_list) >= MAX_LEN:
			break
		binary_value = (x>>(2-i)&1)
		binary_list.append(binary_value)
		binary_list_str += str(binary_value)
	if len(binary_list) >= MAX_LEN:
		break
if IS_TEST:
	binary_list_str = "1100001101100100000111111000010101000100110101111100000000101111001101011000000010110000011111000000111110011000100001111111000011000110101000100111111111110101101010110001110101001010001111100010100111001010111100011001011111001111110000101001100110101110" 
print("binary_list len:", len(binary_list))
print("binary_list:", binary_list)
print("binary_list_str:", binary_list_str)

# 将二进制字符串转换为整数
binary_int = int(binary_list_str, 2)
# 将整数转换为 32 字节（256 位）的二进制数据
binary_data = binary_int.to_bytes(32, byteorder='big')
# 计算 SHA-256 哈希值
sha256_hash = hashlib.sha256(binary_data).digest()
# 取哈希的前 8 位（第一个字节）
first_8_bits = bin(sha256_hash[0])[2:].zfill(8)
print("first_8_bits:", first_8_bits)


final_value_list = []
final_binary_list_str = binary_list_str + first_8_bits
start_index = 0
cnt = 0
for x in reversed(final_binary_list_str):
	cnt += 1
	start_index += 1
	if cnt == 11: 
		final_value_list.append(int(final_binary_list_str[start_index-VALUE_CNT: start_index], 2))
		cnt = 0
print("final_value_list:", final_value_list)

if IS_PRINT_WORD:
	final_bip_list = []
	for i,x in enumerate(final_value_list):
		final_bip_list.append(BIP_0039[x])
		# print(i+1, BIP_0039[x-1])
	print(" ".join(final_bip_list))
