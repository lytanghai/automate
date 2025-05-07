import requests
import json
import csv
import argparse
import sys
import getpass
import os
import webbrowser
import ast
import tkinter as tk
import tkinter.font as tkFont
from requests.auth import HTTPBasicAuth
from tkcalendar import DateEntry
from tkinter import ttk,messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog

from datetime import datetime, timedelta
from external.bitbucket import get_repository, get_pr_detail, check_enforce_rule, get_default_reviewer
from util.config import load_config, load_cache, save_cache, clear_cache
from util.date import format_date_time

# Constants
username, password, workspace, cache_file , min_approval, min_default_reviewer_approval, workspace_list= load_config()
size=5
tree = None
on_result_export=[]

repository_names = load_cache("repository_name")
if repository_names is None:
    print("Cache not found or expired. Fetching fresh data...")
    repository_names = get_repository(workspace, username, password)
else:
    print("Loaded repositories from cache.")

if '--clear-cache' in sys.argv:
    if os.path.exists('.cache.json'):
        os.remove('.cache.json')
        print("Cache cleared.")
    else:
        repository_names = get_repository(workspace, username, password)
        print("No cache to clear.")

def on_filter(raw_response, status, target_branch, enforced_rule,requested_from,requested_to, merged_from, merged_to, repo_slug):
    write_log("filtering pull request records... ")
    if isinstance(raw_response, str):
        json_data = json.loads(raw_response)
    else:
        json_data = raw_response

    default_reviewers = load_cache("default_reviewers")
    if default_reviewers is None:
        write_log("Cache not found or expired. Fetching fresh data for default_reviewer...")
        default_reviewers = get_default_reviewer(username, password, write_log)
    else:
        write_log("Loaded cache default reviewer from cache!")
    result = []

    for pr in json_data.get("values", []):
        closed_by = pr["closed_by"]["display_name"] if isinstance(pr.get("closed_by"), dict) else ""
        id = pr.get("id", "")

        enforced_rule_res, total_approvals, total_default_reviewer_approvals = check_enforce_rule(
            id,
            default_reviewers,
            repo_slug,
            username,
            password,
            write_log,
            int(min_approval),
            int(min_default_reviewer_approval)
        )

        if enforced_rule == 'All': 
            pass

        elif enforced_rule == 'True' and not enforced_rule_res:
            continue 
            
        elif enforced_rule == 'False' and enforced_rule_res:
            continue 

        destination_branch = pr.get("destination", {}).get("branch", {}).get("name", "")
        if target_branch and destination_branch != target_branch:
            continue

        created_on = pr.get("created_on", "")
        if created_on:
            created_dt = datetime.fromisoformat(created_on.replace('Z', '+00:00'))

            if requested_from:
                requested_from_dt = datetime.strptime(requested_from, "%Y-%m-%d %H:%M:%S")
                if created_dt.date() < requested_from_dt.date():
                    continue

            if requested_to:
                requested_to_dt = datetime.strptime(requested_to, "%Y-%m-%d %H:%M:%S")
                if created_dt.date() > requested_to_dt.date():
                    continue

        # Apply merged date filter if PR is merged
        if pr.get("state") == "MERGED":
            updated_on = pr.get("updated_on", "")
            if updated_on:
                updated_dt = datetime.fromisoformat(updated_on.replace('Z', '+00:00'))

                if merged_from:
                    merged_from_dt = datetime.strptime(merged_from, "%Y-%m-%d %H:%M:%S")
                    if updated_dt.date() < merged_from_dt.date():
                        continue

                if merged_to:
                    merged_to_dt = datetime.strptime(merged_to, "%Y-%m-%d %H:%M:%S")
                    if updated_dt.date() > merged_to_dt.date():
                        continue
        rule_detail = f"{total_approvals} approval \n{total_default_reviewer_approvals} default reviewer"
        pr_info = {
            "id": id,
            "title": pr.get("title", ""),
            "state": pr.get("state", ""),
            "source_branch":pr.get("source", {}).get("branch", {}).get("name", ""),
            "target_branch": pr.get("destination", {}).get("branch", {}).get("name", ""),
            "author": pr.get("author", {}).get("display_name", ""),
            "created_on": pr.get("created_on", ""),
            "closed_by": closed_by,
            "updated_on": pr.get("updated_on", ""),
            "enforced_rule": enforced_rule_res,
            "pr_rule": rule_detail
        }
        result.append(pr_info)
    global on_result_export
    on_result_export = result
    return result

