import pandas as pd
import matplotlib.pyplot as plt

df_all_csv = pd.read_csv("RBOB_data_test.csv")

print('Total records on csv: ' + str(len(df_all_csv)))

max_deviations = 1.5

# Important columns
df_important_columns = df_all_csv.loc[:, ["generated_on", "display_name", "load_month", "dlvd_price"]]

# Normalize datetime
df_important_columns['generated_on'] = pd.to_datetime(df_important_columns['generated_on'])

# Mean and standard deviation per load month
mean_per_load_month = df_important_columns.groupby('load_month')['dlvd_price'].mean().to_frame('mean_per_month').reset_index()
std_dev_per_load_month = df_important_columns.groupby('load_month')['dlvd_price'].std().to_frame('std_per_month').reset_index()

# Merge mean, standard deviation and df_important_columns
tmp = pd.merge(df_important_columns, mean_per_load_month, on="load_month", how="inner")
df_to_analize = pd.merge(tmp, std_dev_per_load_month, on="load_month", how="inner")

df_no_outliers = df_important_columns.loc[(abs(df_to_analize['dlvd_price'] - df_to_analize['mean_per_month']) < max_deviations * df_to_analize['std_per_month'])]

print('Num. not outliers records: ' + str(len(df_no_outliers)))
print('Num. outliers records: ' + str(len(df_all_csv)-len(df_no_outliers)))

# Save cleaned csv
df_no_outliers.to_csv('cleaned.csv', index=False)

sorted_df = df_important_columns.sort_values(by='generated_on')

# Plot diagram per load_month
for load_month in df_important_columns['load_month'].unique():
    draw_df = sorted_df.loc[(df_important_columns['load_month'] == load_month)]
    plt.plot(draw_df['generated_on'], draw_df['dlvd_price'],
             label=load_month, linewidth=1)

plt.grid()
plt.xlabel('Timestamp')
plt.savefig("plot.jpg")
