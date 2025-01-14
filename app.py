from flask import Flask,jsonify, render_template, request, redirect, url_for, session, send_from_directory,Response,make_response,send_file
import hashlib
from werkzeug.utils import secure_filename 
import pymysql
import pymysql.cursors
import os
import jwt
import json
import psycopg2
import datetime
from PIL import Image
from tinytag import TinyTag
from io import BytesIO
import base64
from mutagen import mp3, id3, wave
import cv2 as cv2
import numpy as np
import time

app = Flask(__name__)
# app.config['SECRET_KEY']='18062b41611b47c0cfbf45a191a875d0'
app.config['SECRET_KEY']=os.environ.get('SECRET_KE')


def get_upload_connection():
    try:
        # Code to establish database connection
        # connection = pymysql.connect(
        #     host='localhost',
        #     user='root',
        #     password='password',
        #     database='beyond_infinity_db',
        #     cursorclass=pymysql.cursors.DictCursor
        # )
        
        connection = psycopg2.connect(
            os.environ["DATABASE_URL"],
            sslmode='verify-full',
            sslrootcert='root.crt'
        )
        # Return the connection object
        return connection
    except psycopg2.Error as e:
        # Handle connection error
        print("Error connecting to MySQL database:", e)
        return None

def close_connection(connection):
    if connection is not None:
        connection.close()
                
token=''

# def generate_token(user_id):
#     payload = {
#         'user_id': user_id,
#         'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
#     }
#     global token
#     token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

# def generate_token(user_id):
#     print("Generating token for user:", user_id)
#     try:
#         payload = {
#         'user_id': user_id,
#         'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
#         }
#         global token
#         token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
#         print("Token generated successfully:", token)
#     except:
#         print("Error generating token")

