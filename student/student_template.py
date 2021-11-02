from student_base import student_base

class my_flight_controller(student_base):
    
    def student_run(self, latitude, longitude, in_air):
        print(latitude, longitude, in_air)
        
if __name__ == "__main__":
    fcs = my_flight_controller()
    fcs.run()
