from django.shortcuts import render
from textblob import TextBlob
import language_tool_python
# Create your views here.
def index(request):
    return render(request,'spellchecker/index.html')

def spell(request):
    if request.method=='POST':
        text = request.POST.get('text')
        words = text.split()
        corrected_words = []
        for word in words:
            corrected_word = str(TextBlob(word).correct())
            corrected_words.append(corrected_word)
        corrected_text= " ".join(corrected_words)
        tool = language_tool_python.LanguageToolPublicAPI('en-US')
        corrected_grammar = tool.correct(corrected_text)
        data={'corrected_text':corrected_text,'corrected_grammar':corrected_grammar}
        print(data)
        return render(request,'spellchecker/index.html',data)
def grammar(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        x=file.read()
        corrected_words=[]
        for word in x.decode().split():
            print(word)
            corrected_word = str(TextBlob(word).correct())
            corrected_words.append(corrected_word)
        corrected_file_text = " ".join(corrected_words)
        tool = language_tool_python.LanguageToolPublicAPI('en-US')
        corrected_file_grammar = tool.correct(corrected_file_text)
        data={'file_data':x.decode(),'corrected_file_text':corrected_file_text,'corrected_file_grammar':corrected_file_grammar}
    return render(request,'spellchecker/index.html',data)

