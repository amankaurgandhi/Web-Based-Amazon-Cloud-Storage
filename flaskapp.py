###########Aman Kaur Gandhi
###########1001164326
########### CSE6331-001



import boto3
import botocore
from flask import Flask, render_template, request, url_for, make_response
app = Flask(__name__)
ACCESS_KEY =""
SECRET_KEY =""

s3_client = boto3.client('s3')
s3 = boto3.resource('s3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY)
bucket = s3.Bucket('amankaurbucket')

ALLOWED_IMAGE = set([ 'png', 'jpg', 'jpeg', 'gif']) 


def allowed_image(filename):
    print filename
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE	


@app.route('/login', methods=['GET', 'POST'])
def login():
    username= str(request.form['user'])
    print type(username)
    if bucket.objects.all() and username and username !=  " ":
        print "there are objects on s3"
        objlist= [str(key.key) for key in bucket.objects.all()]
        print objlist   
       
        userlist = [key.get()['Body'].read().split(',') for key in bucket.objects.all() if str(key.key) =="authuser.txt" ] 
           # contenrtype = key.get()['ContentType']
           # print contenrtype
        abc = userlist[0]
        ms =  " ".join(abc)
        print ms
            #userlist = [user for user in userlist]
            #print userlist
        if username in ms:
            return render_template("index.html")
        else:
            return render_template("login.html")
    else:
        return render_template("login.html")
    
@app.route('/')
def index():
    return  render_template("login.html")

@app.route('/listfiles',  methods=['GET', 'POST'])
def listfiles():
    data = []
    for key in bucket.objects.all():
        data.append(key)
    return  render_template("index.html", result = data)
@app.route('/uploadfile', methods=['GET', 'POST'])
def uploadfile():
   
    file = request.files['file']
    if allowed_image(file.filename):
        print "inside allowed"
        data= file.read()
        response = s3_client.put_object(ACL = 'public-read',Body = data,Bucket = 'amankaurbucket',Key=str(file.filename))
    return render_template("index.html")

@app.route('/download/<filename>', methods=['GET', 'POST'])
def download(filename):
    for key in bucket.objects.all():
        if str(key.key) == filename:
            response = make_response(key.get()['Body'].read())
            response.headers["Content-Disposition"] = "attachment; filename="+ filename
    return response


@app.route('/delete/<filename>', methods=['GET', 'POST'])
def delete(filename):
    for key in bucket.objects.all():
        if str(key.key) == filename:
            key.delete()
    return render_template("index.html")
if __name__ == '__main__':
  app.run(host= '0.0.0.0', port = 80)

