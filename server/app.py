from flask import Flask, render_template, Response, jsonify, request, session, redirect, url_for, send_file

# FlaskForm = used for file input forms
import csv
from io import StringIO
from flask_wtf import FlaskForm

from wtforms import FileField, SubmitField, StringField, DecimalRangeField, IntegerRangeField, IntegerField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired, NumberRange
import os

from PIL import Image, ImageDraw, ImageFont
import requests
import io

from math import floor
from bson.json_util import dumps

from datetime import datetime

import json
import cv2

# YOLO_Video is the python file which contains the code for our object detection model
# Video Detection is the Function which performs Object Detection on Input Video
from detection import video_detection, get_one_frame, update_lines, update_datetime, update_address
from db_connection import find_traffic_data

app = Flask(__name__)

app.config['SECRET_KEY'] = 'tofuhermit'
app.config['UPLOAD_FOLDER'] = 'static/files'

# Use FlaskForm to get input video file  from user
class UploadFileForm(FlaskForm):
    # We store the uploaded video file path in the FileField in the variable file
    # We have added validators to make sure the user inputs the video in the valid format  and user does upload the
    # video when prompted to do so
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Run")

def generate_frames(path_x=''):
    yolo_output = video_detection(path_x)
    for detection_ in yolo_output:
        ref, buffer = cv2.imencode('.jpg', detection_)

        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def generate_frames_web(path_x):
    yolo_output = video_detection(path_x)
    for detection_ in yolo_output:
        ref, buffer = cv2.imencode('.jpg', detection_)

        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/oneframe')
def oneframe():
    return Response(generate_one_frame(path_x=session.get('video_path', None)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def generate_one_frame(path_x):
    output_ = get_one_frame(path_x)
    ref, buffer = cv2.imencode('.jpg', output_)
    frame = buffer.tobytes()
    return (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
@app.route('/home')
def home():
    session.clear()
    return render_template('index.html')


@app.route('/show')
def show_all():
    return

@app.route('/explorer')
def explorer():
    return render_template('explorer.html')

@app.route('/canvas', methods=['GET', 'POST'])
def canvas():
    print(request.method)
    if request.method == 'POST':
        # slider1_value = request.form['slider1']
        # slider2_value = request.form['slider2']
        # slider3_value = request.form['slider3']
        # slider4_value = request.form['slider4']
        slider1_value = 0
        slider2_value = 0
        slider3_value = 0
        slider4_value = 0
        slider5_value = request.form['slider5']
        slider6_value = request.form['slider6']
        slider7_value = request.form['slider7']
        slider8_value = request.form['slider8']

        image_width = request.form['imgwidth']
        image_height = request.form['imgheight']

        canvas_width = request.form['canvaswidth']
        canvas_height = request.form['canvasheight']

        date = request.form['date']
        time = request.form['time']
        address = request.form['address']

        scale_x = float(image_width) / float(canvas_width)
        scale_y = float(image_height) / float(canvas_height)

        print('Image width: ', image_width)
        print('Image height: ', image_height)
        print('Canvas width: ', canvas_width)
        print('Canvas height: ', canvas_height)

        slider1_value = floor(int(slider1_value) * scale_x)
        slider2_value = floor(int(slider2_value) * scale_y)

        slider3_value = floor(int(slider3_value) * scale_x)
        slider4_value = floor(int(slider4_value) * scale_y)

        slider5_value = floor(int(slider5_value) * scale_x)
        slider6_value = floor(int(slider6_value) * scale_y)

        slider7_value = floor(int(slider7_value) * scale_x)
        slider8_value = floor(int(slider8_value) * scale_y)

        print('Slider 1 X:', slider1_value)
        print('Slider 1 Y:', slider2_value)
        print('Slider 2 X:', slider3_value)
        print('Slider 2 Y:', slider4_value)
        print('Slider 3 X:', slider5_value)
        print('Slider 3 Y:', slider6_value)
        print('Slider 4 X:', slider7_value)
        print('Slider 4 Y:', slider8_value)

        s1 = (int(slider1_value), int(slider2_value))
        s2 = (int(slider3_value), int(slider4_value))
        e1 = (int(slider5_value), int(slider6_value))
        e2 = (int(slider7_value), int(slider8_value))
        # include the values in detection.py for detection. define a function first to add the line values before
        update_lines(s1, s2, e1, e2)
        update_datetime(date, time)
        update_address(address)
        # generating the frames
        # redirect to videoplaying.html
        return render_template('videoplaying.html')
    return render_template('canvas.html')


# Rendering the Webcam Page
@app.route('/live', methods=['GET', 'POST'])
def live():
    return redirect(url_for('canvaslive'))


@app.route('/canvaslive', methods=['GET', 'POST'])
def canvaslive():
    print(request.method)
    if request.method == 'POST':
        # slider1_value = request.form['slider1']
        # slider2_value = request.form['slider2']
        # slider3_value = request.form['slider3']
        # slider4_value = request.form['slider4']
        slider1_value = 0
        slider2_value = 0
        slider3_value = 0
        slider4_value = 0
        slider5_value = request.form['slider5']
        slider6_value = request.form['slider6']
        slider7_value = request.form['slider7']
        slider8_value = request.form['slider8']

        image_width = request.form['imgwidth']
        image_height = request.form['imgheight']

        canvas_width = request.form['canvaswidth']
        canvas_height = request.form['canvasheight']

        date = datetime.today().strftime('%Y-%m-%d')
        time = datetime.now().strftime("%H:%M")
        address = request.form['address']

        scale_x = float(image_width) / float(canvas_width)
        scale_y = float(image_height) / float(canvas_height)

        print('Image width: ', image_width)
        print('Image height: ', image_height)
        print('Canvas width: ', canvas_width)
        print('Canvas height: ', canvas_height)

        slider1_value = floor(int(slider1_value) * scale_x)
        slider2_value = floor(int(slider2_value) * scale_y)

        slider3_value = floor(int(slider3_value) * scale_x)
        slider4_value = floor(int(slider4_value) * scale_y)

        slider5_value = floor(int(slider5_value) * scale_x)
        slider6_value = floor(int(slider6_value) * scale_y)

        slider7_value = floor(int(slider7_value) * scale_x)
        slider8_value = floor(int(slider8_value) * scale_y)

        print('Slider 1 X:', slider1_value)
        print('Slider 1 Y:', slider2_value)
        print('Slider 2 X:', slider3_value)
        print('Slider 2 Y:', slider4_value)
        print('Slider 3 X:', slider5_value)
        print('Slider 3 Y:', slider6_value)
        print('Slider 4 X:', slider7_value)
        print('Slider 4 Y:', slider8_value)

        s1 = (int(slider1_value), int(slider2_value))
        s2 = (int(slider3_value), int(slider4_value))
        e1 = (int(slider5_value), int(slider6_value))
        e2 = (int(slider7_value), int(slider8_value))
        # include the values in detection.py for detection. define a function first to add the line values before
        update_lines(s1, s2, e1, e2)
        update_datetime(date, time)
        update_address(address)
        # generating the frames
        # redirect to videoplaying.html
        return render_template('live.html')
    return render_template('canvastemp.html')


@app.route('/video', methods=['GET', 'POST'])
def video():
    # Upload video
    form = UploadFileForm()
    # If method == post,
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname("input.mp4")), app.config['UPLOAD_FOLDER'],
                               secure_filename("input.mp4")))  # Then save the file
        # Use session storage to save video file path
        session['video_path'] = os.path.join(os.path.abspath(os.path.dirname("input.mp4")), app.config['UPLOAD_FOLDER'],
                                             secure_filename("input.mp4"))

        # Redirect to canvas with a frame in the picture to draw begin and end line
        return render_template('canvas.html')
        # return render_template('video.html', form=form)
    return render_template('video.html', form=form)

