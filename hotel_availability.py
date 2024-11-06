import json
from collections import defaultdict

# Load data from JSON files
def load_data():
    with open('hotels.json', 'r') as hotel_file, open('bookings.json', 'r') as booking_file:
        hotels = json.load(hotel_file)
        bookings = json.load(booking_file)
    return hotels, bookings

# Parse hotel data into a more usable format
def parse_hotels(hotels):
    hotel_dict = {}
    for hotel in hotels:
        hotel_dict[hotel['id']] = {
            'name': hotel['name'],
            'roomTypes': {room['code']: room for room in hotel['roomTypes']},
            'rooms': defaultdict(int)  # Default dict to count room types
        }
        for room in hotel['rooms']:
            hotel_dict[hotel['id']]['rooms'][room['roomType']] += 1
    return hotel_dict

# Parse bookings into a usable format
def parse_bookings(bookings):
    booking_dict = defaultdict(list)
    for booking in bookings:
        booking_dict[booking['hotelId']].append(booking)
    return booking_dict

# Calculate room availability
def calculate_availability(hotel_dict, booking_dict, hotel_id, query_date, room_type):
    available_rooms = hotel_dict[hotel_id]['rooms'].get(room_type, 0)
    
    # Subtract the number of bookings that overlap with the query date
    for booking in booking_dict.get(hotel_id, []):
        if booking['roomType'] == room_type:
            if (query_date >= booking['arrival'] and query_date < booking['departure']):
                available_rooms -= 1

    return available_rooms

# Display availability in the required format
def check_availability(hotel_dict, booking_dict):
    while True:
        query = input("Enter availability query (Format: Availability(H1, 20240901, SGL), blank to exit): ")
        if not query.strip():
            break
        try:
            # Extract the parameters from the query string
            query = query.strip().replace('Availability(', '').replace(')', '')
            hotel_id, query_date, room_type = query.split(',')
            hotel_id = hotel_id.strip()
            query_date = query_date.strip()
            room_type = room_type.strip()
            
            # Ensure that the hotel and room type exist
            if hotel_id in hotel_dict and room_type in hotel_dict[hotel_id]['roomTypes']:
                available_rooms = calculate_availability(hotel_dict, booking_dict, hotel_id, query_date, room_type)
                print(f"Availability({hotel_id}, {query_date}, {room_type}) = {available_rooms}")
            else:
                print("Invalid hotel or room type.")
        except Exception as e:
            print(f"Error processing the query: {e}")

def main():
    # Load the hotel and booking data
    hotels, bookings = load_data()
    
    # Parse the data into usable dictionaries
    hotel_dict = parse_hotels(hotels)
    booking_dict = parse_bookings(bookings)
    
    print("Hotel Room Availability System")
    print("Type the availability query in the format: Availability(hotel id, query date, room type)")
    print("Leave blank and press Enter to exit the program.")
    
    # Start checking availability
    check_availability(hotel_dict, booking_dict)

if __name__ == "__main__":
    main()
