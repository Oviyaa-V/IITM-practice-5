from flask import Flask, request, render_template
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__ , template_folder='template')

@app.route("/", methods=['GET','POST'])
def home():
    if request.method == 'POST':
        l = []
        option = request.form.get('option')
        entered_id = request.form.get('entered_id')

        with open('data.csv') as file:
            file.readline()

            if option == 'student_id':
                if entered_id == "":
                    return render_template('error.html')
                for row in file:
                    row = list(map(int,row.strip().split(",")))
                    if row[0] == int(entered_id):
                        l.append(row)

            elif option == 'course_id':
                if entered_id == "":
                    return render_template('error.html')
                for row in file:
                    row = list(map(int,row.strip().split(",")))
                    if row[1] == int(entered_id):
                        l.append(row)

        if len(l) == 0:
            return render_template('error.html')
        
        elif option == 'student_id':
            total_marks = sum([x[2] for x in l])
            return render_template('students.html', l = l, total = total_marks)
        
        else:
            marks = [x[2] for x in l]
            avg = sum(marks)/len(marks)
            Max = max(marks)
            plt.hist(marks)
            plt.xlabel("marks")
            plt.ylabel("Frequency")
            plt.title("histogram")
            plt.savefig('static/graph.png')

            return render_template('course.html', avg = avg, max = Max, img = 'graph.png')
            
    return render_template('index.html')
    
app.run(debug=True)