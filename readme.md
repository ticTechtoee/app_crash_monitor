# App Monitor

App Monitor is a Python Script for Monitoring an Application Crash.

This script will read the event log and search for a crash uisng event IDs, if found then It will show a message, will send an Email to a specified email address
and finally clear the log to start monitoring again.

Scrip will check for the event every 30 seconds.
## Usage

`python Monitor.py`

update your .env file with `Sender Eamil Address`, `Receiver Eamil Address`, and `Email App Password`

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)