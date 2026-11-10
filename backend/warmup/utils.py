def fiscal_year(input_date):
    """
    Month less than 4 --> starting year = calender year - 1
    Month 4 or greater--> starting year = calender year
    """
    calender_year = input_date.year
    month = input_date.month

    if month < 4:
        starting_year = calender_year - 1
    else:
        starting_year = calender_year

    ending_year = starting_year + 1

    return f"FY{starting_year}-{ending_year%100:02d}"


def format_inr(amount):
    formatted = f"{amount:.2f}"
    integer_part, decimal_part = formatted.split(".")

    remaining = integer_part[:-3]
    last_three = integer_part[-3:]

    if not remaining:
        return f"{last_three}.{decimal_part}"

    reversed_remaining = remaining[::-1]

    groups = []
    for index in range(0, len(reversed_remaining), 2):
        pair = reversed_remaining[index : index + 2]
        groups.append(pair)

    grouped = ",".join(groups)
    indian_grouping = grouped[::-1]
    result = f"{indian_grouping},{last_three}.{decimal_part}"

    return result


def parse_pack_size(size):
    first, second = size.split()
    integer_part = int(first)
    return (integer_part, second)
