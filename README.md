Hotel Room Availability and Reservation System
This program allows users to preview hotel room availability and manage room reservations. It reads hotel and booking data from JSON files, then outputs room availability counts based on user queries.

How to Run the Application
1. Prepare Your Environment:
Make sure you have Python 3.x installed on your machine. You can download it from python.org.

2. Create the Project Directory:
Create a directory for the project, and add the following files:

hotels.json
bookings.json
hotel_availability.py

3. Running the Program:
Open a terminal or command prompt.
Navigate to the project directory.
Run the program by executing the following command:
python hotel_availability.py

4. Example Queries:
Once the program starts, you can enter availability queries like these:

Availability(H1, 20240901, SGL)
Availability(H1, 20240901-20240903, DBL)

The program checks the availability of rooms by comparing the user-specified date against existing bookings and outputs the number of available rooms.

The program will exit if a blank line is entered.