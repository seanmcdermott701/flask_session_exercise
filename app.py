from flask import Flask, request, flash, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as sat_surv


app = Flask(__name__)
app.config['SECRET_KEY'] = 'VSECRET'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def get_start_home():
    title = sat_surv.title
    instructions = sat_surv.instructions
    return render_template('base.html', title=title, instructions=instructions)

@app.route('/questions/<id>')
def get_question_page(id):
    id = int(id)

    if (id != len(responses)):
        flash("You're trying to access an invalid question as part of your redirect.")
        return redirect(f'/questions/{len(responses)}')

    if (len(sat_surv.questions) == len(responses)):
        return redirect('/thank_you')

    else:
        question = sat_surv.questions[id].question
        choices = sat_surv.questions[id].choices
        question_id = id
        return render_template('question_page.html', question=question, choices=choices, question_id=question_id)

@app.route('/answer', methods=['POST'])
def post_answer():
    answer = request.form['answers']
    responses.append(answer)
    if len(responses) == len(sat_surv.questions):
        return redirect('/thank_you')

    else:
        return redirect(f'/questions/{len(responses)}')

@app.route('/thank_you')
def get_thankyou():
    return render_template('thank_you.html')