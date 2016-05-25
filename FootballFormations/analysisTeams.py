import csv
import operator
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def writeFileResults(nameFile, raw):
    with open(nameFile, 'w+') as fResults:
        fResults.write(raw.encode('utf8'))

if __name__ == "__main__":
    teamName = "atleti"
    #teamName = "real-madrid"
    with open(teamName + '.csv', 'rb') as csvfile:
        dictTeam = {}
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            #print ', '.join(row)
            print row
            team = row[len(row)-1].split(',')
            team = team[len(team)-1]
            players = team.split('\t')
            for player in players:
                if player not in dictTeam:
                    dictTeam[player] = 1
                else:
                    dictTeam[player] += 1

        sorted_list = sorted(dictTeam.items(), key=operator.itemgetter(1), reverse=True)
        results = ""
        count = 0
        for player in sorted_list:
            count += 1
            results += player[0] + " " + str(player[1]) + "\n"
            if count == 11:
                results += "---------------------------------------\n"

        writeFileResults(teamName + "_analysis.txt", results)
