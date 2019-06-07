import simplejson as json
import re
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
with open('transfocator.txt', 'r') as handle:
    data = json.load(handle)
    startX = []
    startY = []
    stoppedX = []
    stoppedY = []
    targetX = []
    targetY = []
    #change this to input time
    prevx = data[0].get('start_ts')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # this will need to be changed when not test data to account for nonzero entry slopes
    prevy = data[0].get('start_pos')
    i=0
    while i<len(data)-1:
        i+=1
        startX.append(data[i].get('start_ts'))
        startY.append(data[i].get('start_pos'))
        # Decorate line here with necessary info
        prevLine = mlines.Line2D([prevx, data[i].get('start_ts')],
                          [prevy, data[i].get('start_pos')], picker = 5)
        ax.add_line(prevLine)
        prevx = data[i].get('finish_ts')
        prevy = data[i].get('finish_pos')
        if data[i].get('target') <= data[i].get('finish_pos')+.01 and data[i].get('target') >= data[i].get('finish_pos')-.01:
            targetX.append(data[i].get('finish_ts'))
            targetY.append(data[i].get('finish_pos'))
            # Decorate line here with necessary info
            currLine = mlines.Line2D([data[i].get('start_ts'), (data[i].get('finish_ts'))], [
                              (data[i].get('start_pos')), (data[i].get('finish_pos'))], picker = 5)
            currLine.targetPos = data[i].get('target')
            currLine.date = datetime.fromtimestamp(data[i].get('start_ts'))
            ax.add_line(currLine)
        else:
            m = (data[i].get('finish_pos')-data[i].get('start_pos')) / \
                (data[i].get('finish_ts')-data[i].get('start_ts'))
            targetTime = data[i].get(
                'target')/m - data[i].get('finish_pos')/m + data[i].get('finish_ts')
            stoppedX.append(data[i].get('finish_ts'))
            stoppedY.append(data[i].get('finish_pos'))
            targetY.append(data[i].get('target'))
            # target time = target pos/m - end pos/m +end time
            targetX.append(targetTime)
            targetLine = mlines.Line2D([data[i].get('finish_ts'), targetTime], [
                                data[i].get('finish_pos'), data[i].get('target')], color='red', picker = 5)
            ax.add_line(targetLine)
            #targetLine.set_dashes(1)
            # plot(end time, target time, end pos, target pos) MAKE DASHED
    starter = plt.scatter(startX, startY, marker ='o', color ='limegreen', s=150, label = 'Motion Started')
    ender = plt.scatter(targetX, targetY, marker= 's', color = 'darkblue', label = 'Motion Completed')
    stopper = plt.scatter(stoppedX, stoppedY, marker= 'x', color='r', label = "Motion Stopped Before Target Reached")

    def on_pick(event):
        #table = pd.DataFrame({"User": ["Unknown"],"Date": [event.artist.date], "Target Position": [event.artist.targetPos]})
        data = np.array([['Unknown', event.artist.date, event.artist.targetPos]])
        df = pd.DataFrame(data, columns = ['User', 'Date', 'Target Position'])

        #col_labels = (['User'], ['Request Time'],  ['Target Position'])
        #table_vals = (['Unknown'], [event.artist.date],  [event.artist.targetPos])
        #the_table = plt.table(cellText=table_vals,
        #              colLabels=col_labels,
        #              loc='center')
        #the_table.scale(3,2)
        ax.plot(df)
        print(event.artist.targetPos)
        print("line picked")
    plt.xlabel('Time of Event')
    plt.ylabel('Motor Location')
    plt.title('Motor Status')
    plt.legend(loc='upper right')
    fig.canvas.callbacks.connect('pick_event', on_pick)
    plt.show()
