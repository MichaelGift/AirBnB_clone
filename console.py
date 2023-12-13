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
    """
    Parse a string 'arg' to extract content within curly or square brackets.

    Returns a list of extracted elements with leading/trailing commas removed.

    Used for tokenizing and processing input in a specific format.
    """

    curly_braces_match = re.search(r"\{(.*?)\}", arg)
    brackets_match = re.search(r"\[(.*?)\]", arg)

    if curly_braces_match is None:
        if brackets_match is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets_match.span()[0]])
            return [i.strip(",") for i in lexer] + [brackets_match.group()]
    else:
        lexer = split(arg[:curly_braces_match.span()[0]])
        return [i.strip(",") for i in lexer] + [curly_braces_match.group()]


class HBNBCommand(cmd.Cmd):
    """
    Defines the HolbertonBnB command interpreter.
    Attributes:
        prompt (str): The command prompt.
    """

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
        """Default behavior for cmd module when input is invalid"""
        arg_dict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }

        dot_match = re.search(r"\.", arg)

        if dot_match:
            prefix, suffix = arg.split(dot_match.group(), 1)
            parentheses_match = re.search(r"\((.*?)\)", suffix)

            if parentheses_match:
                command = [suffix[:parentheses_match.span()[0]],
                           parentheses_match.group()[1:-1]]

                if command[0] in arg_dict:
                    call = "{} {}".format(prefix, command[1])
                    return arg_dict[command[0]](call)

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
        """
        Usage: create <class>
        Create a new class instance and print its id.
        """
        class_name = parse(arg)

        if not class_name:
            print("** class name missing **")
        elif class_name[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            new_instance = eval(class_name[0])()
            print(new_instance.id)
            storage.save()

    def do_show(self, arg):
        """
        Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        class_and_id = parse(arg)
        obj_dict = storage.all()

        if not class_and_id:
            print("** class name missing **")
        elif class_and_id[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(class_and_id) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(class_and_id[0], class_and_id[1]) not in obj_dict:
            print("** no instance found **")
        else:
            print(obj_dict["{}.{}".format(class_and_id[0], class_and_id[1])])

    def do_destroy(self, arg):
        """
        Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id.
        """
        class_and_id = parse(arg)
        obj_dict = storage.all()

        if not class_and_id:
            print("** class name missing **")
        elif class_and_id[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(class_and_id) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(class_and_id[0], class_and_id[1]) not in obj_dict:
            print("** no instance found **")
        else:
            del obj_dict["{}.{}".format(class_and_id[0], class_and_id[1])]
            storage.save()

    def do_all(self, arg):
        """
        Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects.
        """
        class_name = parse(arg)

        if class_name and class_name[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            obj_list = [obj.__str__() for obj in storage.all().values()
                        if not class_name or
                        class_name[0] == obj.__class__.__name__]
            print(obj_list)

    def do_count(self, arg):
        """
        Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class.
        """
        class_name = parse(arg)
        count = sum(1 for obj in storage.all().values()
                    if class_name and class_name[0] == obj.__class__.__name__)
        print(count)

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        parsed_args = parse(arg)
        object_dict = storage.all()

        if len(parsed_args) == 0:
            print("** class name missing **")
            return False
        if parsed_args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(parsed_args) == 1:
            print("** instance id missing **")
            return False
        if ("{}.{}".format(parsed_args[0], parsed_args[1])
                not in object_dict.keys()):
            print("** no instance found **")
            return False
        if len(parsed_args) == 2:
            print("** attribute name missing **")
            return False
        if len(parsed_args) == 3:
            try:
                type(eval(parsed_args[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(parsed_args) == 4:
            obj = object_dict["{}.{}".format(parsed_args[0], parsed_args[1])]
            if parsed_args[2] in obj.__class__.__dict__.keys():
                val_type = type(obj.__class__.__dict__[parsed_args[2]])
                obj.__dict__[parsed_args[2]] = val_type(parsed_args[3])
            else:
                obj.__dict__[parsed_args[2]] = parsed_args[3]
        elif type(eval(parsed_args[2])) == dict:
            obj = object_dict["{}.{}".format(parsed_args[0], parsed_args[1])]
            for k, v in eval(parsed_args[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    val_type = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = val_type(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
