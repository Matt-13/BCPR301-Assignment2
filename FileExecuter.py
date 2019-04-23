# Ignore errors below this line.
import sys
import os
import cmd
import coverage
import doctest
from pythonscripts.FileController import FileController
from pythonscripts.FileView import FileView

# Execute code here
# Matthew Whitaker's code.
fv = FileView()
fc = FileController()


# 4/04/19 Code passes the PEP8 Check.
# CMD based code - Matt


class Main(cmd.Cmd):
    def __init__(self):
        super(Main, self).__init__()
        self.intro = \
            "===============================================\n" \
            "PlantUML to Python Converter\n" \
            "Please type 'help' for all available commands.\n" \
            "Please type 'allhelp' to view the help file.\n" \
            "To continue with a default graph.txt in the\n" \
            "root directory, press [Enter]\n" \
            "=============================================="
        self.interrupt = "Ctrl + C pressed, but ignored. " \
                         "Please use 'exit' or 'quit' " \
                         "to stop the program."
        self.verifycommand = "Please verify your command, and try again."
        self.error = "An error has occurred."

    # Extract tests into their own method to prevent duplication and long method.
    def do_tests(self):
        fc.test()  # Test FileController and FileHandler
        fv.test()
        self.test()

    # CMD - Matt
    def cmdloop(self, intro=None):
        # self.do_tests()  # first instance of duplication
        print(self.intro)
        while True:
            try:
                super(Main, self).cmdloop(intro="")
                break
            except KeyboardInterrupt:
                print(self.interrupt)
            except TypeError and ValueError:
                fv.general_error()
                print(self.verifycommand)
            except Exception:
                fv.general_error()
                print(self.error)

    # Continues when no command is entered - Matt
    def emptyline(self):
        fv.fe_defaults()
        fc.handle_command('', '')
        fv.next_command()

    # Load method - Matt
    def do_load(self, line):
        """
        LOADS your SOURCE PlantUML text file, and translates it
        into a python file, from the current working directory.
        Usage: LOAD [filename.txt]
        """
        fc.handle_command("load", line)
        fv.next_command()

    # Absload method - Matt
    def do_absload(self, line):
        """
        LOADS your SOURCE PlantUML text file, and translates it
        into a python file, from the directory of your choosing.
        Usage: ABSLOAD [path_to_filename.txt]
        """
        if "\\" in line:
            fc.handle_command("absload", line)
        else:
            fv.general_error()
            fv.fe_abs_path_error()
        # Next instance of duplication removed.
        fv.next_command()

    # View help file - Matt and Liam
    def do_allhelp(self, line):
        """
        SHOWS all HELP relating to this program.
        Usage: ALLHELP
        """
        fv.print_help()
        fv.next_command()

    # Exit method - Matt
    def do_exit(self, line):
        """
        EXITS the program cleanly. (same as QUIT)
        Usage: quit, exit, q
        """
        exit()

    # TODO: Add exit into quit, q, e, x, stop methods.
    # exit = do_exit()
    # do_quit = exit
    # do_q = exit

    # Save method - Liam
    def do_save(self, line):
        """
        Saves the converted plantuml code from the database to a textfile
        Usage: save {filename.txt} {code_id}
        """
        line = line.split(' ')
        fc.save_file(line[0], line[1])
        fv.next_command()

    # Printcode method - Liam
    def do_printcode(self, line):
        """
        Prints the converted plantuml code from the database to the cmd
        Usage: printcode {code_id}
        """
        fc.print_code(line)
        fv.next_command()

    # Loadcode method - Liam
    def do_loadcode(self, line):
        """
        Loads code from the database into self.data
        Usage: loadcode {code_id}
        """
        fc.load_code(line)
        fv.next_command()

    # Printfile method - Liam
    def do_printfile(self, line):
        """
        Prints the data saved inside self.data to the cmd
        Usage: printfile
        """
        fc.print_file()
        fv.next_command()

    @staticmethod
    def test():
        import doctest
        doctest.testfile("./doctests/fileexecuter_doctest.txt")


