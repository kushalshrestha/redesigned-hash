import pandas as pd
from fuzzywuzzy import fuzz
from datetime import datetime

df_original = pd.read_csv('personal_info.csv')
df_modified = pd.read_csv('personal_info_modified.csv')

df_original = df_original.astype(str)
df_modified = df_modified.astype(str)

df_original['combined'] = df_original['firstname'] + ' ' + df_original['lastname'] + ' ' + df_original['dob'] + ' ' + df_original['gender'] + ' ' + df_original['ssnlast4digit']
df_modified['combined'] = df_modified['firstname'] + ' ' + df_modified['lastname'] + ' ' + df_modified['dob'] + ' ' + df_modified['gender'] + ' ' + df_modified['ssnlast4digit']

def find_best_match(user_combined, user_info, df):
    best_combined_score = 0
    best_average_score = 0
    best_combined_match = None
    best_average_match = None
    best_combined_index = None
    best_average_index = None
    
    for index, row in df.iterrows():
        combined_score = fuzz.ratio(user_combined, row['combined'])
        
        firstname_score = fuzz.ratio(user_info['firstname'], row['firstname'])
        lastname_score = fuzz.ratio(user_info['lastname'], row['lastname'])
        dob_score = fuzz.ratio(user_info['dob'], row['dob'])
        gender_score = fuzz.ratio(user_info['gender'], row['gender'])
        ssn_score = fuzz.ratio(user_info['ssnlast4digit'], row['ssnlast4digit'])
        avg_score = (firstname_score + lastname_score + dob_score + gender_score + ssn_score) / 5
        
        if combined_score > best_combined_score:
            best_combined_score = combined_score
            best_combined_match = row
            best_combined_index = index
            
            # calculating average on the same row 
            best_average_score = avg_score
            best_average_match = row
            best_average_index = index
            
    return best_combined_match, best_combined_score, best_combined_index, best_average_match, best_average_score, best_average_index

results = []

start_time = datetime.now()
print(f"Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
for _, user_info in df_modified.head(10).iterrows():
    user_combined = user_info['combined']
    best_combined_match, best_combined_score, best_combined_index, best_average_match, best_average_score, best_average_index = find_best_match(user_combined, user_info, df_original)
    
    results.append({
        "input_firstname": user_info['firstname'],
        "input_lastname": user_info['lastname'],
        "input_dob": user_info['dob'],
        "input_gender": user_info['gender'],
        "input_ssnlast4digit": user_info['ssnlast4digit'],
        "best_combined_match_firstname": best_combined_match['firstname'] if best_combined_match is not None else None,
        "best_combined_match_lastname": best_combined_match['lastname'] if best_combined_match is not None else None,
        "best_combined_match_dob": best_combined_match['dob'] if best_combined_match is not None else None,
        "best_combined_match_gender": best_combined_match['gender'] if best_combined_match is not None else None,
        "best_combined_match_ssnlast4digit": best_combined_match['ssnlast4digit'] if best_combined_match is not None else None,
        "best_average_match_firstname": best_average_match['firstname'] if best_average_match is not None else None,
        "best_average_match_lastname": best_average_match['lastname'] if best_average_match is not None else None,
        "best_average_match_dob": best_average_match['dob'] if best_average_match is not None else None,
        "best_average_match_gender": best_average_match['gender'] if best_average_match is not None else None,
        "best_average_match_ssnlast4digit": best_average_match['ssnlast4digit'] if best_average_match is not None else None,
        "best_combined_row_index": best_combined_index,
        "best_average_row_index": best_average_index,
        "best_combined_similarity_score": best_combined_score,
        "best_average_similarity_score": best_average_score
    })

results_df = pd.DataFrame(results)


end_time = datetime.now()
print(f"End Time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

time_diff = end_time - start_time
print(f"Time Difference: {time_diff}")

results_df.to_csv('output.csv', index=False)
results_df.to_excel('output.xlsx', index=False)


print("Results have been written to 'output.csv' and 'output.xlsx'.")

