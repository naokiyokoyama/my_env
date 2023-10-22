import os
import datetime
import argparse


def adjust_created_date(directory, hours_shift):
    # Loop through files in the given directory
    for filename in os.listdir(directory):
        if filename.lower().endswith(".jpg"):
            file_path = os.path.join(directory, filename)

            # Get the file's creation time using os.stat()
            stat_info = os.stat(file_path)
            created_timestamp = stat_info.st_birthtime

            # Convert the timestamp to a datetime object
            created_date = datetime.datetime.fromtimestamp(created_timestamp)

            # Adjust the creation date by the specified number of hours
            new_created_date = created_date + datetime.timedelta(hours=hours_shift)

            # Update the creation time of the file
            os.utime(file_path, (stat_info.st_atime, new_created_date.timestamp()))

            print(f"Adjusted '{filename}' from {created_date} to {new_created_date}")


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

    args = parser.parse_args()

    assert str(int(args.hours_shift)) == args.hours_shift, (
        "hours_shift must be an integer"
    )

    adjust_created_date(args.directory_path, int(args.hours_shift))
