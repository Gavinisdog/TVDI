import tkinter as tk
import tkinter.ttk as ttk
import requests
from datetime import datetime

DATA = None


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title_frame = tk.Frame(self, borderwidth=2, padx=50)
        self.title_frame.pack()
        self.buttonFrame = tk.Frame(self, borderwidth=2, padx=50, pady=20)
        self.buttonFrame.pack()
        self.main_frame = tk.Frame(self, borderwidth=2, padx=50, pady=20)
        self.main_frame.pack()
        tk.Label(self.title_frame, text="未來三十六小時全台天氣預報", font=("微軟正黑體", 18)).pack()
        now = datetime.now()
        now_string = "資料更新時間︰" + now.strftime("%Y年%m月%d日 %H:%M")
        self.time = tk.Label(self.title_frame)
        self.time.configure(text=now_string)
        self.time.pack()
        update_button = tk.Button(self.title_frame, text="即時更新", font=("微軟正黑體", 12), command=self.update)
        update_button.pack(pady=10)
        self.inputFrame = tk.Frame(self.title_frame, width=50)
        tk.Label(self.inputFrame, text="請選擇縣市︰", font=("微軟正黑體", 10)).grid(row=0, column=0, sticky=tk.E)
        self.comboboxText = tk.StringVar()
        self.locat_chosen = ttk.Combobox(self.inputFrame, width=15, state="readonly")
        self.locat_chosen.bind("<<ComboboxSelected>>", self.combobox_selected)
        self.locat_chosen["values"] = ["請選擇縣市"] + localList
        self.locat_chosen.grid(row=0, column=1, sticky=tk.E)
        self.inputFrame.pack()
        self.list1 = ["天氣概況", "最高氣溫", "最低氣溫", "體感天氣", "降雨機率"]

        self.button12 = tk.Button(self.buttonFrame, text="未來0~12小時", font=("微軟正黑體", 8), command=self.timeClick, state=tk.DISABLED)
        self.button12.grid(row=0, column=0, padx=5, sticky=tk.E)
        self.button24 = tk.Button(self.buttonFrame, text="未來12~24小時", font=("微軟正黑體", 8), command=self.timeClick1, state=tk.DISABLED)
        self.button24.grid(row=0, column=1, padx=5, sticky=tk.E)
        self.button36 = tk.Button(self.buttonFrame, text="未來24~36小時", font=("微軟正黑體", 8), command=self.timeClick2, state=tk.DISABLED)
        self.button36.grid(row=0, column=2, padx=5, sticky=tk.E)

        tk.Label(self.main_frame, text="天氣概況").grid(row=0, column=0, sticky=tk.E)
        self.label1 = tk.Label(self.main_frame)
        self.label1.grid(row=0, column=1, sticky=tk.W)

        tk.Label(self.main_frame, text="最高氣溫").grid(row=1, column=0, sticky=tk.E)
        self.label2 = tk.Label(self.main_frame)
        self.label2.grid(row=1, column=1, sticky=tk.W)


        tk.Label(self.main_frame, text="最低氣溫").grid(row=2, column=0, sticky=tk.E)
        self.label3 = tk.Label(self.main_frame)
        self.label3.grid(row=2, column=1, sticky=tk.W)


        tk.Label(self.main_frame, text="體感天氣").grid(row=3, column=0, sticky=tk.E)
        self.label4 = tk.Label(self.main_frame)
        self.label4.grid(row=3, column=1, sticky=tk.W)


        tk.Label(self.main_frame, text="降雨機率").grid(row=4, column=0, sticky=tk.E)
        self.label5 = tk.Label(self.main_frame)
        self.label5.grid(row=4, column=1, sticky=tk.W)

    def combobox_selected(self, event, timezone=0):
        self.button12["state"] = tk.DISABLED
        self.button24["state"] = tk.NORMAL
        self.button36["state"] = tk.NORMAL
        comboGet = self.locat_chosen.get()
        self.list2 = self.getWeatherData(locatGet=comboGet)
        self.label1["text"] = "︰" + self.list2[self.list1[0]][0]
        self.label2["text"] = "︰" + self.list2[self.list1[1]][0] + "ºC"
        self.label3["text"] = "︰" + self.list2[self.list1[2]][0] + "ºC"
        self.label4["text"] = "︰" + self.list2[self.list1[3]][0]
        self.label5["text"] = "︰" + self.list2[self.list1[4]][0] + "%"

    def timeClick(self, timezone=0):
        self.button12["state"] = tk.DISABLED
        self.button24["state"] = tk.NORMAL
        self.button36["state"] = tk.NORMAL
        self.label1["text"] = "︰" + self.list2[self.list1[0]][timezone]
        self.label2["text"] = "︰" + self.list2[self.list1[1]][timezone] + "ºC"
        self.label3["text"] = "︰" + self.list2[self.list1[2]][timezone] + "ºC"
        self.label4["text"] = "︰" + self.list2[self.list1[3]][timezone]
        self.label5["text"] = "︰" + self.list2[self.list1[4]][timezone] + "%"

    def timeClick1(self, timezone=1):
        self.button12["state"] = tk.NORMAL
        self.button24["state"] = tk.DISABLED
        self.button36["state"] = tk.NORMAL
        self.label1["text"] = "︰" + self.list2[self.list1[0]][timezone]
        self.label2["text"] = "︰" + self.list2[self.list1[1]][timezone] + "ºC"
        self.label3["text"] = "︰" + self.list2[self.list1[2]][timezone] + "ºC"
        self.label4["text"] = "︰" + self.list2[self.list1[3]][timezone]
        self.label5["text"] = "︰" + self.list2[self.list1[4]][timezone] + "%"

    def timeClick2(self, timezone=2):
        self.button12["state"] = tk.NORMAL
        self.button24["state"] = tk.NORMAL
        self.button36["state"] = tk.DISABLED
        self.label1["text"] = "︰" + self.list2[self.list1[0]][timezone]
        self.label2["text"] = "︰" + self.list2[self.list1[1]][timezone] + "ºC"
        self.label3["text"] = "︰" + self.list2[self.list1[2]][timezone] + "ºC"
        self.label4["text"] = "︰" + self.list2[self.list1[3]][timezone]
        self.label5["text"] = "︰" + self.list2[self.list1[4]][timezone] + "%"

    def update(self):
        download()
        self.locat_chosen.current(0)
        self.button12["state"] = tk.DISABLED
        self.button24["state"] = tk.DISABLED
        self.button36["state"] = tk.DISABLED
        self.label1["text"] = ""
        self.label2["text"] = ""
        self.label3["text"] = ""
        self.label4["text"] = ""
        self.label5["text"] = ""
        now = datetime.now()
        now_string = "資料更新時間︰" + now.strftime("%Y年%m月%d日 %H:%M")
        self.time.configure(text=now_string)

    def getWeatherData(self, locatGet=None):
        get_list = []
        for locat in dataList["location"]:
            if locat["locationName"] == locatGet:
                # print(locat)  # allData
                location_name = locat["locationName"]  # 地點
                weatherList = locat["weatherElement"]
                self.valueList = ["cmt", "maxT", "minT", "feel", "rain"]
                for a, element in enumerate(weatherList):
                    # print(element["time"])
                    timeDict = element["time"]
                    weatherGet = []
                    for b in range(len(timeDict)):
                        cmt_weather = timeDict[b]["parameter"]["parameterName"]
                        weatherGet.append(cmt_weather)
                        # print(cmt_weather)
                    get_list.append(weatherGet)
                    if len(get_list) == 5:
                        break
                localWeatherDict = dict(zip(self.list1, get_list))
                return localWeatherDict


def download():
    global DATA
    url = "https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-C0032-001?Authorization=rdec-key-123-45678-011121314&format=JSON"
    response = requests.get(url)
    if response.status_code == 200:
        DATA = response.json()
        print("Download completed")
        DATA = DATA["cwbopendata"]["dataset"]
        locatList = []
        for locat in DATA["location"]:
            locatList.append(locat["locationName"])
        return DATA, locatList


if __name__ == "__main__":
    dataList, localList = download()
    root = Window()
    root.title("18_許浩文_期末作業")
    root.mainloop()

# python pythonTkinter\fYProject\main.py
