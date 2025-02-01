def reverse_words(sentence):
    words = sentence.split()
    reversed_words = words[::-1]
    return ' '.join(reversed_words)


original = "We are ready"
reversed_sentence = reverse_words(original)
print(reversed_sentence)