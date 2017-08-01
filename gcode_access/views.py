from django.shortcuts import render
from django.http import HttpResponse
import re

def index(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        height = request.POST.get('height', 0)
        duration = request.POST.get('duration', 0)
        frequency = request.POST.get('frequency', 0)
        pause = request.POST.get('pause', False)
        beep = request.POST.get('beep', False)
        paraX = request.POST.get('paramsetX','')
        paraY = request.POST.get('paramsetY','')
        paraZ = request.POST.get('paramsetZ','')
        paraE = request.POST.get('paramsetE','')
        paraL = request.POST.get('paramsetL','')
        inputs = list()
        for line in myfile.readlines():
            inputs.append(line.decode('utf-8'))
        output = process_gcode_file(inputs, height, duration, frequency, pause, beep, (paraX,paraY,paraZ,paraE,paraL))
        fname = myfile.name
        if pause:
            fname = "PAUSE_" + fname
        elif beep:
            fname = "BEEP_" + fname
        response = HttpResponse(output, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=%s' % fname



        return response
    return render(request, 'gcode/index.html')


def process_gcode_file(file_contents, heightInMM, duration, frequency, pause, beep, parameter_set):
    defaults = 'XHome', 'YHome', 'Z1', 'E1', 'L1'
    for i in range(0,len(parameter_set)):
        if parameter_set[i] == '':
            parameter_set[i] = defaults[i]
    height_in_MM = float(heightInMM)
    pause_command = 'M600 ' + ' '.join(parameter_set) + '\n'
    beep_command = 'M300 ' + frequency + ' ' + duration + '\n'

    listOfLines = list()
    height_line = re.compile(" *G1 Z[0-9]+\.?[0-9]* *.*")
    last_known_height = -1
    last_known_height_index = 0
    done = False

    for line in file_contents:
        listOfLines.append(line)
        if height_line.match(line) and not done:
            section = re.search("Z[0-9]+\.?[0-9]*", line).group(0).replace("Z", '')
            height = float(section)
            if height > height_in_MM:
                if last_known_height != -1 and abs(height_in_MM - height) > abs(height_in_MM - last_known_height):
                    #The difference between this height is greater than the distance between the last known height
                    #AND this isn't the first height we've come across
                    if pause:
                        listOfLines.insert(last_known_height_index, pause_command)
                        listOfLines.insert(last_known_height_index, beep_command)
                    elif beep:
                        listOfLines.insert(last_known_height_index, beep_command)
                    done = True
                else:
                    last_known_height = height
                    last_known_height_index = len(listOfLines) - 1
            elif height == height_in_MM:
                #We have found the exact height where the beep should be placed.
                if pause:
                    listOfLines.append(beep_command)
                    listOfLines.append(pause_command)
                elif beep:
                    listOfLines.append(beep_command)
                done = True
            else:
                last_known_height = height
                last_known_height_index = len(listOfLines) - 1
    if not done and not last_known_height == -1:
        '''
        This takes care of the case where only 1 G1 command was found, and
        it wasn't the exact height we wanted
        '''
        if pause:
            listOfLines.insert(last_known_height_index, pause_command)
            listOfLines.insert(last_known_height_index, beep_command)
        elif beep:
            listOfLines.insert(last_known_height_index, beep_command)
    return ''.join(listOfLines)
