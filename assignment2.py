import argparse
import urllib.request
import logging
import datetime

logging.basicConfig(
    filename="error.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)
assignment2 = logging.getLogger("assignment2")

class person:
    """
    Helper class that facilitates adding elements to a dictionary
    Elements are saved as

    Attributes
        dictionary: a dictionary of tuple that contains name, birthday in format dd/mm/YYYY

    """
    def __init__(self):
        self.dictionary = {}

    def add(self, id,name,date):
        #Cleaning up the string
        date = date.replace("/","")

        self.dictionary[id] = (name,datetime.datetime.strptime(date, "%d%m%Y"))

    def displayAll(self):
        if self.dictionary:
            for item in self.dictionary:
                print(item,self.dictionary[item])
        else:
            print("There are no items")

    def getDict(self):
        return self.dictionary

def downloadData(url):
    """Downloads the data from provided URL"""
    with urllib.request.urlopen(url) as response:
        response = response.read().decode('utf-8')

    return response


def processData(file_content):
    """
    Process the data to be saved in a dictionary
    :param file_content: Decoded data downloaded from URL
    :return: instance of class person that contains a dictionary with all the information
    """
    #Creating instance of class person to create the dictionary with tuple
    listPerson = person()
    #spliting the content of the file and cleaning the white spaces
    content = file_content.splitlines(keepends=False)
    #deleting the header to iterate with a loop
    content.pop(0)
    splittedLine = ""
    # counting lines. Starting at 1 because the header wa removed
    counter = 1
    #iterating the list to put the information in a dictionary
    for line in (content):
        splittedLine = line.split(",")
        counter += 1
        try:
            listPerson.add(splittedLine[0], splittedLine[1], splittedLine[2])
        except:
            assignment2.error("Error processing line {} for ID #{}".format(str(counter),splittedLine[0]))

    return listPerson


def displayPerson(id, personData):
    """
    Prints the information of the person stored in personData.
    :param id: String id of the person to look up
    :param personData: Dictionary a dictionary were the data is stored
    """
    birthday = None
    name = ""
    if id in personData.keys():
        birthday = personData[id][1]
        name = personData[id][0]
        print("Person #{} is {} with a birthday of {}".format(id,name ,birthday.strftime("%Y-%m-%d")))
    else:
        print("No user found with that id")


def main(url):
    """
    Main function. The program will download the content of a cvs file,
    process it and then will give the option to search the data given an ID
    :param url:
    :return:
    """
    id = ""
    print(f"Running main with URL = {url}...")
    keepAsking = True
    try:
        csvData = downloadData(url)
    except:
        print("Error retrieving data from url: " + url)
        raise SystemExit

    try:
        personData = processData(csvData)
    except:
        print("Error processing data")
        raise SystemExit


    while keepAsking:
        id = input("Enter and ID: ")
        #Allowing only positive numbers
        if id.isnumeric():
            displayPerson(id,personData.getDict())
        else:
            print("Exiting...")
            raise SystemExit


if __name__ == "__main__":
    """Main entry point
    Accepts a url as argument on CLI
    If the url is empty the program will exit
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    if args.url:
        main(args.url)
    else:
        print("No --url argument provided.")
        print("Exiting...")
        raise SystemExit

    main('https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv')
