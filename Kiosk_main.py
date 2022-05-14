# STT 패키지
import speech_recognition as sr 
# mp3 파일 플레이 패키지
import pygame
#노란 줄 뜰 경우, 콘솔 창에 pip install SpeechRecognition 입력
#pip install pygame

# 특정 텍스트에 리스트의 아이템이 들어있는지 확인하는 메소드
def check_if_exists(txt, _list):
  for item in _list:
    if(txt.find(item)>=0):
      return True
  return False

# 파일 경로를 입력받아서 음성 파일을 실행하는 메소드 
def play_mp3file(path):
  pygame.mixer.music.load(path)
  pygame.mixer.music.play()
  while pygame.mixer.music.get_busy() == True:
      continue

#프로그램 시작
r = sr.Recognizer()
speech = sr.Microphone(device_index=1) #음성 인식 기기 (마이크) 지정.
pygame.mixer.init()

MENU = ['햄버거' , '떡볶이'] #메뉴 리스트

while(True): 

  #음성인식 시작
  with speech as source: 
      print("음성 인식 중!…")
      audio = r.adjust_for_ambient_noise(source) 
      audio = r.listen(source)
      
  try:
      # 구글 STT API 로 음성 -> 텍스트로 변환된 'txt' 변수 지정
      txt = r.recognize_google(audio, language = 'ko-KR') 
      print("STT 결과 : " + txt)
    
      # check_if_exists 메소드로 txt 에 MENU 리스트의 아이템이 포함되어있는지 확인
      if(check_if_exists(txt,MENU)): 
        # 텍스트에 메뉴가 포함 되어 있는 경우~
        print("메뉴가 포함 되어있음")
        play_mp3file("./주문하시겠습니까.mp3") # 음성 파일 실행 메소드로 음성파일 실행
        #...~
      else:
        # 텍스트에 메뉴가 포함되어 있지 않은 경우~
        print("메뉴가 포함 되어있지 않음")
        #...~

  except sr.UnknownValueError:
      print("구글 STT 가 음성인식을 하지 못했습니다.")
  except sr.RequestError as e:
      print("Could not request results from Google Speech Recognition service; {0}".format(e))

