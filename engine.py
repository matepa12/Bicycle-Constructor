import PySimpleGUI as Psgui

test_values = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)


# noinspection PyTypeChecker
class Engine:

    def __init__(self, database):

        self.database = database

        # Column 1 ==========

        self.bicycle_base_list = Psgui.Listbox(
            self.database.get_subsystem_list("Bicycle base"),
            size=(20, 6), pad=(2, (0, 0)))
        self.drive_system_list = Psgui.Listbox(
            self.database.get_subsystem_list("Drive system"),
            size=(20, 6), pad=(2, (0, 0)))
        self.brake_system_list = Psgui.Listbox(
            self.database.get_subsystem_list("Brake system"),
            size=(20, 6), pad=(2, (0, 0)))
        self.wheels_list = Psgui.Listbox(
            self.database.get_subsystem_list("Wheels"),
            size=(20, 6), pad=(2, (0, 0)))
        add_subsystem_button = Psgui.Button("Add subsystem", pad=(2, 10))

        column1_layout = [
            [Psgui.Text("Bicycle base:", pad=(2, (10, 0)))],
            [self.bicycle_base_list],
            [Psgui.Text("Drive system:", pad=(2, (10, 0)))],
            [self.drive_system_list],
            [Psgui.Text("Brake system:", pad=(2, (10, 0)))],
            [self.brake_system_list],
            [Psgui.Text("Wheels: ", pad=(2, (10, 0)))],
            [self.wheels_list],
            [add_subsystem_button]
        ]
        column1 = Psgui.Column(layout=column1_layout, pad=(10, 10))

        # Column 2 ==========

        bicycle_image = Psgui.Image(filename='bicycle-311808_1280.png', pad=(2, 2))
        self.bicycle_base_option = Psgui.OptionMenu(self.database.get_subsystem_list("Bicycle base"), size=(20,))
        self.drive_system_option = Psgui.OptionMenu(self.database.get_subsystem_list("Drive system"), size=(20,))
        self.brake_system_option = Psgui.OptionMenu(self.database.get_subsystem_list("Brake system"), size=(20,))
        self.front_wheel_option = Psgui.OptionMenu(self.database.get_subsystem_list("Wheels"), size=(20,))
        self.rear_wheel_option = Psgui.OptionMenu(self.database.get_subsystem_list("Wheels"), size=(20,))
        final_price = Psgui.Frame(
            title='Bicycle cost',
            layout=[[Psgui.Text("value", pad=(5, 5), font=('Calibri', 15))]],
            element_justification='center'
        )

        column2_layout = [
            [bicycle_image],
            [Psgui.Column(layout=[
                [self.front_wheel_option, self.bicycle_base_option, self.rear_wheel_option],
                [self.drive_system_option, self.brake_system_option]
            ],
                element_justification='center')],
            [Psgui.Column(layout=[[final_price]],
                          element_justification='right',
                          expand_x=True)]
        ]

        column2 = Psgui.Column(layout=column2_layout, pad=(10, 10))

        # Column 3 ==========
        selected_subsystem = Psgui.Text("test subsystem", font=('Calibri', 10), size=(16, 1))
        subsystem_name = Psgui.Frame('Selected subsystem', [[selected_subsystem]])
        subsystem_list = Psgui.Listbox(test_values, size=(20, 6), pad=(2, (0, 0)))
        subsystem_parts_list = Psgui.Listbox(test_values, size=(20, 18), pad=(2, (0, 0)))
        add_parts_button = Psgui.Button("Add a part", pad=(2, 10), enable_events=True)

        column3_layout = [
            [subsystem_name],
            [Psgui.Text("Subsystem:", pad=(2, (10, 0)))],
            [subsystem_list],
            [Psgui.Text("Parts:", pad=(2, (10, 0)))],
            [subsystem_parts_list],
            [add_parts_button],
        ]
        column3 = Psgui.Column(layout=column3_layout, pad=(10, 10))

        window_layout = [
            [Psgui.Column([
                [Psgui.Text("Here you can compose your bicycle:", font=('Calibri', 22))]
            ],
                element_justification='center',
                expand_x=True)
            ],
            [column1, column2, column3]
        ]

        self.window = Psgui.Window('Bicycle Composer', layout=window_layout)
        self.db_part_input = []
        self.db_subsystem_input = []

    def add_parts_window(self):

        parts_window = Psgui.Window(
            'Add a part',
            [[Psgui.Column([[Psgui.Text('Enter the name of the part:')],
                            [Psgui.Text('Choose the manufacturer or add a new one:')],
                            # [Psgui.Text('')],
                            [Psgui.Text('Enter the value of the part:')],
                            [Psgui.Text('Choose the part group:')],
                            ], element_justification='right'),
              Psgui.Column([[Psgui.In(key='-part_name-')],
                            # [Psgui.OptionMenu(test_values, key='-company_name-')],
                            [Psgui.In(key='-company_name_new-')],
                            [Psgui.In(key='-part_value-')],
                            [Psgui.OptionMenu(self.database.get_table_names_list('part_groups'), key='-part_group-')]])],
             [Psgui.Column([[Psgui.B('OK'), Psgui.B('Cancel')]],
                           expand_x=True, element_justification='right')]]
        )

        event, values = parts_window.read(close=True)

        if event == 'OK':
            for key in values:
                if key == '-part_value-':
                    try:
                        self.db_part_input.append(float(values[key]))
                    except ValueError:
                        self.db_part_input = []
                        parts_window.close()
                        Psgui.popup('Part value must be a number. ')
                        break
                else:
                    self.db_part_input.append(values[key])

            if self.db_part_input:
                self.db_part_input = tuple(self.db_part_input)
                self.database.part_input(self.db_part_input)
                self.db_part_input = []

    def add_subsystem_window(self):

        event, values = Psgui.Window(
            'Add subsystem',
            [[Psgui.Column([[Psgui.Text('Enter the name of the subsystem:')],
                            [Psgui.Text('Choose the subsystem group:')],
                            ], element_justification='right'),
              Psgui.Column([[Psgui.In(key='-subsystem_name-')],
                            [Psgui.OptionMenu(self.database.get_table_names_list("subsystem_groups"),
                                              key='-subsystem_group-')]])],
             [Psgui.Column([[Psgui.B('OK'), Psgui.B('Cancel')]],
                           expand_x=True, element_justification='right')]]
        ).read(close=True)

        if event == 'OK':
            for key in values:
                self.db_subsystem_input.append(values[key])
            self.db_subsystem_input = tuple(self.db_subsystem_input)
            self.database.subsystem_input(self.db_subsystem_input)
            self.db_subsystem_input = []

            self.bicycle_base_list.update(values=self.database.get_subsystem_list("Bicycle base"))
            self.drive_system_list.update(values=self.database.get_subsystem_list("Drive system"))
            self.brake_system_list.update(values=self.database.get_subsystem_list("Brake system"))
            self.wheels_list.update(values=self.database.get_subsystem_list("Wheels"))

            self.front_wheel_option.update(values=self.database.get_subsystem_list("Wheels"))
            self.bicycle_base_option.update(values=self.database.get_subsystem_list("Bicycle base"))
            self.rear_wheel_option.update(values=self.database.get_subsystem_list("Wheels"))
            self.drive_system_option.update(values=self.database.get_subsystem_list("Drive system"))
            self.brake_system_option.update(values=self.database.get_subsystem_list("Brake system"))

    def mainloop(self):

        while True:
            event, values = self.window.read()
            if event == Psgui.WIN_CLOSED or event == 'Exit':
                break
            if event == "Add a part":
                self.add_parts_window()

            if event == "Add subsystem":
                self.add_subsystem_window()

        self.window.close()
