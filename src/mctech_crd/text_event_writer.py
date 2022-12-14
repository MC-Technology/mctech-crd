class TextEventWriter:
    def __init__(self, filepath, logger=None):
        self.filepath = filepath

    def write_event(self, iso_time, serial_number, extra_fields):
        values = [iso_time, serial_number]
        for key in extra_fields:
            values.append(extra_fields[key])
        # Force None values to string
        values = ["" if v is None else v for v in values]
        line = ", ".join(values)

        try:
            with open(self.filepath, "a") as file:
                file.write("{}\n".format(line))
                file.close()
        except PermissionError:
            pass
