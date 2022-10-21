from random import choices
from collections import Counter

def main():


    def draw() -> tuple:
        # TODO the basic draw mechanism for the winning and purchased tickets
        a, b = (
            tuple(sorted(choices(list(range(1, 71)), k=6))),
            tuple(choices(list(range(1, 26)), k=1)),
        )
        return a, b

    ticket_lst = tuple([draw() for i in range(5)])
    

    win_number = draw()
    # print(f"win_number is {win_number}")

    
    # match_ls = []
    # for ticket in ticket_lst:
    #     c, d, e, f = (
    #         Counter(ticket[0]),
    #         ticket[1][0],
    #         Counter(win_number[0]),
    #         win_number[1][0],
    #     )

    #     match_ls.append((len(set(c).intersection(e)), 1 if d == f else 0))
    
    def match_gen():
        wns , wgb = Counter(win_number[0]), win_number[1][0]
        # print(f" wns and wgb is {wns}, {wgb}")

        for ticket in ticket_lst:
            tns, tgb = (
            Counter(ticket[0]),
            ticket[1][0],
            )
            print(f" tns and tgb is {tns}, {tgb}")

            yield((len(set(wns).intersection(tns)), 1 if wgb == tgb else 0))
    
    mg = match_gen()
    match_lst = [next(mg) for _ in ticket_lst]
    print(f"match list is {match_lst}")

if __name__ == "__main__":
    main()
