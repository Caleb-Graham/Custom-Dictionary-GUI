import requests
import json
import sqlite3
from tkinter import *
import center_tk_window
from tkinter import messagebox


def api():
    """Calls the twinword api and allows you to parse 'r' """
    url = "https://twinword-word-graph-dictionary.p.rapidapi.com/definition/"

    headers = {
        'x-rapidapi-host': "twinword-word-graph-dictionary.p.rapidapi.com",
        'x-rapidapi-key': "340d528947mshe2fbc39eb0dd579p11a01bjsn46992916a685"
    }

    querystring = {"entry": word}
    response = requests.request("GET", url, headers=headers, params=querystring)

    r = json.loads(response.text)
    return r


def get_definition():
    """Parses the api and gets the definition of the word you want and shows it in a new window"""
    global word
    word = search_for_word_textbox.get()
    search_for_word_textbox.delete(0, END)

    if api()['result_msg'] == "Entry word not found":
        messagebox.showerror("Word Error", "This word could not be found in our database. Please check your "
                                           "spelling or try a new word.")

    else:
        global find_definition
        find_definition = Tk()
        find_definition.title("Definition")

        global noun
        global verb
        global adverb
        global adjective
        noun = api()['meaning']['noun']
        verb = api()['meaning']['verb']
        adverb = api()['meaning']['adverb']
        adjective = api()['meaning']['adjective']
        word_def = Label(find_definition, text=noun + "\n\n" +
                                               verb + "\n\n" +
                                               adverb + "\n\n" +
                                               adjective,
                         font=("Helvetica", 15, "bold"))
        word_def.grid(row=0, column=0, columnspan=5)

        add_to_dictionary_button = Button(find_definition, text="Add to my Dictionary", command=commit_to_database)
        add_to_dictionary_button.grid(row=1, column=0, columnspan=5)

        exit_button = Button(find_definition, text="Exit", command=find_definition.destroy)
        exit_button.grid(row=2, column=0, columnspan=5)


def create_database():
    """Creates a new database and table to store definitions"""
    connection = sqlite3.connect('dictionary_db')
    # Creates cursor
    cursor = connection.cursor()

    table_exists = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='{dictionary2}' ")

    if table_exists:
        pass

    else:
        # Create a table """""" == docstring
        cursor.execute("""CREATE TABLE dictionary2 (
              word TEXT,
              noun TEXT,
              verb TEXT,
              adverb TEXT,
              adjective TEXT
              )""")

    # Commit our command
    connection.commit()
    # Close our connection
    connection.close()


def commit_to_database():
    """Adds new definitions into the database and notify's user if done correctly"""
    create_database()

    connection = sqlite3.connect('dictionary_db')
    cursor = connection.cursor()

    commit = cursor.execute("INSERT INTO dictionary2 VALUES(?, ?, ?, ?, ?)",
                            (str(word.capitalize()), str(noun), str(verb), str(adverb), str(adjective)))
    if commit:
        messagebox.showinfo("Item Added", "The word " + word + " has been successfully added to your dictionary!")
        find_definition.destroy()

    else:
        item_add = messagebox.showerror("Error", "No word could be added to your dictionary. Please try again.")
        Label(root, text=item_add).grid()

    connection.commit()
    connection.close()


def show_dictionary():
    show_dict = Tk()
    show_dict.title("Custom Dictionary")

    connection = sqlite3.connect('dictionary_db')
    cursor = connection.cursor()
    cursor.execute("SELECT rowid, * FROM dictionary2 ORDER BY word")
    items = cursor.fetchall()

    scrollbar = Scrollbar(show_dict)
    scrollbar.pack(side=RIGHT, fill=Y)
    text = Text(show_dict, wrap=WORD, yscrollcommand=scrollbar.set)
    text.pack()
    for item in items:
        dictionary = item[1] + ": \n" + "Noun - " + item[2] + "\n" + "Verb - " + item[3] + "\n" + "Adverb - " + item[4] \
                     + "\n" + "Adjective - " + item[5] + "\n\n\n"
        text.insert(END, dictionary)

    text.config(state=DISABLED)
    text.config(font=("Verdana", 16))
    scrollbar.config(command=text.yview)

    exit_button = Button(show_dict, text="Exit", command=show_dict.destroy)
    exit_button.pack()

    connection.commit()
    connection.close()