@app.route('/videoframe')
def videoframe():
    # return Response(generate_frames(path_x='static/files/bikes.mp4'), mimetype='multipart/x-mixed-replace; boundary=frame')
    return Response(generate_frames(path_x=session.get('video_path', None)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# To display the Output Video on Webcam page
@app.route('/liveframe')
def liveframe():
    # return Response(generate_frames(path_x = session.get('video_path', None),conf_=round(float(session.get('conf_', None))/100,2)),mimetype='multipart/x-mixed-replace; boundary=frame')
    return Response(generate_frames_web(path_x=0), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/find')
def find():
    query_params = request.args.to_dict()

    documents = list(find_traffic_data(query_params))

    json_data = dumps(documents, indent=2)
    return Response(json_data, mimetype='application/json')

@app.route('/export')
def export():
    query_params = request.args.to_dict()
    documents = list(find_traffic_data(query_params))

    # Create a CSV buffer
    csv_buffer = StringIO()

    headers = documents[-1].keys()

    csv_writer = csv.DictWriter(csv_buffer, fieldnames=headers)

    csv_writer.writeheader()

    for document in documents:
        csv_writer.writerow(document)

    csv_data = csv_buffer.getvalue()

    response = Response(csv_data, mimetype='text/csv')

    response.headers.set("Content-Disposition", "attachment", filename="traffic_data.csv")

    return response


@app.route('/summary')
def summary():
    query_params = request.args.to_dict()
    documents = list(find_traffic_data(query_params))

    if not documents:
        return jsonify({"error": "No data found"}), 404

    class_counts_by_hour = {}
    total_count = 0
    date = documents[0]["date"]
    address = documents[0]["full_address"]
    start_time = datetime.max
    end_time = datetime.min

    for doc in documents:
        vehicle_class = doc.get("class", "")
        hour = doc["out_time"][:2] + ":00"
        
        if hour not in class_counts_by_hour:
            class_counts_by_hour[hour] = {cls: 0 for cls in ['Bicycle', 'Bus', 'Car', 'Jeepney', 'Motorcycle', 'Tricycle', 'Truck']}
        
        if vehicle_class in class_counts_by_hour[hour]:
            class_counts_by_hour[hour][vehicle_class] += 1
        total_count += 1
        
        try:
            in_time = datetime.strptime(doc["out_time"], "%H:%M:%S.%f")
            if in_time < start_time:
                start_time = in_time
        except ValueError:
            print(f"Invalid in_time format: {doc['out_time']}")
        
        try:
            out_time = datetime.strptime(doc["out_time"], "%H:%M:%S.%f")
            if out_time > end_time:
                end_time = out_time
        except ValueError:
            print(f"Invalid out_time format: {doc['out_time']}")

    summary_data = {
        "Address": address,
        "Date": date,
        "Totals": class_counts_by_hour,
        "Time Span": {
            "Start": start_time.strftime("%H:%M:%S.%f")[:-3] if start_time != datetime.max else "N/A",
            "End": end_time.strftime("%H:%M:%S.%f")[:-3] if end_time != datetime.min else "N/A"
        },
        "Sum Total": total_count
    }

    return jsonify(summary_data)

@app.route('/report')
def report():
    with app.test_request_context('/summary', query_string=request.args):
        summary_response = summary()
        summary_data = summary_response.get_json()

    # Set up image properties
    vehicle_classes = list(summary_data["Totals"].values())[0].keys()
    img_width = 700
    img_height = 200 + 40 * (len(summary_data["Totals"]) + 1)  # Adjust height based on the number of rows + 1 for header
    background_color = (255, 255, 255)
    text_color = (0, 0, 0)
    line_color = (0, 0, 0)
    title_font_size = 20
    header_font_size = 16
    table_font_size = 14
    header_background_color = (200, 200, 200)
    row_colors = [(240, 255, 240), (255, 255, 255)]  # Alternating colors: light green and white

    # Create an image
    image = Image.new("RGB", (img_width, img_height), background_color)
    draw = ImageDraw.Draw(image)

    # Load fonts
    try:
        title_font = ImageFont.truetype("times.ttf", title_font_size)  # Times New Roman
        header_font = ImageFont.truetype("times.ttf", header_font_size)  # Times New Roman
        table_font = ImageFont.truetype("times.ttf", table_font_size)  # Times New Roman
    except IOError:
        title_font = ImageFont.load_default()
        header_font = ImageFont.load_default()
        table_font = ImageFont.load_default()

    # Draw title and headers
    title = summary_data["Address"]
    header = f"Date: {summary_data['Date']}\nFrom {summary_data['Time Span']['Start']} to {summary_data['Time Span']['End']}"

    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_height = title_bbox[3] - title_bbox[1]

    header_bbox = draw.textbbox((0, 0), header, font=header_font)
    header_width = header_bbox[2] - header_bbox[0]
    header_height = header_bbox[3] - header_bbox[1]

    draw.text(((img_width - title_width) / 2, 20), title, fill=text_color, font=title_font)
    draw.text(((img_width - header_width) / 2, 60), header, fill=text_color, font=header_font)

    # Draw the table headers
    table_x = 50
    table_y = 120
    col_width = (img_width - 2 * table_x) // (len(vehicle_classes) + 1)  # +1 for the hour column
    row_height = 40

    # Draw column headers
    draw.rectangle([table_x, table_y, img_width - table_x, table_y + row_height], fill=header_background_color, outline=line_color, width=2)
    draw.text((table_x + 10, table_y + 10), "Hour", fill=text_color, font=header_font)
    for i, vehicle_class in enumerate(vehicle_classes):
        draw.text((table_x + (i + 1) * col_width + 10, table_y + 10), vehicle_class, fill=text_color, font=header_font)

    table_y += row_height

    # Draw table rows with alternating colors
    for hour, totals in summary_data["Totals"].items():
        row_color = row_colors[(table_y // row_height) % 2]
        draw.rectangle([table_x, table_y, img_width - table_x, table_y + row_height], fill=row_color, outline=line_color, width=2)
        draw.text((table_x + 10, table_y + 10), hour, fill=text_color, font=table_font)
        for i, vehicle_class in enumerate(vehicle_classes):
            draw.text((table_x + (i + 1) * col_width + 10, table_y + 10), str(totals[vehicle_class]), fill=text_color, font=table_font)
        table_y += row_height

    # Draw the total row
    row_color = row_colors[(table_y // row_height) % 2]
    draw.rectangle([table_x, table_y, img_width - table_x, table_y + row_height], fill=row_color, outline=line_color, width=2)
    draw.text((table_x + 10, table_y + 10), "Sum Total", fill=text_color, font=table_font)
    draw.text((table_x + col_width + 10, table_y + 10), str(summary_data["Sum Total"]), fill=text_color, font=table_font)

    # Save the image to a byte buffer
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0)

    # Send the image as a downloadable file
    return send_file(buffer, mimetype='image/jpeg', as_attachment=True, download_name="report.jpg")


if __name__ == "__main__":
    app.run(debug=True)
