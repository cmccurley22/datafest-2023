import text2emotion as t2e
import matplotlib.pyplot as plt

from filter_for_divorce import divorce_posts


divorce_emotions = {
    "Happy": 0,
    "Angry": 0,
    "Surprise": 0,
    "Sad": 0,
    "Fear": 0
}
    
for post in divorce_posts[0:100]:
    post_emotions = t2e.get_emotion(post)
    for emotion in post_emotions:
        divorce_emotions[emotion] += post_emotions[emotion]


print(divorce_emotions)