class DrawingControls:
    def __init__(self, initial_pr=0.001, depth_modifier=3):
        self.pr = initial_pr
        self.depth_modifier = depth_modifier
        self.min_pr = 0.000001 
        self.max_pr = 0.1    

    def is_finger_down(self, tip, pip):
        return tip.y > pip.y

    def adjust_precision(self, landmarks):
        index_tip = landmarks[8]
        index_pip = landmarks[6]
        middle_tip = landmarks[12]
        middle_pip = landmarks[10]

        index_down = self.is_finger_down(index_tip, index_pip)
        middle_down = self.is_finger_down(middle_tip, middle_pip)

        if index_down and not middle_down:
            self.pr = max(self.pr / 2, self.min_pr)
            return True
        elif middle_down and not index_down:
            self.pr = min(self.pr * 2, self.max_pr)
            return True

        return False

    def simplify_point(self, p):
        return (
            round(p.x/self.pr) * self.pr,
            round(p.y/self.pr) * self.pr,
            round(p.z*self.depth_modifier/self.pr) * self.pr
        )

    def get_current_precision(self):
        return self.pr 