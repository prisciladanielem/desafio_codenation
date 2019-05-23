import requests
import json
import hashlib

def request(arquivo, url_request):
    #Faz a request para o endereço do codenation
    rq = requests.get(url_request)
    #Guarda o resultado na variável text
    text = rq.text
    #Cria o arquivo answer.json conforme solicitado
    with open(arquivo, 'w') as fileJson:
        json.dump(text, fileJson)
    #Retorna o texto mandado na request
    return print(text)

def updateJson(file, newJson):
    with open(file, "w") as fileJson:
        json.dump(newJson, fileJson)

def decode(file):
    with open (file,'r',encoding='utf-8') as fileJson:
        aux = json.load(fileJson) #Load transforma o arquivo em String

    answer = json.loads(aux) # Loads transforma o json em um dicionário

    alphabet = 'abcdefghijklmnopqrstuvwxyz'

    text_decoded = ''

    answer['cifrado'] = answer['cifrado'].lower() #Converte o texto para letras minúsculas

    for letter in answer['cifrado']:
        if letter in alphabet:
            num = alphabet.find(letter) - int(answer['numero_casas']) # Encontra a posição da letra e 
            text_decoded = text_decoded + alphabet[num]
        else:
            text_decoded = text_decoded + letter # Mantém caracteres que não estão na variável alphabet

    #Guarda no dicionário a frase decodificada
    answer['decifrado'] = text_decoded 
    answer['resumo_criptografico'] = hashlib.sha1(answer['decifrado'].encode('utf-8')).hexdigest() # Biblioteca hashlib (hash) criptografa o texto decifrado
    #Atualiza o arquivo json com o texto decifrado
    updateJson(file,answer)

    print('texto ',text_decoded)
    print(answer['resumo_criptografico'])

#Função para enviar uma request post multipart
def sendAnswer(file, url):
    u = url
    answer = {'answer': open(file, 'rb')}

    r = requests.post(u, answer=answer)
    print(r.text)
    print(r.status_code)

if __name__ == "__main__":
    file = 'answer.json'
    url_request = 'https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token=fb7ba5effdc7e776af83ed8ee9bd214d7d9ddd7e'
    url_submit = 'https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token=fb7ba5effdc7e776af83ed8ee9bd214d7d9ddd7e'
    request(file, url_request)
    decode(file)
    sendAnswer(file, url_submit)