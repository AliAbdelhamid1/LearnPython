"""Model for aircraft flights"""

class Aircraft:

    def __init__(self, registration):
        self._registration = registration

    def registration(self):
        return self._registration

    def num_seats(self):
        rows, row_seats = self.seating_plan()
        return len(rows) * len(row_seats)


class AirbusA319(Aircraft):

    def model(self):
        return "Airbus A319"

    def seating_plan(self):
        return range(1,23), "ABCDEF"



class Boeing777(Aircraft):

    def model(self):
        return "Boeing 777"

    def seating_plan(self):
        return range(1,56), "ABCDEFGHJK"



class Flight:
    """ A flight with a particular passenger aircraft.
    
    Args:
        number: Flight number, such as AB234
        Aircraft method: such as Aircraft("BOUGY", "Airbus 123", 3, 4)
    """

    def __init__(self, number, aircraft):

        #Check if the first two letter are alphabets
        if not number[:2].isalpha():
            raise ValueError(f"No airline code in '{number}'")

        #Check if the first two letters are capitalized
        if not number[:2].isupper():
            raise ValueError(f"Invalid airline code '{number}'")

        #Check if the numbers are digits, and are between 0 and 9999
        if not (number[2:].isdigit() and int(number[2:]) <= 9999):
            raise ValueError("Invalid route number '{number}'")

        self._number = number
        self._aircraft = aircraft
        rows, seats = self._aircraft.seating_plan()

        #For every letter in seats, replace letter with None, then do that for every row (dict comprehension)
        self._seating = [None] + [{letter: None for letter in seats} for _ in rows] #Row indices are 1-based, lists are 0-based, 
                                                                                    #so waste one entry in list

    def allocate_seat(self, seat, passenger):
        """Allocate a seat to a passenger.

        Args: 
            seat: A seat designator such as "12C" or "21F".
            passenger: The passenger name.

        Raises:
            ValueError: If the seat is unavailable.
        """

        row, letter = self._parse_seat(seat)

        if self._seating[row][letter] is not None:
            raise ValueError(f"Seat {seat} already occupied!")

        self._seating[row][letter] = passenger

    def _parse_seat(self, seat):
        rows, seat_letters = self._aircraft.seating_plan()

        letter = seat[-1]
        if letter not in seat_letters:
            raise ValueError(f"Invalid seat letter {letter}")

        row_text = seat[:-1]
        try:
            row = int(row_text)
        except ValueError:
            raise ValueError(f"Invalid seat row {row_text}")

        if row not in rows:
            raise ValueError(f"Inavlid row number {row}")
        
        return row, letter

    def relocate_passenger(self, from_seat, to_seat):
        """Relocate a passenger to a different seat.

        Args: 
            from_seat: The existing desginator for 
                        the passenger to be moved.
            
            passenger: The new seat designator.
        """

        from_row, from_letter = self._parse_seat(from_seat)
        if self._seating[from_row][from_letter] is None:
            raise ValueError(f"No passenger to relocate in seat {from_seat}")

        to_row, to_letter = self._parse_seat(to_seat)
        if self._seating[to_row][to_letter] is not None:
            raise ValueError(f"Seat {to_seat} already occupied!")

        self._seating[to_row][to_letter] = self._seating[from_row][from_letter]
        self._seating[from_row][from_letter] = None

    def make_boarding_cards(self, card_printer):
        for passenger, seat in sorted(self._passenger_seats()):
            card_printer(passenger, seat, self.number(), self.aircraft_model())

    def _passenger_seats(self):
        """An iterable series of passenger seating locations."""
        row_numbers, seat_letters = self._aircraft.seating_plan()
        for row in row_numbers:
            for letter in seat_letters:
                passenger = self._seating[row][letter]
                if passenger is not None:
                    yield (passenger, f"{row}{letter}")

    def aircraft_model(self):
        return self._aircraft.model()
    
    def number(self):
        return self._number

    def airline(self):
        return self._number[:2]




#class Aircraft:

    #def __init__(self, registration, model, num_rows, num_seats_per_row):
        #self._registration = registration
        #self._model = model
        #self._rows = num_rows
        #self._num_seats_per_row = num_seats_per_row

    #def registration(self):
        #return self._registration

    #def model(self):
        #return self._model

    #def seating_plan(self):
        #return (range(1,self._rows + 1), "ABCDEFGHJK"[:self._num_seats_per_row])



def console_card_printer(passenger, seat, flight_number, aircraft):
    output = f"| Name: {passenger}"       \
             f"  Flight: {flight_number}" \
             f"  Seat: {seat}"            \
             f"  Aircraft: {aircraft}"    \
             " |"
    banner = "+" + "-" * (len(output)-2) + "+"
    border = "|" + "-" * (len(output)-2) + "|"
    lines = [banner, border, output, border, banner]
    card = "\n".join(lines)
    print(card)
    print()

def make_flights():
    f = Flight("BA758", AirbusA319("G-EUPT"))
    f.allocate_seat("12A", "Ali")
    f.allocate_seat("15F", "Alaa")
    f.allocate_seat("13D", "Mom")

    g = Flight("AF73", Boeing777("F-GSPS"))
    g.allocate_seat("12A", "Baba")
    g.allocate_seat("15F", "Ahmad")
    g.allocate_seat("13D", "Me")

    return f, g

