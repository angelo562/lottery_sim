"""
Run a simulation of a lottery
For Mega Millions:

Each ticket  = $ 2
Has 6 numbers from 2 separate pools of numbers.  
    First number set = 5 numbers from 1-70.
    Golden ball (gb) = 1 number from 1-25.

9 ways to win.
    0 match & 0 gb = 0
    1 match & 0 gb = 0
    2 match & 0 gb = 0


    0 match & 1 gb = $2 
    1 match & 1 gb = $4
    2 match & 1 gb = 10
    3 match & 0 gb = 10
    3 match & 1 gb = 200
    4 match & 0 gb = 500
    4 match & 1 gb = 10 000
    5 match & 0 gb = 1 000 000
    5 match & 1 gb = jackpot...
"""
from random import choices
from collections import Counter


def main():
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
            self.number_of_tickets: int = tickets
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
            for _ in range(times):
                a, b = (
                    tuple(choices(range(1, 71), k=6)),
                    tuple(choices(range(1, 26), k=1)),
                )

                yield (a, b)

        def win_numbers(self):
            self.win_numbers = self.draw()

        def purchased_tickets(self, number_of_tickets):
            self.ticket_list = [i for i in self.draw(number_of_tickets)]

        def get_match_lst(self) -> tuple:
            # compares ticket_list which is saved to the instance to the winning ticket. Should return tuple of tuples.

            match_ls = []
            for ticket in self.ticket_list:
                c, d, e, f = (
                    Counter(ticket[0]),
                    ticket[1][0],
                    Counter(self.win_numbers[0]),
                    self.win_numbers[1][0],
                )
                match_ls.append((len(set(c).intersection(e)), 1 if d == f else 0))
            self.match_lst = tuple(match_ls)

        def get_winnings(self) -> int:
            # Updates sum of total winnings referencing prize  dictionary
            self.total_winnings = sum([self.prizes[match] for match in self.match_lst])

        def get_win_distribution(self) -> dict:
            # Updates self.win_distr of the round
            c = Counter(self.match_lst)
            self.win_distr = dict(sorted(dict(c).items(), key=lambda item: item[0]))

        def get_net(self) -> int:
            # TODO total winnings - total cost
            self.net = total_winnings - total_cost

    def monte_carlo(ticket_cost: int, times: int) -> dict:
        list_of_wins = []
        for _ in times:
            round = Round()
            list_of_wins.append((round.total_winning))
        dollars_won = sum(list_of_wins)
        cost = times * ticket_cost

        return {
            "dollars_won": dollars_won,
            "total_cost": cost,
            "net": dollars_won - cost,
        }


if __name__ == "__main__":
    main()


#  class for purchased ticket? No, try to keep it in the same class? Class attribute?

#  need a way to keep track of purchased tickets and winning ticket. Use self. number_of_tickets, self.ticket_list, self.win_numbers

# Should we instantiate a new class for every purchased ticket?  YES.

#  Purchased tickets per Round.  # of Rounds for Monte Carlo.

#  class for winning ticket? NO

# TODO Need a way to keep track of matches, winning, and overall losses for all rounds.
