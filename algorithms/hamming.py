def difference(test: str, other: str) -> int:
    count = 0
    for i in range(len(test)):
        if test[i] != other[i]:
            count += 1
    return count


def generate_words(size: int, field: tuple = (0, 1), memo=None):
    if memo is None:
        memo = {}

    if size in memo:
        return memo[size]

    list_of_words = []
    for x in field:
        if size == 1:
            memo[size] = list(map(lambda w: str(w), field))
            return memo[size]
        else:
            for sub_word in generate_words(size - 1, field, memo):
                # print(f"sub--word:{sub_word}")
                sub_word += str(x)
                list_of_words.append(sub_word)
    memo[size] = list_of_words
    return memo[size]


def hamming_code_brute(n: int, d: int, m: int, field: tuple = (0, 1)):
    possible_words = generate_words(n, field)
    length = len(possible_words)
    print(possible_words)

    hamming_map = {}

    for test in possible_words:
        hamming_map[test] = []
        for other in possible_words:
            if test != other:
                if difference(test, other) == d:
                    hamming_map[test].append(other)
        hamming_map[test].append(test)
        if len(hamming_map[test]) < m:
            hamming_map.pop(test)

    for base in hamming_map.keys():
        sub_map = {}
        for test in hamming_map[base]:
            sub_map[test] = [test]
            for other in hamming_map[base]:
                if test != other:
                    if difference(test, other) == d:
                        sub_map[test].append(other)
            if len(sub_map[test]) >= m:
                print(len(sub_map[test]))
                return {base: sub_map[test]}
            else:
                sub_map.pop(test)
    return hamming_map


if __name__ == '__main__':
    print(len(generate_words(5)))
    print(difference("00000", "11111"))
    res = hamming_code_brute(8, 3, 30)
    for key in res.keys():
        print(f"{key}: {{{res[key]}}}")
