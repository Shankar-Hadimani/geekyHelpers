from  gtts import gTTS

#  input Text
input_user_text  =  input('Enter the text to be converted to Speech.... ! \t')

# convert to text To Speech
voice = gTTS(text=input_user_text, lang='en', slow=False)

# save the voice / sppech into a file : MP3
voice.save(r"output\TextToSpeechConverted.mp3")
