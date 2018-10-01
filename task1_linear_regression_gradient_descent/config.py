df_path = 'dataset/Training/Features_Variant_1.csv'
df_columns_list = ["Page Popularity", "Page Checkins", "Page Talking About", "Page Category",
                   "extra_0", "extra_1", "extra_2", "extra_3", "extra_4", "extra_5", "extra_6",
                   "extra_7", "extra_8", "extra_9", "extra_10", "extra_11", "extra_12", "extra_13",
                   "extra_14", "extra_15", "extra_16", "extra_17", "extra_18", "extra_19", "extra_20",
                   "extra_21", "extra_22", "extra_23", "extra_24", "CC1", "CC2", "CC3", "CC4", "CC5",
                   "Base Time", "Post Length", "Post Share Count", "Post Promotion Status", "H Local",
                   "published_weekday_0", "published_weekday_1", "published_weekday_2",
                   "published_weekday_3", "published_weekday_4", "published_weekday_5",
                   "published_weekday_6", "base_weekday_0", "base_weekday_1", "base_weekday_2",
                   "base_weekday_3", "base_weekday_4", "base_weekday_5", "base_weekday_6", "Target"]

stochastically = False

eps_no_stoch = 1e-03
step_no_stoch = 0.28
when_to_log_no_stoch = 100

eps_stoch = 1e-5 * 1.5
step_stoch = 1 / 50
when_to_log_stoch = 30000
