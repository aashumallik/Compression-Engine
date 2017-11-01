import huffman
import bitstring
from bitstring import BitArray

myfile = open("foo.txt","r") # open file
allofthefile = myfile.read() # save file to a variable
myfile.close() # close the file we dont need it anymore

mycharset = u"\u000A" # unicode of the new line character needed for resurrection of the file later
mycharset = mycharset + " abcdefghijklmnopqrstuvwxyz"+\
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"+\
        "0123456789!#$%&'()\"*+,-./:;<=>?@[\]^_`{|}~"+\
            "àæçèéêôëü" # all of the other unicode charecters
countset = [0 for i in range (0,len(mycharset))] # will hold how many apperance of the characters

for i in range (0,len(allofthefile)):
    singlechar = allofthefile[i]
    for j in range (0,len(mycharset)):
        if mycharset[j] == singlechar:
            countset[j] = countset[j]+1 # count the apperance of the charecters
            break

totalcount = 0 # will hold how many characters in the text file
for i in range (0,len(countset)):
    totalcount = totalcount + countset[i] # count how many charecters text contains

probabilityset = [0 for i in range (0,len(mycharset))] # will hold probabilities of the characters

for i in range (0,len(countset)):
    probabilityset[i] = countset[i]/totalcount # calculate appearance probability of the charecters

mydict = {} # initiate probability dictionary

for i in range (0, len(mycharset)):
    if countset[i] != 0: # precaution to dont create a Huffman code for zero elements
        mydict[str(mycharset[i])] = probabilityset[i] # create dictionary as characters and its probabilities

mycodebook = huffman.codebook(mydict.items()) # create Huffman codebook dictionary with probability dictionary above

# print characters, their apperances, corresponding probabilitiesand their Huffman codes
for i in range (0,len(mycharset)):
    if countset[i] != 0: # suppress the zero appearance charecters
        print(mycharset[i] , " has " , '{0:04d}'.format(countset[i]) , " times appeared. "+\
              "Probability = " , '{:.10f}'.format(probabilityset[i]) + " Huffman: " + mycodebook[str(mycharset[i])]) # just a print out operation

onesandzeros = "" # initiate bit array

for i in range (0, len(allofthefile)):
    onesandzeros = onesandzeros + mycodebook[str(allofthefile[i])] # create ones and zeros array

binary_file = open('compressed_foo.bin', 'wb') # open the binary compressed file for writing

i = 0
while (i < len(onesandzeros)):
    b = BitArray(bin=onesandzeros[i:i+8]) # divide array with 8 many bits and make them into a byte
    b.tofile(binary_file) # write the calculated byte to file
    i = i+8

binary_file.close()

binary_file = open('compressed_foo.bin', "rb") # open the binary compressed file for reading
allofthebinaryfile = binary_file.read() # read all of the bytes in the compressed file
binary_file.close()

newonesandzeros = "" # initiate new bit sequance to decompression of the file

for i in range (0, len(allofthebinaryfile)):
    newonesandzeros = newonesandzeros + str(bin(allofthebinaryfile[i])[2:].zfill(8)) # tranform bytes into bit array

mynewfile = "" # initiate character array

i=0
while (i < len(newonesandzeros)):
    for j in range (0, len(list(mycodebook.values()))):
        check = list(mycodebook.values())[j]
        if (newonesandzeros[i:i+len(check)] == check): # check the Binary Huffman sequence in the bit array
            mynewfile = mynewfile + list(mycodebook.keys())[j] # if the sequence is found, transform it into the character and add it to the character array
            i = i + len(check)
            break

mynewfile = mynewfile[:-1] # remove the new line character at the end of the character array

newfile = open("foonew.txt","w") # open file
newfile.write(mynewfile) # save variable to file
newfile.close() # close the file we dont need it anymore

