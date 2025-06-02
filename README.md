# USB Device Monitor

This project monitors connected USB devices and notifies you when a new device is connected. It leverages the macOS `ioreg` command to gather device information and a Python script to process and report changes.

It's not meant to be real time, rather it's meant to run as a cron job every minute. This adds a slight delay between plugging in a device and getting notified, but this decision means the script doesn't need root access for any reason, and isn't getting in the middle of any io tasks.

## Prerequisites

* **macOS:** This project is designed for macOS.
* **Python 3:**  Ensure you have Python 3 installed.
* **Dependencies:** 
    * terminal-notifier (https://github.com/julienXX/terminal-notifier)


## Installation and Cron Setup

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd <project_directory>
   ```

2. **Set Cron Job**
   This script works best running every minute. Here's my cron job.
   ```
   * * * * * /Users/patrick/.local/venv/usb-watcher/bin/python3 /Users/patrick/Developer/usb-watcher/main.py
   ```

## Manual Usage

Run the `main.py` script:

```bash
python3 main.py
```

**Optional Arguments:**

* `-v`:  Verbose mode. Prints the name and parent device of each connected device as it's discovered.

## How it Works

1. **Gather USB Information:** The script first executes the following bash command:

   ```bash
   /usr/sbin/ioreg -p IOUSB -a | /usr/bin/plutil -convert json -o -
   ```

   This command retrieves detailed information about all connected USB devices in JSON format.

2. **Parse JSON Data:** The Python script parses the JSON output from the bash command.

3. **Detect New Devices:** The script compares the current list of devices with a previously saved list (stored in `devices.json`). If a new device is found, it prints a message to the console and displays a desktop notification.

4. **Save Device List:** The script saves the current list of devices to `devices.json` for future comparisons.

## `devices.json`

The script uses a file named `devices.json` to store the list of previously detected USB devices. This file is created automatically if it doesn't exist.  It's a JSON file containing a dictionary where the keys are the device names and the values are dictionaries containing device information (parent device, class, name).

## Troubleshooting

* **`osascript` not found:** If you receive an error message about `osascript` not being found, it means that the command-line tools for desktop notifications are not installed or not in your system's PATH.  This is usually not an issue on macOS.
* **No notifications:**  Ensure that desktop notifications are enabled in your macOS System Preferences.
* **Script doesn't run:** Double-check that you have Python 3 installed and that the script is executable (`chmod +x main.py`).

## Future Improvements

* **More robust error handling:** Add more comprehensive error handling to gracefully handle unexpected situations.
* **Device filtering:** Allow users to filter the list of devices based on specific criteria (e.g., vendor ID, product ID).
* **Logging:** Implement logging to record events and errors for debugging purposes.
