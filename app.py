import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Load data from CSV file
df = pd.read_csv('personal_info.csv')

# Ensure all relevant fields are strings
df['ssnlast4digit'] = df['ssnlast4digit'].astype(str)
df['firstname'] = df['firstname'].astype(str)
df['lastname'] = df['lastname'].astype(str)
df['dob'] = df['dob'].astype(str)
df['gender'] = df['gender'].astype(str)

# Prompt user for their personal information
user_info = {
    "firstname": input("Enter Firstname: "),
    "lastname": input("Enter Lastname: "),
    "dob": input("Enter Date of Birth (YYYY-MM-DD): "),
    "gender": input("Enter Gender (Male/Female): "),
    "ssnlast4digit": input("Enter Last 4 digits of SSN: ")
}

# Function to find the best match using fuzzy matching
def find_best_match(user_info, df):
    best_match = None
    best_score = 0
    row_number = None
    
    for index, row in df.iterrows():
        firstname_score = fuzz.ratio(user_info['firstname'], row['firstname'])
        lastname_score = fuzz.ratio(user_info['lastname'], row['lastname'])
        dob_score = fuzz.ratio(user_info['dob'], row['dob'])
        gender_score = fuzz.ratio(user_info['gender'], row['gender'])
        ssn_score = fuzz.ratio(user_info['ssnlast4digit'], row['ssnlast4digit'])
        
        avg_score = (firstname_score + lastname_score + dob_score + gender_score + ssn_score) / 5
        
        if avg_score > best_score:
            best_score = avg_score
            best_match = row
            row_number = index
    
    return best_match, best_score, row_number

# Find and display the best match
best_match, best_score, row_number = find_best_match(user_info, df)

if best_match is not None:
    print("\nBest Match Found:")
    print(best_match)
    print("\nIndex:")
    print(row_number)
    print(f"Similarity Score: {best_score}")
else:
    print("No match found.")
