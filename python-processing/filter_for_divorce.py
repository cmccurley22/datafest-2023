import pandas as pd

df_c = pd.read_csv("./data/controversial500.csv")
df_n = pd.read_csv("./data/new500.csv")
df_r = pd.read_csv("./data/rising500.csv")
df_t = pd.read_csv("./data/top500.csv")

test_res = pd.concat([df_c, df_n, df_r, df_t])

test_res.to_csv("./data/full_data.csv")

# print(test_res["text"].to_list())

divorce_posts = []

word_list = ["divorce", "custody", "separati", "seperati", "alimony", "child support", " ex ", "prenup"]

for aaa in test_res["text"].to_list():
    if type(aaa) == type("aaa"):
        if any([word in aaa for word in word_list]):
            divorce_posts.append(aaa)

big_txt = "\n\n\nNEWPOST:\n".join(divorce_posts)

with open("divorce.txt", "w") as f:
    f.write(big_txt)