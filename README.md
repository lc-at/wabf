# WABF - WhatsApp Brute-Forcer
WhatsApp phone number bruteforcer. This tool is great in case you have an already existing WhatsApp phone number with
a few missing digits.
Wabf works by (ab)using WhatsApp Web API. That's why, in order for wabf to work, you need to log in with your WhatsApp mobile app.
This project is an early implementation of one of my project, [Kyros](https://github.com/p4kl0nc4t/kyros).
To run this tool, you need to have at least Python 3.6 installed.

## Installation
The installation is actually pretty straightforward.
```
git clone https://github.com/p4kl0nc4t/wabf
cd wabf
pip install -r requirements.txt
```

## Usage
To simply run the tool (notice the "x" this is thenumber which we are unsure of):
```
In Windows CMD
    python3 wabf.py 6281288x272x7
In Linux:
    sudo chmod 777 wabf.py
    python3 wabf.py
     
```
### `PHONE_NUMBER` argument
The content of this first and only argument is the phone number which has a missing digit identified by "x". 
"x" means that it is possible that the missing digit is between 0 and 9 (0, 1, 2, 3, 4, 5, 6, 7, 8, 9).
If you already know the missing digit candidates (e.g. you have seen those digits partially), you can wrap all
those possible digits in a square bracket like this: `628122[123][456]27726`. 
Later on, wabf will bruteforce all those possible missing digits.

#### TL;DR
Assume that the complete phone number is `123`.
- The first digit is missing: `x23`
- The second digit is missing but you know that it must be 1, 2, or 3: `1[123]3`
- Both of the above statements are true: `x[123]3`

### Options
The options are pretty straightforward, too. You could also look for their explanations by appending `-h` or `--help`.
These are their simple explanations.
- `--disable-cache`, `-dc`: do not save the logged in session (by default, wabf saves it to prevent unnecessary relogin)
- `--output-format`, `-f`: the desired output format (`wa.me` is `https://wa.me/<phone_number>`, `jid` is the format used
by WhatsApp, and `pn` is the phone number only format)
- `--output-file`, `-o`: the output file, specify this if you want to save the results in a file
- `--help`, `-h`: show the help message


## Contribution
Any kind of contribution is highly appreciated. Do not hesitate to open an issue or pull request.

## License
This project is licensed with MIT License.

## Disclaimer
This code is in no way affiliated with, authorized, maintained, sponsored
or endorsed by WhatsApp or any of its affiliates or subsidiaries. This is
an independent and unofficial software. Use at your own risk.
