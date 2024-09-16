import argparse
from pydub import AudioSegment
from pydub.generators import Sine
import tempfile

def morse_to_audio(morse_code, frequency=700, dot_duration=100):
    # Morse code dictionary
    morse_dict = {
        '.': dot_duration,
        '-': dot_duration * 3,
        ' ': dot_duration * 7  # space between words
    }

    # Create an empty audio segment
    audio = AudioSegment.silent(duration=0)

    # Generate the audio for each symbol
    for symbol in morse_code:
        if symbol in morse_dict:
            duration = morse_dict[symbol]
            if symbol != ' ':
                tone = Sine(frequency).to_audio_segment(duration=duration)
                silence = AudioSegment.silent(duration=dot_duration)  # silence between dots/dashes
                audio += tone + silence
            else:
                audio += AudioSegment.silent(duration=duration)  # silence between words

    # Save the audio to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    audio.export(temp_file.name, format="wav")
    
    return temp_file.name

def main():
    parser = argparse.ArgumentParser(description="Convert Morse code to an audio file.")
    parser.add_argument("morse_code", type=str, help="The Morse code to convert (use '.' for dot, '-' for dash, and ' ' for space).")
    parser.add_argument("--frequency", type=int, default=700, help="Frequency of the tone in Hz (default: 700).")
    parser.add_argument("--dot_duration", type=int, default=100, help="Duration of a dot in milliseconds (default: 100).")

    args = parser.parse_args()

    # Call the morse_to_audio function
    audio_file = morse_to_audio(args.morse_code, args.frequency, args.dot_duration)
    AudioSegment.from_file(audio_file)
    
    print(f"Audio file saved as: {audio_file}")

if __name__ == "__main__":
    main()
