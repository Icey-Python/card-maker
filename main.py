from fpdf import FPDF
from tkinter import Tk, filedialog
from PIL import Image

# Constants
CARD_WIDTH_MM = 85.6
CARD_HEIGHT_MM = 54.0
CARDS_PER_PAGE = 10
MARGIN = 5  # Margin between cards
PAGE_WIDTH = 210  # A4 width in mm
PAGE_HEIGHT = 297  # A4 height in mm

class PDF(FPDF):
    def add_card(self, x, y, width, height, image_path):
        self.image(image_path, x, y, width, height)

def select_single_image():
    root = Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(title="Select an Image",
                                           filetypes=[("Image Files", "*.png"),("Image files", "*.jpg"),("Image files", "*.jpeg")])
    if file_path:
        count = int(input("How many times do you want to use this image? "))
        return [file_path] * count
    return []

def select_multiple_images():
    root = Tk()
    root.withdraw()  # Hide the root window
    file_paths = filedialog.askopenfilenames(title="Select Images",
                                             filetypes=[("Image Files", "*.png"),("Image files", "*.jpg"),("Image files", "*.jpeg")])
    return list(file_paths)

def create_pdf(filename, image_paths):
    pdf = PDF()
    pdf.set_auto_page_break(auto=False, margin=0)
    
    # Calculate number of rows and columns to fit 10 cards per page
    cards_per_row = 2
    cards_per_column = 5
    
    total_cards = len(image_paths)
    num_pages = (total_cards + CARDS_PER_PAGE - 1) // CARDS_PER_PAGE
    
    for page_num in range(num_pages):
        pdf.add_page()
        start_x = ((PAGE_WIDTH - 10) - (cards_per_row * CARD_WIDTH_MM)) / 2
        start_y = ((PAGE_HEIGHT - 20) - (cards_per_column * CARD_HEIGHT_MM)) / 2
        
        for row in range(cards_per_column):
            for col in range(cards_per_row):
                card_index = page_num * CARDS_PER_PAGE + row * cards_per_row + col
                if card_index >= total_cards:
                    break  # Stop if we have added all cards
                x = start_x + col * (CARD_WIDTH_MM + MARGIN)
                y = start_y + row * (CARD_HEIGHT_MM + MARGIN)
                pdf.add_card(x, y, CARD_WIDTH_MM, CARD_HEIGHT_MM, image_paths[card_index])

    pdf.output(filename)

def main():
    print("Choose an option:")
    print("1. Use a single image multiple times")
    print("2. Use multiple images")
    choice = input("Enter 1 or 2: ")
    
    if choice == '1':
        image_paths = select_single_image()
    elif choice == '2':
        image_paths = select_multiple_images()
    else:
        print("Invalid choice.")
        return

    if image_paths:
        create_pdf("cards.pdf", image_paths)
    else:
        print("No images selected.")
# Call the main function
if __name__ == "__main__":
    main()
