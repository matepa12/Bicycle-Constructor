import PySimpleGUI as Psgui


test_values = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

class BCGUIEngine:
    def __init__(self):

    # Column 1 ==========

        bicycle_base_list = Psgui.Listbox(test_values, size=(20, 6), pad=(2, (0, 0)))
        drive_system_list = Psgui.Listbox(test_values, size=(20, 6), pad=(2, (0, 0)))
        brake_system_list = Psgui.Listbox(test_values, size=(20, 6), pad=(2, (0, 0)))
        wheels_list = Psgui.Listbox(test_values, size=(20, 6), pad=(2, (0, 0)))
        add_subsystem_button = Psgui.Button("Add subsystem", pad=(2, 10))

        column1_layout = [
            [Psgui.Text("Bicycle base:", pad=(2, (10, 0)))],
            [bicycle_base_list],
            [Psgui.Text("Drive system:", pad=(2, (10, 0)))],
            [drive_system_list],
            [Psgui.Text("Brake system:", pad=(2, (10, 0)))],
            [brake_system_list],
            [Psgui.Text("Wheels: ", pad=(2, (10, 0)))],
            [wheels_list],
            [add_subsystem_button]
        ]
        column1 = Psgui.Column(layout=column1_layout, pad=(10, 10))

        # Column 2 ==========

        bicycle_image = Psgui.Image(filename='bicycle-311808_1280.png', pad=(2, 2))
        bicycle_base_option = Psgui.OptionMenu(test_values, size=(20,))
        drive_system_option = Psgui.OptionMenu(test_values, size=(20,))
        brake_system_option = Psgui.OptionMenu(test_values, size=(20,))
        front_wheel_option = Psgui.OptionMenu(test_values, size=(20,))
        rear_wheel_option = Psgui.OptionMenu(test_values, size=(20,))
        final_price = Psgui.Frame(
            title='Bicycle cost',
            layout=[[Psgui.Text("value", pad=(5, 5), font=('Calibri', 15))]],
            element_justification='center'
        )

        column2_layout = [
            [bicycle_image],
            [Psgui.Column(layout=[
                [front_wheel_option, bicycle_base_option, rear_wheel_option],
                [drive_system_option, brake_system_option]
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
        add_parts_button = Psgui.Button("Add a part", pad=(2, 10))

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

        while True:
            event, values = self.window.read()
            print(event, values)
            if event == Psgui.WIN_CLOSED or event == 'Exit':
                break

        self.window.close()
