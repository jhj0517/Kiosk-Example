import speech_recognition as sr 
# mp3 파일 플레이 패키지
import pygame
# 날씨 스크래핑 모듈
import API.weather_recommendation as weather_recommendation 
import requests
#tts
from gtts import gTTS
# 자체 NLP 모듈
import API.NLP as nlp
import time
#노란 줄 뜰 경우, 콘솔 창에 pip install SpeechRecognition 입력 
#pip install pygame
#pip gtts

# 텍스트에 리스트의 아이템이 들어있는지 확인하는 메소드
def getExtractedMenubyAPI(txt, _list):
  API_URL = '이 URL 을 교체해서 실행'
  param = {'mylist':_list, 'sentence':txt}
  return requests.get(url=API_URL,params=param).json()
  
# 파일 경로를 입력받아서 음성 파일을 실행하는 메소드 
def play_mp3file(path):
  pygame.mixer.music.load(path)
  pygame.mixer.music.play()
  while pygame.mixer.music.get_busy() == True:
      continue

# 마이크로 부터 받은 음성 데이터를 전처리
def exprocess_audiodata(_speech):
    with _speech as source: 
      print("음성 인식 중!…")
      audio = r.adjust_for_ambient_noise(source) 
      audio = r.listen(source)
    return audio

def recognize_speech():
  audio = exprocess_audiodata(speech)
  return r.recognize_google(audio, language = 'ko-KR') 

count = 0
def speak_TTS(data):
    global count
    language_toSay= 'ko' #_lang = en or ko
    tts = gTTS(text=data, lang=language_toSay)
    tts.save(f'speech{count%2}.mp3')
    play_mp3file(f'speech{count%2}.mp3')
    count += 1    

"""사용할 커스텀 변수들"""
MENU = ['햄버거' , '떡볶이'] #메뉴 리스트
시동어 = "경북대"
추가메뉴주문확인 = "추가로 주문 하시겠습니까?"
#recommend = weather_recommendation.get_recommendedList() #웹스크래핑으로 얻어온 추천메뉴

"""장치 초기화"""
r = sr.Recognizer()
speech = sr.Microphone(device_index=1) #음성 인식 기기 (마이크) 지정.
pygame.mixer.init()
""""""

#프로그램 시작

#speak_TTS("프로그램 시작")
while(True): 
  #음성인식 시작
  try:
      txt = recognize_speech() #음성인식해서 문장으로 만드는 STT 메소드
      print(f'STT 음성 인식 문장:{txt}')
      print(txt.find(시동어))

      if(txt.find(시동어)>=0): #문장에서 시동어 찾기
        print("시동어 인식됨, 1단계 로직 실행")
        txt = recognize_speech() #시동어 인식한 이후 다시 STT로 음성인식

        print(f'STT 음성 인식 문장:{txt}')
        Mymenu = nlp.getWordsFromList(txt,MENU)
        print(f"인식한 메뉴 : {Mymenu}")
        Mynums = nlp.extract_nums(txt)
        print(f"인식한 숫자: {Mynums}")
        NLPedtext = nlp.makeTextwithMenuAndNum(Mymenu,Mynums)

        if(Mymenu and len(Mymenu)==len(Mynums)): 
          # 유효한 메뉴를 최소 하나 이상 말했고, 유효한 각 메뉴에 대해 갯수를 각각 전부 말한 경우
          print("유효한 메뉴와 숫자를 각각 말함, 2단계 로직 실행")
          speak_TTS(NLPedtext) # NLPedtext = 주문한 메뉴1 몇개, 메뉴 2 몇개 ..~ 가 맞습니까? 를 나타내는 문장
          print(f'{NLPedtext}')  

          speak_TTS(추가메뉴주문확인) #추가주문확인문장 = 추가로 주문하시겠습니까? 
  
          txt = recognize_speech() #다시 STT로 음성인식 
          print(f'STT 음성 인식 문장:{txt}')
  
          if(txt.find("네")>=0): #문장에 '네' 가 포함 되어 있는경우 
            print("'네'를 말함, 3단계 로직 실행")
            speak_TTS("주문화면에서 다시 주문해주세요.")
            #``
          elif(txt.find("아니요")>=0):
            print("'아니오'를 말함, 3단계 로직 실행")
            speak_TTS("결제를 도와드리겠습니다.")

          else:
            #그 외의 경우 , 3단계 로직
            print("그 외의 경우")
            #...~
      else:
        #시동어로 시작하지 않은 경우
        print("시동어가 인식 안됨")    

  except sr.UnknownValueError:
      print("구글 STT 가 음성인식을 하지 못했습니다.")
  except sr.RequestError as e:
      print("Could not request results from Google Speech Recognition service; {0}".format(e))


#pip install pygame
#pip install gtts
#pip install SpeechRecognition 
#pip install deep_translator
#pip install nltk
#pip install word2number
#pip install num2words