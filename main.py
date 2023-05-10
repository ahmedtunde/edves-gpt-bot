import openai
from flask import Flask, request, render_template, redirect
from googlesearch import search
import requests
import json
# import openai_secret_manager
from bs4 import BeautifulSoup

server = Flask(__name__)

# openai.api_key = "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"

# def generate_openai_image(question):
#     # Get API key
#     # secrets = openai_secret_manager.get_secrets("openai")
#     api_key ="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"
    
#     # Define headers and payload
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {api_key}"
#     }
#     data = """
#     {
#         """
#     data += f'"prompt": "{question}",'
#     data += """
#         "model": "image-alpha-001",
#         "num_images":1,
#         "size":"1024x1024",
#         "response_format":"url"
#     }
#     """

#     # Send post request
#     resp = requests.post('https://api.openai.com/v1/images/generations',
#                          headers=headers, data=data)
#     response_text = json.loads(resp.text)
#     return response_text['data'][0]['url']


# # def get_links_and_images(question):
# #     links = []
# #     images = []
# #     for url in search(question, num=1, stop=1, safe='on'):
# #         links.append(url)
# #         try:
# #             page = requests.get(url)
# #             soup = BeautifulSoup(page.content, 'html.parser')
# #             img_tags = soup.find_all('img')
# #             for img in img_tags:
# #                 img_url = img.attrs.get('src')
# #                 if not img_url.startswith('http'):
# #                     # if no absolute URL, build it
# #                     img_url = '{}{}'.format(url, img_url)
# #                 images.append(img_url)
# #         except:
# #             continue
# #     return links, images

# def get_images(question):
#     for image in search(question, num=5, stop=10, safe=True):
#         return image


# def get_links(question):
#     for url in search(question, num=10, stop=10, safe=True):
#         return [url]


# def get_completion(question):
#     try:
#         response = openai.Completion.create(
#             model="text-davinci-003",
#             prompt=f"{question}\n",
#             temperature=0.9,
#             max_tokens=2048,
#             # top_p=1,
#             frequency_penalty=0,
#             presence_penalty=0.6,
#             stop=None
#         )
#     except Exception as e:

#         print(e)
#         return e
#     return response["choices"][0].text


# @server.route('/chat', methods=['GET', 'POST'])
# def get_request_json():
#     if request.method == 'POST':
#         if len(request.form['question']) < 1:
#             return render_template(
#                 'chat.html', question="null", res="question cannot be empty")
#         question = request.form['question']
#         print("======================================")
#         print("received a request:", question)
#         res1 = get_completion(question)
#         res2 = generate_openai_image(question)
#         res3 = get_links(question)
#         print("question：\n", question)
#         print("Answer：\n", res1)
#         print("Images：\n", res2)
#         print("links：\n", res3)
#         return render_template('chat.html', question=question, res1=(res1), res2 =(res2), res3 =(res3))
#     return render_template('chat.html', question=0)


# if __name__ == '__main__':
#     server.run(debug=True, host='0.0.0.0', port=80)



# from flask import Flask, request, jsonify
# from transformers import GPT2Tokenizer, GPT2LMHeadModel

# app = Flask(__name__)

# # Load the GPT-2 model and tokenizer
# model = GPT2LMHeadModel.from_pretrained("gpt2")
# tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# @app.route('/chat', methods=['POST'])
# def chat():
#     # Get the user's input from the request
#     input_text = request.json["input"]
    
#     # Tokenize the input
#     input_ids = tokenizer.encode(input_text, return_tensors="pt")
    
#     # Generate a response
#     response = model.generate(input_ids)
    
#     # Decode the response
#     response_text = tokenizer.decode(response[0], skip_special_tokens=True)
    
#     # Return the response as a


from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import openai

app = Flask(__name__)
cors = CORS(app)
cors = CORS(app, resources={r"/chat": {"origins": "https://edves.net"}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/chat', methods=['GET','POST'])
@cross_origin(allow_headers=["Content-Type"], methods=["GET","POST"])

def chat():
    openai.api_key = "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"
    # prompt = request.json['prompt']
    prompt = request.args.get('prompt')

    # Define headers and payload
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
    }
    data = """
    {
        """
    data += f'"prompt": "{prompt}",'
    data += """
        "model": "image-alpha-001",
        "num_images":1,
        "size":"256x256",
        "response_format":"url"
    }
    """

    # Send post request
    resp = requests.post('https://api.openai.com/v1/images/generations',
                         headers=headers, data=data)
    response_text = json.loads(resp.text)
    print(response_text)
    image = response_text['data'][0]['url']
    print("this is image" + image)
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
           temperature=1.0,
            max_tokens=512,
            top_p=1,
            n=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=None
            # logprobs=100
        )
    text = response['choices'][0]['text']
    print ('this is text' + text)

    link = []
    for url in search(prompt, num=3, stop=10, safe=True):
        link.append(url)
    return jsonify({'AI':text, 'image':[image], 'links':[link]})

if __name__ == '__main__':
    app.run()
