import PyTango
from PyTango import AttrWriteType, DispLevel, AttrWriteType, DispLevel
from PyTango.server import Device, DeviceMeta, attribute, command, \
    server_run, device_property


class BuggyDS(Device):

    AorB = device_property(dtype=str, default_value="A", doc="A or B")

    def init_device(self):
        self.debug_stream("In init_device()")
        self.get_device_properties(self.get_device_class())
        self.AttrA = {
            # causes trouble if different types, or different R / RW
            "OffendingValue":  {
                 "Type": PyTango.DevDouble,
                 "Access": AttrWriteType.READ_WRITE,
                 "r_meth": self.read1,
                 "w_meth": self.write1,
            },
            "BestValueA": {
                "Type": PyTango.DevDouble,
                "Access": AttrWriteType.READ_WRITE,
                "r_meth": self.read2,
                "w_meth": self.write2,
            },
            # must be read-only, can have different names
            "WorstValue": {
                "Type": PyTango.DevDouble,
                "Access": AttrWriteType.READ,
                "r_meth": self.read3,
            },
        }
        self.AttrB = {
            "OffendingValue": {
                "Type": PyTango.DevDouble,
                "Access": AttrWriteType.READ,
                "r_meth": self.read1,
            },
        }

    def initialize_dynamic_attributes(self):
        if self.AorB == "A":
            attrs = self.AttrA
        elif self.AorB == "B":
            attrs = self.AttrB
        # Comment this out to try my "fix"
        for attr_name in attrs:
            self.remove_unwanted_dynamic_attributes(attr_name)
        # --

        for attr_name, params in attrs.items():
            print("Create dynamic attribute:", attr_name)
            attr = Attr(attr_name, params["Type"], params["Access"])
            attr.set_disp_level(DispLevel.OPERATOR)
            if "w_meth" in params:
                self.add_attribute(
                    attr,
                    r_meth=params["r_meth"],
                    w_meth=params["w_meth"]
                )
            else:
                self.add_attribute(attr, r_meth=params[
                    "r_meth"])
                # Uncomment this out to try my "fix"
                # self.remove_unwanted_dynamic_attributes(attr_name)

    def remove_unwanted_dynamic_attributes(self, attr_name):
        """Removes unwanted dynamic attributes from previous device creation"""

        dev_class = self.get_device_class()
        multi_class_attr = dev_class.get_class_attr()

        klass_attr_names = []
        klass_attrs = multi_class_attr.get_attr_list()
        for ind in range(len(klass_attrs)):
            klass_attr_names.append(klass_attrs[ind].get_name())

        if attr_name in klass_attr_names:
            print("Remove existing class attr:", attr_name)
            attr = multi_class_attr.get_attr(attr_name)
            multi_class_attr.remove_attr(attr.get_name(), attr.get_cl_name())

    @command()
    def DumpInfo(self):
        dev_class = self.get_device_class()
        multi_class_attr = dev_class.get_class_attr()
        klass_attrs = multi_class_attr.get_attr_list()
        multi_attr = self.get_device_attr()
        dev_attrs = multi_attr.get_attribute_list()
        print("-- attributes")
        for ind in range(len(dev_attrs)):
            self.print_attr_info(dev_attrs[ind])
        print("-- class")
        print(dev_class)
        print("-- class attributes")
        for ind in range(len(klass_attrs)):
            self.print_attr_info(klass_attrs[ind])

    def print_attr_info(self, attr):
        print(attr.get_name())
        print(type(attr))

    def read1(self, attr):
        print("read", attr.get_name())
        attr.set_value(1.0)

    def read2(self, attr):
        print("read", attr.get_name())
        attr.set_value(2.0)

    def read3(self, attr):
        print("read", attr.get_name())
        attr.set_value(3.0)

    def write1(self, attr):
        print("write", attr.get_name())

    def write2(self, attr):
        print("write", attr.get_name())

    def write3(self, attr):
        print("write", attr.get_name())


def main():
    server_run((BuggyDS,))


if __name__ == "__main__":
    main()