def edit_dictionary():
    global edit_dict
    edit_dict = Tk()
    edit_dict.title("Custom Dictionary")
    # edit_dict.geometry("665x50")

    connection = sqlite3.connect('dictionary_db')
    cursor = connection.cursor()
    cursor.execute("SELECT rowid, * FROM dictionary2 ORDER BY word")
    items = cursor.fetchall()

    scrollbar = Scrollbar(edit_dict)
    scrollbar.pack(side=RIGHT, fill=Y)

    text = Text(edit_dict, wrap=WORD, yscrollcommand=scrollbar.set)
    text.pack()
    for item in items:
        dictionary = item[1] + ": \n" + "Noun - " + item[2] + "\n" + "Verb - " + item[3] + "\n" + "Adverb - " + item[4] \
                     + "\n" + "Adjective - " + item[5] + "\n\n\n"
        text.insert(END, dictionary)

    text.config(state=DISABLED)
    text.config(font=("Verdana", 16))
    scrollbar.config(command=text.yview)

    delete_dictionary_button = Button(edit_dict, text="Click Here to Delete a Definition",
                                      command=delete_dictionary_window)
    delete_dictionary_button.pack()

    exit_button = Button(edit_dict, text="Exit", command=edit_dict.destroy)
    exit_button.pack()

    connection.commit()
    connection.close()


def delete_dictionary_window():
    global delete_record_layer
    delete_record_layer = Tk()
    delete_record_layer.title("Delete Record")
    delete_record_layer.geometry("700x130")

    delete_record_label = Label(delete_record_layer, text="Enter the Word You Would Like to Delete Below", font=("symbol", 20, "bold"))
    delete_record_label.grid(row=0, column=0, columnspan=10)

    global remove_word_textbox
    remove_word_textbox = Entry(delete_record_layer, font=("Verdana", 30))
    remove_word_textbox.grid(row=1, column=0, columnspan=3, padx=10, pady=15)

    remove_from_dictionary_button = Button(delete_record_layer, text="Remove from Dictionary", padx=45, pady=13,
                                           command=delete_record)
    remove_from_dictionary_button.grid(row=1, column=5, columnspan=5)

    exit_button = Button(delete_record_layer, text="Exit", command=delete_record_layer.destroy)
    exit_button.grid(row=2, column=0, columnspan=10)


def delete_record():
    delete_word = remove_word_textbox.get()
    remove_word_textbox.delete(0, END)

    connection = sqlite3.connect('dictionary_db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM dictionary2 WHERE word=?", [delete_word])

    grab_word = cursor.fetchone()
    if grab_word:
        cursor.execute("DELETE from dictionary2 WHERE word=?", (delete_word,))
        messagebox.showinfo("Item Removed",
                            "The word " + delete_word + " has been successfully removed from your dictionary.")
        edit_dict.destroy()
        delete_record_layer.destroy()

    else:
        messagebox.showerror("Error",
                             "The word " + delete_word + " could not be removed. Check your spelling and try again.")

    connection.commit()
    connection.close()


root = Tk()
root.title("My Dictionary")
root.geometry("650x210")
center_tk_window.center_on_screen(root)
# root.configure(background="blue")


# Create Labels
dictionary_label = Label(root, text="A dictionary is merely the universe arranged in alphabetical order.  - Anatole "
                                    "France", font=("Symbol", 15, "bold"))
dictionary_label.grid(row=0, column=0, columnspan=5)

# Create Text Boxes
search_for_word_textbox = Entry(root, font=("Verdana", 30))  # borderwidth=5 (option)
search_for_word_textbox.grid(row=1, column=0, columnspan=3, padx=10, pady=15)

# Create Buttons
get_definition_button = Button(root, text="Get Definition", padx=45, pady=13, command=get_definition)
get_definition_button.grid(row=1, column=4)

show_dictionary_button = Button(root, text="Show My Dictionary", padx=261, pady=15, command=show_dictionary)
show_dictionary_button.grid(row=3, column=1, columnspan=5)

edit_dictionary_button = Button(root, text="Edit My Dictionary", padx=266, pady=15, command=edit_dictionary)
edit_dictionary_button.grid(row=4, column=1, columnspan=5)

root.mainloop()
