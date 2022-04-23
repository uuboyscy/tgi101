from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
import sys
sys.path.append("./testFolder")
from testFolder import poker as p
from model import model

app = Flask(__name__, static_url_path="/photo", static_folder="./photo")


@app.route("/")
def test():
    return "<h1>Hello Flask!</h1><br>123123123321321321"


# @app.route("/hello/<username>")
# def hello(username):
#     output = "<h1>Hello {}!</h1>".format(username)
#     print(username)
#     return output


@app.route("/hello/<username>")
def hello(username):
    output = "<h1>Hello {}!</h1>".format(username)
    print(username)
    return render_template(
        "hello.html",
        username=username
    )


@app.route("/addTowNumber/<x>/<y>")
def addTwoNumber(x, y):
    return str(int(x) + int(y))


@app.route("/get_student/<classNumber>")
def getStudent(classNumber):
    sql = """
        SELECT student_no, class_number, name 
        FROM students
        WHERE class_number = 'tgi101';
        """
    # outputData = getStudentFromDB()
    return "outputData"

# http://127.0.0.1:5001/hello_get?name=Allen&age=22
@app.route("/hello_get")
def hello_get():
    name = request.args.get("name")
    age = request.args.get("age")

    if name == None:
        htmlStr = """
        What's your name?
        """
    elif age == None:
        htmlStr = """
        <h1>
            Hello {}.
        </h1>
        """
    else:
        htmlStr = """
        <h1>
            Hello {}, you are {} years old.
        </h1>
        """
    return htmlStr.format(name, age)


@app.route("/hello_post", methods=["GET", "POST"])
def hello_post():
    method = request.method
    htmlStr = """
    <form action="/hello_post" method="POST">
        <label>What's your name?</label>
        <input name="username">
        <button type="submit">SUBMIT</button>
    </form>
    """

    if method == "POST":
        username = request.form.get("username")
        htmlStr += """
        <h1>Hello {}!</h1>
        """.format(username)

    return htmlStr

@app.route("/hello_post2", methods=["GET", "POST"])
def hello_post2():
    method = request.method
    username = "" if method == "GET" else request.form.get("username")
    return render_template("hello_post.html", method=method, username=username)

# /pokers?players=5
@app.route("/pokers")
def pokers():
    players = int(request.args.get("players"))
    result = p.poker(players)
    return jsonify(result)


@app.route('/poker', methods=['GET', 'POST'])
def poker():
    request_method = request.method
    players = 0
    cards = dict()
    if request_method == 'POST':
        players = int(request.form.get('players'))
        cards = p.poker(players)
    return render_template('poker.html', request_method=request_method,
                                         cards=cards)


@app.route("/getimage")
def getimage():
    return """hcljvcklzjvclx;<img src="/static/google.png">"""


@app.route('/show_staff')
def hello_google():
    staff_data = model.getStaff()
    column = ['ID', 'Name', 'DeptId', 'Age', 'Gender', 'Salary']
    return render_template('show_staff.html', staff_data=staff_data,
                                              column=column)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)

