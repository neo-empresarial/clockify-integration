import sys

sys.path.append("../")
from models import Member
from datetime import datetime


def main():
    print("Type the acronyms of the members who are no longer active.")
    print("Example: 'JNR LAB FSN PYC'")
    acronyms = input("").lower().split()
    for acronym in acronyms:
        member = Member.where("acronym", acronym).first()
        if member is not None:
            member.is_active = False
            date_deactivated_str = input(
                "Type the date of when {} got deactived. Format=DD/MM/YYYY, example: 15/03/2020\n".format(
                    member.acronym
                )
            )
            member.date_deactivated = datetime.strptime(
                date_deactivated_str, "%d/%m/%Y"
            )
            member.update()
            print("Member with acronym {} updated".format(acronym))
        else:
            print("Member with acronym {} not found".format(acronym))


if __name__ == "__main__":
    main()
