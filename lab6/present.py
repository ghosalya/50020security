#!/usr/bin/env python3

# Present skeleton file for 50.020 Security
# Oka, SUTD, 2014

# constants
FULLROUND = 31

# S-Box Layer
sbox = [0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD,
        0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2]

sbox_inv = [0x5, 0xE, 0xF, 0x8, 0xC, 0x1, 0x2, 0xD,
            0xB, 0x4, 0x6, 0x3, 0x0, 0x7, 0x9, 0xA]

# PLayer
pmt = [0, 16, 32, 48, 1, 17, 33, 49, 2, 18, 34, 50, 3, 19, 35, 51,
       4, 20, 36, 52, 5, 21, 37, 53, 6, 22, 38, 54, 7, 23, 39, 55,
       8, 24, 40, 56, 9, 25, 41, 57, 10, 26, 42, 58, 11, 27, 43, 59,
       12, 28, 44, 60, 13, 29, 45, 61, 14, 30, 46, 62, 15, 31, 47, 63]

# Rotate left: 0b1001 --> 0b0011


def rol(val, r_bits, max_bits): return \
    (val << r_bits % max_bits) & (2**max_bits - 1) | \
    ((val & (2**max_bits - 1)) >> (max_bits - (r_bits % max_bits)))

# Rotate right: 0b1001 --> 0b1100


def ror(val, r_bits, max_bits): return \
    ((val & (2**max_bits - 1)) >> r_bits % max_bits) | \
    (val << (max_bits - (r_bits % max_bits)) & (2**max_bits - 1))


def genRoundKeys(key):
    # blen = key.bit_length()
    blen = 80

    current_key = key
    round_keys = [32, current_key >> 16]

    for i in range(1, FULLROUND + 3):

        # step 1
        key1 = rol(current_key, 61, 80)

        # step 2
        front_key = key1 >> 76
        key2f_ = sbox[front_key]
        key2f = key2f_<< 76
        key2b = key1 & ((1 << 76) -1)
        key2 = key2f + key2b

        # step 3
        mask3 = ((1 << 5) -1) << 15
        key3pre = key2 & mask3
        key3xor = ((key3pre >> 15) ^ i)
        key3 = (key2 & ~mask3) + (key3xor << 15)

        # finally updating key
        current_key = key3
        round_keys.append(current_key >> 16)

    return round_keys


def addRoundKey(state, Ki):
    return state ^ Ki

def sBoxLayer(state, inv=False):
    output = 0
    for i in range(16):
        inp = ((state >> (i*4)) & 15)
        if inv:
            outp = sbox_inv[inp]
        else:
            outp = sbox[inp]
        output += (outp << (i*4))
    return output

def pLayer(state):
    statelist = []
    state_ = state
    while state_ > 1:
        statelist = [state_%2] + statelist
        state_ = state_ >> 1
    # final leftmost bit
    statelist = [state_] + statelist 
    statelist_ = statelist[::-1]

    # permutating
    newlist = [0] * 64
    for i in range(len(statelist)):
        newlist[pmt[i]] = statelist_[i]

    newlist = newlist[::-1]

    # combination
    result = 0
    for j in newlist:
        result = result << 1
        result += j

    return result


def present_round(state, roundKey):
    s1 = addRoundKey(state, roundKey)
    # print('s1', s1)
    s2 = sBoxLayer(s1)
    # print('s2', s2)
    s3 = pLayer(s2)
    # print('cipher', s3)
    return s3


def present_inv_round(state, roundKey):
    # pLayer inverse - do twice
    s3 = pLayer(pLayer(state))
    # print('inv-s2',s3)
    s2 = sBoxLayer(s3, inv=True)
    # print('inv-s1',s2)
    s1 = s2 ^ roundKey
    # print('inv-plain',s1)
    return s1


def present(plain, key):
    K = genRoundKeys(key)
    state = plain
    for i in range(1, FULLROUND + 1):
        state = present_round(state, K[i])
    state = addRoundKey(state, K[32])
    return state


def present_inv(cipher, key):
    K = genRoundKeys(key)
    state = cipher
    state = addRoundKey(state, K[32])
    for i in range(FULLROUND, 0, -1):
        state = present_inv_round(state, K[i])
    return state

if __name__ == "__main__":
    # Testvector for key schedule
    key1 = 0x00000000000000000000
    keys = genRoundKeys(key1)
    keysTest = {0: 32, 1: 0, 2: 13835058055282163712, 3: 5764633911313301505, 4: 6917540022807691265, 5: 12682149744835821666, 6: 10376317730742599722, 7: 442003720503347, 8: 11529390968771969115, 9: 14988212656689645132, 10: 3459180129660437124, 11: 16147979721148203861, 12: 17296668118696855021, 13: 9227134571072480414, 14: 4618353464114686070, 15: 8183717834812044671, 16: 1198465691292819143, 17: 2366045755749583272, 18: 13941741584329639728, 19: 14494474964360714113, 20: 7646225019617799193, 21: 13645358504996018922, 22: 554074333738726254, 23: 4786096007684651070, 24: 4741631033305121237, 25: 17717416268623621775, 26: 3100551030501750445, 27: 9708113044954383277, 28: 10149619148849421687, 29: 2165863751534438555, 30: 15021127369453955789, 31: 10061738721142127305, 32: 7902464346767349504}
    for k in keysTest.keys():
        assert keysTest[k] == keys[k]
    
    # Testvectors for single rounds without keyscheduling
    # IS TEST CORRECT??
    plain1 = 0x0000000000000000
    key1 = 0x00000000000000000000
    round1 = present_round(plain1, key1)
    round11 = 0xffffffff00000000
    assert round1 == round11 

    round2 = present_round(round1, key1)
    round22 = 0xff00ffff000000
    assert round2 == round22

    round3 = present_round(round2, key1)
    round33 = 0xcc3fcc3f33c00000
    assert round3 == round33

    # invert single rounds
    plain11 = present_inv_round(round1, key1)
    assert plain1 == plain11
    round2 = present_round(round1, key1)
    plain22 = present_inv_round(round2, key1)
    assert round1 == plain22
    plain33 = present_inv_round(round3, key1)
    assert round2 == plain33
    
    # Everything together
    plain1 = 0x0000000000000000
    key1 = 0x00000000000000000000
    cipher1 = present(plain1, key1)
    plain11 = present_inv(cipher1, key1)
    assert plain1 == plain11

    plain2 = 0x0000000000000000
    key2 = 0xFFFFFFFFFFFFFFFFFFFF
    cipher2 = present(plain2, key2)
    plain22 = present_inv(cipher2, key2)
    assert plain2 == plain22

    plain3 = 0xFFFFFFFFFFFFFFFF
    key3 = 0x00000000000000000000
    cipher3 = present(plain3, key3)
    plain33 = present_inv(cipher3, key3)
    assert plain3 == plain33

    plain4 = 0xFFFFFFFFFFFFFFFF
    key4 = 0xFFFFFFFFFFFFFFFFFFFF
    cipher4 = present(plain4, key4)
    plain44 = present_inv(cipher4, key4)
    assert plain4 == plain44

    print("All test passed!")