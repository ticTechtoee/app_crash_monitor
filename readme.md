# Easysales Sync Assistant

Easysales-Sync-Assistant is a Python Script for Monitoring an Application Crash.

This script will read the event log and search for a crash uisng event IDs, if found then It will look for the applicaiton name in the crash description, if found a specific applicaiton name then script will show a message, will send an Email to a specified email address, restart the target applicaiton and finally clear the log to start monitoring again.

Script will check for the event every 30 seconds.
## Usage

`python Easysales-Sync-Assistant.py`

update your .env file with `Sender Eamil Address`, `Receiver Eamil Address`, `Email App Password`, `Name of the customer`, and `Restart Time`

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)