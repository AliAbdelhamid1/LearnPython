"""Model for aircraft flights"""

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

        if self._seating[row][letter] is not None:
            raise ValueError(f"Seat {seat} already occupied!")

        self._seating[row][letter] = passenger

    def aircraft_model(self):
        return self._aircraft.model()
    
    def number(self):
        return self._number

    def airline(self):
        return self._number[:2]

class Aircraft:

    def __init__(self, registration, model, num_rows, num_seats_per_row):
        self._registration = registration
        self._model = model
        self._rows = num_rows
        self._num_seats_per_row = num_seats_per_row

    def registration(self):
        return self._registration

    def model(self):
        return self._model

    def seating_plan(self):
        return (range(1,self._rows + 1), "ABCDEFGHJK"[:self._num_seats_per_row])
