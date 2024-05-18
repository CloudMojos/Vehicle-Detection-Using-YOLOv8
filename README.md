### Installation guide.
1. `cd server`
2. `pip install` (hopefully this works)
3. `python app.py`

### To change model:
1. go to `detection.py`
2. `ctrl + f` "model ="
3. change the directory of the model you want to use
4. You will also have to change the class names, similarly:
5. `ctrl + f` "class_names ="
6. Change the `class_names` array