import tkinter as tk

tooltip_window = None

def show_tooltip(event, text):
    global tooltip_window
    if tooltip_window or not text:
        return

    x, y, _, _ = event.widget.bbox("insert")
    x += event.widget.winfo_rootx() + 25
    y += event.widget.winfo_rooty() + 25

    tooltip_window = tw = tk.Toplevel(event.widget)
    tw.wm_overrideredirect(True)
    tw.wm_geometry(f"+{x}+{y}")

    label = tk.Label(tw, text=text, justify='left',
                     background="#ffffe0", relief='solid', borderwidth=1,
                     font=("tahoma", "8", "normal"))
    label.pack(ipadx=1)

def hide_tooltip(event):
    global tooltip_window
    if tooltip_window:
        tooltip_window.destroy()
        tooltip_window = None

def bind_tooltip(widget, text):
    widget.bind("<Enter>", lambda event: show_tooltip(event, text))
    widget.bind("<Leave>", hide_tooltip)
