import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="student_result"
)

cursor = conn.cursor()

query = "SELECT * FROM student"

df = pd.read_sql(query, conn)

print("\nOriginal Data\n")
print(df)

df["Total"] = (
    df["maths"]+df["science"]+df["english"]+df["computer"]+df["english"]
)

df["Percentage"] = (df["Total"]/500)*100

def assign_grade(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    else:
        return "F"

df["Grade"] = df["Percentage"].apply(assign_grade)

df["Result"] = df["Grade"].apply(lambda x: "Pass" if x != "F" else "Fail")

print("\nData with Total, Percentage, Grade, and Result\n")
print(df)

print("\n Average Percentage of Students: ", df["Percentage"].mean())

print("\n Highest Percentage of Students: ", df["Percentage"].max())
print("\n Lowest Percentage of Students: ", df["Percentage"].min())
print("\nMedian Percentage of Students: ", df["Percentage"].median())
print("\n Standard Deviation of Percentage of Students: ", df["Percentage"].std())

print("\n Top Student", df.nlargest(1, 'Percentage'))

print("\n Top Five Students", df.nlargest(5, 'Percentage'))

print("\nDepartment-wise Average Percentage of Students\n")
print(df.groupby("department")["Percentage"].mean())

print("\n Gender-wise Average Percentage of Students\n")
print(df.groupby("gender")["Percentage"].mean())

subjects = ["maths", "science", "english", "computer"]
print("\n Subject Average \n")
print(df[subjects].mean())

df.to_excel("student_result.xlsx", index=False)
print("\n Excel report saved")

plt.figure(figsize=(8, 5))
df[subjects].mean().plot(kind="bar", color=["blue", "orange", "green", "red"])
plt.title("Average Marks in Subjects")
plt.xlabel("Subjects")
plt.ylabel("Average Marks")
plt.show()

plt.figure(figsize=(8, 5))
sns.histplot(df["Percentage"], bins=10, kde=True, color="purple")
plt.title("Distribution of Percentage")
plt.xlabel("Percentage")
plt.ylabel("Frequency")
plt.show()

plt.figure(figsize=(7,7))
df["Grade"].value_counts().plot(
    kind="pie",
    autopct="%1.1f%%"
)
plt.title("Grade Distribution")
plt.show()

plt.figure(figsize=(7,5))
sns.heatmap(
    df[subjects].corr(),
    annot=True,
    cmap="coolwarm"
)
plt.title("Subject Correlation")
plt.show()

plt.figure(figsize=(9,5))
plt.plot(
    df["student_name"],
    df["Percentage"],
    marker="o"
)
plt.xticks(rotation=45)
plt.title("Student Percentage")
plt.show()

cursor.close()
conn.close()