def on_export():
    default_filename = f"PR_Report_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.csv"
    if not on_result_export:
        print("No data to export.")
        return

    file_path = filedialog.asksaveasfilename(
        initialfile=default_filename,
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")],
        title="Save report as"
    )    
    if not file_path:
        return

    if file_path:
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            # Row 1: Metadata
            username = getpass.getuser()
            writer.writerow([f"Generated by: {username}, Generate date = {timestamp}"])
            writer.writerow([f"Generate on = {timestamp}"])

            writer.writerow([])

            headers = ["PR #", "PR Name", "Source Branch", "Target Branch", "Status", "Requested By", "Requested Date",
                       "Merged By", "Merged Date", "Enforced Rule", "PR Rule"]
            writer.writerow(headers)

            # Data Rows
            for row in on_result_export:
                writer.writerow([
                    row.get("id", ""),
                    row.get("title", ""),
                    row.get("source_branch", ""),
                    row.get("target_branch", ""),
                    row.get("state", ""),
                    row.get("author", ""),
                    row.get("created_on", ""),
                    row.get("closed_by", ""),
                    row.get("updated_on", ""),
                    row.get("enforced_rule", ""),
                    row.get("pr_rule", "")
                ])

        print(f"CSV exported to {file_path}")

def on_submit():
    clear_log()
    workspace = workspace_var.get()
    report_in = report_in_var.get()
    status = status_var.get()
    target_branch = target_branch_var.get()
    enforced_rule = enforced_rule_var.get()
    requested_from = requested_from_var.get()
    requested_to = requested_to_var.get()
    merged_from = merged_from_var.get()
    merged_to = merged_to_var.get()
    size = page_size_var.get()

    if requested_from:
        requested_from += " 00:00:00"

    if requested_to:
        requested_to += " 23:59:59"

    if merged_from:
        merged_from += " 00:00:00"

    if merged_to:
        merged_to += " 23:59:59"

    if not workspace:
        messagebox.showwarning("Error", "Workspace Field is required!")
        return
    elif not report_in:
        messagebox.showwarning("Error", "Report In Field is required!")
        return
    elif not status:
        messagebox.showwarning("Error", "Status Field is required!")
        return
    elif not size:
        messagebox.showwarning("Error", "Size Field is required!")
        return
    elif not enforced_rule:
        messagebox.showwarning("Error", "Size Field is required!")
        return
        
    print("Filter Param")
    print(f"Workspace: {workspace}")
    print(f"Report In: {report_in}")
    print(f"Status: {status}")
    print(f"Size: {size}")
    print(f"Target Branch: {target_branch}")
    print(f"Enforced Rule: {enforced_rule}")
    print(f"Requested Date: From {requested_from} To {requested_to}")
    print(f"Merged Date: From {merged_from} To {merged_to}")

    raw_response = get_pr_detail(workspace, report_in, status, size, username, password ,write_log)
    filtered_result = on_filter(raw_response, status, target_branch, enforced_rule, requested_from, requested_to, merged_from, merged_to, report_in)
    write_log(f"Found {len(filtered_result)} pull request matching the filter.")

    for row in tree.get_children():
        tree.delete(row)

    for pr in filtered_result:
        created_on = format_date_time(datetime.fromisoformat(pr["created_on"]) + timedelta(hours=7))
        updated_on = "" if pr["state"] != "MERGED" else format_date_time(datetime.fromisoformat(pr["updated_on"]) + timedelta(hours=7))

        row = (
            pr["id"],
            pr["title"],
            pr["source_branch"],
            pr["target_branch"],
            pr["state"],
            pr["author"],
            created_on,
            pr["closed_by"],
            updated_on,
            pr["enforced_rule"],
            pr["pr_rule"]
        )
        tree.insert("", tk.END, values=row)

def clear_dates():
    requested_from_var.set("")
    requested_to_var.set("")
    merged_from_var.set("")
    merged_to_var.set("")

log_counter = 1

def write_log(message):
    global log_widget, log_counter
    if log_widget:
        log_widget.config(state='normal')
        log_widget.insert(tk.END, f"{log_counter}. {message}\n")
        log_widget.see(tk.END)
        log_widget.config(state='disabled')
        log_widget.update_idletasks()
        log_counter += 1
    else:
        print(f"[{log_counter}]: {message}")
        log_counter += 1

