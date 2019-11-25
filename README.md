since I like to manage most of my cards via text files, I created some helper functions to create
those cards for me. featuring:

# cloze overlapper creator

inspired by [Cloze Overlapper](https://ankiweb.net/shared/info/969733775), and [supermemo](https://www.supermemo.com/en/archives1990-2015/articles/20rules#Enumerations)

the script expects a csv file with tab as delimiter and the following column order: id, tags, text.
For the cards with lists the script does not expect any cloze in the text field.

It will create a new file next the given one with `_mod.csv` at the end, you can then import this
file into anki.

