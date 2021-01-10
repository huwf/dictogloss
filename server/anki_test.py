# See: https://eshapard.github.io/anki/open-the-anki-database-from-python.html

from anki.collection import Note


if __name__ == '__main__':
    # import sys
    # sys.path.append('/usr/share/anki')
    import anki
    from anki.collection import Collection
    import os
    import shutil
    import sys
    # collection_path = "/opt/project/collection.anki2"
    original_collection = '/home/worker/anki2/User 1/collection.anki2'
    collection_path = '/home/worker/temp.anki2'
    shutil.copy(original_collection, collection_path)

    print(os.path.getsize(collection_path))
    print(os.listdir('/home/worker'))

    col = Collection(original_collection, server=True)
    model = col.models.byName('Cloze reversed')
    deck = col.decks.byName('Swedish 2')
    col.decks.select(deck['id'])

    col.models.setCurrent(model)
    # note = Note(col, model)
    # note.
    note = col.newNote()
    # note.model()
    note.fields = [
        # 'Heja på'.encode('utf-8'), 'Heja <<c1:på>>'.encode('utf-8'), 'Support'.encode('utf-8'), ''.encode('utf-8'),
        'Heja på', 'Heja {{c1::på}}', 'Support', '',
    ]
    # col.addNote(note)

    # card = col.sched.getCard()
    # card_note = card.note()
    # print(card_note)
    # col.close()


# today = intTime()  # anki function returns current integer time
# nextTwenty = today + 20 * 60  # integer time in 20 minutes
#
# query="select count(id) from cards where queue = 1 and due < %s" % nextTwenty
# learnAheadCards = col.db.scalar(query)
#
# print("You have %s learning cards due in Anki" % learnAheadCards)
#
# col.close()
