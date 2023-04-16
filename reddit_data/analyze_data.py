import text2emotion as t2e
import matplotlib.pyplot as plt

from all_data import divorce_posts


emotions = {
    "Happy": 0,
    "Angry": 0,
    "Surprise": 0,
    "Sad": 0,
    "Fear": 0
}
    
for post in divorce_posts[0:100]:
    bitch = t2e.get_emotion(post)
    for emotion in bitch:
        emotions[emotion] += bitch[emotion]


print(emotions)