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
        self.command = ''
        self.data = 'empty'
        self.file_location = ''
        self.loop_running = False

    def user_choose(self):
        self.loop_running = True
        while self.loop_running:
            userinput = input("Would you like to view the file in your default text editor? (Y/N) ")
            if userinput.lower() == "y":
                os.startfile("Output.txt")
                break
            elif userinput.lower() == "n":
                break
            else:
                print("Please enter either Y or N.. {} was entered.".format(userinput))
                pass
        self.loop_running = False

    # Command Handler - Made by Matthew
    def handle_command(self, cmd, file_location):
        self.file_location = file_location
        self.command = cmd
        try:
            if cmd == "":
                self.no_command(file_location)
            elif cmd == "load":
                self.load_command(file_location)
            elif cmd == "absload":
                self.absload_command(file_location)
        except FileNotFoundError:
            fv.fc_load_file_error(file_location)

    @staticmethod
    def is_file(filename):
        if os.path.isfile("{}".format(filename)):
            return True
        else:
            return False

    def no_command(self, file_location):
        fv.fc_defaults(file_location)
        try:
            if os.path.isfile("../Graph.txt"):
                fv.fc_file_found()
                self.read_file("../Graph.txt")
            self.user_choose()
        except FileNotFoundError:
            fv.general_error()
            fv.fc_file_not_found(file_location, "r", "")

    def load_command(self, file_location):
        if file_location.endswith(".txt"):
            try:
                if os.path.isfile("../{}".format(file_location)):
                    fv.fc_file_found()
                    self.read_file("../{}".format(file_location))
                self.user_choose()
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

    def absload_command(self, file_location):
        if file_location.endswith(".txt"):
            try:
                if self.is_file(file_location):
                    fv.fc_file_found()
                    self.read_file("../{}".format(file_location))
                    self.user_choose()
                else:
                    fv.general_error()
                    fv.fc_load_file_error(file_location)
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
            fw.write_file(self.data, "Output.py")
            db.data_entry(self.data)
            # fv.file_written("Output.txt, Output.py")
        except AttributeError as e:
            print(e)
        except IOError:
            print("System failed to save to file")
        except Exception as e:
            fv.general_error()
            print("An error has occurred")
            print(e)

    # Liam
    def print_file(self):
        try:
            fv.display_graph_code(self.data)
        except IOError:
            print("System failed to load to file")
        except Exception as e:
            fv.general_error()
            print("An error has occurred")
            print(e)

    # Liam
    def save_file(self, file_name, code_id):
        self.data = db.get_code(code_id)
        try:
            fw.write_file(db.get_code(code_id), file_name)
        except AttributeError as e:
            print(e)
        except IOError as e:
            print("System failed to save to file")
        except Exception as e:
            fv.general_error()
            print("An error has occurred")
            print(e)

    # Liam
    def load_code(self, code_id):
        try:
            code = db.get_code(code_id)
            if code != '':
                self.data = code
                fv.display("Code has loaded successfully")
            else:
                fv.display("ERROR: code failed to load:")
                fv.display('\t' + code)
        except AttributeError as e:
            print(e)
        except IOError:
            print("System failed to save to file")
        except ValueError and TypeError:
            fv.display("Please enter an integer")
        except Exception as e:
            fv.general_error()
            print("An error has occurred")
            print(e)

    # Liam
    def print_code(self, code_id):
        try:
            code = db.get_code(code_id)
            if code != '':
                fv.display_graph_code(code)
            else:
                fv.display("ERROR: code failed to load:")
                fv.display('\t' + code)
        except ValueError and TypeError:
            fv.display("Please enter an integer")
        except IOError as e:
            print("System failed to load to file")
            print(e)

    # Matthew
    def quit(self):
        pass

    # Matthew
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
