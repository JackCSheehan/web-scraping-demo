#----------------------------------------------------------------
# This program scrapes data from the UTD ACM website
# and displays it to the console.
#
# Created by Jack Sheehan
# March 7th, 2020
# The University of Texas at Dallas
#----------------------------------------------------------------

# Note: Before you begin, you will need the following Python
# libraries:
#   BeautifulSoup4
#   requests

# Import the BeautifulSoup module for web scraping.
# 'bs' serves as shorthand so we don't have to keep typing out
# 'BeautifulSoup'
import bs4 as bs

# Import the urllib.requests module to get HTML docs from websites
import urllib.request

# Finally, we need the requests module for downloading images
import requests

# Create a variable to hold our HTML document. This document is
# read from the target URL using urllib.request.urlopen().
# Notice the https://. This is required.
source = urllib.request.urlopen("https://www.acmutd.co/team.html").read()

# Create an object called soup that has functions that let us
# parse our HTML document. 'lxml' is an XML parser that lets
# the soup object parse the HTML doc.
soup = bs.BeautifulSoup(source, "lxml")

# Prints the title of the webpage
print("Page Title: %s" %soup.title.string)

# Let's search for some specific information on the webpage

# Use the soup.find function to find the header of the page. On
# our example webpage, the <div> tag is used for the header, and
# the class of the tag is 'text-block.'
page_header_1 = soup.find("strong")
print("\n%s" %page_header_1.string)

# The header of this page is split up a bit, so we can't get it
# all at once. Now to grab the second part of that header:
page_header_2 = soup.find("div", {"class" : "contrast-white"})

# The .strip() function removes some extra pesky whitespace characters
print(page_header_2.string.strip())

# Let's grab the text underneath the header. This text is stored
# in <p> tags with the class name 'lead contrast-white-p.'
page_description = soup.find("p", {"class" : "lead contrast-white-p"})

# The .strip() function gets rid of some extra pesky whitespaces
print("\n%s" %page_description.string.strip())

# Now let's grab all of the officer descriptions! These are all
# stored in <div> tags with the class name
# 'col-md-3 col-sm-4 project team-2 officers.' We can use the
# find_all function to find all of the divs that match this
# criteria.
officers = soup.find_all("div", {"class" : "col-md-3 col-sm-4 project team-2 officers"})

# The find_all function returns a list of the found tags, so we'll
# have to use a loop to go through them and print what's there.
print("\nOfficers:")

for officer in officers:
    # Notice how we can look for tags within other tags by calling
    # .find() on officer.
    print("Name: %s" %officer.find("h3").string)
    print("Position: %s" %officer.find("span").string)

    # Some officers do not have a link, so we must make sure that
    # an officer has a link before we try to display it.
    if officer.find("a") is not None:
        # <a> is how links are handled in HTML, and we can use
        # [] to get the link that <a> contains.
        print("Link: %s" %officer.find("a")["href"])
 
    # This newline is just for formatting purposes
    print("")

# Now let's display some information about the individual branches

# Since we're now scraping a new page located at a new URL ,we
# need a new source.
projects_page_source = urllib.request.urlopen("https://www.acmutd.co/projects").read()

# Since we have a new source, we also need a new soup object
projects_page_soup = bs.BeautifulSoup(projects_page_source, "lxml")

# Let's get the description of the ACM projects page
print("ACM Projects\n-------------")

projects_description = projects_page_soup.find("p", {"class" : "super-lead left-align-mobile"})
print(projects_description.string.strip())

# Now let's get all of the Q&As from this page. All of the questions
# are stored under two different <section>s called with class name
# 'wide-features,' so we'll use find all to get both of these.
wide_features = projects_page_soup.find_all("section", {"class" : "wide-features"})

# Now we can iterate through each wide feature and .find()s every
# <h4> within them since each question is stored in <h4> tags.
print("\nFAQs:")

# Declares some empty lists to fill full of questions and answers
questions = []
answers = []

# First loop iterates through all wide features sections
for wide_feature in wide_features:

    # This loop finds all the questions in the page and adds them
    # to the questions list
    for question in wide_feature.find_all("h4"):
        questions.append(question)

    # This loop finds all answers in the page and adds them to
    # the anwsers list
    for answer in wide_feature.find_all("p"):
        answers.append(answer)

# Finally, let's iterate through the parallel arrays and print
# their contents.
for counter in range(len(questions)):
    # First, print the question
    print(questions[counter].string)

    # Then, print the anwser
    print("%s\n" %answers[counter].string.strip())

# Now that all the dirty work is done, let's download an image

# Before I can download the image, I must create the file
# on my machine.
image = open("C:/Users/Jack/Desktop/ed.jpg", "wb")

# Next, I can get the image's data using the requests module
image_content = requests.get("https://www.acmutd.co/png/team-education-eduardo.jpg", stream = True).content

# Finally, we write the image data that we got from the URL
# to the file on my machine.
image.write(image_content)

# Don't forget to close the image!
image.close()

print("\nDone!")

