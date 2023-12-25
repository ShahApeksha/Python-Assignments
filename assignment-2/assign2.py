
import csv

class Train:
    def __init__(self, train_id, name, source, destination, total_seats, fare_per_seat):
        # Initialize train attributes
        self.train_id = train_id
        self.name = name
        self.source = source
        self.destination = destination
        self.total_seats = int(total_seats)
        self.fare_per_seat = float(fare_per_seat)
        self.available_seats = self.total_seats

class Passenger:
    def __init__(self, name, train_id, num_tickets):
        # Initialize passenger attributes
        self.name = name
        self.train_id = train_id
        self.num_tickets = int(num_tickets)

class RailwayTicketReservationSystem:
    def __init__(self):
        # Initialize the system with empty train and passenger data
        self.trains = {}
        self.passengers = []

    def load_train_data(self, filename):
        try:
            # Load train data from the CSV file and populate the 'trains' dictionary
            with open(filename, 'r', newline='') as file: # Open the CSV file for reading
                reader = csv.reader(file)
                next(reader)   # Skip the header row (the first row) as it contains column names
                for row in reader: 
                     # Extract train attributes from the row
                    train_id, name, source, destination, total_seats, fare_per_seat = row
                    # Create a new Train object using the extracted attributes and add it to the 'trains_data' dictionary
                    self.trains[train_id] = Train(train_id, name, source, destination, total_seats, fare_per_seat)
        except FileNotFoundError:
            # If the specified file is not found, handle the FileNotFoundError and print an error message
            print(f"Error: File '{filename}' not found.")
            return

    def load_passenger_data(self, filename):
        try:
            # Load passenger data from the CSV file and populate the 'passengers' list
            with open(filename, 'r', newline='') as file:
                reader = csv.reader(file)  
                next(reader)  
                for row in reader:
                    name, train_id, num_tickets = row  
                    passenger = Passenger(name, train_id, num_tickets) 
                    self.passengers.append(passenger)
        except FileNotFoundError: 
            # If the specified file is not found, handle the FileNotFoundError and print an error message
            print(f"Error: File '{filename}' not found.")
            return

    def check_seat_availability(self, train_id, num_tickets):
        if train_id not in self.trains: # Check if the train ID exists in the 'trains_data' dictionary
            return False
        train = self.trains[train_id]  # Get the Train object corresponding to the train ID  
        return train.available_seats >= num_tickets  # Check if there are enough available seats on the train for booking

    def book_tickets(self):
        for passenger in self.passengers:
            try:
                if not self.check_seat_availability(passenger.train_id, passenger.num_tickets):
                    raise ValueError("Insufficient seats")
                train = self.trains[passenger.train_id] # Get the Train object for the specified train ID
                # Calculate the fare for the booking based on the fare per seat and the number of tickets
                fare = train.fare_per_seat * passenger.num_tickets

                if fare <= 0: # Check if the calculated fare is valid (greater than zero)
                    raise ValueError("Invalid fare")
                
                # Check if the passenger name is not empty or contains only whitespaces
                if passenger.name.strip() == '':
                    raise ValueError("Invalid passenger name")
                
                # Update the available seats on the train after booking
                train.available_seats -= passenger.num_tickets
                print(f"Booking Confirmed: Passenger {passenger.name}, Train {train.name}, "
                      f"{passenger.num_tickets} tickets, Fare: {fare}")
                
            except KeyError:
                print(f"Error: Invalid train ID '{passenger.train_id}'")
            except ValueError as e:
                # Handle various value-related errors (e.g., insufficient seats, invalid fare, invalid passenger name)
                print(f"Error: {e}")
            except Exception as e:
                # Handle any other unexpected exceptions
                print(f"Error: {e}")

    def generateReport1(self, filename):
        # Generate Report 1 and store it in a CSV file
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Train ID', 'Train Name', 'Source Station', 'Destination Station', 'Total Seats', 'Available Seats'])
            for train in self.trains.values():
                writer.writerow([train.train_id, train.name, train.source, train.destination,
                                 train.total_seats, train.available_seats])

    def generateReport2(self, filename):
        # Generate Report 2 and store it in a CSV file
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Train ID', 'Train Name', 'Total Bookings', 'Total Fare'])
            for train in self.trains.values():
                booked_seats = train.total_seats - train.available_seats
                total_fare = booked_seats * train.fare_per_seat
                writer.writerow([train.train_id, train.name, booked_seats, total_fare])

if __name__ == "__main__":
    # Load data from CSV files
    ticket_system = RailwayTicketReservationSystem()
    ticket_system.load_train_data("trains.csv")
    ticket_system.load_passenger_data("passengers.csv")

    # Book tickets and generate reports
    ticket_system.book_tickets()
    ticket_system.generateReport1("report1.csv")
    ticket_system.generateReport2("report2.csv")
