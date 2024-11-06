import json
from datetime import datetime

# Helper function to parse date string into a datetime object
def parse_date(date_str):
    return datetime.strptime(date_str, "%Y%m%d")

# Helper function to check if a date is within a range
def is_date_in_range(date, start_date, end_date):
    return start_date <= date <= end_date

# Load hotel and booking data from the JSON files
def load_data(hotels_file, bookings_file):
    with open(hotels_file, 'r') as f:
        hotels = json.load(f)
    
    with open(bookings_file, 'r') as f:
        bookings = json.load(f)
    
    return hotels, bookings

# Check availability based on hotel, date range, and room type
def check_availability(hotels, bookings, hotel_id, date_range, room_type):
    # Split the date range if it's a multi-day range
    date_range_split = date_range.split('-')
    start_date = parse_date(date_range_split[0])
    end_date = parse_date(date_range_split[1]) if len(date_range_split) > 1 else start_date

    # Find the hotel in the list of hotels
    hotel = next((h for h in hotels if h['id'] == hotel_id), None)
    if not hotel:
        print(f"Hotel {hotel_id} not found!")
        return

    # Find the room types and the rooms available in the hotel
    available_rooms = [r for r in hotel['rooms'] if r['roomType'] == room_type]
    if not available_rooms:
        print(f"No rooms of type {room_type} available in {hotel['name']}.")
        return

    # Count rooms and consider bookings
    room_count = len(available_rooms)
    bookings_count = 0
    for booking in bookings:
        if booking['hotelId'] == hotel_id and booking['roomType'] == room_type:
            booking_start_date = parse_date(booking['arrival'])
            booking_end_date = parse_date(booking['departure'])

            # Check if the booking overlaps with the requested date range
            if is_date_in_range(booking_start_date, start_date, end_date) or is_date_in_range(booking_end_date, start_date, end_date):
                bookings_count += 1
    
    # Consider overbookings (negative bookings)
    available_rooms_after_booking = room_count - bookings_count
    print(f"Availability for hotel {hotel_id}, room type {room_type}, date range {date_range}: {available_rooms_after_booking}")

def main():
    # Get file paths from user or command line
    hotels_file = input("Enter path to hotels JSON file: ")
    bookings_file = input("Enter path to bookings JSON file: ")

    # Load hotel and booking data
    hotels, bookings = load_data(hotels_file, bookings_file)

    while True:
        user_input = input("Enter availability query or blank to exit: ").strip()
        
        if not user_input:
            break  # Exit on blank input
        
        # Parse the query in the format Availability(H1,20240901, SGL)
        if user_input.startswith("Availability(") and user_input.endswith(")"):
            query = user_input[len("Availability("):-1]
            parts = query.split(",")
            if len(parts) == 3:
                hotel_id = parts[0].strip()
                date_range = parts[1].strip()
                room_type = parts[2].strip()
                check_availability(hotels, bookings, hotel_id, date_range, room_type)
            else:
                print("Invalid query format. Use Availability(H1,20240901, SGL)")

if __name__ == "__main__":
    main()
