#!/usr/bin/python3
""" Console Module """
import cmd
import sys
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console """

    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = {
        'BaseModel': BaseModel, 'User': User, 'Place': Place,
        'State': State, 'City': City, 'Amenity': Amenity,
        'Review': Review
    }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
        'number_rooms': int, 'number_bathrooms': int,
        'max_guest': int, 'price_by_night': int,
        'latitude': float, 'longitude': float
    }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for advanced command syntax."""
        _cmd = _cls = _id = _args = ''

        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:
            pline = line[:]
            _cls = pline[:pline.find('.')]
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                pline = pline.partition(', ')
                _id = pline[0].replace('\"', '')
                pline = pline[2].strip()
                if pline:
                    if pline[0] == '{' and pline[-1] == '}' and isinstance(eval(pline), dict):
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """ Method to exit the HBNB console """
        exit()

    def help_quit(self):
        """ Prints the help documentation for quit """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        exit()

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def do_create(self, arg):
        """Create a new instance of a class with given parameters.

        Command syntax: create <Class name> <param1=value1> <param2=value2> ...
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        params = {}
        for param in args[1:]:
            if "=" in param:
                key, value = param.split("=", 1)
                # Handle string values
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1].replace('_', ' ').replace('\\"', '"')
                # Handle float values
                elif '.' in value:
                    try:
                        value = float(value)
                    except ValueError:
                        continue
                # Handle integer values
                else:
                    try:
                        value = int(value)
                    except ValueError:
                        continue
                params[key] = value

        # Create a new instance of the class
        new_instance = HBNBCommand.classes[class_name]()
        for key, value in params.items():
            setattr(new_instance, key, value)
        new_instance.save()
        print(new_instance.id)

    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type")
        print("[Usage]: create <className> <param1=value1> <param2=value2> ...\n")

    def do_show(self, args):
        """ Method to show an individual object """
        args = args.split()
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return

        key = f"{class_name}.{args[1]}"
        try:
            print(storage.all()[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """ Destroys a specified object """
        args = args.split()
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return

        key = f"{class_name}.{args[1]}"
        try:
            del storage.all()[key]
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, arg):
        """Retrieve all objects of a given class or all objects."""
        if not arg:
            objects = storage.all()
        else:
            try:
                objects = storage.all(arg)
            except ValueError as e:
                print(f"** class doesn't exist **")
                return

        for obj in objects.values():
            print(obj)

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """ Count current number of class instances """
        count = 0
        for key in storage.all():
            if key.startswith(args):
                count += 1
        print(count)

    def help_count(self):
        """ Help information for the count command """
        print("Usage: count <class_name>")

    def do_update(self, args):
        """ Updates a certain object with new info """
        args = args.split()
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return

        key = f"{class_name}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return

        obj = storage.all()[key]
        attr_name = args[2]
        attr_value = args[3]

        if attr_name in HBNBCommand.types:
            attr_value = HBNBCommand.types[attr_name](attr_value)

        setattr(obj, attr_name, attr_value)
        obj.save()

    def help_update(self):
        """ Help information for the update command """
        print("Updates an object with new information")
        print("[Usage]: update <className> <id> <attName> <attVal>\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()