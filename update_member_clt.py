from models import Member


def main():
    print("Type the acronyms of the members who are CLT now.")
    print("Example: 'JNR LAB FSN PYC'")
    acronyms = input("").lower().split()
    for acronym in acronyms:
        member = Member.where("acronym", acronym).first()
        if member is not None:
            member.is_clt = True
            member.update()
            print("Member with acronym {} updated".format(acronym))
        else:
            print("Member with acronym {} not found".format(acronym))


if __name__ == "__main__":
    main()
