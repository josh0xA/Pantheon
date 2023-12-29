'''
MIT License

Copyright (c) 2021 Josh Schiavone

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import sys
import os
sys.dont_write_bytecode = True

import tkinter as tk
import tkintermapview 
import tkinter.font as tkFont
from tkinter import filedialog as fd
from tkinter import messagebox 
import threading 
import webview, webbrowser

import concurrent.futures
import re

import requests
import pycountry
import urllib3

from src.crawler import PantheonWebcam
from src.config import PantheonConfiguration
from src.logger import PantheonLogger


from src.geo import *

from headers.agents import Agents
import random

__author__ = "Josh Schiavone"
__version__ = "1.2"

class Pantheon:
    def __init__(self, root):
        self.setup_window(root)
        self.create_widgets(root)
        self.markers = []

        self.auto_log_data = []
        self.ip_data = []

    def setup_window(self, root):
        width, height = 1261, 807
        screenwidth, screenheight = root.winfo_screenwidth(), root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % ((width, height, (screenwidth - width) / 2, (screenheight - height) / 2))
        root.geometry(alignstr)
        root.configure(bg="#000000")
        root.resizable(width=False, height=False)
        root.title(self.get_platform_title())
   
    def create_widgets(self, root):
        self.results_box = tk.Listbox(root, selectmode=tk.SINGLE)
        self.results_box2 = tk.Listbox(root, selectmode=tk.SINGLE)

        self.setup_results_box()
        if sys.platform == "darwin":
            self.results_box.bind("<Control-Button-1>", self.get_http_data)
            self.results_box.bind("<Return>", self.browser_load_url)
            self.results_box.bind("<<ListboxSelect>>", self.add_ip_location)
        else:
            self.results_box.bind("<Return>", self.browser_load_url)
            self.results_box.bind("<<ListboxSelect>>", self.add_ip_location)
            self.results_box.bind("<Button-3>", self.get_http_data)

        country_buttons = self.create_country_widgets(root)
        self.create_country_buttons(country_buttons)

        self.map_widget = tkintermapview.TkinterMapView(root, width=100, height=100, corner_radius=0)
        self.map_widget.set_tile_server("https://basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", max_zoom=20)  

        self.map_widget.place(x=650, y=470, width=530, height=300)
        self.map_widget.set_zoom(0)

        self.slider = tk.Scale(root, from_=30, to=300, orient=tk.HORIZONTAL, bg="#000000", fg="#ffffff", font=("Arial", 10))
        self.slider.place(x=950, y=95, width=260, height=40)

        slider_label = tk.Label(root, text="Crawling Verbosity (def=30): ", bg="#000000", fg="#ffffff", font=("Arial", 8))
        slider_label.place(x=800, y=95)

        PantheonConfiguration.PANTHEON_DEFAULT_COUNT = self.slider.get()

        centered_label = tk.Label(
            root, text="IOT Camera Links (<Enter> to view LIVE\u25CF feed): ", bg="#000000", fg="#ffffff", font=("Arial", 10)
        )
        centered_label.place(x=75, y=135)
        geo_label = tk.Label(
            root, text="Geolocation: ", bg="#000000", fg="#ffffff", font=("Arial", 10)
        )
        geo_label.place(x=650, y=140)

        http_data_label = tk.Label(
            root, text="Map View: ", bg="#000000", fg="#ffffff", font=("Arial", 10)
        )
        http_data_label.place(x=650, y=440)
        self.setup_labels(root)

        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar, tearoff=0, fg="white", bg="black")
        filemenu.add_command(label="Save Pantheon Crawl", command=self.write_file_handler)
        filemenu.add_command(label="Load Pantheon Crawl", command=self.load_logfile)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="Pantheon File Controller", menu=filemenu)

        helpmenu = tk.Menu(menubar, tearoff=0, fg="white", bg="black")
        helpmenu.add_command(label="About", command=self.open_github_no_event)
        helpmenu.add_command(label="Legal", command=self.open_legal_no_event)
        helpmenu.add_command(label="Commands", command=self.command_list)
        menubar.add_cascade(label="Pantheon Help", menu=helpmenu)

        root.config(menu=menubar)

    def setup_results_box(self):
        self.results_box.pack(fill=tk.BOTH, expand=True)
        self.results_box["bg"] = "#000000"
        self.results_box["borderwidth"] = "3px"
        ft = tkFont.Font(family="Arial", size=16)
        self.results_box["font"] = ft
        self.results_box["fg"] = "#9f9f9f"
        self.results_box["justify"] = "left"
        self.results_box.place(x=80, y=200, width=530, height=580)

        scrollbar = tk.Scrollbar(self.results_box, orient=tk.VERTICAL, activebackground="red")
        scrollbar.config(command=self.results_box.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_box.config(yscrollcommand=scrollbar.set)

        # create another results box to the right of the main one
        self.results_box2.pack(fill=tk.BOTH, expand=True)
        self.results_box2["bg"] = "#000000"
        self.results_box2["borderwidth"] = "3px"
        ft = tkFont.Font(family="Arial", size=12)
        self.results_box2["font"] = ft
        self.results_box2["fg"] = "#9f9f9f"
        self.results_box2.place(x=650, y=180, width=530, height=250)


    def create_country_buttons(self, country_buttons):
        x, y, row_height = 100, 5, 30
        for country, command in country_buttons.items():
            country_button = tk.Button(root, text=country, command=command, bg="#000000", fg="green", font=("Arial", 7, "bold"))
            country_button.place(x=x, y=y, width=90, height=25)
            x += 100

            if x > 1000:
                x = 100
                y += row_height

    def setup_labels(self, root):
        panthlabel = tk.Label(root, bg="#000000")
        ft = tkFont.Font(family="Terminal", size=14, weight="bold")
        panthlabel["font"] = ft
        panthlabel["fg"] = "#ffffff"
        panthlabel["justify"] = "center"
        panthlabel["text"] = "Pantheon."
        panthlabel.place(x=1150, y=0, width=100, height=37)

        p2label = tk.Label(root, bg="#000000", fg="green", font=("Arial Italic", 8), text="Insecure Camera Parser")
        p2label.place(x=1120, y=25, width=150, height=37)

        github_label = tk.Label(
            root, text="GitHub", fg="#ffffff", bg="#000000", cursor="hand2", underline=0, font=("Arial", 10, "italic")
        )
        github_label.bind("<Button-1>", self.open_github)
        github_label.place(x=10, y=780)

        legal_label = tk.Label(
            root, text="Ethical Notice", fg="#ffffff", bg="#000000", cursor="hand2", underline=0, font=("Arial", 10, "italic")
        )
        legal_label.bind("<Button-1>", self.open_legal)
        legal_label.place(x=75, y=780)

        copyright_label = tk.Label(
            root, text="Copyright (c) 2023 Josh Schiavone", fg="#ffffff", bg="#000000", cursor="hand2",
            font=("Arial", 10, "italic")
        )
        copyright_label.place(x=1050, y=780)

        self.results_label = tk.Label(
            root, text="", bg="#000000", fg="red", font=("Arial Italic", 8, "bold")
        )
        self.results_label.place(x=80, y=160)

        clear_markers_button = tk.Button(root, text="Clear Markers", command=self.clear_markers, bg="#000000", fg="red", font=("Arial", 8, "bold"))
        clear_markers_button.place(x=1080, y=440, width=100, height=25)


    def get_platform_title(self):
        if sys.platform == "win32":
            return f"Pantheon: Developed by {__author__} - Ver {__version__} - Pantheon user: Windows"
        elif sys.platform == "darwin":
            return f"Pantheon: Developed by {__author__} - Ver {__version__} - Pantheon user: MacOS"
        elif sys.platform == "linux":
            return f"Pantheon: Developed by {__author__} - Ver {__version__} - Pantheon user: Linux"
        else:
            return f"Pantheon - Developed by {__author__}"

    def create_country_widgets(self, root):
        return {
            "Canada": lambda: self.clear_and_execute_webcam("CA"),
            "USA": lambda: self.clear_and_execute_webcam("US"),
            "Mexico": lambda: self.clear_and_execute_webcam("MX"),
            "Brazil": lambda: self.clear_and_execute_webcam("BR"),
            "Romania": lambda: self.clear_and_execute_webcam("RO"),
            "Poland": lambda: self.clear_and_execute_webcam("PL"),
            "South Africa": lambda: self.clear_and_execute_webcam("ZA"),
            "France": lambda: self.clear_and_execute_webcam("FR"),
            "Russia": lambda: self.clear_and_execute_webcam("RU"),
            "Germany": lambda: self.clear_and_execute_webcam("DE"),
            "Finland": lambda: self.clear_and_execute_webcam("FI"),
            "China": lambda: self.clear_and_execute_webcam("CN"),
            "Japan": lambda: self.clear_and_execute_webcam("JP"),
            "Norway": lambda: self.clear_and_execute_webcam("NO"),
            "South Korea": lambda: self.clear_and_execute_webcam("KR"),
            "Taiwan": lambda: self.clear_and_execute_webcam("TW"),
            "Spain": lambda: self.clear_and_execute_webcam("ES"),
            "Netherlands": lambda: self.clear_and_execute_webcam("NL"),
            "United Kingdom": lambda: self.clear_and_execute_webcam("GB"),
            "Ireland": lambda: self.clear_and_execute_webcam("IE"),
            "Sweden": lambda: self.clear_and_execute_webcam("SE"),
            "Israel": lambda: self.clear_and_execute_webcam("IL"),
            "India": lambda: self.clear_and_execute_webcam("IN"),
            "Australia": lambda: self.clear_and_execute_webcam("AU"),
            "Italy": lambda: self.clear_and_execute_webcam("IT"),
            "Switzerland": lambda: self.clear_and_execute_webcam("CH"),
            "Belarus": lambda: self.clear_and_execute_webcam("BY"),
            "Iran": lambda: self.clear_and_execute_webcam("IR"),
            "Indonesia": lambda: self.clear_and_execute_webcam("ID"),
            "Estonia": lambda: self.clear_and_execute_webcam("EE"),
            "Czech Republic": lambda: self.clear_and_execute_webcam("CZ"),
            "Austria": lambda: self.clear_and_execute_webcam("AT"),
            "Belgium": lambda: self.clear_and_execute_webcam("BE"),
            "Bulgaria": lambda: self.clear_and_execute_webcam("BG"),
            "Serbia": lambda: self.clear_and_execute_webcam("RS"),
            "Ukraine": lambda: self.clear_and_execute_webcam("UA"),
            "Slovakia": lambda: self.clear_and_execute_webcam("SK"),
        }

    def open_github(self, event):
        github_url = "https://github.com/josh0xA/Pantheon"
        webbrowser.open_new_tab(github_url)

    def open_github_no_event(self):
        github_url = "https://github.com/josh0xA/Pantheon"
        webbrowser.open_new_tab(github_url)

    def open_legal(self, event):
        legal_url = "https://joshschiavone.com/panth_info/panth_ethical_notice.html"
        webbrowser.open_new_tab(legal_url)

    def open_legal_no_event(self):
        legal_url = "https://joshschiavone.com/panth_info/panth_ethical_notice.html"
        webbrowser.open_new_tab(legal_url)

    def browser_load_url(self, event):
        selected_index = self.results_box.curselection()[0]
        selected_url = self.results_box.get(selected_index)
        webbrowser.open_new(selected_url)

    def clear_results(self):
        self.results_box.delete(0, tk.END)
        PantheonConfiguration.webcams_found = []

    def clear_results2(self):
        self.results_box2.delete(0, tk.END)

    def clear_results3(self):
        self.results_box3.delete(0, tk.END)

    def apply_slider(self):
        PantheonConfiguration.PANTHEON_DEFAULT_COUNT = self.slider.get()

    def execute_webcam(self, country):
        self.loading_label = tk.Label(root, text="Loading...", font=("Arial", 12), fg="yellow", bg="black")
        self.loading_label.place(x=530, y=140)
        self.webcam_execute(country)

    def clear_and_execute_webcam(self, country):
        self.clear_results()
        self.execute_webcam(country)

    def country_code_to_name(self, country_code):
        try:
            country = pycountry.countries.get(alpha_2=country_code)
            if country:
                if hasattr(country, 'official_name') and country.official_name:
                    return country.official_name
                else:
                    return country.name
            else:
                return "[Null]"
        except Exception as e: pass

    def webcam_execute(self, country):
        self.apply_slider()
        def crawl_and_display():
            PantheonConfiguration.num_webcams_found = 0
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(PantheonWebcam().crawl, country)
                future.result()  
                concurrent.futures.wait([future])  
            # remove duplicates
            PantheonConfiguration.webcams_found = list(dict.fromkeys(PantheonConfiguration.webcams_found)) 
            self.auto_log_data = PantheonConfiguration.webcams_found          
            for idx, webcam in enumerate(PantheonConfiguration.webcams_found, start=1):
                PantheonConfiguration.num_webcams_found += 1
                self.results_box.insert(tk.END, f"{idx}. {webcam}")
                self.results_box.itemconfig(tk.END, {"fg": "#18E63B"})
            self.loading_label.destroy()
            country_name = self.country_code_to_name(country)
            self.results_label.config(fg="red",
                text=f"Webcams Found: ({PantheonConfiguration.num_webcams_found}) in country: {country_name}\nCrawling Verbosity: {PantheonConfiguration.PANTHEON_DEFAULT_COUNT}")

        self.clear_results()
        self.clear_results2()
        self.results_label.config(text="")

        threading.Thread(target=crawl_and_display).start()

    def add_ip_location(self, event):
        self.clear_results2()
        try:
            selected_index = self.results_box.curselection()[0]
            selected_item = self.results_box.get(selected_index)

            match = re.search(r'https?://([^:/\s]+)', selected_item)
            if match:
                selected_url = match.group(1)
            else:
                selected_url = selected_item
        except IndexError:
            pass # Handle the case where the user clicks an empty listbox
        try: 
            import ipapi
            ip_location = ipapi.location(ip=selected_url)
            try:
                if ip_location:
                    self.results_box2.insert(tk.END, f"GeoDump for camera #{(selected_index + 1)}")
                    self.results_box2.insert(tk.END, "*" * 45)
                    self.results_box2.insert(tk.END, f"IP: {selected_url}")
                    self.results_box2.insert(tk.END, f"City: {ip_location.get('city')}")
                    self.results_box2.insert(tk.END, f"Region: {ip_location.get('region')}")
                    self.results_box2.insert(tk.END, f"Country: {ip_location.get('country_name')}")
                    self.results_box2.insert(tk.END, f"Latitude: {ip_location.get('latitude')}")
                    self.results_box2.insert(tk.END, f"Longitude: {ip_location.get('longitude')}")
                    self.results_box2.insert(tk.END, f"Postal: {ip_location.get('postal')}")
                    self.results_box2.insert(tk.END, f"Organization/ISP: {ip_location.get('org')}")

                    self.markers.append(self.map_widget.set_marker(ip_location['latitude'], ip_location['longitude'], 
                                            text=f"{ip_location['city']}, {ip_location['country']}\n({ip_location['ip']})",
                                            font=("Arial", 9), text_color="blue", image_zoom_visibility=(0, float('inf'))))
            except UnboundLocalError: pass # this is fine

        except ImportError:
            ip_location = IPGeolocation.get_location_ip2(selected_url)
            try:
                if ip_location:
                    self.results_box2.insert(tk.END, f"GeoDump for camera #{(selected_index + 1)}")
                    self.results_box2.insert(tk.END, "*" * 45)
                    self.results_box2.insert(tk.END, f"IP: {ip_location['ip']}")
                    self.results_box2.insert(tk.END, f"City: {ip_location['city']}")
                    self.results_box2.insert(tk.END, f"Region: {ip_location['region']}")
                    self.results_box2.insert(tk.END, f"Country: {ip_location['country']}")
                    self.results_box2.insert(tk.END, f"Latitude: {ip_location['latitude']}")
                    self.results_box2.insert(tk.END, f"Longitude: {ip_location['longitude']}")

                    self.markers.append(self.map_widget.set_marker(ip_location['latitude'], ip_location['longitude'], 
                                            text=f"{ip_location['city']}, {ip_location['country']}\n({ip_location['ip']})",
                                            font=("Arial", 9), text_color="blue", image_zoom_visibility=(0, float('inf'))))

            except UnboundLocalError: pass # this is fine

    def get_markers(self):
        return self.markers

    def clear_markers(self):
        for marker in self.get_markers():
            self.map_widget.delete(marker)
        self.get_markers().clear()

    def get_http_data(self, event):
        try:
            selected_index = self.results_box.curselection()[0]
            selected_item = self.results_box.get(selected_index)

            match = re.search(r'https?://\S+', selected_item)
            if match:
                selected_url = match.group(0)
            else:
                selected_url = selected_item

            user_agent = {
                'User-Agent': random.choice(Agents.useragent)
            }
            response = requests.get(selected_url, headers=user_agent)
            self.show_http_data_window(response)
        except Exception as e: pass

    def show_http_data_window(self, response):
        http_data_window = tk.Toplevel(root)
        http_data_window.title(f"HTTP Data for: {response.url}")
        http_data_window.geometry("800x600")

        search_var = tk.StringVar()
        search_entry = tk.Entry(http_data_window, textvariable=search_var)
        search_entry.pack(side=tk.TOP, fill=tk.X)
        search_var.trace_add("write", lambda *args: self.filter_http_data(response, search_var.get()))

        self.text_widget = tk.Text(http_data_window, wrap="word", font=("Arial", 12), bg="#000000", fg="#ffffff")
        self.text_widget.insert(tk.END, f"Note: Fetching w/ Random User-Agent: \n\t{response.request.headers['User-Agent']}\n\n")
        self.text_widget.insert(tk.END, f"HTTP Request URL: {response.url}\n")
        self.text_widget.insert(tk.END, f"HTTP Response Code: {response.status_code}\n\n")

        headers_text = str(response.headers)
        self.text_widget.insert(tk.END, "HTTP Headers:\n")
        self.text_widget.insert(tk.END, headers_text + "\n\n")

        response_text = response.text
        self.text_widget.insert(tk.END, "HTTP Response Text:\n")
        self.text_widget.insert(tk.END, response_text)

        self.text_widget.config(state=tk.DISABLED) 
        self.text_widget.pack(expand=True, fill="both")

    def filter_http_data(self, response, search_query):
        start_pos = "1.0"
        for tag in self.text_widget.tag_names():
            self.text_widget.tag_remove(tag, "1.0", "end")
            countVar = tk.StringVar()
        try:
            while start_pos != "end":
                pos = self.text_widget.search(search_query, start_pos, stopindex="end", 
                count=countVar, nocase=True)
                start_pos =  "%s + %sc" % (pos, int(countVar.get()) + 1)
                self.text_widget.tag_configure("search", background="green")
                self.text_widget.tag_add("search", pos, "%s + %sc" % (pos, countVar.get()))
        except tk.TclError:
            pass
        except ValueError:
            pass

    def write_file_handler(self):
        from datetime import datetime
        
        logfilename = f'{datetime.now().strftime("PantheonLog__%Y-%m-%d_%H--%M--%S")}.pantheon_log'

        if self.results_box.size() == 0:
            messagebox.showerror("Error", "No crawling data to save.")
            return

        PantheonLogger(logfilename).log_info("Do not modify this file directly if you want to load it into Pantheon.")
        PantheonLogger(logfilename).log_text(f"Pantheon Crawl Results ({os.path.abspath(logfilename)})")
        PantheonLogger(logfilename).log_text(self.results_label.cget("text"))
        PantheonLogger(logfilename).log(self.results_box.get(0, tk.END))
        messagebox.showinfo("Log File Created Successfully", "Log file saved to: " + os.path.abspath(logfilename))


    def load_logfile_handler(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
            self.results_label.config(fg="yellow", text=f"From Log File: {filename.split('/')[-1]}")
            lines = lines[4:]
            for line in lines:
                self.results_box.insert(tk.END, line)
                self.results_box.itemconfig(tk.END, {"fg": "#18E63B"})
        f.close()

    def load_logfile(self):
        filetypes = (
            ('Pantheon Log Files', '*.pantheon_log'),
        )

        filename = fd.askopenfilename(
            title='Open a Pantheon Log File',
            initialdir='/',
            filetypes=filetypes)
        
        if filename:
            self.clear_results()
            self.clear_results2()
            self.load_logfile_handler(filename)

    def command_list(self):
        # new tk window
        command_window = tk.Toplevel(root)
        command_window.title("Pantheon Commands")
        command_window.geometry("500x500")

        command_list = tk.Text(command_window, wrap="word", font=("Arial", 12), bg="#000000", fg="#ffffff")
        command_list.insert(tk.END, "Pantheon Commands\n")
        command_list.insert(tk.END, "*" * 45)
        command_list.insert(tk.END, "\n\n")
        command_list.insert(tk.END, f"View Feed: {PantheonConfiguration.controls['view-feed']}\n\n")
        command_list.insert(tk.END, f"View HTTP Data: {PantheonConfiguration.controls['view-http']}\n\n")
        command_list.insert(tk.END, f"Adjust Verbosity: {PantheonConfiguration.controls['verbosity']}\n\n")
        command_list.insert(tk.END, f"Save Crawl: {PantheonConfiguration.controls['save-crawl']}\n\n")
        command_list.insert(tk.END, f"Load Crawl: {PantheonConfiguration.controls['load-crawl']}\n\n")
        command_list.insert(tk.END, f"Search HTTP Data: {PantheonConfiguration.controls['search-http']}\n\n")

        command_list.config(state=tk.DISABLED)
        command_list.pack(expand=True, fill="both")


    def open_web_browser(self, url):
        webview.create_window('Pantheon Integrated Live Feed', url)
        webview.start(private_mode=True)

    def browser_load_url(self, event):
        selected_index = self.results_box.curselection()[0]
        selected_item = self.results_box.get(selected_index)

        match = re.search(r'https?://\S+', selected_item)
        if match:
            selected_url = match.group(0)
        else:
            selected_url = selected_item
                
        self.open_web_browser(selected_url)


if __name__ == "__main__":
    root = tk.Tk()
    app = Pantheon(root)
    root.mainloop()