#!/usr/bin/python3
"""THE HBNB Console"""


import cmd
import json
from models import storage
from models.base_model import BaseModel


class HBNBCommand(cmd.Cmd):
    """HBNBCommand class"""
    prompt = "(hbnb) "

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        print()
        return True

    def emptyline(self):
        """Do nothing on empty line"""
        pass

    def do_create(self, arg):
        """ Creates a new instance of BaseModel
            USAGE: create <classname>
            Example: create BaseModel
        """
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        else:
            cls_name = args[0]
            try:
                obj = eval(cls_name)
                obj = obj()
                storage.new(obj)
                print(storage.save())
                print(obj.id)
            except NameError:
                print("** class doesn't exist **")

    def do_show(self, arg):
        """
            Display the string representation of
            a class instance of a given id.
            USAGE: show <class> <id>
        """

        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            class_name = args[0]
            instance_id = args[1]
            try:
                filename = "file.json"
                with open(filename, "r") as f:
                    data = json.load(f)
                key = "{}.{}".format(class_name, instance_id)
                obj_data = data.get(key)
                if obj_data is None:
                    print("** no instance found **")
                else:
                    obj = eval(class_name)(**obj_data)
                    print(obj)
            except NameError:
                print("** class doesn't exist **")




if __name__ == '__main__':
    HBNBCommand().cmdloop()