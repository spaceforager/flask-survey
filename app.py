from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

RESPONSES_KEY = "responses"

@app.route("/")
def show_home():
    """Shows title, instructions and a button to start the survey"""

    return render_template('root.html', title=survey.title, instructions=survey.instructions)

@app.route("/start", methods=["POST"])
def start_survey():
    session[RESPONSES_KEY] = []
    return redirect('/questions/0')


@app.route("/questions/<int:ques_num>")
def show_question(ques_num):
    """Displays current question"""

    responses = session.get(RESPONSES_KEY)
    if responses is None:
        #redirect to home page
        return redirect('/')
    
    if len(responses) == len(survey.questions):
        #all questions answered. redirect to completion
        return redirect('/complete')
    
    if len(responses) != ques_num:
        #Accessing questions out of order
        flash(f"Invalid question id: {ques_num}")
        return redirect(f'/questions/{len(responses)}')


    question = survey.questions[ques_num]
    return render_template('question.html', qnum=ques_num, question=question)

@app.route('/answer', methods=['POST'])
def handle_response():
    """Handles and saves response and redirects to next question"""

    #gets the response
    choice = request.form['answer']

    # add response to the responses key list 
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses 

    if len(responses) == len(survey.questions):
        #all questions answered. 
        return redirect('/complete')
    else:
        # redirect user to next question
        return redirect(f'/questions/{len(responses)}')

@app.route('/complete')
def show_completed_page():
    """Shows completion page for survey"""
    return render_template('complete.html')

    

    