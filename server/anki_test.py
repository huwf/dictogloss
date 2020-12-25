# See: https://eshapard.github.io/anki/open-the-anki-database-from-python.html

if __name__ == '__main__':
    # import sys
    # sys.path.append('/usr/share/anki')
    import anki
    from anki.collection import Collection
    import os
    collection_path = "/opt/project/collection.anki2"
    print(os.path.getsize(collection_path))

    col = Collection(collection_path, server=True)

    card = col.sched.getCard()
    print(card)

# today = intTime()  # anki function returns current integer time
# nextTwenty = today + 20 * 60  # integer time in 20 minutes
#
# query="select count(id) from cards where queue = 1 and due < %s" % nextTwenty
# learnAheadCards = col.db.scalar(query)
#
# print("You have %s learning cards due in Anki" % learnAheadCards)
#
# col.close()
