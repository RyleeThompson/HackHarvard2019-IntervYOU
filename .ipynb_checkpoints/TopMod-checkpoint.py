import Speech
import Conversion

def main():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\rylee\GCloud\Path.json"
    Speech.getAudioInput(2)
    Conversion.getTextFiles(2)
    
main()