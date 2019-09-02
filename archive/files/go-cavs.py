import csv

def extract_data(filename, column_names):

    filecsv = open(filename)               # Reads in CSV file
    input_file = csv.DictReader(filecsv)   # creates a dictionary for each row

    list = []


    for line in input_file:
            
            player_dict = {}

            player = line['Player']
            player = player.replace("'",'')
            player_dict['Name'] = player

            minutes = line['min']
            minutes = minutes.replace(" ",'')
            player_dict['Mins'] = minutes

            points = line['pts']
            points = points.replace(" ",'')
            player_dict['Points'] = points

            list.append(player_dict)

    return list

def print_stuff(list_of_dict):
    print list_of_dict
    for line in list_of_dict:

            player = line['Player']
            player = player.replace("'",'')
            minutes = line['min']
            minutes = minutes.replace(" ",'')
            points = line['pts']
            points = points.replace(" ",'')
            print "From the Cleveland Cavaliers", player, "played a total of", minutes, "and scored", points, "points."


def who_sucks(list_of_players, col):
    for player in list_of_players:

        if int(player[col]) >= 50:
            print player['Name'], "is the best player ever and he is the main reason why the Cavs made the playoffs."

        elif int(player[col]) > 10:
            print "Fine, I'll give", player['Name'], "some credit for helping the King in this game because he scored,",player[col], "points."

        else:
            print player['Name'], "did not contribute to this game at all in terms of points. Bro, you only scored", player[col],"the whole game! Get your shit together!"

def intro():
    print "This is Elizabeth's attempt to analyze the 2018 NBA Finals Game 1 with Python!"

def main():
    intro()
    val = extract_data('game1.csv', ['Player', 'min', 'pts'])
    print "This is our team data!"
    print
    print val
    print
    print "Now, let's see how each player is contributing to the King's road to the 2018 Finals Championship..."
    print
    who_sucks(val, 'Points')

if __name__ == "__main__":
     main()
