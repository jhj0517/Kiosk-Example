import speech_recognition as sr 
import requests
# 자체 날씨 스크래핑 모듈
import API.weather_recommendation as weather_recommendation 
#tts
from TTS import GoogleTTS
#자체 NLP 모듈
import API.NLP as nlp
#자체 변수들 모듈
import Constants as c

#노란 줄 뜰 경우, 깃허브 에서 명령어 실행해 다 설치되어 있는지 확인

# """텍스트에 리스트의 아이템이 들어있는지 확인하는 메소드"""
# def getExtractedMenubyAPI(txt, _list):
#   API_URL = '이 URL 을 교체해서 실행'
#   param = {'mylist':_list, 'sentence':txt}
#   return requests.get(url=API_URL,params=param).json()

"""마이크로 부터 받은 음성 데이터를 전처리"""
def exprocess_audiodata(_speech):
    with _speech as source: 
      print("음성 인식 중!…")
      audio = r.adjust_for_ambient_noise(source) 
      audio = r.listen(source)
    return audio
    
"""음성인식해서 문장으로 만드는 STT 메소드"""
def recognize_speech():
  audio = exprocess_audiodata(speech)
  return r.recognize_google(audio, language = 'ko-KR') 

r = sr.Recognizer()
speech = sr.Microphone(device_index=1) #음성 인식 기기 (마이크) 지정.

#GoogleTTS("프로그램 시작")
while(True): 
  try:
      print("시동어 인식 대기 중, 0단계 로직")
      txt = recognize_speech()
      print(f'STT 음성 인식 문장:{txt}')

      if(txt.find(c.시동어)>=0): #문장에서 시동어 찾기
        print("시동어 인식됨, 1단계 로직")
        txt = recognize_speech() #시동어 인식한 이후 다시 STT로 음성인식

        print(f'STT 음성 인식 문장:{txt}')
        Mymenu = nlp.getWordsFromList(txt,c.MENU)
        print(f"NLP 통해 인식한 메뉴 : {Mymenu}")
        Mynums = nlp.extract_nums(txt)
        print(f"NLP 통해 문장에서 인식한 숫자: {Mynums}")
        NLPedtext = nlp.makeTextwithMenuAndNum(Mymenu,Mynums)

        if(Mymenu and len(Mymenu)==len(Mynums)): # 유효한 메뉴를 최소 하나 이상 말했고, 유효한 각 메뉴에 대해 갯수를 각각 전부 말한 경우
          print("유효한 메뉴와 숫자를 각각 말함, 2단계 로직")
          GoogleTTS(NLPedtext) # 위에서 인식한 메뉴와 숫자들을 TTS로 말함
          print(f'{NLPedtext}')  
          GoogleTTS(c.추가메뉴주문확인문구) #추가로 주문하시겠습니까? 를 TTS로 말함
  
          txt = recognize_speech() #다시 STT로 다음 문장 음성인식
          print(f'STT 음성 인식 문장:{txt}')
  
          if(txt.find("네")>=0): #문장에 '네' 가 포함 되어 있는경우 
            print("'네'를 말함, 3단계 로직")
            GoogleTTS("주문화면에서 추가 주문을 해주세요.")

          elif(txt.find("아니요")>=0): #문장에 '아니오' 가 포함 되어 있는경우 
            print("'아니오'를 말함, 3단계 로직")
            GoogleTTS("결제를 도와드리겠습니다.")

          else: #그 외의 경우 
            print("그 외의 경우, 3단계 로직")
            #...~
      else:
        #맨 처음 시작할 때 시동어가 인식 안 된 경우
        print("시동어가 되지 않음, 대기")    

  except sr.UnknownValueError:
      print("구글 STT에서 아무 음성도 받지 않음.")
  except sr.RequestError as e:
      print("Could not request results from Google Speech Recognition service; {0}".format(e))
