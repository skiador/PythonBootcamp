import smtplib
import os


EMAIL = os.environ["MY_EMAIL"]
PASSWD = os.environ["PASSWORD"]
SMTP = "smtp.gmail.com"
RECEIVER = os.environ["RECEIVER"]


def send_notification(data):
    # Create an SMTP connection
    connection = smtplib.SMTP(SMTP)
    connection.starttls()
    connection.login(user=EMAIL, password=PASSWD)

    # Access the IATA Code for the city
    iata_code = data["IATA Code"]

    # Access the outbound flight details (nested DataFrame)
    outbound_details = data["Outbound"]

    # Access the inbound flight details (nested DataFrame)
    inbound_details = data["Inbound"]

    # Access the price for the flight
    price = data["Price"]

    subject = f"Check out these low prices to {outbound_details.iloc[-1]['Destination']}:"

    # Create a string with the desired information
    email_content = f"Destination: {outbound_details.iloc[-1]['Destination']}\n\n"
    email_content += "Outbound Flights:\n"
    for index, outbound_flight in outbound_details.iterrows():
        origin = outbound_flight["Origin"]
        destination = outbound_flight["Destination"]
        departure_date = outbound_flight["Date"]
        airline = outbound_flight["Airline"]
        email_content += f"{index+1}.- {origin} - {destination}, {departure_date} with {airline}\n"
    email_content += "\n\nInbound Flights:\n"
    for index, inbound_flight in inbound_details.iterrows():
        origin = inbound_flight["Origin"]
        destination = inbound_flight["Destination"]
        departure_date = inbound_flight["Date"]
        airline = inbound_flight["Airline"]
        email_content += f"{index+1}.- {origin} - {destination}, {departure_date} with {airline}\n"
    email_content += f"\n\nPrice: {price} EUR"

    connection.sendmail(
        from_addr=EMAIL,
        to_addrs=RECEIVER,
        msg=f"Subject:{ subject}\n\n{email_content}".encode('utf-8')
    )
    connection.quit()
    print("Email sent")