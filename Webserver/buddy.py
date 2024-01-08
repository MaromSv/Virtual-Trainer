import copy
#Single entry: [ID, Experience, Age, Gender, GenderPreference, DaysAvailable, ExperiencePreference, AgeGroupPref]
#ID = int
#Experience = {'Beginner', 'Intermediate', 'Advanced'}, Age = int, Gender = {'Male', 'Female', 'Other'}, 
#GenderPreference = {'Same', 'Any'}, DaysAvailable = [Bool, Bool, Bool, Bool, Bool, Bool, Bool]
#ExperiencePreference = [Bool, Bool, Bool], AgeGroupPref = {'Similair', 'Any'}



buddies = [
    [2,'Beginner', 21, 'Male', 'Same', [True, True, False, False, True, True, False], [True, True, True], 'Any'],
    [6,'Advanced', 12, 'Female', 'Same', [True, False, False, False, True, False, False], [False, False, True], 'Similair'], 
    [1,'Intermediate', 31, 'Male', 'Any', [False, False, False, False, True, True, False], [True, True, True], 'Any'], 
    [11,'Advanced', 10, 'Male','Same', [False, False, False, False, True, True, False], [True, True, True], 'Any'], 
    [12,'Beginner', 25, 'Female','Any', [False, True, False, False, False, False, False], [True, False, False], 'Any'],
    [3,'Beginner', 63, 'Male','Any', [False, False, False, False, False, False, False], [True, False, False], 'Any']
    ]

def removeBadIndicies(listOfStuff, badIndicies):
    for index in badIndicies:
        listOfStuff.pop(index)
    return listOfStuff

def findBuddy(ID, Experience, Age, Gender, GenderPreference, DaysAvailable, ExperiencePreference, AgeGroupPref):
    #Make a copy of the buddies table
    possibleBuddies = copy.deepcopy(buddies)
    badBuddyIndicies = []

    #Remove yourself from possible buddies:
    for index, buddy in enumerate(possibleBuddies):
            if buddy[0] == ID:
                badBuddyIndicies.append(index)

    #Remove all possible buddies that dont abide by gender requirement
    if GenderPreference == 'Same':
        for index, buddy in enumerate(possibleBuddies):
            if buddy[3] != Gender:
                badBuddyIndicies.append(index)
    
    #Remove people that dont share days with you
    for index, buddy in enumerate(possibleBuddies):
        sharedDay = False
        for i in range(7):
            if buddy[5][i] == True and DaysAvailable[i] == True:
                sharedDay = True

        if sharedDay == False:
            badBuddyIndicies.append(index)

    #Remove people that dont share experience with you
    for i in range(len(ExperiencePreference)):
        if ExperiencePreference[i] == False and i == 0:
            for index, buddy in enumerate(possibleBuddies):
                if buddy[1] == 'Beginner':
                    badBuddyIndicies.append(index)
        elif ExperiencePreference[i] == False and i == 1:
            for index, buddy in enumerate(possibleBuddies):
                if buddy[1] == 'Intermediate':
                    badBuddyIndicies.append(index)
        elif ExperiencePreference[i] == False and i == 2:
            for index, buddy in enumerate(possibleBuddies):
                if buddy[1] == 'Advanced':
                    badBuddyIndicies.append(index)

    #Remove duplicates from badBuddyIndicies
    badBuddyIndicies = list(dict.fromkeys(badBuddyIndicies))
    badBuddyIndicies.sort(reverse=True)
    #Remove unsuitable buddies
    possibleBuddies = removeBadIndicies(possibleBuddies, badBuddyIndicies)

    buddyAgeDifferences = []
    for buddy in possibleBuddies:
        buddyAgeDifferences.append((buddy[0], abs(buddy[2] - Age)))
    
    sorted (
    buddyAgeDifferences, 
    key=lambda x: x[1]
    )

    return buddyAgeDifferences[0][0]

a = findBuddy(2,'Beginner', 21, 'Male', 'Same', [True, True, False, False, True, True, False], [True, True, True], 'Any')

print(a)