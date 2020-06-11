from tkinter import *
from tkinter import ttk as ttk
from json import *
from urllib.request import urlopen
import urllib.error
import requests
from requests import *


class addresslist():

    def __init__(self):
        self.addresses = """
        {
            "postcode": "XX4 04x",
            "latitude": "00.0000000",
            "longitude": "00.0000000",
            "addresses": 
            [
                {
                    "formatted_address": 
                        [
                        "NO ADDRESS LINE",
                        "NO ADDRESS LINE",
                        "NO ADDRESS LINE",
                        "NO TOWN LINE",
                        "NO COUNTY LINE"
                        ],
                    "thoroughfare": "NO ADDRESS LINE",
                    "building_name": "NO NAME",
                    "sub_building_name": "NO SUB BUILDING",
                    "sub_building_number": "NO SUB NUMBER",
                    "building_number": "0",
                    "line_1": "NO ADDRESS LINE",
                    "line_2": "NO ADDRESS LINE",
                    "line_3": "NO ADDRESS LINE",
                    "line_4": "NO ADDRESS LINE",
                    "locality": "NO LOCALITY",
                    "town_or_city": "NO TOWN",
                    "county": "NO COUNTY",
                    "district": "NO DISTRICT",
                    "country": "NO COUNTRY"
                }
            ]
        }
        """

    @property
    def addresses(self):
        return self.jaddresses

    @addresses.setter
    def addresses(self, value):
        self.jaddresses = loads(value)
        return

    @addresses.deleter
    def addresses(self):
        self.__init__()
        return self.jaddresses


def get_list(add_obj):
    url_params = {"api-key": "cUUoXDYbL0KAA21wbWKU1w26454", "sort": True, "expand": True}
    urlstring = f"https://api.getAddress.io/find/{inp_entry.get()}"

    try:
        with requests.get(urlstring, params=url_params) as response:
            if response.status_code > 299:
                response.raise_for_status()
            else:
                my_postcode_data = loads(response.text)
                add_obj.addresses = response.text
    except requests.exceptions.HTTPError as err_obj:
        list_box.delete(0, END)
        list_box.insert(END, f"Error...{err_obj.response}")
        return
    else:
        list_box.delete(0, END)
        for address in my_postcode_data["addresses"]:
            list_box.insert(END, address["formatted_address"][0])

    return


def select_address(add_obj):
    my_addresses = add_obj.addresses
    add_ret = list()
    for address in my_addresses["addresses"]:
        if address["formatted_address"][0] == list_box.get(ANCHOR):
            for item in range(5):
                add_ret.insert(item, address["formatted_address"][item])
            add_ret.insert(5, my_addresses["postcode"])

    print("selected address")
    return add_ret


address_list = addresslist()

root = Tk()
top_frame = Frame(root)
bottom_frame = Frame(root)
top_frame.pack()
bottom_frame.pack()

inp_label = Label(top_frame, text="please enter a post code:")
inp_entry = Entry(top_frame)
add_button = Button(top_frame, text="Find Addresses", command=lambda: get_list(address_list))
my_sep = ttk.Separator(top_frame, orient=HORIZONTAL)

list_scroll = Scrollbar(bottom_frame, orient=VERTICAL)
list_box = Listbox(bottom_frame,
                   yscrollcommand=list_scroll.set,
                   height=10,
                   width=50,
                   selectmode=SINGLE
                   )

list_scroll.configure(command=list_box.yview)
list_box.configure(yscrollcommand=list_scroll.set)

address_button = Button(bottom_frame, text="Select Address", command=lambda: select_address(address_list))

add_button.pack()
my_sep.pack(fill=X)
inp_label.pack(side=LEFT)
inp_entry.pack(side=RIGHT)
list_scroll.pack(side=RIGHT, fill=Y)
list_box.pack()
address_button.pack()

mainloop()
