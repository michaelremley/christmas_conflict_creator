from flask import render_template, request, Response
from app import app
from app.forms import SubmitForm
import app.graph_builder as gb
import app.clique as clq
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = SubmitForm()
    if form.validate_on_submit():
        uploaded_file = request.files['file']
        data = gb.preprocessing(uploaded_file)
        G = gb.build_graph(data)
        print(G.edges)
        print(G.nodes)
        fig = clq.make_seating(G.nodes,G.edges)
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')

    return render_template('submit.html', title='Submit', form=form)