def generate_token(user_id):
    global token  # Access the global token variable
    try:
        payload = {
            'user_id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        secret_key = os.environ.get('SECRET_KE')
        if not secret_key:
            raise ValueError("SECRET_KEY environment variable is not set.")
        
        token = jwt.encode(payload, secret_key, algorithm='HS256')
    except Exception as e:
        print("Error generating token:", e)

def getuserid():
    try:
        global token        
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        print(data)
        user_id = data['user_id']
        print(user_id)
        return user_id
    except:
        return None

@app.route('/')
def home():
    curuser = getuserid()
    if curuser:
        return redirect("/profile")
    else:
        return render_template('index.html')

@app.route('/login',methods = ['GET','POST'])
def login():
    curuser = getuserid()
    if curuser:
        return redirect("/profile")

    if(request.method == 'POST'):

        username = request.form['login-username']
        entered_password = hashlib.sha256((request.form['login-password']).encode()).hexdigest()

        if username == "admin" and request.form['login-password'] == "adminpassword":
            print("at admin login")
            generate_token(-1)
            return redirect("/admin")
        else:
            upload_connection=get_upload_connection()
            try:
                with upload_connection.cursor() as cursor:
                    print("at line 96")
                    sql = "SELECT * FROM user_details WHERE username = %s"
                    cursor.execute(sql, (username,))
                    print("at line 99")
                    result = cursor.fetchone()
                    print(result)
                    print(result[4])
                    print(entered_password)
                    print("at line 100")
                    
                    if result[4] == entered_password:
                        print("Passwords match")
                        generate_token(result[0])     
                        close_connection(upload_connection) 
                        print("redirecting to profile")
                        return redirect("/profile")
                    else:
                        close_connection(upload_connection)
                        print("at line 109")
                        return render_template('login_page.html')
            except:
                close_connection(upload_connection)
                print("at line 114")
                return render_template('login_page.html')
    else:
        print("at line 117")
        return render_template('login_page.html')
        

@app.route('/signup',methods=['GET','POST'])
def signup():
    cur_user = getuserid()
    if cur_user:
        return redirect("/profile")

    if(request.method == 'POST'):

        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password =hashlib.sha256((request.form['password']).encode()).hexdigest()

        try:
            upload_connection=get_upload_connection()
            with upload_connection.cursor() as cursor:
                sql = "INSERT INTO user_details (name, username, user_email, hash_password) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (name, username, email, password))
                upload_connection.commit()
                close_connection(upload_connection)
            return redirect("/login")
        except:
            return render_template('signup_page.html')
    else:
        return render_template('signup_page.html')

@app.route('/upload',methods=['GET','POST'])
def upload():
    curuser = getuserid()
    if curuser == -1:
        return redirect("/admin")

    if request.method == 'POST':
        upload_connection=get_upload_connection()
        if 'image' in request.files:
            images = request.files.getlist('image')

            for i in range(len(images)):
                image = images[i]
                
                curstring = "select-image-"
                curstring += str(i)
                save = request.form.get(curstring)

                if save == "select":
                    try:
                        user_id = getuserid()
                        image_blob =image.read()
                        
                        filename=secure_filename(image.filename)

                        if not filename:
                            continue

                        _, file_extension = os.path.splitext(filename)
                        with Image.open(image) as img:
                            width, height = img.size

                        with upload_connection.cursor() as cursor:
                            cursor.execute("INSERT INTO images (user_id, Image, filename, filetype, height, width) VALUES (%s, %s, %s, %s, %s, %s)", (user_id, image_blob, filename, file_extension, height, width))
                            upload_connection.commit()
                    except:
                        continue

        if 'audio' in request.files:

            audios = request.files.getlist('audio')

            for i in range(len(audios)):
                
                audio = audios[i]

                curstring = "select-audio-"
                curstring += str(i)
                save = request.form.get(curstring)

                if save == "select":
                    try:      
                        user_id = getuserid()
                        audio_blob = BytesIO(audio.read())
                        audio_filename = secure_filename(audio.filename)

                        if not audio_filename:
                            continue

                        with upload_connection.cursor() as cursor:
                            cursor.execute("INSERT INTO audios (user_id, audio, audio_filename,created_at) VALUES (%s, %s, %s, %s)",(user_id, audio_blob.getvalue(), audio_filename, datetime.datetime.now()))
                            upload_connection.commit()
                    except:
                        continue
        close_connection(upload_connection)
        return redirect("/profile")
    else:
        return render_template('upload_page.html')
   

@app.route('/profile')
def profile():

    userid = getuserid()
    print(userid)

    if userid == -1:
        return redirect("/admin")

    if userid:
        upload_connection=get_upload_connection()
        username = ""

        cursor = upload_connection.cursor()
        print("at line 229")
        cursor.execute("SELECT * FROM user_details WHERE user_id=%s",[userid])
        print("at line 232")
        result = cursor.fetchone()
        print("at line 233")
        username = result[1]
        name=result[2]
        email=result[3]
        print("email: ", email)
        imagelist = []

        cursor = upload_connection.cursor()
        cursor.execute("SELECT Image,filename FROM images WHERE user_id=%s",[userid])
        result = cursor.fetchall()
        print("at line 243")

        for image in result:
            image_data = base64.b64encode(image[0]).decode('utf-8')
            filename = image[1]
            imagelist.append((image_data, filename))

        
        imagelist_length = len(imagelist)
        audiolist = []

        cursor = upload_connection.cursor()
        cursor.execute("SELECT audio,audio_filename FROM audios WHERE user_id=%s",[userid])
        result = cursor.fetchall()

        for audi in result:
            audio_data = base64.b64encode(audi[0]).decode('utf-8')
            audio_filename = audi[1]
            audiolist.append((audio_data, audio_filename))

        close_connection(upload_connection)
        print("going to  home page")
        return render_template('home_page.html',images=imagelist, username = username,userid=userid,name=name,audios=audiolist,email=email)  
    else:
        return redirect("/login")
 
@app.route('/admin')
def admin():
    curuserid = getuserid()
    if curuserid != -1:
        return redirect("/profile")
    else:
        upload_connection=get_upload_connection()

        cursor = upload_connection.cursor()
        cursor.execute("SELECT * FROM user_details")
        result = cursor.fetchall()

        allusers = []

        for user in result:
            curdict = {}
            curdict['userid'] = user[0]
            curdict['name'] = user[2]
            curdict['email'] = user[3]
            curdict['username'] = user[1]
            allusers.append(curdict)

        close_connection(upload_connection)
        return render_template('admin_page.html',users=allusers,count=len(allusers))

@app.route('/logout')
def logout():
    global token
    token = None
    return redirect("/")

@app.route('/create' , methods=['GET', 'POST'])
def create():
    userid = getuserid()

    if userid == -1:
        return redirect("/admin")

    elif userid:
        upload_connection=get_upload_connection()
        imagelist = []

        cursor = upload_connection.cursor()
        cursor.execute("SELECT Image,filename FROM images WHERE user_id=%s", [userid])
        result = cursor.fetchall()

        for image in result:
            image_data = base64.b64encode(image[0]).decode('utf-8')
            filename = image[1]
            imagelist.append((image_data, filename))

        audiolist = []

        cursor = upload_connection.cursor()
        cursor.execute("SELECT audio, audio_filename FROM audios WHERE user_id=%s", [userid])
        result = cursor.fetchall()
        print(result)
        for audi in result:
            audio_data = base64.b64encode(audi[0]).decode('utf-8')
            audio_filename = audi[1]
            audiolist.append((audio_data, audio_filename))
        # print(audiolist[0])
        cursor = upload_connection.cursor()
        cursor.execute("SELECT username FROM user_details WHERE user_id=%s", [userid])
        data = cursor.fetchall()
        username = data[0][0]

        close_connection(upload_connection)
        timestamp = int(time.time())

        video_path=f"/videos/{username}_slideshow_video.mp4?version={timestamp}"
        print(video_path)

        response = make_response(render_template('create_page.html', images=imagelist, audios=audiolist, video_path=video_path))
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return response
    else:
        return redirect("/login")
    


from flask import Flask, request, redirect, render_template
from moviepy.editor import *
from moviepy.video.VideoClip import ColorClip
import numpy as np
import cv2
from moviepy.video.fx import fadein, fadeout

DEFAULT_DURATION = 5
DEFAULT_TRANSITION = 'None'

def slide_in(clip, duration):
    # Define the animation function
    def anim(clip, t):
        return clip.set_position(("left", clip.screen[1]/2)).fx(afx.slide_in, t)

    # Apply the animation function over the duration
    return clip.fl(anim, duration)

def fit_image_into_box(image, output_width, output_height):
    original_height, original_width = image.shape[:2]
    original_aspect_ratio = original_width / float(original_height)

    output_aspect_ratio = output_width / float(output_height)
    if original_aspect_ratio > output_aspect_ratio:
        scale_factor = output_width / float(original_width)
        new_height = int(original_height * scale_factor)
        new_width = output_width
    else:
        scale_factor = output_height / float(original_height)
        new_width = int(original_width * scale_factor)
        new_height = output_height

    resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
    black_canvas = np.zeros((output_height, output_width, 3), dtype=np.uint8)
    x_offset = (output_width - new_width) // 2
    y_offset = (output_height - new_height) // 2
    black_canvas[y_offset:y_offset+new_height, x_offset:x_offset+new_width] = resized_image

    return black_canvas


@app.route('/create_video', methods=['POST', 'GET'])
def create_video():
    userid = getuserid()

    if userid == -1:
        return redirect("/admin")
    elif userid:
        if request.method == 'POST':
            upload_connection = get_upload_connection()
            cursor = upload_connection.cursor()
            cursor.execute("SELECT Image FROM images WHERE user_id=%s", [userid])
            images = cursor.fetchall()
            if not images: 
                return "No images found for the user."

            durations = []
            transitions = []

            # Extract image data, durations, and transitions from the request JSON
            request_data = request.json
            for imageData in request_data.get('imageData', []):
                duration_value = int(imageData.get('duration')) if imageData.get('duration') is not None else DEFAULT_DURATION
                transition = imageData.get('effect') if imageData.get('effect') is not None else DEFAULT_TRANSITION
                durations.append(duration_value)
                transitions.append(transition)
            
            print("Durations:", durations)
            print("Transitions:", transitions)
            # Create a list to hold the resized images
            image_list = []
            
            # Define the output width and height
            resolution = request_data.get('resolution', '720')
            if resolution == '720':
                bitrate = '200K' 
            elif resolution == '1080':
                bitrate = '200K' 
            elif resolution == '360':
                bitrate = '200K'
            elif resolution == '480':
                bitrate = '200K'  
            
            dimension = request_data.get('dimension', '16:9')
            if dimension == '16:9':
                output_width = 1280
                output_height = 720
            elif dimension == '4:3':
                output_width = 1024
                output_height = 768
            # Iterate through each image data

            for image_data in images:
                image_np = np.frombuffer(image_data[0], np.uint8)
                img = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                fitted_image = fit_image_into_box(img_rgb, output_width, output_height)
                image_list.append(fitted_image)

            clips = [ImageClip(img, duration=duration) for img, duration in zip(image_list, durations)]

            processed_clips = []
            # Iterate through the clips
            for i, clip in enumerate(clips):
                clip_with_transition = clip
                # Add a FadeIn effect to the clip
                if i < len(clips):  # Add FadeIn to all clips except the last one
                    if(transitions[i] == 'FadeIn'):
                        clip_with_transition = fadein.fadein(clip, 0.5, initial_color=[0, 0, 0])
                    elif transitions[i] == 'FadeOut':
                        clip_with_transition = fadeout.fadeout(clip, 0.5, final_color=[0, 0, 0])
                    elif transitions[i] == 'FadeIn & FadeOut':
                        duration=clip.duration
                        if(duration>1):
                            clip_with_transition = fadein.fadein(clip, 0.5, initial_color=[0, 0, 0])
                            clip_with_transition = fadeout.fadeout(clip_with_transition, 0.5, final_color=[0, 0, 0])
                        else:
                            clip_with_transition = fadein.fadein(clip, duration/2, initial_color=[0, 0, 0])
                            clip_with_transition = fadeout.fadeout(clip_with_transition, duration/2, final_color=[0, 0, 0])

                    elif transitions[i] == 'None':
                        clip_with_transition = clip
                    else:
                        clip_with_transition = clip

                processed_clips.append(clip_with_transition)
            # processed_clips = [demo_clip.crossfadein(2) for demo_clip in clips]

            # Concatenate the processed clips into a single video
            final_clip = concatenate_videoclips(processed_clips)
            
            cursor.execute("SELECT username FROM user_details WHERE user_id=%s", [userid])
            data = cursor.fetchall()
            username = data[0][0]
            output_video_path = f'videos/{username}_slideshow_video.mp4'

            # final_clip = concatenate_videoclips(clips_with_transitions, method="compose")
            
            # final_audio_clip = AudioFileClip("static/media/audios/Indie Corporate.mp3").set_duration(final_clip.duration)
            cursor.execute("SELECT audio FROM audios WHERE user_id=%s", [userid])
            audios = cursor.fetchall()
            # printing filename of audio
            print(audios)
            database_audios=[file[0] for file in audios]

            durations_audio = []
            for audioData in request_data.get('audioData', []):
                audio_duration = audioData.get('duration', 0)
                if audio_duration is None:
                    audio_duration = 0
                durations_audio.append(audio_duration)

            print("Audio Durations:", durations_audio)
            audio_clips = []
            
            audio_clips = [
                AudioFileClip('static/media/audios/Idea 22 (Sped Up).mp3'),
                AudioFileClip('static/media/audios/My_Way.mp3'),
                AudioFileClip('static/media/audios/Indie Corporate.mp3'),
            ]
            for i,audio_blob in enumerate(database_audios):
                audio_file=f"audio_{i}.mp3"
                with open(audio_file, 'wb') as file:
                    file.write(audio_blob)
                audio_clip = AudioFileClip(audio_file)
                audio_clips.append(audio_clip)


            print("Durations_audio:",durations_audio)
            audio_clips = [clip.set_duration(duration) for clip, duration in zip(audio_clips, durations_audio)]
            print("Audio_clips:",audio_clips)
            # Create a final audio clip by concatenating the audio clips and set duration for each from the durations_audio list
            final_audio_clip = concatenate_audioclips(audio_clips)

            final_audio_clip = final_audio_clip.set_duration(final_clip.duration)
            if(final_clip.duration > 5):
                final_audio_clip = final_audio_clip.fx(afx.audio_fadein ,3).fx(afx.audio_fadeout, 3)
            else:
                final_audio_clip = final_audio_clip.fx(afx.audio_fadein ,final_clip.duration/3).fx(afx.audio_fadeout, final_clip.duration/3)
            video_with_audio = final_clip.set_audio(final_audio_clip)
            video_with_audio.write_videofile(output_video_path, codec="libx264", fps=15, preset='medium', bitrate=bitrate, ffmpeg_params=['-pix_fmt', 'yuv420p'])

            print("Video saved at:", output_video_path) 
            close_connection(upload_connection)

            return render_template('create_page.html')
        else:
            return redirect('/create')
    else:
        return redirect("/login")


@app.route('/videos/<path:filename>')
def media_files(filename):
    response = send_from_directory('videos', filename)
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

if __name__ == '__main__':
    app.run(debug=True)
