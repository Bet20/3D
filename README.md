# Tridimensional Drawing

Application to create 3D lines and shapes with your hands and camera.
Has two modes, single hand mode and dual hand mode.

With the single hand mode, drawing is done by putting your index finger up, stopping the drawing is done by closing your hand and quiting is done by opening your hand.

## How to install
```sh
# note: It's a good practice to create an
# environment to run the application
pip install mediapipe opencv trimesh numpy
pip install --no-cache-dir -r requirements.txt
```

## How to run
```sh
python src/tridraw --mode single # for single hand mode
python src/tridraw --mode dual # for dual hand mode
```