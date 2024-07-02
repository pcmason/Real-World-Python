"""
Use the wordcloud module to generate a shaped word cloud for Doyle's 'The Hound of the Baskervilles'
"""
# Step 1 - Imoprt modules, text files, images and stop words
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

# Load a text file as a string
with open('hound.txt', encoding='utf-8', errors='ignore') as infile:
    text = infile.read()

# Load an image as a numpy array
mask = np.array(Image.open('holmes.png'))

# Get stop words as a set and add extra words
stopwords = STOPWORDS
stopwords.update(['us', 'one', 'will', 'said', 'now', 'well', 'man', 'may', 'little', 'say', 'must', 'way', 'long',
                  'yet', 'mean', 'put', 'seem', 'asked', 'made', 'half', 'much', 'certainly', 'might', 'came'])

# Step 2 - Generating the word cloud
wc = WordCloud(max_words=500,
               relative_scaling=0.5,
               mask=mask,
               background_color='white',
               stopwords=stopwords,
               margin=2,
               random_state=7,
               contour_width=2,
               contour_color='brown',
               colormap='copper').generate(text)  # Build the wordcloud based on text string

# Convert word cloud image to numpy array to use with pyplot
colors = wc.to_array()

# Step 3 - Plotting the word cloud
plt.figure()
# Label image generated
plt.title('Porko Presents:\n', fontsize=15, color='brown')
plt.text(-10, -3, 'The Hound of the Baskervilles', fontsize=20, fontweight='bold', color='brown')
plt.suptitle('7:00 PM July 10-12 Porko Theatre', x=0.52, y=0.095, fontsize=15, color='brown')
# Show the word cloud without the x and y axes
plt.imshow(colors, interpolation='bilinear')
plt.axis('off')
plt.savefig('hound_wordcloud.png')
plt.show()


