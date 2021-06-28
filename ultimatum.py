import random
import os
import csv


class Player(object):
    def __init__(self, name, points=0):
        self.name = name
        self.points = points
        self.num_responses = 0
        self.num_proposals = 0

    def __repr__(self):
        return self.name + ' (' + str(self.points) + ' points)'


def say(string, priority=3):
    print(string)
    if priority <= speech_priority:
        os.system("say " + string)


def addGamesToQueue(queue, players):
    ids = list(range(len(players)))
    props = list()
    resps = list()
    random.shuffle(ids)
    for i in range(0, len(players), 2):
        props.append(ids[i])
        resps.append(ids[i + 1])
        queue.append((ids[i], ids[i + 1]))
    random.shuffle(props)
    random.shuffle(resps)
    for i in range(len(props)):
        queue.append((resps[i], props[i]))


def createFile(filename):
    numPlayers = int(input("How many players are there? "))
    players = []
    for i in range(numPlayers):
        players.append(input())
    file = open(filename, "w")
    file.write(str(len(players)) + '\n')
    for player in players:
        file.write(player + ',0\n')
    file.write('0\n')


def loadFile(filename):
    file = open(filename, 'r')
    n = int(file.readline())
    players = []
    for i in range(n):
        player = file.readline().strip().split(',')
        players.append(Player(player[0], int(player[1])))

    k = int(file.readline())
    queue = []
    for i in range(k):
        game = file.readline().strip().split(',')
        queue.append((int(game[0]), int(game[1])))

    return players, queue


def writeToFile(filename, players, queue):
    file = open(filename, "w")
    file.write(str(len(players)) + '\n')
    for player in players:
        file.write(str(player.name) + ',' + str(player.points) + '\n')
    file.write(str(len(queue)) + '\n')
    for game in queue:
        file.write(str(game[0]) + ',' + str(game[1]) + '\n')
    return True


def getProposal():
    def isValid(k):
        return k.isdigit() and 0 <= int(k) <= 10
    k = input()
    while not isValid(k):
        say("That is an invalid input. Please try again: ")
        k = input()
    return int(k)


def getResponse():
    responses = {"y": True, "n": False}
    S = input()
    while not(S.lower()[0] in responses):
        S = input()
    return responses[S.lower()[0]]

def createFileFromNames(namefile, gamefile):
    players = []
    queue = []
    for line in open(namefile, 'r'):
        players.append(Player(line.strip()))
    writeToFile(gamefile, players, queue)

def play(gamefile):
    players, queue = loadFile(gamefile)
    say("Good evening, young contestants. My name is Mr. Hera. Welcome to the ultimatum game.", 1)
    round_num = 1
    # Play them!
    while queue:
        proposer_id, responder_id = queue.pop()
        proposer = players[proposer_id]
        responder = players[responder_id]
        proposer.num_proposals += 1
        responder.num_responses += 1
        print("\n" * 5 + "#" * 30)
        say("Round " + str(round_num), 1)
        say("The proposer is " + proposer.name +
            ", and the responder is " + responder.name, 2)
        say(proposer.name + ", out of 10 units, how many do you propose to give " +
            responder.name + '?', 3)
        proposal = getProposal()
        say(responder.name + ", do you accept the proposal of " +
            str(proposal) + " units?")
        response = getResponse()
        if response:
            proposer.points += 10 - proposal
            responder.points += proposal
        round_num += 1
        writeToFile(gamefile, players, queue)
    say("And with that, we've reached the end of the queue. Thanks for playing!", 1)

def addRoundsToFile(filename, numRounds):
    players, queue = loadFile(filename)
    for i in range(numRounds):
        addGamesToQueue(queue, players)
    writeToFile(filename, players, queue)

# MANDATORY SETTINGS
speech_priority = 2

# CODE
filename = 'game2.csv'
#
# createFileFromNames('names.txt', filename)
# addRoundsToFile(filename, 2)

play(filename)
