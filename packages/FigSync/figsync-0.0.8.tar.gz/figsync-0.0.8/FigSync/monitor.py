import os
import tkinter as tk
from .git import *
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil
import fitz
import time
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Figure Synchronization Tool: Keep your vector and bitmap figures synchronized')
    parser.add_argument('local_folder', type=str, help='Local folder containing the pdf files')
    parser.add_argument('repo_folder', type=str, help='git repository folder where the files must be copied in')
    args = parser.parse_args()
    return args


def log(msg, log_textbox=None):
    if log_textbox:
        log_textbox.insert(tk.END, msg)
    else:
        print(msg)

class PDFChangeHandler(FileSystemEventHandler):
    def __init__(self,
                 vector_folder,
                 bitmap_folder,
                 log_textbox):
        self.vector_folder = vector_folder
        self.bitmap_folder = bitmap_folder
        self.log_textbox = log_textbox
        self.last_file = None
        self.last_update = time.time()

    def on_modified(self, event):
        if event.src_path == self.last_file:
            if time.time() - self.last_update < 1:
                return
        if not event.is_directory and event.src_path.endswith(".pdf"):
            log(f"PDF file modified: {event.src_path}\n", self.log_textbox)
            self.process_update(event.src_path)

    # def on_created(self, event):
    #     # Check if the newly created file has a .pdf extension
    #     if event.src_path == self.last_file:
    #         if time.time() - self.last_update < 1:
    #             return
    #     if not event.is_directory and event.src_path.endswith(".pdf"):
    #         self.log_textbox.insert(tk.END, f"PDF file created: {event.src_path}\n")
    #         self.process_update(event.src_path)

    def process_update(self, src_path):
        self.last_file = src_path
        self.last_update = time.time()
        time.sleep(.5)
        shutil.copy(src_path, self.vector_folder)
        log(f"{src_path} copied to vector folder", self.log_textbox)
        pdf_document = fitz.open(src_path)
        if len(pdf_document) == 0:
            log(f"ERROR: {src_path} is empty", self.log_textbox)
            return
        if len(pdf_document) > 1:
            log(f"WARNING: {src_path} contains more than one page, only the first page will be converted to bitmap\n")
        file_name = os.path.basename(src_path).replace(".pdf", ".jpg")
        output_path = os.path.join(self.bitmap_folder, file_name)
        page = pdf_document.load_page(0)
        pix = page.get_pixmap()
        pix.save(output_path)
        log(f"{file_name} copied to bitmap folder", self.log_textbox)


def monitor(localFolder,
            repoFolder,
            log_textbox=None):
    if not os.path.isdir(localFolder):
        log(f"{localFolder} folder does not exist", log_textbox)
        return None
    if not os.path.isdir(repoFolder):
        log(f"{repoFolder} folder does not exist", log_textbox)
        return None
    fig_folder = os.path.join(repoFolder, "figures")
    if not os.path.isdir(fig_folder):
        log(f"{fig_folder} folder does not exist", log_textbox)
        return None
    vector_folder = os.path.join(fig_folder, "vector")
    if not os.path.isdir(vector_folder):
        log(f"{vector_folder} folder does not exist", log_textbox)
        return None
    bitmap_folder = os.path.join(fig_folder, "bitmap")
    if not os.path.isdir(bitmap_folder):
        log(f"{bitmap_folder} folder does not exist", log_textbox)
        return None

    git_accessible, message = is_git_accessible()
    if not git_accessible:
        log("{message}", log_textbox)
        return None

    event_handler = PDFChangeHandler(vector_folder=vector_folder,
                                     bitmap_folder=bitmap_folder,
                                     log_textbox=log_textbox)
    observer = Observer()
    observer.schedule(event_handler, path=localFolder, recursive=False)
    observer.start()
    return observer


if __name__ == "__main__":
    try:
        args = parse_arguments()
        observer = monitor(localFolder=args.local_folder, repoFolder=args.repo_folder)
        if observer is not None:
            observer.join()
    except argparse.ArgumentError as e:
        print("Error:", e)
        exit(1)
