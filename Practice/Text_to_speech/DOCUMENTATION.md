# Text-to-Speech Practice - Documentation

## 1. What does the project do?
This project is a local Text-to-Speech (TTS) converter. It loads a multilingual voice model to synthesize natural-sounding spoken audio from a hardcoded English text string.

## 2. What is the request flow?
1. **Startup**: The user runs `app.py`.
2. **Model Load**: The Coqui TTS class constructor loads the pre-trained `xtts_v2` model.
3. **Voice Synthesis**: `tts.tts_to_file` translates the multi-line text string into audio waveforms.
4. **Output Saving**: The generated audio is saved to `output.wav`.

## 3. Which packages are used and why?
- **`coqui-tts` (`TTS`)**: Main engine used to load pre-trained multilingual speech synthesis networks (`xtts_v2`) and write audio waveforms.

## 4. Where does the data come from?
The input data is a hardcoded text string inside `app.py`.

## 5. Where is the data stored?
The synthesized audio is saved locally as: `output.wav`.

## 6. What is the role of the LLM?
There is no generative chat LLM. A specialized acoustic speech neural network (`xtts_v2`) translates character phonemes into audio waves.

## 7. What breaks if the LLM is removed?
The local speech generation process will break, and the script will throw errors.
