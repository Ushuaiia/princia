from facebook_scraper import  get_posts
import pandas as pd
import matplotlib.pyplot as plt
import seaborn  as sns

post_id = "pfbid036ZorY1u7araDucZE5WGogupTovbSGGiZETHZGK43tamHRzzrowHST5dqyDXQwgEZl"

for post in get_posts('CryptoComOfficial',extra_info=True, pages=10, options={"comments":True}):
    post_entry = post
    fb_post_df = pd.DataFrame.from_dict(post_entry, orient='index')
    fb_post_df = fb_post_df.transpose()
    fb_post_df_full = fb_post_df_full.append(fb_post_df)
    print(post['post_id']+' get')
    fb_post_df_full.info()
    