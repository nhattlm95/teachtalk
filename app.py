from flask import Flask, flash, request, redirect, url_for, render_template
from models.HierarchicalClassification import HierarchicalClassification
import os, requests

from werkzeug.utils import secure_filename


UPLOAD_FOLDER = './uploaded_files'
UPLOAD_EXTENSIONS = {'.txt', '.doc', '.docx'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_EXTENSIONS'] = UPLOAD_EXTENSIONS

text_s1 = ["Teacher does not make any effort to link student contributions.", 
"Teacher repeats student contributions but does not show how ideas/positions relate to each other. OR 1 time, the teacher connects student contributions to each other and shows how ideas/ positions shared during the discussion relate to teach other",
"2 times, the teacher connects student contributions to each other and shows how ideas/ positions shared during the discussion relate to teach other.",
"3+ times, teacher connects student contributions to each other and shows how ideas/ positions shared during the discussion relate to teach other."]

text_s2 = ["Teacher does not ask students to provide evidence for their contributions or explain their reasoning.", 
"Teacher makes superficial or formulaic efforts to ask students to provide evidence for their contributions and/or explain their reasoning. OR 1 time, the teacher asks students to provide evidence for their contributions and/or explain their reasoning.",
"2 times, the teacher asks Ss to provide evidence for their contributions and/or explain their reasoning. ",
"3+ times, the teacher asks students to provide evidence for their contributions and/or to explain their reasoning."]

text_s3 = ["Students do not link to each other’s contributions", 
"Students link contributions to each other in a superficial way, (e.g., ‘I agree with Maria’). OR 1 time, the students connect their contributions to each other and show how ideas/positions shared during the discussion relate to each other.",
"2 times, the students connect their contributions to each other and show how ideas/positions shared during the discussion relate to each other.",
"3+ times, the students connect their contributions to each other and show how ideas/positions shared during the discussion relate to each other."]

text_s4 = ["Students do not support their claims and reasoning with evidence (e.g., provide short 1-2 word responses).", 
"Students provide superficial support for their claims and reasons. OR 1 time, students support their claims and reasoning with specific evidence.",
"2 times, students support their claims and reasoning with specific evidence.",
"3+ times, students support their claims and reasoning with specific evidence."]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['uploaded-file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        # print(file_ext)
        # print(app.config['UPLOAD_EXTENSIONS'])
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        # uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    # iqa_scores = [1, 0, 3, 4]
    my_model = HierarchicalClassification()
    iqa_scores = my_model.run(filename)
    for x in iqa_scores:
        x = str(x)
    
    # return redirect(url_for('show_iqa', iqa_scores))
    mouse_over_text = [text_s1[iqa_scores[0]-1], text_s2[iqa_scores[1]-1], text_s3[iqa_scores[2]-1], text_s4[iqa_scores[3]-1]]
    return render_template('result.html', s = iqa_scores, text_s = mouse_over_text)
    # return render_template('test2.html')
    # dictToSend = {'iqa_scores': iqa_scores}
    # requests.post('http://localhost:5000/show_IQA', json=dictToSend)

