import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv("fastfoodData.csv")




print(df.info())

# BEFORE DROP DUPLICATES
print("Initial Data Shape:", df.shape)
print("Number of null values per column:\n", df.isnull().sum())
print("Number of Duplicates:", df.duplicated().sum())

critical_cols = ["Company", "Item", "Protein (g)", "Calories", "Sodium  (mg)", "Cholesterol (mg)"]
df = df.dropna(subset=critical_cols)
df = df.drop_duplicates()

# AFTER DROP DUPLICATES
print("Data Shape:", df.shape)

# Changing Objects -> Integer  
df["Protein (g)"] = pd.to_numeric(df["Protein (g)"],errors='coerce')
df["Calories"] = pd.to_numeric(df["Calories"],errors='coerce')
df["Sodium  (mg)"] = pd.to_numeric(df["Sodium  (mg)"],errors='coerce')
df["Cholesterol (mg)"] = pd.to_numeric(df["Cholesterol (mg)"],errors='coerce')

# PRINTING THE INFORMATION AFTER CONVERTING "Objects" to "Integers"
print(df.info())

#Step Three

#fill in null values with averages of column
df["Protein (g)"].fillna(df["Protein (g)"].mean(), inplace=True)
df["Calories"].fillna(df["Calories"].mean(), inplace=True)
df["Sodium  (mg)"].fillna(df["Sodium  (mg)"].mean(), inplace=True)
df["Cholesterol (mg)"].fillna(df["Cholesterol (mg)"].mean(), inplace=True)

# PRINTING THE INFORMATION AFTER FILLING IN NULL VALUES
print(df.info())

#Step Four

#Data Filtering

# Sort by Protein in descending order and display the top 10 items with the most protein
most_protein = df.sort_values(["Protein (g)"], ascending = False).groupby('Item').head(10)
print("Top 10 fast food items with the most protein:\n", most_protein)



# Which items are highest in sodium?
most_sodium = df.sort_values(["Sodium  (mg)"], ascending = False).groupby("Item").head(10)
print("Top 10 fast food items with the most sodium:\n", most_sodium)


# Strong Correlation
numerical_cols = df.select_dtypes(include=["number"])
matrix = numerical_cols.corr()

print("Correlation Matrix:", matrix)


top_protein = most_protein.head(10)
plt.figure(figsize=(10,6))
plt.barh(top_protein["Item"], top_protein["Protein (g)"], color="darkblue")
plt.title("Top 10 fast food with the most protein")
plt.xlabel("Protein (g)", fontsize=12)
plt.ylabel("Item", fontsize=12)

top_sodium = most_sodium.head(10)
plt.figure(figsize=(10,6))
plt.barh(top_sodium["Item"], top_sodium["Sodium  (mg)"], color="darkblue")
plt.title("Top 10 fast food with the most sodium")
plt.xlabel("Sodium (mg)", fontsize=12)
plt.ylabel("Item", fontsize=12)

plt.tight_layout()
plt.show()

plt.figure(figsize=(8,6))
plt.scatter(df["Calories"], df["Protein (g)"], alpha=0.7, color="green")
plt.title("Protein Vs. Calories")
plt.xlabel("Calories")
plt.ylabel("Protein")
plt.grid(True)
plt.show()


plt.figure(figsize=(8,6))
sns.heatmap(matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation of Nutrirents")
plt.yticks(rotation=0)
plt.show()