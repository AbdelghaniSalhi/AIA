import speech_recognition as sr
import time

def recognize(recognizer, microphone):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    recognizer.recognize_google(audio, language='fr-FR')

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


if __name__ == "__main__":
    PROMP_LIMIT = 5
    r = sr.Recognizer()
    microphone = sr.Microphone()

    time.sleep(3)
    for j in range(PROMP_LIMIT):
        print("Quelles sont vos stations")
        guess = recognize(r, microphone)
        if guess["transcription"]:
            break
        if not guess["success"]:
            break
    if guess["error"]:
        print("ERROR: {}".format(guess["error"]))

    print(guess["transcription"])