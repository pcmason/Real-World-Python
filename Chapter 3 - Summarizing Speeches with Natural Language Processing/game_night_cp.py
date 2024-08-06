"""
Program that will have ~10 of the IMDB synopses of movies shown as a word cloud and have the user guess what the name
of the movie based on the cloud. Keep track of total score and output at end.
"""
import random

import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import requests
import bs4
from nltk.tokenize import word_tokenize
import numpy as np
import random


# First want to create a method that grabs the summary and movie title based on links given
def get_title_summary(url):
    url_string = url
    # Will need headers to bypass IMDB bot protection
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }
    page = requests.get(url, headers=headers)
    page.raise_for_status()
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    # Get text of summary calling the specific class the synopsis can be found
    div_elem = [element.text for element in soup.find_all('div', attrs={'class': 'ipc-html-content-inner-div'})]
    div_elem = set(div_elem)
    # Get the movie title based on the h2 attribute
    movie_name = [element.text for element in soup.find_all('h2')]

    # Make the summary one long text string
    summ = ' '.join(div_elem)

    return summ, movie_name


# Create a method to create a wordcloud for the summary provided
def output_wc(summ, movie_name):
    stopwords = STOPWORDS
    # Add words from the movie name to stoppwords so that does not make it too easy
    title_words = word_tokenize(str(movie_name[0]))
    stopwords.update(title_words)

    # Method to make wordcloud
    wc = WordCloud(max_words=100,
                   relative_scaling=.5,
                   background_color='white',
                   stopwords=stopwords,
                   margin=2,
                   random_state=7).generate(summ)

    # Convert word cloud image to numpy array to use with pyplot
    colors = wc.to_array()
    # Plotting the word cloud
    plt.figure()
    # Show the word cloud without the x and y axes
    plt.imshow(colors, interpolation='bilinear')
    plt.axis('off')
    plt.show()


# This method really gets the multiple choice options for each quiz question
def get_quiz(imbd_links):
    # Store all movie names here
    names = list()

    # Loop through links
    for link in imbd_links:
        # Get name of linked movie
        summ, name = get_title_summary(link)
        names.append(name)

    # Now get the list of 4 options for each question
    alternatives = list()
    for i in range(len(names)):
        # Will return a list of sets [so no repeating options]
        alts = set()
        # Get list of ints in ascending order
        numbers = list(range(len(names)))
        # Add the correct answer to the set
        alts.add(str(names[i]))
        # Now remove the correct answer from the numbers list and shuffle that list
        numbers.remove(i)
        random.shuffle(numbers)
        # Now get the next 3 options for the multiple choice question and add to set
        for j in range(3):
            h = numbers[j]
            alts.add(str(names[h]))
        # Append the multiple choice set to the list
        alternatives.append(alts)

    # Return the list of sets
    return alternatives


# Create main function that will get title and IMDB summary of movies and then output a word cloud quiz
def main():
    imbd_links = ['https://www.imdb.com/title/tt0111161/plotsummary/?ref_=tt_stry_pl',
                  'https://www.imdb.com/title/tt0468569/plotsummary/?ref_=tt_stry_pl',
                  'https://www.imdb.com/title/tt15398776/plotsummary/?ref_=tt_stry_pl',
                  'https://www.imdb.com/title/tt0910970/plotsummary/?ref_=tt_stry_pl',
                  'https://www.imdb.com/title/tt0266543/plotsummary/?ref_=tt_stry_pl',
                  'https://www.imdb.com/title/tt0268978/plotsummary/?ref_=tt_stry_pl',
                  'https://www.imdb.com/title/tt0317705/plotsummary/?ref_=tt_stry_pl',
                  'https://www.imdb.com/title/tt0075148/plotsummary/?ref_=tt_stry_pl',
                  'https://www.imdb.com/title/tt0198781/plotsummary/?ref_=tt_stry_pl',
                  'https://www.imdb.com/title/tt0097165/plotsummary/?ref_=tt_stry_pl',
                  'https://www.imdb.com/title/tt1049413/plotsummary/?ref_=tt_stry_pl',
                  'https://www.imdb.com/title/tt0109830/plotsummary/?ref_=tt_stry_pl',
                  'https://www.imdb.com/title/tt1375666/plotsummary/?ref_=tt_stry_pl',
                  'https://www.imdb.com/title/tt0133093/plotsummary/?ref_=tt_stry_pl',
                  'https://www.imdb.com/title/tt0172495/plotsummary/?ref_=tt_stry_pl',
                  'https://www.imdb.com/title/tt0110357/plotsummary/?ref_=tt_stry_pl',
                  'https://www.imdb.com/title/tt4154756/plotsummary/?ref_=tt_stry_pl',
                  'https://www.imdb.com/title/tt0114709/plotsummary/?ref_=tt_stry_pl',
                  'https://www.imdb.com/title/tt0107290/plotsummary/?ref_=tt_stry_pl']

    # Store all movie names and summaries here, may be useful to multiple choice versions of this
    quiz_info = dict()
    # Get the multiple choice answers
    answers = get_quiz(imbd_links)
    # Keep user score
    score = 0
    count = 0

    # Loop through links
    for link in imbd_links:
        # Get summary and name of linked movie
        summ, name = get_title_summary(link)
        quiz_info[str(name)] = summ
        # Now output a wordcloud for the summary of the movie
        output_wc(summ, name)
        # Create count variable to give user 3 tries
        tries = 0
        while tries < 1:
            # Create multiple choice list very user to get answer from [loaded from get_quiz() above]
            ans = answers[count]
            ans = list(ans)
            random.shuffle(ans)
            for val in ans:
                print(val)
            # get user input
            user_answer = input('Type which of the movies above is this word cloud about? ')
            answer = str(name[0])
            # Regardless if answer is right or wrong move onto next question
            if str(user_answer) == answer:
                score += 1
                tries += 1
                count += 1
            else:
                tries += 1
                count += 1

    # When done playing game print out total user score
    print("User score: %d" % score)


if __name__ == '__main__':
    main()



"""
Basically done for now, if anything would make the quiz multiple choice instead of 
"""
