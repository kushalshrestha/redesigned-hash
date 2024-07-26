import csv
import random
import faker

# Initialize the faker generator
fake = faker.Faker()
count = 0

# Function to generate random personal information
def generate_personal_info():
    return {
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "dob": fake.date_of_birth(minimum_age=18, maximum_age=90).strftime("%Y-%m-%d"),
        "gender": random.choice(["Male", "Female"]),
        "ssnlast4digit": fake.ssn()[-4:]
    }

# Function to create slight variations in personal information
def create_variation(record):
    variation = record.copy()
    fields_to_change = random.sample(["firstname", "lastname", "dob", "gender", "ssnlast4digit"], 2)
    print(fields_to_change, ' --- ', count + 1)
    for field in fields_to_change:
        if field == "firstname":
            variation[field] = introduce_typo(record[field])
        elif field == "lastname":
            variation[field] = introduce_typo(record[field])
        elif field == "dob":
            variation[field] = introduce_date_error(record[field])
        elif field == "gender":
            variation[field] = "Male" if record["gender"] == "Female" else "Female"
        elif field == "ssnlast4digit":
            variation[field] = introduce_ssn_error(record[field])
    return variation

def introduce_typo(name):
    if len(name) <= 3:
        return name
    typo = random.choice([name[:3], name[:2] + name[3:], name[:-1], name + random.choice("abcdefghijklmnopqrstuvwxyz")])
    return typo

def introduce_date_error(dob):
    parts = dob.split('-')
    year, month, day = parts
    error_type = random.choice(["year", "month", "day", "null", "full"])
    if error_type == "year":
        year = str(random.randint(1900, 2023))
    elif error_type == "month":
        month = str(random.randint(1, 12)).zfill(2)
    elif error_type == "day":
        day = str(random.randint(1, 28)).zfill(2)
    elif error_type == "null":
        return ""
    elif error_type == "full":
        return fake.date_of_birth(minimum_age=18, maximum_age=90).strftime("%Y-%m-%d")
    return f"{year}-{month}-{day}"

def introduce_ssn_error(ssn):
    errors = ["", ssn[:-1], ssn[:-2], ssn[:-3]]
    return random.choice(errors)

# Generate 50 unique records
records = [generate_personal_info() for _ in range(5000)]

# Create variations of some records to simulate data entry errors
variation_records = [create_variation(record) for record in records]

# Write the original records to a CSV file
header = ["firstname", "lastname", "dob", "gender", "ssnlast4digit"]
with open('personal_info.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=header)
    writer.writeheader()
    for record in records:
        writer.writerow(record)

# Write the variation records to a separate CSV file
with open('personal_info_modified.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=header)
    writer.writeheader()
    for record in variation_records:
        writer.writerow(record)

print("CSV files 'personal_info.csv' and 'personal_info_modified.csv' have been generated.")
