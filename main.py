from flask import Flask, render_template, request, jsonify
from deep_translator import GoogleTranslator

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def index():
    lang_list = GoogleTranslator().get_supported_languages(as_dict=True)
    from_lang = request.form.get('from_lang')
    to_lang = request.form.get('to_lang')
    exchange = request.form.get('reverse')

    if exchange:
        from_lang, to_lang = to_lang, from_lang
            
    return render_template("index.html", from_lang=from_lang, to_lang=to_lang, languages= lang_list.keys())

@app.route('/translate', methods=['GET','POST'])
def translate():
    if request.method == 'POST':
        from_lang = request.form.get('from_lang')
        to_lang = request.form.get('to_lang')
        text = request.form['original_text']
        
        if from_lang and to_lang and text:
            translated = GoogleTranslator(source=from_lang, target=to_lang)
            translated_text = translated.translate(text)
            return jsonify({'final_text': translated_text})
        else:
            return jsonify({'error': 'Invalid input!'}), 400

    return jsonify({'error': 'Invalid request method!'}), 405

app.run(debug=True)
