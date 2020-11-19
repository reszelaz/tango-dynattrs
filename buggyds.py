import PyTango

from PyTango import AttrWriteType, DispLevel
from PyTango.server import Device, DeviceMeta, attribute, command, server_run, device_property
from PyTango import Attr, UserDefaultAttrProp


class BuggyDS(Device):
    AorB = device_property(dtype=str, default_value="A", doc="A or B")

    def init_device(self):
        self.debug_stream("In init_device()")
        self.get_device_properties(self.get_device_class())
        self.AttrA = {
            "FirstValue":  # causes trouble if different types, or different R / RW
                {"Type": PyTango.DevDouble,
                 "Access": AttrWriteType.READ_WRITE,
                 "r_meth": self.read_1_a,
                 "w_meth": self.write_1_a,
                 },
            "SecondValue":
                {"Type": PyTango.DevDouble,
                 "Access": AttrWriteType.READ_WRITE,
                 "r_meth": self.read_2_a,
                 "w_meth": self.write_2_a,
                 },
            "ThirdValue":  # must be read-only, can have different names
                {"Type": PyTango.DevDouble,
                 "Access": AttrWriteType.READ,
                 "r_meth": self.read_3_a,
                 },
        }
        self.AttrB = {
            "FirstValue":
                {"Type": PyTango.DevDouble,
                 "Access": AttrWriteType.READ,
                 "r_meth": self.read_1_b,
                 },
        }

    def initialize_dynamic_attributes(self):
        if self.AorB == "A":
            attrs = self.AttrA
        elif self.AorB == "B":
            attrs = self.AttrB

        for attr_name, params in attrs.items():
            print("Create dynamic attribute:", attr_name)
            attr = Attr(attr_name, params["Type"], params["Access"])
            attr.set_disp_level(DispLevel.OPERATOR)
            try:
                if "w_meth" in params:
                    self.add_attribute(
                        attr, r_meth=params["r_meth"], w_meth=params["w_meth"])
                else:
                    self.add_attribute(attr, r_meth=params[
                        "r_meth"])
            except Exception as e:
                print(e)

    def read_1_a(self, attr):
        print("A read {}, got read method for FirstValue A".format(attr.get_name()))
        attr.set_value(1.0)

    def read_2_a(self, attr):
        print("A read {}, got read method for SecondValue A".format(attr.get_name()))
        attr.set_value(2.0)

    def read_3_a(self, attr):
        print("A read {}, got read method for ThirdValue A".format(attr.get_name()))
        attr.set_value(3.0)

    def write_1_a(self, attr):
        print("A write {}, got read method for FirstValue A".format(attr.get_name()))

    def write_2_a(self, attr):
        print("A write {}, got read method for SecondValue A".format(attr.get_name()))

    def read_1_b(self, attr):
        print("B read {}, got read method for FirstValue B".format(attr.get_name()))
        attr.set_value(4.0)


def main():
    server_run((BuggyDS,))


if __name__ == "__main__":
    main()
