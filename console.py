#!/usr/bin/python3

"""
command line implementation
for managing my application
"""

import cmd
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models import storage

expected_class = {
        "BaseModel": BaseModel, "User": User,
        "State": State, "City": City,
        "Place": Place, "Amenity": Amenity,
        "Review": Review
        }


def parsed_dict(arg):
    """parse arg(str)and returns a dictionary objects"""
    extracted_dict = arg[
            arg.find("{"):arg.find("}") + 1]
    inside_curly = extracted_dict[
            1:extracted_dict.find("}")]
    no_comma = inside_curly.split(",")
    diction = {}
    for item in no_comma:
        item = item.split(":")
        key = item[0].strip().strip('"')
        value = item[1].strip().strip('"')
        diction[key] = value
    return diction


class HBNBCommand(cmd.Cmd):
    """class that implement command line
    functionality for managing my application
    """
    prompt = "(hbnb)"

    def do_quit(self, line):
        """exit the program"""
        return True

    def do_EOF(self, line):
        """End of File exit the program"""
        return True

    def emptyline(self):
        """don't do anything"""
        return

    def _clean_d(self, g):
        """takes a dictionary g and returns
        a formatted dictionary of required
        data types"""
        d = {}
        for k, v in g.items():
            if '"' in v:
                v = v.strip('"').replace("_", " ")
            else:
                try:
                    v = eval(v)
                except ValueError:
                    continue
            d[k] = v
        return d

    def do_create(self, line):
        """create command create a new instance of basemodel,
        using the format:
        create <class name> <param1>
        <param2>...
        where param is of the form:
            <key>=<value>"""
        line_args = line.split()
        if len(line_args) < 1:
            print("** class name missing **")
            return
        if line_args[0] not in expected_class:
            print("** class doesn't exist **")
            return
        try:
            passed_args = line_args[1:]
            list_of_tup = [tuple(i.split("=")) for i in passed_args]
            # print(list_of_tup)
            dict_of_args = dict(list_of_tup)
            formatted_args = self._clean_d(dict_of_args)
            obj = expected_class[line_args[0]](**formatted_args)
            obj.save()
            print(obj.id)
        except IndexError:
            pass

    def do_show(self, line):
        """print the string representation of an instance
        base on the class name and id"""
        args = line.split()
        if len(args) < 1:
            print("** class name missing **")
            return
        if args[0] not in expected_class:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return

        all_inst = storage.all()
        key = ".".join(args)
        if key not in all_inst:
            print("** no instance found **")
            return
        print(all_inst[key])

    def do_destroy(self, line):
        """deletes an instance based on the class name
        and id, save the change into JSON file"""
        args = line.split()
        if len(args) < 1:
            print("** class name missing **")
            return
        if args[0] not in expected_class:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return

        all_inst = storage.all()
        key = ".".join(args)
        if key not in all_inst:
            print("** no instance found **")
            return
        del all_inst[key]
        storage.save()

    def do_all(self, line):
        """print all string representation ofi nstances
        based or not on the classname"""
        args = line.split()
        all_inst = storage.all()
        if len(args) < 1:
            list_inst = [str(val) for val in all_inst.values()]
            print(list_inst)
        elif args[0] not in expected_class:
            print("** class doesn't exist **")
            return
        else:
            key = args[0]
            match_class = [
                    str(v) for k, v in all_inst.items()
                    if key == k.split(".")[0]
                    ]
            print(match_class)

    def do_update(self, line):
        """update an instance based on the class name
        and id by adding or updating attributes and
        saving change into JSON file
        usage: update <classname> <id> <attribute name>
        '<attribute value>'"""
        args = line.split()
        if len(args) < 1:
            print("** class name missing **")
            return
        if args[0] not in expected_class:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        all_inst = storage.all()
        key = ".".join(args[:2])
        if key not in all_inst:
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        arg_val = args[3].strip('"')
        if arg_val.isdigit():
            arg_val = int(arg_val)
        attr_name = args[2]
        obj = all_inst[key]
        obj_dict = obj.to_dict()
        if attr_name not in obj_dict:
            obj.__dict__[attr_name] = arg_val
            obj.save()
        else:
            if type(obj_dict[attr_name]) != type(arg_val):
                # try-except may come here
                arg_val = type(obj_dict[attr_name])(arg_val)
                obj.__dict__[attr_name] = arg_val
            else:
                obj.__dict__[attr_name] = arg_val
                obj.save()

    def default(self, line):
        """executed as the default when argument doesn't
        start with the given methods"""
        args = line.split(".")
        ind = args[1].find("(")
        last_ind = args[1].find(")")
        method = args[1][:ind]
        if method == "all":
            self.do_all(args[0])
        elif method == "count":
            all_inst = storage.all()
            list_of_class_inst = [
                    key for key in all_inst.keys()
                    if args[0] == key.split(".")[0]
                    ]
            print(len(list_of_class_inst))
        elif method == "show":
            passed_id = args[1][ind + 1:last_ind].strip('"')
            line_args = "{} {}".format(args[0], passed_id)
            self.do_show(line_args)
        elif method == "destroy":
            passed_id = args[1][ind + 1:last_ind].strip('"')
            line_args = "{} {}".format(args[0], passed_id)
            self.do_destroy(line_args)
        elif method == "update":
            inside_brac = line[line.find("(") + 1: line.find(")")]
            id_ex = inside_brac.split("{")[0].strip().rstrip(",").strip('"')
            if "{" and "}" in inside_brac:
                dict_of_args = parsed_dict(inside_brac)
                for k, v in dict_of_args.items():
                    attr_value = "{} {}".format(k, v)
                    all_args = "{} {} {}".format(args[0], id_ex, attr_value)
                    self.do_update(all_args)
            else:
                line_arg = inside_brac.split(",")
                trimmed_arg = [c.strip().strip('"') for c in line_arg]
                joined_arg = " ".join(trimmed_arg)
                joined_arg_and_class = "{} {}".format(args[0], joined_arg)
                self.do_update(joined_arg_and_class)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
