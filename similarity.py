import string
import csv
# words to remove from document
STOP_WORDS = ['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am',
              'an', 'and', 'any', 'are', "aren't", 'as', 'at', 'be', 'because',
              'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by',
              "can't", 'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does',
              "doesn't", 'doing', "don't", 'down', 'during', 'each', 'few', 'for',
              'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't",
              'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers',
              'hereself', 'him', 'himself', 'his', 'how', "how's", 'i', "i'd", "i'll",
              "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its',
              'itself', "let's", 'me', 'more', 'most', "mustn't", 'my', 'myself', 'no',
              'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought',
              'our', 'ours', 'ourselves', 'out', 'own', 'same', "shan't", 'she', "she'd",
              "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such', 'than', 'that',
              "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's",
              'these', 'they', "they'd", "they'll", "they're", "they've", 'this', 'those', 'through',
              'to', 'too', 'under', 'until', 'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll",
              "we're", "we've", 'were', "weren't", 'what', "what's", 'when', "when's", 'where',
              "where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's", 'with', "won't",
              'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours',
              'yourself', 'yourselves'
              ]
# lev distance algorithm
def levDistance(ogString, cpString):
  rows = len(ogString)+1
  cols = len(cpString)+1
  distance = [[0 for x in range(cols)] for y in range(rows)]

  for i in range(1, rows):
    for k in range(1, cols):
      distance[i][0] = i
      distance[0][k] = k
  
  for col in range(1, cols):
    for row in range(1, rows):
      if( ogString[row-1] == cpString[col-1] ):
        cost = 0
      else:
        cost = 2
      
      distance[row][col] = min(distance[row-1][col] +1, distance[row][col-1] +1, distance[row-1][col-1] + cost)
  
  ratio = ( ( len(ogString) + len(cpString) - distance[row][col] ) / (len(ogString) + len(cpString)) )
  return ratio
  


# def mongeElkan(a, b):
#   sum =0
#   for x in a:
#     arr1= []
#     for j in b:
#       arr1.append(levDistance(x,j))
#     sum += max(arr1)
  
#   return sum/len(a)

  
# remove stop words and punctuation beacuse it does not give usefull information
def processStrings(string1, string2):
  result1 = string1.lower().translate(str.maketrans('', '', string.punctuation)).split()
  result2 = string2.lower().translate(str.maketrans('', '', string.punctuation)).split()
  
  for x in STOP_WORDS:
    for y in result1:
      if x in result1:
        result1.remove(x)
  
    for j in result2:
      if x in result2:
        result2.remove(x)
  
  return (result1, result2)
 
#open files saves them on array then calls processtring and saves it returns the levDiscantece call on the two process strings
def openFileGetProcessed(ogFile, cpFile):
  ogFullString = []
  cpFullString = []
  with open(ogFile, 'rb') as originalFile:
    for line in originalFile:
      ogFullString.append(line.decode(errors='replace'))
  originalFile.close()

  with open(cpFile, 'rb') as copyFile:
    for line in copyFile:
      cpFullString.append(line.decode(errors='replace'))
  copyFile.close()
  
  ogString, cpString = processStrings(''.join(ogFullString), ''.join(cpFullString) )

  return levDistance(''.join(ogString), ''.join(cpString))


# Looping through all 100 file while comparing them to abdce txt save values to be exported into a csv file
csv_values = []
for i in range(1, 101):
  vals = []
  for x in 'abcde':
    c = 'evaluation/' + str(i) + '.txt'
    o = 'evaluation/' + x + '.txt'
    vals.append(round(openFileGetProcessed(o, c),2))
  print("evaluation/" + str(i) + '.txt vs abcde' )
  print(vals)
  csv_values.append(vals)
  
#Saving the similarity values to a csv file
with open('csv_out.csv', 'w') as csvFile:
  csv_writer = csv.writer(csvFile, delimiter=',')
  for line in csv_values:
    csv_writer.writerow(line)
csvFile.close()   


