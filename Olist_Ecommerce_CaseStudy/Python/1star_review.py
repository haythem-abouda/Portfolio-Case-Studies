import pandas as pd
import nltk
from nltk.corpus import stopwords
from collections import Counter
import string
import matplotlib.pyplot as plt

# Download stopwords if not already downloaded
nltk.download('stopwords')

# SQL Query to get 1-star reviews
query = """
SELECT review_comment_message 
FROM order_reviews 
WHERE review_score = 1 
AND review_comment_message IS NOT NULL;
"""

# Read data into pandas
df_1star = pd.read_sql(query, engine)

# Convert all text to lowercase
df_1star['review_comment_message'] = df_1star['review_comment_message'].str.lower()

# Tokenization: Split text into words & remove punctuation
stop_words = set(stopwords.words('portuguese'))  # Use Portuguese stopwords
all_words = []
for comment in df_1star['review_comment_message'].dropna():
    words = comment.translate(str.maketrans('', '', string.punctuation)).split()
    words = [word for word in words if word not in stop_words and word.isalpha()]  # Remove stopwords & numbers
    all_words.extend(words)

# Count most common words
word_freq = Counter(all_words).most_common(20)

# Convert to DataFrame for plotting
df_word_freq = pd.DataFrame(word_freq, columns=['word', 'count'])

# Plot the word frequency
plt.figure(figsize=(12, 6))
plt.barh(df_word_freq['word'], df_word_freq['count'], color='red')
plt.xlabel("Frequency")
plt.ylabel("Words")
plt.title("Most Frequent Words in 1-Star Reviews")
plt.gca().invert_yaxis()  # Invert so highest frequency is at top

# Save the plot
plt.savefig("plots/1star_review_word_freq.png", bbox_inches='tight', dpi=300)

# Show the plot
plt.show()

# Show the most common words
# df_word_freq
