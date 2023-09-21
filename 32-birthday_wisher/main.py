import csv
import datetime
import pandas as pd
import smtplib
import os
import random

MY_EMAIL = ""
PASSWORD = ""
SMTP = "smtp.gmail.com"


def add_data():
    add_new_data = input("Do you want to add new birthdays?")
    if add_new_data.lower() == "yes":
        name = input("Enter name: ")
        email = input("Enter email: ")
        year = input("Enter  of birth: ")
        month = input("Enter month of birth (as a number): ")
        day = input("Enter day of birth: ")
        new_birthday = [name, email, year, month, day]

        with open("./birthdays.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(new_birthday)
            print("Birthday added successfully")
        add_data()


def send_email(recipient):
    def choose_template():
        folder = "./letter_templates"
        templates = os.listdir(folder)
        template_name = random.choice(templates)
        return template_name

    connection = smtplib.SMTP(SMTP)
    connection.starttls()
    connection.login(user=MY_EMAIL, password=PASSWORD)
    template = choose_template()
    with open(f"./letter_templates/{template}") as file:
        content = file.read()
    message = content.replace("[NAME]", f"{recipient['name']}")
    connection.sendmail(from_addr=MY_EMAIL, to_addrs=recipient["email"], msg=f"Subject: Happy Birthday!\n\n{message}")
    print("Email Sent")


def main():
    add_data()
    today = datetime.date.today()
    birthdays = pd.read_csv("./birthdays.csv")
    for index, row in birthdays.iterrows():
        birthdate = datetime.date(year=int(row.loc["year"]), month=int(row.loc["month"]), day=int(row.loc["day"]))
        print(birthdate, today)
        if birthdate.day == today.day and birthdate.month == today.month:
            print(f"Birthday of {row['name']}")

            send_email(row)


if __name__ == '__main__':
    main()



