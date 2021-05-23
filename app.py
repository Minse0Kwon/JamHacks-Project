from random import*
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_session import Session
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
socketio = SocketIO(app, manage_session=False)

def good(text):
    issues = ["depression", "anxiety", "lonely", "fat"]
    tips = [[""]*5]*len(issues)
    #depression-----------------------
    tips[0][0] = "Don’t let life discourage you; everyone who got where he is had to begin where he was."
    tips[0][1] = "There is hope, even when your brain tells you there isn’t."
    tips[0][2] = "Give yourself another day, another chance. You will find your courage eventually. Don’t give up on yourself just yet.”"
    tips[0][3] = "You say you’re ‘depressed’ – all I see is resilience. You are allowed to feel messed up and inside out. It doesn’t mean you’re defective – it just means you’re human."
    tips[0][4] = "Those who have a 'why' to live, can bear with almost any 'how'.”"
    #anxiety-------------------------
    tips[1][0] = "Trust yourself. You’ve survived a lot, and you’ll survive whatever is coming."
    tips[1][1] = "Inner peace begins the moment you choose not to allow another person or event to control your emotions."
    tips[1][2] = "Smile, breathe, and go slowly."
    tips[1][3] = "Life is ten percent what you experience and ninety percent how you respond to it."
    tips[1][4] = "Good humor is a tonic for mind and body. It is the best antidote for anxiety. It attracts and keeps friends. It lightens human burdens. It is the direct route to serenity and contentment."
    #lonely-------------------------
    tips[2][1] = "It’s easy to stand in the crowd but it takes courage to stand alone."
    tips[2][2] = "The woman who follows the crowd will usually go no further than the crowd. The woman who walks alone is likely to find herself in places no one has ever been before."
    tips[2][3] = "Loneliness adds beauty to life. It puts a special burn on sunsets and makes night air smell better."
    tips[2][4] = "Time spent undistracted and alone, in self-examination, journaling, meditation, resolves the unresolved and takes us from mentally fat to fit."
    #fat------------------------------
    tips[3][0] = "Don’t let a stumble in the road be the end of your journey"
    tips[3][1] = "Don’t dig your grave with your own knife and fork"
    tips[3][2] = "When you eat crap, you feel crap"
    tips[3][3] = "When you feel like quitting, think about why you started"
    tips[3][4] = "Every step is progress, no matter how small"

    userIssues = []
    suggestions = []
    for i in range(len(issues)):
        if (issues[i] in text):
            userIssues.append(issues[i])
    print(userIssues)

    for i in range(len(userIssues)):
        for j in range(len(issues)):
            if(userIssues[i] == "depression"):
                suggestions.append(tips[0][randint(0,2)])
            elif(userIssues[i] == "anxiety"):
                suggestions.append(tips[1][randint(0,2)])
            elif(userIssues[i] == "paranoid"):
                suggestions.append(tips[2][randint(0,2)])
            elif(userIssues[i] == "fat"):
                suggestions.append(tips[3][randint(0,2)])

    out = []
    print(str(len(suggestions)))
    for i in range(len(suggestions)):
        if(suggestions[i] not in out):
            print(suggestions[i])
            out.append(suggestions[i])
    


#Home page
@app.route('/', methods=['GET', 'POST'])
def buttons():
    if request.method == 'POST':
        if request.form.get('new') == 'Meet new people!':
            #Go to meet new people section
            return redirect(url_for('index'))

        elif  request.form.get('tips') == 'Tips and tricks':
            #Go to professional help and tips section
            return redirect(url_for('tips'))

    elif request.method == 'POST':
        return render_template('buttons.html', form='form')
    
    return render_template("buttons.html")

#Meet new people --> index.html
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

#Tips and tricks --> tips.html
@app.route('/tips', methods=['GET', 'POST'])
def tips():
    return render_template('tips.html')#--> suggest
    
#Suggest --> suggestions.html
@app.route('/suggest', methods=['GET', 'POST'])
def suggest():

    return render_template('suggestions.html')

#-----------------------Chat room---------------------------#
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if(request.method=='POST'):
        username = request.form['username']
        room = request.form['room']
        session['username'] = username
        session['room'] = room
        return render_template('chat.html', session = session)
    else:
        if(session.get('username') is not None):
            return render_template('chat.html', session = session)
        else:
            return redirect(url_for('index'))

@socketio.on('join', namespace='/chat')
def join(message):
    room = session.get('room')
    join_room(room)
    emit('status', {'msg':  session.get('username') + ' has entered the room.'}, room=room)

@socketio.on('text', namespace='/chat')
def text(message):
    room = session.get('room')
    emit('message', {'msg': session.get('username') + ' : ' + message['msg']}, room=room)

@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    username = session.get('username')
    leave_room(room)
    session.clear()
    emit('status', {'msg': username + ' has left the room.'}, room=room)

if __name__ == '__main__':
    socketio.run(app)