def clear_log():
    global log_widget
    if log_widget:
        log_widget.config(state='normal')
        log_widget.delete(1.0, tk.END)
        log_widget.config(state='disabled')
        log_widget.update_idletasks()

def change_workspace():
    global repository_names
    selected = workspace_var.get()
    write_log(f"refreshing to new workspace {selected}")
    clear_cache()
    repository_names = get_repository(selected, username, password)
    report_in_combobox.config(values=repository_names)
    report_in_var.set("")

def create_ui():
    global workspace_var, report_in_var, status_var, target_branch_var, enforced_rule_var
    global merged_from_var, merged_to_var, page_size_var, requested_from_var, requested_to_var
    global log_widget

    root = tk.Tk()
    root.title("Pull Request Viewer")
    root.state("zoomed")

    label_font = ("Segoe UI", 10)
    entry_width = 22
    padx, pady = 10, 5
    
    # ========== Filters Frame ==========
    filters_frame = tk.Frame(root)
    filters_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nw")

    # --- Row 0 ---
    workspace_var = tk.StringVar(value="wingdev")
    tk.Label(filters_frame, text="Workspace*", font=label_font).grid(row=0, column=0, padx=padx, pady=pady, sticky="e")

    workspace_frame = tk.Frame(filters_frame)
    workspace_frame.grid(row=0, column=1, padx=padx, pady=pady, sticky="w")

    ttk.Combobox(workspace_frame, textvariable=workspace_var, values=ast.literal_eval(workspace_list), width=entry_width).pack(side="left")
    ttk.Button(workspace_frame, text="⟳", width=3, command=change_workspace).pack(side="left", padx=(5, 0))

    global report_in_combobox
    report_in_var = tk.StringVar()
    tk.Label(filters_frame, text="Report In*", font=label_font).grid(row=0, column=2, padx=padx, pady=pady, sticky="e")
    report_in_combobox = ttk.Combobox(filters_frame, textvariable=report_in_var, values=repository_names, width=entry_width)
    report_in_combobox.grid(row=0, column=3, padx=padx, pady=pady, sticky="w")
    # ttk.Combobox(filters_frame, textvariable=report_in_var, values=repository_names, width=entry_width).grid(row=0, column=3, padx=padx, pady=pady, sticky="w")

    rule_var = tk.StringVar()
    rule_text = f"""
    📝Pull Request Rule Checklist::
    1.Minimum {min_approval} approvals
    \t\t\t2. Minimum {min_default_reviewer_approval} approvals from default reviewers
    """
    tk.Label(filters_frame, text=rule_text, font=label_font).grid(row=0, column=4, padx=padx, pady=pady, sticky="e")

    # --- Row 1 ---
    status_var = tk.StringVar(value="ALL")
    tk.Label(filters_frame, text="Status*", font=label_font).grid(row=1, column=0, padx=padx, pady=pady, sticky="e")
    ttk.Combobox(filters_frame, textvariable=status_var, values=["ALL", "OPEN", "MERGED", "DECLINED"], width=entry_width).grid(row=1, column=1, padx=padx, pady=pady, sticky="w")

    target_branch_var = tk.StringVar()
    tk.Label(filters_frame, text="Target Branch", font=label_font).grid(row=1, column=2, padx=padx, pady=pady, sticky="e")
    ttk.Combobox(filters_frame, textvariable=target_branch_var, values=["dev", "stage", "uat", "pvt", "main", "master"], width=entry_width).grid(row=1, column=3, padx=padx, pady=pady, sticky="w")

    # --- Row 2 ---
    enforced_rule_var = tk.StringVar(value="All")
    tk.Label(filters_frame, text="Enforced Rule*", font=label_font).grid(row=2, column=0, padx=padx, pady=pady, sticky="e")
    ttk.Combobox(filters_frame, textvariable=enforced_rule_var, values=["All", "True", "False"], width=entry_width).grid(row=2, column=1, padx=padx, pady=pady, sticky="w")

    page_size_var = tk.StringVar(value="10")
    tk.Label(filters_frame, text="Page Size*", font=label_font).grid(row=2, column=2, padx=padx, pady=pady, sticky="e")
    ttk.Combobox(filters_frame, textvariable=page_size_var, values=["5", "10", "20"], width=entry_width).grid(row=2, column=3, padx=padx, pady=pady, sticky="w")

    # --- Row 3: Dates ---
    tk.Label(filters_frame, text="Requested / Merged Dates", font=label_font).grid(row=3, column=0, padx=padx, pady=(15, 5), sticky="e")

    date_frame = tk.Frame(filters_frame)
    date_frame.grid(row=3, column=1, columnspan=3, padx=padx, pady=(15, 5), sticky="w")

    requested_from_var = tk.StringVar()
    requested_to_var = tk.StringVar()
    merged_from_var = tk.StringVar()
    merged_to_var = tk.StringVar()

    # Requested
    tk.Label(date_frame, text="Request From:", font=label_font).grid(row=0, column=0, padx=5, sticky="e")
    DateEntry(date_frame, textvariable=requested_from_var, date_pattern="yyyy-mm-dd", width=15).grid(row=0, column=1, padx=5)
    tk.Label(date_frame, text="Request To:", font=label_font).grid(row=0, column=2, padx=5, sticky="e")
    DateEntry(date_frame, textvariable=requested_to_var, date_pattern="yyyy-mm-dd", width=15).grid(row=0, column=3, padx=5)

    # Merged
    tk.Label(date_frame, text="Merged From:", font=label_font).grid(row=1, column=0, padx=5, pady=(5, 0), sticky="e")
    DateEntry(date_frame, textvariable=merged_from_var, date_pattern="yyyy-mm-dd", width=15).grid(row=1, column=1, padx=5, pady=(5, 0))
    tk.Label(date_frame, text="Merged To:", font=label_font).grid(row=1, column=2, padx=5, pady=(5, 0), sticky="e")
    DateEntry(date_frame, textvariable=merged_to_var, date_pattern="yyyy-mm-dd", width=15).grid(row=1, column=3, padx=5, pady=(5, 0))

    # --- Row 4: Action Buttons ---
    actions_frame = tk.Frame(filters_frame)
    actions_frame.grid(row=4, column=0, columnspan=4, pady=15)

    tk.Button(actions_frame, text="Clear Dates", command=clear_dates, width=15).pack(side="left", padx=10)
    tk.Button(actions_frame, text="Apply Filter", command=on_submit, width=15).pack(side="left", padx=10)
    tk.Button(actions_frame, text="Export", command=on_export, width=15).pack(side="left", padx=10)

    # ========== Table Section ==========
    create_table(root)

    # ========== Log Section ==========
    log_text = ScrolledText(root, height=15, width=185, state='disabled', bg="#2e2e2e", fg="white", insertbackground="white")
    log_text.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")

    log_widget = log_text
    font_style = tkFont.Font(family="Segoe UI", size=10)
    log_widget.tag_configure("custom_font", font=font_style)

    clear_dates()
    root.mainloop()

