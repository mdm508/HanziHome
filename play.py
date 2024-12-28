

from anki.collection import Collection

# Open a collection file
col = Collection("/Users/m/Library/Application Support/Anki2/User 1/collection.anki2")

# Print deck due tree (shows due cards)
print(col.sched.deck_due_tree())

