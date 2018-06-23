"""Add the 'course' functionality"""

# A list of functions
course_content = []

def course_set_time(block, t):
        if t < block.t or block.t == -1:
                block.t = 0
        while block.t <= t and course_content[block.t]:
                course_content[block.t]()
                block.t += 1
        block.t -= 1


try:
        CAQ.time_travel = ["F5", "F6"]
        CAQ.add_filter('set_time', course_set_time)
except:
        pass

