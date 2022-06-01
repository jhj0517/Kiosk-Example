

  except sr.UnknownValueError:
      print("구글 STT 가 음성인식을 하지 못했습니다.")
  except sr.RequestError as e:
      print("Could not request results from Google Speech Recognition service; {0}".format(e))

