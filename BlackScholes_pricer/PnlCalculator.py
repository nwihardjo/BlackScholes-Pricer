PNL_FACTOR = 10000
CROSSING_FIX = 500
CROSSING_RATIO = 2


def calculate_pnl(bid, ask, theo):
    if theo == 0:
        return -CROSSING_FIX

    midmarket = (bid + ask) / 2
    spread = (ask - bid)
    diff_to_midmarket = abs(theo - midmarket)

    if diff_to_midmarket < spread / 2:
        return (spread / 2 - diff_to_midmarket) * PNL_FACTOR

    crossed_amount = abs(diff_to_midmarket - spread / 2)

    return -(CROSSING_FIX + (CROSSING_RATIO * PNL_FACTOR) * crossed_amount)
