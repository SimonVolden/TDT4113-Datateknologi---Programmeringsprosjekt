from statistics import mode
import matplotlib.pyplot as plt

opponentsChoices =[1, 1, 2, 2, 1, 2, 2, 0, 1, 2, 2]

"""print(mode(opponentsChoices))

print((mode(opponentsChoices) + 2) % 3)

print(opponentsChoices[-3:])
print(tuple(opponentsChoices[-3:]))
"""
#counts = {}
remember = 1
nextPlayCounter = [0, 0, 0]
moves = ["Rock", "Paper", "Scissors"]

print(opponentsChoices[-remember:])
recent_sequence = opponentsChoices[-remember:]

for i in range(len(opponentsChoices) - remember):
    if opponentsChoices[i: i + remember] == recent_sequence:
        nextPlayCounter[opponentsChoices[i + remember]] += 1

print(nextPlayCounter)
print(moves[nextPlayCounter.index(max(nextPlayCounter))])


"""
counts = {}
lastSequence = tuple(plays[-2:])

lastSequenceRock = lastSequence + (0,)
lastSequenceScissors = lastSequence + (1,)
lastSequencePaper = lastSequence + (2,)


if lastSequenceRock in counts.keys():
    counts[lastSequenceRock] += 1


if lastSequenceScissors in counts.keys():
    counts[lastSequenceScissors] += 1


if lastSequencePaper in counts.keys():
    counts[lastSequencePaper] += 1
"""

plt.plot([1,1.5, 1.5])
plt.show()

