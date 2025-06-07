import cv2
import mediapipe as mp
import obj
from controls import DrawingControls

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands()

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera")
    exit()

all_meshes = []
current_mesh = []
controls = DrawingControls(initial_pr=0.001, depth_modifier=3)

def is_hand_open(landmarks):
    index_tip = landmarks[8]
    index_pip = landmarks[6]
    middle_tip = landmarks[12]
    middle_pip = landmarks[10]
    return (index_tip.y < index_pip.y) and (middle_tip.y < middle_pip.y)

def draw_mesh_overlay(img, mesh, color=(0, 255, 0), thickness=2):
    if len(mesh) < 2:
        return

    points = []
    for point in mesh:
        x = int(point[0] * img.shape[1])
        y = int(point[1] * img.shape[0])
        points.append((x, y))
    
    for i in range(len(points) - 1):
        cv2.line(img, points[i], points[i+1], color, thickness)
    
    for point in points:
        cv2.circle(img, point, 3, color, -1)

is_drawing_enabled = False

while True:
    success, img = cap.read()
    if not success:
        print("Failed to capture video")
        break
        
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    for mesh in all_meshes:
        draw_mesh_overlay(img, mesh, color=(255, 0, 0), thickness=1)

    if results.multi_hand_landmarks:
        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
            landmarks = hand_landmarks.landmark
            wrist_x = landmarks[0].x
            is_right_hand = wrist_x > 0.5
            
            if is_right_hand:
                if is_drawing_enabled:
                    index_tip = landmarks[8]
                    point = controls.simplify_point(index_tip)
                    current_mesh.append(point)
            else:
                # Adjust precision with left hand (index or middle finger down)
                controls.adjust_precision(landmarks)
                is_drawing_enabled = is_hand_open(landmarks)
                
                if not is_drawing_enabled and current_mesh and len(current_mesh) > 1:
                    all_meshes.append(current_mesh)
                    current_mesh = []

    if current_mesh:
        draw_mesh_overlay(img, current_mesh, color=(0, 255, 0), thickness=2)

    status = "Drawing Enabled" if is_drawing_enabled else "Drawing Disabled"
    cv2.putText(img, status, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(img, f"Meshes Created: {len(all_meshes)}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(img, f"Precision: {controls.get_current_precision():.6f}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Hand Gesture", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

if current_mesh and len(current_mesh) > 1:
    all_meshes.append(current_mesh)
    print(f"Saved final mesh with {len(current_mesh)} points")

if all_meshes:
    print(f"Generating visualization with {len(all_meshes)} meshes")
    obj.generate_visualization(all_meshes)
    obj.export_to_obj(all_meshes)
else:
    print("No meshes were created. Please try again.")