# Liam
"""
def print_to_screen():
    their_answer = input("Would you like to print the "
                         "code to the screen? y/n: ")
    if their_answer == "y":
        fc.print_file()

    their_answer = input("Would you like to save the code to Output.txt y/n: ")
    if their_answer == "y":
        fc.save_file("Output.txt")
"""

m = Main()


class SystemArgs:
    def __init__(self):
        self.command = ""
        self.commandargs = ""
        self.commands = ["absload", "load", "loadcode", "help", "save", "printcode"]
        self.args = sys.argv[1:]

    def check_if_commands_present(self):
        # If there is commands then:
        if len(self.args) > 2:
            fv.general_error()
            fv.fe_too_many_args()
        elif len(self.args) >= 1:
            self.command = str(sys.argv[1]).lower()
            # TODO: Sorta duplication, will fix later :)
            if self.check_if_commandargs_present():
                self.check_command()
            else:
                self.check_command()
        # Otherwise, Start the CMD.cmdloop
        else:
            m.cmdloop()

    def check_if_commandargs_present(self):
        if len(self.args) == 2:
            return True
        else:
            return False

    def check_command(self):
        if self.command in self.commands:
            fv.output("Command Found.. Parsing..")
            self.command_to_function()
        else:
            fv.output("'" + self.command + "' Command not Found, "
                                           "type 'FileExecuter.py help' for all available commands.")

    def command_to_function(self):
        if self.command == "help":
            self.do_help_command()
        elif self.command == "absload":
            self.do_absload_command()
        elif self.command == "load":
            self.do_load_command()
        elif self.command == "save":
            self.do_save_command()
        elif self.command == "loadcode":
            self.do_loadcode_command()
        elif self.command == "printcode":
            self.do_printcode_command()

    def do_absload_command(self):
        pass
    def do_load_command(self):
        pass
    def do_save_command(self):
        pass

    @staticmethod
    def do_help_command():
        fc.view_help()

    def do_loadcode_command(self):

    def do_printcode_command(self):

    def do_save_command(self):



if __name__ == "__main__":
    a = SystemArgs()
    a.check_if_commands_present()
    # test()
    # For Debugging Sys.Argv
    # print('Number of arguments:', len(sys.argv), 'arguments.')
    # print('Argument List:', str(sys.argv))
    try:
        if len(sys.argv) < 2:
            pass
            # fv.fe_defaults()
            # fc.handle_command('', '')
            # print_to_screen()
        """
        elif len(sys.argv) > 3:
            # Liam's save command
            if command == "save":
                if len(sys.argv) == 2:
                    fv.general_error()
                    fv.fe_command_syntax("Save")
                else:
                    fc.save_file(sys.argv[2], sys.argv[3])
            else:
                fv.fe_too_many_args()
        else:
            if command == "help":
                

            # Liam's save command
            elif command == "save":
                if len(sys.argv) == 2:
                    fv.general_error()
                    fv.fe_command_syntax("Save")
                else:
                    fc.save_file(sys.argv[2], sys.argv[3])

            # Liam's loadcode command
            elif command == "loadcode":
                if len(sys.argv) == 2:
                    fv.general_error()
                    fv.fe_loadcode_syntax("loadcode")
                else:
                    fc.load_code(sys.argv[2])

            # Liam's printcode command
            elif command == "printcode":
                if len(sys.argv) == 2:
                    fv.general_error()
                    fv.fe_loadcode_syntax("printcode")
                else:
                    fc.print_code(sys.argv[2])

            elif command == "load":
                if len(sys.argv) == 2:
                    fv.general_error()
                    fv.fe_command_syntax("Load")
                else:
                    fc.handle_command("load", str(sys.argv[2]))
            elif command == "absload":
                if len(sys.argv) == 2:
                    fv.general_error()
                    fv.fe_abs_syntax()
                if "\\" in str(sys.argv[2]):
                    fc.handle_command("absload", str(sys.argv[2]))
                else:
                    fv.general_error()
                    fv.fe_abs_path_error()
            else:
                fv.general_error()
                fv.output("Command not found!")
        """
    # Ignores issues with Sys.argv
    except IndexError:
        pass
    # Checks for file permission errors.
    except PermissionError:
        print("Permission Error!\n"
              "Check you have the permission to read the file!")
    else:
        pass
        # m.cmdloop()
