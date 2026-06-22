# Voice Calculator - Documentation

## 1. What does the project do?
This project is an AI-powered voice calculator. It captures mathematical word queries from a user's microphone, transcribes them into text, uses a local lightweight LLM (Qwen) to process and solve the math equation, and outputs the final result through system speakers.

## 2. What is the request flow?
1. **Model Loading & Init**:
   - The user runs `calculator.py`.
   - The text-to-speech engine `pyttsx3` is initialized.
   - The text-generation pipeline `Qwen/Qwen2.5-0.5B-Instruct` is loaded into PyTorch system memory.
2. **Audio Capture**:
   - The bot says: "Voice calculator started. What would you like to calculate?".
   - `listen()` uses the `speech_recognition` module to open the microphone.
   - The recorded audio is sent to the Google Web Speech API to get a transcription.
3. **LLM Evaluation & Speaking**:
   - The transcribed text is checked for exit keywords ("exit", "quit", "stop").
   - If not exit, the text query is packaged with a system prompt instructing the model to return ONLY the final numerical answer.
   - Qwen generates the calculation result.
   - The result is printed to the console and spoken out loud using the local `pyttsx3` engine ("The result is {answer}").

## 3. Which packages are used and why?
- **`speech_recognition`**: Connects to user microphone hardware and utilizes the Google Speech API for transcription.
- **`pyttsx3`**: Runs local offline text-to-speech voice generation.
- **`torch`**: Required for executing neural network tensor operations.
- **`transformers`**: HuggingFace library to load and run the local instruct model `Qwen/Qwen2.5-0.5B-Instruct`.

## 4. Where does the data come from?
The data comes from voice commands recorded via the user's microphone.

## 5. Where is the data stored?
All evaluations, models, and audio transcriptions are processed dynamically in RAM. No persistent files or databases are saved.

## 6. What is the role of the LLM?
The local Qwen model (`Qwen2.5-0.5B-Instruct`) interprets spoken math commands (e.g. "three divided by two", "square of five") and returns the calculated numeric result, bypassing the need for complex string regex parsing.

## 7. What breaks if the LLM is removed?
The spoken query evaluation process will fail. The system would need a fallback math compiler based on regular expressions to map numbers and operations, which would fail on complex phrasing.