def create_table(root):
    global tree

    # Create style to increase row height
    style = ttk.Style()
    style.configure("Treeview", rowheight=30) 

    columns = ("PR #", "PR Name", "Source Branch", "Target Branch", "Status", "Requested By", "Requested Date", 
               "Merged By", "Merged Date", "Enforced Rule", "Actual Check Result")

    # Create Treeview widget
    tree = ttk.Treeview(root, columns=columns, show="headings", style="Treeview")
    
    # Set headings and columns
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    # Custom column widths
    tree.column("PR #", width=60, anchor="center")
    tree.column("PR Name", width=300, anchor="center")
    tree.column("Source Branch", width=125, anchor="center")
    tree.column("Target Branch", width=125, anchor="center")
    tree.column("Status", width=70, anchor="center")
    tree.column("Requested By", width=120, anchor="center")
    tree.column("Requested Date", width=150, anchor="center")
    tree.column("Merged By", width=150, anchor="center")
    tree.column("Merged Date", width=150, anchor="center")
    tree.column("Enforced Rule", width=90, anchor="center")
    tree.column("Actual Check Result", width=160, anchor="center")

    # Create a vertical scrollbar and link it to the Treeview
    vsb = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    vsb.grid(row=4, column=5, sticky="ns", pady=10)
    
    tree.configure(yscrollcommand=vsb.set)

    # Grid configuration to make it stretchable
    tree.grid(row=4, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")
    
    # Make the table resizable with window
    root.grid_rowconfigure(4, weight=1)
    root.grid_columnconfigure(0, weight=1)

create_ui()