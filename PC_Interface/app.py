from __future__ import absolute_import
from pprint import pprint
import os
from flask import Flask, render_template, request, session, abort, flash, url_for, send_file
from detect_intent_texts import detect_intent_texts, line_manipulator
from read_attributes import get_columns, get_file_name
from werkzeug.utils import secure_filename, redirect
from API_manager import enter_new_entity
import DB_Manager
import Similarity
from entities import create_attribute_dict
app = Flask(__name__)

app.secret_key = "AS9UjjJI0J0JS9j"

PROJECT_ID = os.getenv('GCLOUD_PROJECT')
SESSION_ID = 'session_pc'
UPLOAD_FOLDER = '/media/arshad/Data/FYP/FYP/UserSpecs2PseudoCode/PC_Interface/Resources'
ALLOWED_EXTENSIONS = {'csv', 'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
url_ds_attributes = 'https://api.dialogflow.com/v1/entities/ds_attributes'
url_ds_name = 'https://api.dialogflow.com/v1/entities/Dataset_Name'
data_set_name = ''


@app.route('/payload', methods=['POST'])
def payload():
    if not request.json:
        abort(400)
    if request.json:
        response = request.json
        pprint(response)

    try:
        content = request.json['queryResult']
        print("_" * 20)
        pprint(content)

    except:
        print("JSON not found")

    return 'none'


@app.route('/send_message', methods=['POST'])
def send_message():
    message = "Hi, Name please"
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
    response_text = {"message": fulfillment_text}
    print(response_text)


@app.route('/')
def home():
    return render_template('home.html')


@app.route("/find/<string:name>/")
def hello(name):
    return render_template('found_wim_phone.html', name=name)


@app.route('/home', methods=['GET'])
def search():
    try:
        phone_price = request.form['price']

        users = findUsersByPrice(phone_price)
        return render_template('home.html', ph_price=phone_price, users_list=users)
    except:
        return render_template('home.html')


@app.route('/pc', methods=['GET'])
def receive_pseudo_code():
    try:
        pseudocode = request.form['pcode']
        lines_raw = pseudocode.split('\n')
        lines = []
        for l in lines_raw:
            if l is not '' and l is not '\r':
                lines.append(l)
        DB_Manager.insert_pseudocode_into_db(lines)
        return render_template('result1.html', statements=lines)
    except:
        return render_template('input_form1.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/ds', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            global data_set_name
            data_set_name = filename
            create_attribute_dict.find_filename(data_set_name)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            columns = get_columns(UPLOAD_FOLDER + '/' + filename)
            file_names = get_file_name(filename)
            enter_new_entity(file_names, url_ds_name, 'Dataset_Name')
            enter_new_entity(columns, url_ds_attributes, 'ds_attributes')
            return render_template('pseudocode_input.html', filename=filename)
            # return redirect(url_for('uploaded_file',
            #                         filename=filename))
    return render_template('input_form1.html')


@app.route('/intermediate', methods=['GET', 'POST'])
def generate_intermediate_code():
    lines = DB_Manager.get_pseudocode_from_db()[0]
    # full_pc = ""
    full_pc = line_manipulator(lines, data_set_name)
    # for line in lines:
    #     pc = detect_intent_texts(PROJECT_ID, SESSION_ID, line, 'en-US')
    #     full_pc = full_pc + '\n' + pc

    print(str(full_pc[0])+'\n')
    f = open("ipc.txt", "w+")
    f.write(str(full_pc[0])+'\n')
    f.close()
    os.system('python3 featureEngineering.py')
    os.system('python3 Translate.py')
    DB_Manager.insert_standard_pc_into_db(full_pc[1])
    DB_Manager.delete_all_documents("pseudocodes_temp")
    return render_template('result2.html', statements=full_pc[1])


@app.route('/pc_my', methods=['GET'])
def view_my_pc():
    try:
        lines = DB_Manager.get_pseudocode_from_db_temp2()[0]

        return render_template('result1.html', statements=lines)
    except:
        return render_template('notfound.html')


@app.route('/pc_in', methods=['GET'])
def view_pc_in():
    try:
        lines = DB_Manager.get_pseudocode_from_db_out()[0]
        DB_Manager.delete_all_documents("Output2")

        return render_template('result2.html', statements=lines)
    except:
        return render_template('notfound.html')


@app.route('/scp', methods=['GET'])
def generate_source_code_p():
    try:
        source_p = open(
            '/media/arshad/Data/FYP/FYP/UserSpecs2PseudoCode/PC_Interface/translations/ipcPythonClean.py')
        pcode = [line for line in source_p.readlines() if line.strip()]

        # print(pcode)

        return render_template('result4.html', statements=pcode)
    except:
        return render_template('notfound.html')


@app.route('/scr', methods=['GET'])
def generate_source_code_r():
    try:
        source_r = open(
            '/media/arshad/Data/FYP/FYP/UserSpecs2PseudoCode/PC_Interface/translations/ipcRClean.py')
        rcode = [line for line in source_r.readlines() if line.strip()]

        # print(rcode)

        return render_template('result5.html', statements=rcode)
    except:
        return render_template('notfound.html')


@app.route('/evlHome', methods=['GET'])
def evlHome():
    match_df,line1,line2,libaryName1,libaryName2,RalgoArr,SKalgoArr = Similarity.match()
    RalgoArr = list(RalgoArr["algorithm"].values)
    SKalgoArr = list(SKalgoArr["algorithm"].values)
    return render_template('result3.html', match_df=match_df.to_html(),line1 = line1,line2=line2,libaryName1=libaryName1,libaryName2=libaryName2,RalgoArr=RalgoArr,SKalgoArr=SKalgoArr,algoName1=Similarity.algoName1,algoName2=Similarity.algoName2,lang1=Similarity.lang1,lang2=Similarity.lang2)


@app.route('/evl', methods=['GET'])
def evaluate_results():
    Similarity.algoName1 = request.form['select1']
    Similarity.algoName2 = request.form['select2']
    Similarity.lang1 = request.form['selectLan1']
    Similarity.lang2 = request.form['selectLan2']
    match_df,line1,line2,libaryName1,libaryName2,RalgoArr,SKalgoArr = Similarity.match()
    RalgoArr = list(RalgoArr["algorithm"].values)
    SKalgoArr = list(SKalgoArr["algorithm"].values)
    return render_template('result3.html', match_df=match_df.to_html(),line1 = line1,line2=line2,libaryName1=libaryName1,libaryName2=libaryName2,RalgoArr=RalgoArr,SKalgoArr=SKalgoArr,algoName1=Similarity.algoName1,algoName2=Similarity.algoName2,lang1=Similarity.lang1,lang2=Similarity.lang2)


@app.route('/about', methods=['GET'])
def about():
    try:
        user_name = request.form['username']
        brand_name = request.form['brandname']
        os = request.form['os']

        return render_template('result4.html', name=user_name)
    except:
        return render_template('input_form4.html')


app.add_url_rule('/pc', 'pc', receive_pseudo_code, methods=['GET', 'POST'])
app.add_url_rule('/pc_my', 'pc_my', view_my_pc, methods=['GET', 'POST'])
app.add_url_rule('/pc_in', 'pc_in', view_pc_in, methods=['GET', 'POST'])
app.add_url_rule('/ds', 'ds', upload_file, methods=['GET', 'POST'])
app.add_url_rule('/intermediate', 'intermediate', generate_intermediate_code, methods=['GET', 'POST'])
app.add_url_rule('/sc', 'sc', generate_source_code_p, methods=['GET', 'POST'])
app.add_url_rule('/scp', 'scp', generate_source_code_r, methods=['GET', 'POST'])
app.add_url_rule('/evlHome', 'evlHome', evlHome, methods=['GET', 'POST'])
app.add_url_rule('/evl', 'evl', evaluate_results, methods=['GET', 'POST'])
app.add_url_rule('/about', 'about', about, methods=['GET', 'POST'])

if __name__ == "__main__":
    app.run(host='localhost', port=3550, debug=True)
