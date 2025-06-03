import pandas as pd 
import matplotlib.pyplot as plt

df = pd.read_csv("laptopData.csv")
print(df.info())
print("Data Shape:", df.shape) # # of Rows and Columns

print("Missing Values BEFORE cleaning:")
print(df.isnull().sum())
print("DUPLICATES:", df.duplicated().sum())

# Handle Missing Values (NaN) -> ?
df.replace("?", pd.NA, inplace=True)

critical_cols = ["Company", "Cpu","Ram","Price","Gpu","Memory"]
df = df.dropna(subset=critical_cols)

# Drop all duplicates
df = df.drop_duplicates()

print("Data shape AFTER cleaning:", df.shape)

# Standarize Data (Convert Data Types)
df["Weight"] = df["Weight"].str.replace("kg","", regex=False)
df["Weight"] = pd.to_numeric(df["Weight"],errors='coerce')
df["Price"] = pd.to_numeric(df["Price"],errors='coerce')
df["OpSys"] = df["OpSys"].str.lower().str.replace(" ","_")

def plastic_knife(cpu_speed):
    try: 
        return float(cpu_speed.split()[-1][:-3])
    except Exception as e:
        return None

df["Cpu_Speed"] = df["Cpu"].apply(plastic_knife)

# Convert all Memory to MB
def paper_dish(memory):
    try:
        if "GB" in memory:
            return int(memory.replace("GB","")) * 1024
        elif "TB" in memory:
            return int(memory.replace("TB","")) * 1024 * 1024
    except Exception as e:
        return None

df["Memory_MB"] = df["Memory"].apply(paper_dish)
print(df.info())


df["Weight"].fillna(df["Weight"].mean(), inplace=True)
df["Price"].fillna(df["Price"].mean(), inplace=True)
df["Cpu_Speed"].fillna(df["Cpu_Speed"].mean(), inplace=True)
df["Memory_MB"].fillna(df["Memory_MB"].mean(), inplace=True)

print(df.head())


# DATA FILTERING
filtered_ram = df[df['Ram'].str.replace("GB","").astype(int) >= 8]

filtered_cpu = df[df['Cpu_Speed'] > 2.5]

Average_price = df['Price'].mean()

filtered_price = df[df['Price'] > Average_price]

print(filtered_price.head())

# DATA GROUPING
company_group = df.groupby("Company")["Price"].mean()

ram_size = df.groupby("Ram")["Cpu_Speed"].mean()

Op_system = df.groupby("OpSys")["Weight"].mean()

print(company_group)



# DATA AGGREGATION

aggregated_data = df.groupby('Company').agg(
    Average_price=("Price","mean"),
    Total_Laptops=("Price",'count'),
    Max_Price=("Price","max"),
    Min_Price=("Price",'min'),
    Avg_CPU_Speed=("Cpu_Speed","mean"),
    Avg_Memory=("Memory_MB",'mean'),
)

print(aggregated_data)

pivot_table = df.pivot_table(values="Price", index="Company", columns="Ram", aggfunc="mean")
print(pivot_table)

# DATA VISUALIZATION

# Create my Subplot (window)
fig, ax = plt.subplots(2,3, figsize=(18,12))

# Chart 1 : Average price by company (bar chart)
company_group.plot(kind="bar", ax=ax[0,0], color="orange")
ax[0,0].set_title("Average Price by Company")
ax[0,0].set_ylabel("Average Price")

filtered_ram["Ram"].value_counts().plot(kind='pie', ax=ax[0,1], pctdistance=0.85)
ax[0,1].set_title("Count of Laptops by Ram Size")
ax[0,1].set_ylabel("")

pivot_table.mean().plot(kind="line", marker="o", ax = ax[0,2])
ax[0,2].set_title("Average Price by Ram Size")
ax[0,2].set_ylabel("Average Price")

aggregated_data["Max_Price"].plot(kind="barh", ax=ax[1,0], color="orange")
ax[1,0].set_title("Average Price by Company")
ax[1,0].set_ylabel("Average Price")

ax[1,1].scatter(aggregated_data.index, aggregated_data["Avg_CPU_Speed"], color="red")
ax[1,1].set_title("Average CPU Speed by Company")
ax[1,1].set_ylabel("Average Speed (Ghz)")
ax[1,1].set_ylabel("Company")
ax[1,1].set_xticklabels(aggregated_data.index, rotation=90)

ax[1,2].hist(df["Price"].dropna(), bins=20)
ax[1,2].set_title("Distribution of Price")
ax[1,2].set_ylabel("Frequency")
ax[1,2].set_ylabel("Price")
ax[1,2].set_xticklabels(aggregated_data.index, rotation=90)

plt.show()


