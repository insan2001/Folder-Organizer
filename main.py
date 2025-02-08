from organizer import FileOrganizer


if __name__ == "__main__":
    fo = FileOrganizer(r"C:\Users\gaming\Downloads")
    fo.organize(fo.categorizeByType)
    
    