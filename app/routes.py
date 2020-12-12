from flask import render_template, request, Response
from app import app
from app.forms import SubmitForm
import app.graph_builder as gb
import app.clique as clq

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/sources')
def sources():
    return render_template("sources.html")

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = SubmitForm()
    if form.validate_on_submit():
        uploaded_file = request.files['file'] # Get csv from request
        data = gb.preprocessing(uploaded_file) # Turn survey responses into graph
        agreement_graph = gb.build_graph(data)
        image = clq.make_seating(agreement_graph,form.chaotic.data) # Create the seating arrangement
        return render_template('result.html', title='Result', image=image, chaotic=form.chaotic.data)

    return render_template('submit.html', title='Submit', form=form)
