from flask import Flask, render_template, request, url_for
import pandas as pd
import numpy as np
import os






app = Flask(__name__)

num_scen = 0
li_cyc = 0
in_r = 0
a = 0
t = 0
@app.route('/')
def main():
    return render_template('index.html')





@app.route('/upload', methods=['GET','POST'])
def upload_file():

    if request.method == 'POST':
        file = request.files["file"]
        df = pd.read_excel(file, index_col=0)
        del df.index.name

        metal = 0
        brick = 0
        concrete = 0
        g = 0
        if 'Metal' in list(df.index):
            metal += df.loc['Metal'] * 5436
        if 'Concrete' in list(df.index):
            concrete += df.loc['Concrete'] * 6450
        if 'Brick' in list(df.index):
            brick += df.loc['Brick'] * 3488
        if 'g' in list(df.index):
            g += df.loc['g'] * 200

        resg = metal + concrete + brick + g

        global a
        a += resg[0]
        #file.save(os.path.join("uploads", file.filename))
        return render_template('upload.html',message="Success!", resg=resg[0])
    return render_template('upload.html')


@app.route('/scenario', methods=['GET','POST'])
def scen():

        if request.method == 'POST':
            num_of_scenarios = int(request.form['num_of_scenarios'])
            life_cycle = int(request.form['life_cycle'])
            int_rate = float(request.form['int_rate'])

            global num_scen, li_cyc, in_r
            num_scen = num_of_scenarios
            li_cyc = life_cycle
            in_r = int_rate

            return render_template('scen2.html', ind = num_scen)
        return render_template('scenario.html')


@app.route('/optimizer', methods=['GET','POST'])
def fin_cal():
    s = {}
    
    if request.method == 'POST':
        for i in range(num_scen):
            npv = (float(request.form[f'ann{i+1}']) / ((1+ in_r)**li_cyc))
            nn = npv + float(request.form[f'emb{i+1}'])
            s[i]=nn

        key_min = min(s.keys(), key=(lambda k: s[k]))
        min_tuple = (key_min, s[key_min])

        min_val = min_tuple[1]
        min_key = min_tuple[0]+1

        return render_template('scen2.html', min_val = min_val,
                                min_key = min_key , ind = num_scen)

    return render_template('scen2.html', ind = num_scen)






if __name__ == ' __main__':
    app.debug = True
    app.run()
