# Code passes the PEP8 check. 4/04/19

# Ignore errors here.
from pythonscripts.FileHandler import FileConverter
from pythonscripts.FileView import FileView
from pythonscripts.FileWriter import FileWriter
import os
from pythonscripts.DataBase import DataBase

fconv = FileConverter()
fw = FileWriter()
fv = FileView()
db = DataBase()


class FileController:
    def __init__(self):
        fconv.test()
        self.data = 'empty'
        self.loop_running = False
        self.get_commands = {
            "": self.no_command,
            "load": self.load_command,
            "absload": self.absload_command
        }

    def user_choose(self):
        self.loop_running = True
        while self.loop_running:
            userinput = input("Would you like to view the file"
                              "in your default text editor? (Y/N) ")
            if userinput.lower() == "y":
                os.startfile("Output.txt")
                break
            elif userinput.lower() == "n":
                break
            else:
                print("Please enter either Y or N.. "
                      "{} was entered.".format(userinput))
                pass
        self.loop_running = False

    # Command Handler - Made by Matthew
    # Refactored with a dictionary.
    def handle_command(self, cmd, file_location):
        try:
            self.get_commands[cmd](file_location)
        except FileNotFoundError:
            fv.fc_file_not_found(file_location, "lf", "")

    @staticmethod
    def is_file(filename):
        if os.path.isfile("{}".format(filename)):
            return True
        elif os.path.isfile("./{}".format(filename)):
            return True
        else:
            return False

    # Good removal of duplication.
    def no_command(self, file_location):
        fv.fc_defaults(file_location)
        try:
            if self.is_file("Graph.txt"):
                fv.fc_file_found()
                self.read_file("./Graph.txt")
                self.user_choose()
            else:
                fv.output("Graph.txt Not Found in root!")
        except FileNotFoundError:
            fv.general_error()
            fv.fc_file_not_found(file_location, "r", "")

    # Will look at refactoring when I start with Long Methods.
    def load_command(self, file_location):
        if file_location.endswith(".txt"):
            try:
                if self.is_file(file_location):
                    fv.fc_file_found()
                    self.read_file("./{}".format(file_location))
                    self.user_choose()
                else:
                    fv.output("File Not Found! '{}'".format(file_location))
            except FileNotFoundError:
                fv.general_error()
                fv.fc_file_not_found(file_location, "r", "load")
            except PermissionError:
                fv.general_error()
                fv.fc_permission_error()
        elif file_location == "":
            fv.general_error()
            fv.fc_file_not_found(file_location, "", "load")
        else:
            fv.general_error()
            fv.fc_syntax_error("load")

    # Will look at refactoring when I start with Long Methods.
    def absload_command(self, file_location):
        if file_location.endswith(".txt"):
            try:
                if self.is_file(file_location):
                    fv.fc_file_found()
                    self.read_file("{}".format(file_location))
                    self.user_choose()
                else:
                    fv.general_error()
                    fv.fc_file_not_found(file_location, "lf", "")
            except FileNotFoundError:
                fv.fc_file_not_found(file_location, "a", "absload")
            except PermissionError:
                fv.fc_permission_error()
        elif file_location == "":
            fv.general_error()
            fv.fc_file_not_found(file_location, "", "absload")
        else:
            fv.general_error()
            fv.fc_syntax_error("absload")

    # Reads file - Liam
    def read_file(self, filename):
        try:
            fconv.read_file(filename)
            fconv.convert_file()
            fconv.return_program()
            self.data = fconv.codeToText
            fw.write_file(self.data, "Output.txt")
            db.data_entry(self.data)
        except IOError:
            print("System failed to save to file")
        except Exception as e:
            fv.general_error()
            print("An error has occurred")
            print(e)

    # Liam
    def save_file(self, file_name, code_id):
        self.data = db.get_code(code_id)
        try:
            fw.write_file(db.get_code(code_id), file_name)
        except IOError as e:
            print("System failed to save to file" + e)
        except Exception as e:
            fv.general_error()
            print("An error has occurred" + str(e))

    # Liam
    def load_code(self, code_id):
        try:
            code = db.get_code(code_id)
            if code != '':
                self.data = code
                fv.output("Code has loaded successfully")
            else:
                fv.output("ERROR: code failed to load:" + '\t' + code)
        except IOError:
            print("System failed to save to file")
        except Exception as e:
            fv.general_error()
            print("An error has occurred" + str(e))

    # Liam
    def print_code(self, code_id):
        try:
            code = db.get_code(code_id)
            if code != '':
                fv.output(code)
            else:
                fv.output("ERROR: code failed to load:")
                fv.output('\t' + code)
        except ValueError and TypeError:
            fv.output("Please enter an integer")
        except IOError as e:
            print("System failed to load to file" + e)

    # Matthew - Possible Middle Man Smell..
    @staticmethod
    def view_help():
        fv.print_help()

    # Matthew
    @staticmethod
    def output_error(message):
        fv.general_error()
        fv.output(message)

    @staticmethod
    def test():
        import doctest
        doctest.testfile("../doctests/filecontroller_doctest.txt", verbose=1)
