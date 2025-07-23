import os
from pydub import AudioSegment
import pygame as pg
import speech_recognition as sr

myfolder = "/Users/xuzijun/Desktop/working/Beijing audio"
newfolder = "matched_clips"
keywords = ["家庭","购买","放心","实惠","推荐"]  #️["family" "purchase" "assured" "affordable" "recommend"] These words were chosen because the audio content comes from a Chinese radio shopping program.
os.makedirs(newfolder, exist_ok=True)
r = sr.Recognizer()
segment_length_ms = 20 *1000

for filename in os.listdir(myfolder):
    if filename.endswith(".aac"):
        filepath= os.path.join(myfolder,filename)
        audio = AudioSegment.from_file(filepath,format="aac")
        audio_length = len (audio)
        num_segments = audio_length // segment_length_ms
        for i in range(num_segments):
            start = i * segment_length_ms
            end = start + segment_length_ms
            segment = audio [start:end]
            tem_wav = "temp.wav"
            segment.set_frame_rate(16000).set_channels(1).set_sample_width(2).export(tem_wav, format = "wav")
            with sr.AudioFile(tem_wav) as source:
                audio_data = r.record(source)
            try: 
                text = r.recognize_google (audio_data, language="zh-CN")
                print(f"No.{i+1}result: {text}")
                if any(kw in text for kw in keywords):
                    print ("matched")
                    outputname = f"{filename.replace('.aac',' ')}_chunk{i+1}.wav"
                    outputpath = os.path.join(newfolder,outputname)
                    segment.set_frame_rate(16000).set_channels(1).set_sample_width(2).export(outputpath, format = "wav")
            except sr.UnknownValueError:
                    print(f"No.{i+1}cannot be read")
            except sr.RequestError as e:
                    print(f"wrongrequest: {e}")

