# Tridimensional Drawing

Application to create 3D lines and shapes with your hands and camera.

You need to use both hands, the right hand works as the cursor and the left controls the drawing. If you open your left hand it starts drawing, if you close it it stops. If you put your left index finger down you increase the definition of the drawing if you put your middle finger down it decreases it.

## How to install
```sh
# note: It's a good practice to create an
# environment to run the application (with something like venv)
pip install mediapipe opencv trimesh numpy # or
pip install --no-cache-dir -r requirements.txt
```

## How to run
```sh
python src/tridraw
```