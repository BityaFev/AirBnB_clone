#!/usr/bin/python3
"""Defines the HBnB console."""

import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    """Parses the input arguments.

    Given a string argument, returns a list of parsed arguments.
    The function supports both curly braces and square brackets.

    Args:
        arg (str): The argument string.

    Returns:
        A list of parsed arguments.
    """
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter."""

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def default(self, arg):
        """Default behavior for cmd module when input is invalid."""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            argl = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argl[1])
            if match is not None:
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(argl[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, arg):
        """Creates a new class instance and prints its id.

        Usage: create <class>

        Args:
            arg (str): The argument string.

        Returns:
            None.
        """
        argl = parse(arg)
        if not argl:
            print("** class name missing **")
            return
        if argl[0] not in self.__classes:
            print("** class doesn't exist **")
            return
        obj = eval(argl[0])()
        obj.save()
        print(obj.id)

    def do_show(self, arg):
        """Displays the string representation of a class instance of a given id.

        Usage: show <class> <id> or <class>.show(<id>)

        Args:
            arg (str): The argument string.

        Returns:
            None.
        """
        argl = parse(arg)
        if not argl:
            print("** class name missing **")
            return
        if argl[0] not in self.__classes:
            print("** class doesn't exist **")
            return
        if len(argl) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(argl[0], argl[1])
        obj = storage.all().get(key)
        if obj is None:
            print("** no instance found **")
            return
        print(obj)

    def do_destroy(self, arg):
        """Deletes a class instance of a given id.

        Usage: destroy <class> <id> or <class>.destroy(<id>)

        Args:
            arg (str): The argument string.

        Returns:
            None.
        """
        argl = parse(arg)
        if not argl:
            print("** class name missing **")
            return
        if argl[0] not in self.__classes:
            print("** class doesn't exist **")
            return
        if len(argl) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(argl[0], argl[1])
        obj = storage.all().get(key)
        if obj is None:
            print("** no instance found **")
            return
        del storage.all()[key]
        storage.save()
    
    def do_all(self, arg):
        """
        Display string representations of all instances of a given class or of
        all instantiated objects if no class is specified.

        Usage: all or all <class> or <class>.all()

        Args:
            arg (str): The argument string containing the class name, if any.

        """
        argl = parse(arg)
        objdict = storage.all()
        objl = []
        if not argl:
            objl = [str(obj) for obj in objdict.values()]
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        else:
            objl = [str(obj) for obj in objdict.values()
                    if obj.__class__.__name__ == argl[0]]
        print(objl)


if __name__ == "__main__":
    HBNBCommand().cmdloop()