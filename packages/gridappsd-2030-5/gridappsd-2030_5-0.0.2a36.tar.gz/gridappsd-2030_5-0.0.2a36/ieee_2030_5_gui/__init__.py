# from __future__ import annotations

# import io
# import logging
# import os
# import sys

# from dotenv import load_dotenv
# from fastapi import FastAPI
# from nicegui import ui

# from .pages import Pages, show_global_header

# logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)
# _log = logging.getLogger(__name__)

# app = FastAPI()

# __all__ = [
#     "run_gui"
# ]

# def initialize_app():

#     show_global_header(Pages.HOME)

#     ui.markdown("""

# # Welcome to the IEEE 2030.5 Admin GUI

# This is a work in progress""")

#     # device_list = get_end_devices()
#     # certs = get_certs()

#     # print(certs)
#     # print(device_list)
#     # row_data = []
#     # for ed in device_list.EndDevice:
#     #     row = dict(name=f'{ed.lFDI}',
#     #             cert=f'<a href="/admin/cert/{ed.lFDI}">cert</a>')
#     #     row_data.append(row)


#     # ui.aggrid({
#     #     'columnDefs': [
#     #         {'headerName': '', 'field': 'cert'},
#     #         {'headerName': 'Name', 'field': 'name'},
#     #     ],
#     #     'rowData': row_data,
#     # }, html_columns=[0])
# def run_gui():
#     out_file = open(sys.stdout.fileno(), 'wb', 0)
#     sys.stdout = io.TextIOWrapper(out_file, write_through=True)
#     from pathlib import Path

#     PREFIX = "2030_5"

#     # Allow custmization of the 2030_5_ENV_PATH
#     env_path = Path(os.environ.get(f"{PREFIX}_ENV_PATH",
#                                    str(Path(__file__).parent / ".env")))


#     load_dotenv(dotenv_path=env_path.as_posix())

#     required_env = [
#         f"{PREFIX}_HOST",
#         f"{PREFIX}_PORT",
#         f"{PREFIX}_CLIENT_KEY",
#         f"{PREFIX}_CLIENT_CERT",
#         f"{PREFIX}_CA_CERT"
#     ]

#     for x in required_env:
#         if os.getenv(x) is None or os.getenv(x).strip() == "":
#             sys.stderr.write(f'Missing {x} in .env file\n')
#             sys.exit(1)

#     logging.basicConfig(filename="gui-server.log", level=logging.DEBUG)

#     initialize_app()

#     ui.run(show=False)
#     # from pathlib import Path

#     # env_path = Path(__file__).parent / ".env"

#     # load_dotenv(dotenv_path=env_path.as_posix())

#     # PREFIX = "2030_5"
#     # required_env = [
#     #     f"{PREFIX}_HOST",
#     #     f"{PREFIX}_PORT",
#     #     f"{PREFIX}_CLIENT_KEY",
#     #     f"{PREFIX}_CLIENT_CERT",
#     #     f"{PREFIX}_CA_CERT"
#     # ]

#     # for x in required_env:
#     #     if os.getenv(x) is None or os.getenv(x).strip() == "":
#     #         sys.stderr.write(f'Missing {x} in .env file\n')
#     #         sys.exit(1)

#     # logging.basicConfig(level=logging.DEBUG)

#     # initialize_app()


#     # ui.run(show=False)





# # ui.html("""
# #     <table>
# #         <tr>
# #             <td>1</td>
# #             <td>2</td>
# #         </tr>
# #     </table>
# # """)


# # columns = [
# #     {'name': 'name', 'label': 'Name', 'field': 'name', 'required': True},
# #     {'name': 'age', 'label': 'Age', 'field': 'age', 'sortable': True},
# # ]
# # rows = [
# #     {'id': 0, 'name': 'Alice', 'age': 18},
# #     {'id': 1, 'name': 'Bob', 'age': 21},
# #     {'id': 2, 'name': 'Lionel', 'age': 19},
# #     {'id': 3, 'name': 'Michael', 'age': 32},
# #     {'id': 4, 'name': 'Julie', 'age': 12},
# #     {'id': 5, 'name': 'Livia', 'age': 25},
# #     {'id': 6, 'name': 'Carol'},
# # ]

# # with ui.table(title='My Team', columns=columns, rows=rows, selection='multiple', pagination=10).classes('w-96') as table:
# #     with table.add_slot('top-right'):
# #         with ui.input(placeholder='Search').props('type=search').bind_value(table, 'filter').add_slot('append'):
# #             ui.icon('search')
# #     with table.add_slot('body'):
# #         with table.row() as row:
# #             with table.cell() as cell:
# #                 pprint(row.props)
# #                 ui.link('Download', f'https://nicegui.io?{row.props.id}')
# #             with table.cell():
# #                 ui.link('Download', 'https://nicegui.io')
# #             with table.cell():
# #                 ui.link('Download', 'https://nicegui.io')
# #     with table.add_slot('bottom-row'):
# #         with table.row():
# #             with table.cell():
# #                 ui.button(on_click=lambda: (
# #                     table.add_rows({'id': time.time(), 'name': new_name.value, 'age': new_age.value}),
# #                     new_name.set_value(None),
# #                     new_age.set_value(None),
# #                 ), icon='add').props('flat fab-mini')
# #             with table.cell():
# #                 new_name = ui.input('Name')
# #             with table.cell():
# #                 new_age = ui.number('Age')

# # ui.label().bind_text_from(table, 'selected', lambda val: f'Current selection: {val}')
# # ui.button('Remove', on_click=lambda: table.remove_rows(*table.selected)) \
# #     .bind_visibility_from(table, 'selected', backward=lambda val: bool(val))

#     #ui.run(show=False)
