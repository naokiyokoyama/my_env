import os
import datetime
import argparse
from exif import Image

def adjust_created_date(directory, hours_shift, minutes_shift):
    # Loop through files in the given directory
    for filename in os.listdir(directory):
        if filename.lower().endswith(".jpg"):
            file_path = os.path.join(directory, filename)
            
            # Open the image file
            with open(file_path, "rb") as image_file:
                image = Image(image_file)
            
            # Check if the image has EXIF data
            if image.has_exif:
                # Get the "Date Time Original" EXIF tag
                created_date_str = image.datetime_original
                
                if created_date_str:
                    # Convert the EXIF date string to a datetime object
                    created_date = datetime.datetime.strptime(created_date_str, "%Y:%m:%d %H:%M:%S")
                    
                    # Adjust the creation date by the specified number of hours and minutes
                    new_created_date = created_date + datetime.timedelta(hours=hours_shift, minutes=minutes_shift)
                    
                    # Update the "Date Time Original" and "Date Time Digitized" EXIF tags
                    image.datetime_original = new_created_date.strftime("%Y:%m:%d %H:%M:%S")
                    image.datetime_digitized = new_created_date.strftime("%Y:%m:%d %H:%M:%S")
                    
                    # Save the modified image with updated EXIF data
                    with open(file_path, "wb") as modified_image_file:
                        modified_image_file.write(image.get_file())
                    
                    print(f"Adjusted '{filename}' from {created_date} to {new_created_date}")
                else:
                    print(f"Skipping '{filename}' due to missing 'Date Time Original' EXIF tag.")
            else:
                print(f"Skipping '{filename}' due to missing EXIF data.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Adjust the creation dates of .JPG files in a directory."
    )
    parser.add_argument(
        "directory_path", type=str, help="Path to the directory containing .JPG files."
    )
    parser.add_argument(
        "hours_shift",
        type=str,
        help="Number of hours to adjust the creation date by (can be negative).",
    )
    parser.add_argument(
        "minutes_shift",
        type=str,
        help="Number of minutes to adjust the creation date by (can be negative).",
    )
    
    args = parser.parse_args()
    
    assert str(int(args.hours_shift)) == args.hours_shift, "hours_shift must be an integer"
    assert str(int(args.minutes_shift)) == args.minutes_shift, "minutes_shift must be an integer"
    
    adjust_created_date(args.directory_path, int(args.hours_shift), int(args.minutes_shift))
