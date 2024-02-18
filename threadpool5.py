import concurrent.futures
from PIL import Image
import time
import os
import tkinter as tk
from tkinter import filedialog
import threading

# Define a function to apply a transformation to an image
def apply_filter(image_path):
    # Open the image file
    image = Image.open(image_path)
    
    # Apply a filter (e.g., convert to grayscale)
    gray_image = image.convert('L')

    # Construct a new file path for the transformed image
    base_dir = os.path.dirname(image_path)
    base_name = os.path.basename(image_path)
    new_name = 'gray_' + base_name
    new_path = os.path.join(base_dir, new_name)
    
    # Save the transformed image
    gray_image.save(new_path)
    print(f'Filter applied to {image_path}')

# Worker function( Not Used ),
#  The threading.get_ident() function is used to get a unique identifier for the current thread, 
# which is then passed to the job function as an argument. This allows the job function to print a message that includes the thread identifier,
#  showing that the threads are indeed reusing the same worker threads from the pool.
# Placeholder for the actual work that will be done by worker threads example, processing of Images.
def worker():
            # Each worker thread will do its job and then return to the pool
            job(f'Thread-{threading.get_ident()}')


# Job func (not used, we can use it to simulate the threads sho)
def job(thread_name):
    print(f'{thread_name} is starting a job')
    time.sleep(1)  # Simulate work by sleeping
    print(f'{thread_name} has completed the job')


def select_images():
    root = tk.Tk()  
    root.withdraw()
    image_paths = filedialog.askopenfilenames(filetypes=[('Image files', '*.jpg *.png *.bmp')])
    return image_paths  

# List of image paths to process
image_paths = select_images()

# Create a thread pool of 5 workers
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    futures = []
    for i, image_path in enumerate(image_paths):
        futures.append(executor.submit(apply_filter, image_path))
        if (i +  1) % 5 ==  0:
            # Wait for the current batch of tasks to complete
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f'An error occurred while processing an image: {e}')
            futures = []  # Reset the list for the next batch
            print(f'Batch is Completed\n')
            time.sleep(10)  # Sleep for  1 second before starting the next batch
    
    # Process the remaining tasks as they complete
    for future in concurrent.futures.as_completed(futures):
        try:
            # Get the result of the task
            future.result()
        except Exception as e:
            print(f'An error occurred while processing {futures[future]}: {e}')
