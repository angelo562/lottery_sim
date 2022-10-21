"""
Run a simulation of a lottery

"""
from random import choices
from collections import Counter
from pprint import pprint


class Round:
    """ Class for each Round of a lottery draw
    In every round, will store 
    1. Winning numbers
    2. All purchased tickets
    3. {prize dictionary}
    4. All Matches. e.g. All winning matches that give $
    5. Total Winnings.
    6. Net Losses/Wins.

    """

    def __init__(self, tickets: int, ticket_cost: int, jackpot: int) -> None:
        self.win_numbers()
        self.number: int = tickets
        self.ticket_cost = ticket_cost
        self.prizes: dict = {
            (0, 0): 0,
            (1, 0): 0,
            (2, 0): 0,
            (0, 1): 2,
            (1, 1): 4,
            (2, 1): 10,
            (3, 0): 10,
            (3, 1): 200,
            (4, 0): 500,
            (4, 1): 10_000,
            (5, 1): jackpot,
        }

        self.purchased_tickets(tickets)
        self.get_match_lst()

        self.get_winnings()
        self.get_win_distribution()
        self.get_net()

    def draw(self, times=1) -> tuple:
        # The basic draw mechanism for the winning and purchased tickets
        lst = []

        for _ in range(times):
            a, b = (
                tuple(sorted(choices(range(1, 71), k=6))),
                tuple(sorted(choices(range(1, 26), k=1))),
            )

            lst.append((a, b))
        return tuple(lst)

    def win_numbers(self):
        self.win_numbers = self.draw()

    def purchased_tickets(self, number):
        self.ticket_list = [i for i in self.draw(number)]

    def get_match_lst(self) -> tuple:
        # compares ticket_list which is saved to the instance to the winning ticket. Should return tuple of tuples.

        match_ls = []
        for ticket in self.ticket_list:

            c, d, = Counter(ticket[0]), ticket[1][0]

            e, f = Counter(self.win_numbers[0][0]), self.win_numbers[0][1][0]

            match_ls.append((len(set(c).intersection(e)), 1 if d == f else 0))

        self.match_lst = tuple(match_ls)

    def get_winnings(self) -> int:
        # Updates sum of total winnings referencing prize  dictionary
        self.total_winnings = sum([self.prizes[match] for match in self.match_lst])

    def get_win_distribution(self) -> dict:
        # Updates self.win_distr of the round of any winning ticket

        no_wins = [(0,0), (1,0), (2,0)]
        w = [w for w in self.match_lst if w not in no_wins]
        w.sort()
        self.win_distr = dict(Counter(w))


    def get_net(self) -> int:
        # Gets total winnings and updates it
        self.net = self.total_winnings - self.ticket_cost * self.number


def monte_carlo(
    tickets_a_round: int, ticket_cost: int, jackpot: int, times: int
) -> list:
    """ returns a list of dictionaries, each per Monte Carlo round with lottery data.
    {Round number : int,
    "dollars_won": int,
    "total_cost": int,
    "net": int,
    "win_types": dict,
    }
    
    """
    lst_dct = []
    for round in range(times):
        round_obj = Round(tickets_a_round, ticket_cost, jackpot)

        d = {
            "round": round,
            "total_winnings": round_obj.total_winnings,
            "total_cost": (tickets_a_round * ticket_cost),
            "net": (round_obj.total_winnings - (tickets_a_round * ticket_cost)),
            "win_distribution" : round_obj.win_distr,
        }

        lst_dct.append(d)

    return lst_dct

def analyze(d: dict) -> dict:
    # analyze the input dictionary and spit out net loss, total rounds, & how many ticket wins of each type?
    pass


def main():
    dct = monte_carlo(10, 2, 30_000_000, 50)
    pprint(dct)
    # t = Round(10, 2, 30_000_000)
    # pprint(f" The winning ticket is : {t.win_numbers}")
    # pprint(f"ticket list is {t.ticket_list}")
    # pprint(f" total winnings this round is {t.total_winnings}")
    # pprint(f" Net winnings is {t.net}")
    # pprint(f" Win distribution is {t.win_distr}")


if __name__ == "__main__":
    main()
