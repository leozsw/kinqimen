import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime
import pytz # Using pytz as pendulum is not explicitly available
import kinqimen
import config
# Attempt to import kinliuren, will handle its absence in the functions
try:
    from kinliuren import kinliuren
    KINLIUREN_AVAILABLE = True
except ImportError:
    KINLIUREN_AVAILABLE = False
    print("Warning: kinliuren module not found. Chart output will be limited.")

# Create the main window
root = tk.Tk()
root.title("堅奇門 Desktop")

# Configure main window grid to be resizable
root.columnconfigure(0, weight=1)
root.rowconfigure(3, weight=1) # Output area row (changed from 2 to 3 due to new status bar)

# --- Date and Time Inputs ---
input_frame = ttk.Frame(root, padding="10")
input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Date Frame
date_frame = ttk.LabelFrame(input_frame, text="日期", padding="10")
date_frame.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(date_frame, text="年:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
year_entry = ttk.Entry(date_frame, width=5)
year_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(date_frame, text="月:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
month_entry = ttk.Entry(date_frame, width=3)
month_entry.grid(row=0, column=3, padx=5, pady=5)

ttk.Label(date_frame, text="日:").grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
day_entry = ttk.Entry(date_frame, width=3)
day_entry.grid(row=0, column=5, padx=5, pady=5)

# Time Frame
time_frame = ttk.LabelFrame(input_frame, text="時間", padding="10")
time_frame.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(time_frame, text="時:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
hour_entry = ttk.Entry(time_frame, width=3)
hour_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(time_frame, text="分:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
minute_entry = ttk.Entry(time_frame, width=3)
minute_entry.grid(row=0, column=3, padx=5, pady=5)

# --- Dropdown Menus (Comboboxes) ---
options_frame = ttk.Frame(root, padding="10")
options_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(options_frame, text="起盤方式:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
chart_method_combo = ttk.Combobox(options_frame, values=["時家奇門", "刻家奇門"], state="readonly")
chart_method_combo.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
chart_method_combo.set("時家奇門")

ttk.Label(options_frame, text="排盤:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
arrangement_type_combo = ttk.Combobox(options_frame, values=["置閏", "拆補"], state="readonly")
arrangement_type_combo.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)
arrangement_type_combo.set("置閏")

# --- Buttons ---
button_frame = ttk.Frame(options_frame, padding="5")
button_frame.grid(row=0, column=4, padx=20, pady=5, sticky=tk.E)

# --- Status Bar ---
status_bar = ttk.Label(root, text="準備就緒", relief=tk.SUNKEN, anchor=tk.W, padding="2 5")
status_bar.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.S))


def generate_chart():
    status_bar.config(text="正在生成圖表...")
    root.update_idletasks() # Force update of status bar

    try:
        year_str = year_entry.get()
        month_str = month_entry.get()
        day_str = day_entry.get()
        hour_str = hour_entry.get()
        minute_str = minute_entry.get()

        if not all([year_str, month_str, day_str, hour_str, minute_str]):
            messagebox.showerror("輸入錯誤", "所有日期和時間字段都必須填寫。")
            status_bar.config(text="輸入錯誤")
            return

        try:
            y = int(year_str)
            m = int(month_str)
            d = int(day_str)
            h = int(hour_str)
            mi = int(minute_str)
        except ValueError:
            messagebox.showerror("輸入錯誤", "日期和時間必須是有效的整數。")
            status_bar.config(text="輸入錯誤")
            return

        if not (1 <= m <= 12):
            messagebox.showerror("輸入錯誤", "月份必須在 1 到 12 之間。")
            status_bar.config(text="輸入錯誤")
            return
        if not (1 <= d <= 31): # Basic validation, could be improved with calendar logic
            messagebox.showerror("輸入錯誤", "日期必須在 1 到 31 之間。")
            status_bar.config(text="輸入錯誤")
            return
        if not (0 <= h <= 23):
            messagebox.showerror("輸入錯誤", "小時必須在 0 到 23 之間。")
            status_bar.config(text="輸入錯誤")
            return
        if not (0 <= mi <= 59):
            messagebox.showerror("輸入錯誤", "分鐘必須在 0 到 59 之間。")
            status_bar.config(text="輸入錯誤")
            return

        chart_method = chart_method_combo.get()
        arrangement_type = arrangement_type_combo.get()

        num = 1 if chart_method == "時家奇門" else 2
        pai = 2 if arrangement_type == "置閏" else 1

        qimen_instance = kinqimen.Qimen(y, m, d, h, mi)
        
        qtext = None
        if num == 1: # 時家奇門
            qtext = qimen_instance.pan(pai)
        elif num == 2: # 刻家奇門
            qtext = qimen_instance.pan_minute(pai)

        if not qtext:
            messagebox.showerror("錯誤", "無法生成奇門盤數據。")
            status_bar.config(text="生成失敗")
            return

        output_lines = []
        eg = list("巽離坤震兌艮坎乾")
        
        gz = config.gangzhi(y, m, d, h, mi)
        j_q = config.jq(y, m, d, h, mi)
        lunar_month_num = config.lunar_date_d(y,m,d).get("月")
        lunar_month_str = dict(zip(range(1,13), config.cmonth)).get(lunar_month_num)


        # Placeholder for kinliuren data
        e_to_s = {branch: "  " for branch in config.di_zhi}
        e_to_g = {branch: "  " for branch in config.di_zhi}

        if KINLIUREN_AVAILABLE:
            try:
                if num == 1: # 時家奇門
                    lr_day_ganzhi = gz[2]
                    lr_hour_ganzhi = gz[3]
                    lr = kinliuren.Liuren(qtext.get("節氣"), lunar_month_str, lr_day_ganzhi[1], lr_hour_ganzhi[1]).result(0)
                elif num == 2: # 刻家奇門
                    lr_hour_ganzhi = gz[3]
                    lr_minute_ganzhi = gz[4]
                    lr = kinliuren.Liuren(qtext.get("節氣"), lunar_month_str, lr_hour_ganzhi[1], lr_minute_ganzhi[1]).result(0)
                
                if lr:
                    e_to_s = lr.get("地轉天盤", e_to_s)
                    e_to_g = lr.get("地轉天將", e_to_g)
            except Exception as e_lr:
                print(f"Error during kinliuren processing: {e_lr}")
                messagebox.showwarning("六壬處理錯誤", f"處理六壬數據時發生錯誤: {e_lr}\n部分盤面信息可能不完整。")
        else:
            output_lines.append("注意: 六壬盤信息未生成 (kinliuren 模塊不可用)。\n")


        qd = [qtext.get("地盤", {}).get(i, "  ") for i in eg]
        qt = [qtext.get("天盤", {}).get(i, "  ") for i in eg]
        god = [qtext.get("神", {}).get(i, "  ") for i in eg]
        door = [qtext.get("門", {}).get(i, "  ") for i in eg]
        star = [qtext.get("星", {}).get(i, "  ") for i in eg]
        md = qtext.get("地盤", {}).get("中", "  ")

        if num == 1: # 時家奇門
            output_lines.append(f"時家奇門 | {qtext.get('排盤方式', '')}")
            output_lines.append(f"{y}年{m}月{d}日{h}時\n")
            output_lines.append(f"{qtext.get('干支', '')} |")
            output_lines.append(f"{qtext.get('排局', '')} | 節氣︰{j_q} |")
            zf_info = qtext.get('值符值使', {})
            zf_tg = zf_info.get('值符天干', [' ', ' '])
            zf_xg = zf_info.get('值符星宮', [' ', ' '])
            zs_mg = zf_info.get('值使門宮', [' ', ' '])
            output_lines.append(f"值符天干︰{zf_tg[0]}{zf_tg[1]} |")
            output_lines.append(f"值符星宮︰天{zf_xg[0]}-{zf_xg[1]}宮 | 值使門宮︰{zs_mg[0]}門{zs_mg[1]}宮\n")
        elif num == 2: # 刻家奇門
            output_lines.append(f"刻家奇門 | {qtext.get('排盤方式', '')}")
            output_lines.append(f"{y}年{m}月{d}日{h}時{mi}分\n")
            output_lines.append(f"{qtext.get('干支', '')} |")
            output_lines.append(f"{qtext.get('排局', '')} | 節氣︰{j_q} |")
            zf_info = qtext.get('值符值使', {})
            zf_xg = zf_info.get('值符星宮', [' ', ' '])
            zs_mg = zf_info.get('值使門宮', [' ', ' '])
            output_lines.append(f"值符星宮︰天{zf_xg[0]}-{zf_xg[1]}宮 | 值使門宮︰{zs_mg[0]}門{zs_mg[1]}宮\n")
        
        lunar_date_info = config.lunar_date_d(y, m, d)
        # Always get qimen_ju_name_zhirun_raw for display, as in app.py
        qimen_ju_raw_info_for_display = config.qimen_ju_name_zhirun_raw(y,m,d,h,mi)
        
        output_lines.append(f"農曆月︰{lunar_date_info.get('農曆月','')} | " +
                            (f"節氣日數差距︰{qimen_ju_raw_info_for_display.get('距節氣差日數','N/A')}天\n" 
                             if qimen_ju_raw_info_for_display else "節氣日數差距︰N/A天\n"))

        output_lines.append("＼  {}{}  　 │  {}{}　 │  {}{}　 │  　 {}{}　 ／".format(e_to_s.get("巳","  "),e_to_g.get("巳","  "),e_to_s.get("午","  "),e_to_g.get("午","  "),e_to_s.get("未","  "),e_to_g.get("未","  "),e_to_s.get("申","  "),e_to_g.get("申","  ")))
        output_lines.append("  ＼────────┴──┬─────┴─────┬──┴────────／")
        output_lines.append(" 　│　　{}　　　 │　　{}　　　 │　　{}　　　 │".format(god[0], god[1], god[2]))
        output_lines.append(" 　│　　{}　　{} │　　{}　　{} │　　{}　　{} │".format(door[0], qt[0], door[1], qt[1], door[2], qt[2]))
        output_lines.append(" 　│　　{}　　{} │　　{}　　{} │　　{}　　{} │".format(star[0], qd[0], star[1], qd[1], star[2], qd[2]))
        output_lines.append(" {}├───────────┼───────────┼───────────┤{}".format(e_to_s.get("辰","  "),e_to_s.get("酉","  ")))
        output_lines.append(" {}│　　{}　　　 │　　　　　　 │　　{}　　　 │{}".format(e_to_g.get("辰","  "),god[3], god[4],e_to_g.get("酉","  ")))
        output_lines.append("　─┤　　{}　　{} │　　　　　　 │　　{}　　{} ├─".format(door[3], qt[3],  door[4], qt[4]))
        output_lines.append(" 　│　　{}　　{} │　　　　　{} │　　{}　　{} │".format(star[3], qd[3], md, star[4], qd[4]))
        output_lines.append(" 　├───────────┼───────────┼───────────┤")
        output_lines.append("　 │　　{}　　　 │　　{}　　　 │　　{}　　　 │".format(god[5], god[6], god[7]))
        output_lines.append(" {}│　　{}　　{} │　　{}　　{} │　　{}　　{} │{}".format(e_to_s.get("卯","  "),door[5], qt[5], door[6], qt[6], door[7], qt[7], e_to_s.get("戌","  ")))
        output_lines.append(" {}│　　{}　　{} │　　{}　　{} │　　{}　　{} │{}".format(e_to_g.get("卯","  "),star[5], qd[5], star[6], qd[6], star[7], qd[7], e_to_g.get("戌","  ")))
        output_lines.append("  ／────────┬──┴─────┬─────┴──┬────────＼")
        output_lines.append("／  {}{}  　 │  {}{}　 │  {}{}　 │  　 {}{}　 ＼".format(e_to_s.get("寅","  "),e_to_g.get("寅","  "),e_to_s.get("丑","  "),e_to_g.get("丑","  "),e_to_s.get("子","  "),e_to_g.get("子","  "),e_to_s.get("亥","  "),e_to_g.get("亥","  ")))

        chart_string = "\n".join(output_lines)

        output_text.config(state='normal')
        output_text.delete('1.0', tk.END)
        output_text.insert(tk.END, chart_string)
        output_text.config(state='disabled')
        status_bar.config(text="圖表已生成")

    except Exception as e:
        messagebox.showerror("生成錯誤", f"生成圖表時發生錯誤: {e}")
        status_bar.config(text="生成錯誤")
        import traceback
        traceback.print_exc() # For debugging in the console

def generate_current_time_chart():
    status_bar.config(text="正在獲取當前時間...")
    root.update_idletasks()
    try:
        # Using Asia/Hong_Kong as in app.py example, can be changed to Asia/Shanghai
        tz = pytz.timezone('Asia/Hong_Kong') 
        now = datetime.datetime.now(tz)
        
        year_entry.delete(0, tk.END)
        year_entry.insert(0, str(now.year))
        month_entry.delete(0, tk.END)
        month_entry.insert(0, str(now.month))
        day_entry.delete(0, tk.END)
        day_entry.insert(0, str(now.day))
        hour_entry.delete(0, tk.END)
        hour_entry.insert(0, str(now.hour))
        minute_entry.delete(0, tk.END)
        minute_entry.insert(0, str(now.minute))
        
        status_bar.config(text="當前時間已填入")
        generate_chart() # Call the main chart generation function
    except Exception as e:
        messagebox.showerror("時間錯誤", f"獲取當前時間時發生錯誤: {e}")
        status_bar.config(text="時間錯誤")


current_time_button = ttk.Button(button_frame, text="即時", command=generate_current_time_chart)
current_time_button.grid(row=0, column=0, padx=5, pady=5)

generate_chart_button = ttk.Button(button_frame, text="起盤", command=generate_chart)
generate_chart_button.grid(row=0, column=1, padx=5, pady=5)


# --- Output Area ---
output_frame = ttk.LabelFrame(root, text="奇門盤", padding="10")
output_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10) # Changed row to 3
output_frame.columnconfigure(0, weight=1)
output_frame.rowconfigure(0, weight=1)

output_text = tk.Text(output_frame, wrap=tk.WORD, state="disabled", height=20, width=70) # Increased height
output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

scrollbar = ttk.Scrollbar(output_frame, orient=tk.VERTICAL, command=output_text.yview)
scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
output_text['yscrollcommand'] = scrollbar.set

# Start the Tkinter event loop
root.mainloop()
