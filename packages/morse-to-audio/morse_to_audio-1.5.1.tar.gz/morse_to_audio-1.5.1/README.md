

# Morse to Audio


----

try our demo in spaces!


[![open in hf](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Space-s?labelColor=YELLOW&color=FFEA00)](https://huggingface.co/spaces/kindahex/morse-to-audio)


---



A simple Python package that converts Morse code into an audio file. This tool supports customizable frequencies and dot durations to generate Morse code tones.

## Features
- Convert Morse code (`.`, `-`, and spaces) into audio.
- Customize the tone frequency and dot duration.
- Outputs a `.wav` file of the generated Morse code audio.

## Installation

You can install the package using pip:

```bash
pip install morse-to-audio
```

## Usage

Once installed, you can use the `morse-to-audio` command in your terminal to convert Morse code to audio:

```bash
morse-to-audio ".- .- -" --frequency 700 --dot_duration 100
```

### Arguments
- `morse_code`: The Morse code to convert. Use `.` for dots, `-` for dashes, and spaces between words.
- `--frequency`: The frequency of the tone in Hz. Default is `700`.
- `--dot_duration`: The duration of a dot in milliseconds. Default is `100`.

### Example
```bash
morse-to-audio "-- .- -." --frequency 750 --dot_duration 120
```

This will generate a `.wav` file with the Morse code for "MAN" and save it to your system.

## How It Works

The package uses the `pydub` library to generate sine waves representing the Morse code tones. Each dot, dash, and space is converted into an audio segment and combined into a final output file.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

