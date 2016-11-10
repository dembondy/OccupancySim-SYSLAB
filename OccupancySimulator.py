import pandas as pd
import numpy as np
import csv
from random import randint, shuffle


class OccSim:
    def __init__(self, variables):
        self.start_date = variables['StartDate']
        self.end_date = variables['EndDate']
        self.rooms = int(variables['Rooms'])
        self.engineers = int(variables['Engineers'])
        self.senior_managers = int(variables['SeniorManagers'])
        self.middle_managers = int(variables['MiddleManagers'])
        self.administrative_staff = int(variables['AdministrativeStaff'])
        self.ts = variables['Ts']
        self.time_vector = pd.date_range(start=self.start_date, end=self.end_date, freq=self.ts)
        self.days = (pd.to_datetime(self.end_date)-pd.to_datetime(self.start_date)).days
        #self.bdays = np.busday_count(pd.to_datetime(self.start_date),pd.to_datetime(self.end_date))

    def simulate(self):
        worker_list = ['Engineer']*self.engineers+['SeniorManager']*self.senior_managers+\
                      ['MiddleManager']*self.middle_managers+['AdministrativeStaff']*self.administrative_staff
        shuffle(worker_list)  # Shuffle so we can assign workers to random room numbers
        self.simulation = pd.DataFrame(index=self.time_vector)
        for room,worker in zip(range(self.rooms),worker_list):  # Iterate over room and worker. Only valid if they have
            room_no = 'room_'+str(room)                         # same amount of items
            self.simulation[room_no] = self.simulate_worker(worker)

    def simulate_worker(self, worker_role):
        # The engineer pattern is to arrive at work around 8:30, leave at around 17:00, have lunch at around 12:00.
        # He has (fixed) 2 1-hour meetings a week. other worker have variations of this pattern, with extra meetings.
        # Returns a pandas DataFrame with room number as column. 0 his is not at his office, 1 he is.
        # He only works on weekdays.
        t = 1  # hard coded for now, but must match the ts in the setup file!
        delta_day = pd.Timedelta('1 days')
        delta_hour = pd.Timedelta('1 hour')
        delta_10min = pd.Timedelta('10 minutes')

        if worker_role == 'Engineer':
            meeting1_day = randint(0, 4)
            meeting2_day = randint(0, 4)
            meeting3_day = randint(0, 4)
            meeting4_day = randint(0, 4)
            meeting_time_1 = '09:00:00'
            meeting_time_2 = '10:00:00'
            meeting_time_3 = '13:00:00'
            meeting_time_4 = '14:30:00'
            arrival = '08:30:00'
            departure = '17:00:00'
            lunch = '12:00:00'

        if worker_role == 'MiddleManager':
            meeting1_day = randint(0, 4)
            meeting2_day = randint(0, 4)
            meeting3_day = randint(0, 4)
            meeting4_day = randint(0, 4)
            meeting_time_1 = '11:00:00'
            meeting_time_2 = '10:00:00'
            meeting_time_3 = '13:00:00'
            meeting_time_4 = '14:30:00'
            arrival = '09:00:00'
            departure = '16:30:00'
            lunch = '12:00:00'

        if worker_role == 'SeniorManager':
            meeting1_day = randint(0, 4)
            meeting2_day = randint(0, 4)
            meeting3_day = randint(0, 4)
            meeting4_day = randint(0, 4)
            meeting_time_1 = '11:00:00'
            meeting_time_2 = '10:00:00'
            meeting_time_3 = '13:30:00'
            meeting_time_4 = '14:30:00'
            arrival = '09:30:00'
            departure = '16:00:00'
            lunch = '12:30:00'

        if worker_role == 'AdministrativeStaff':
            meeting1_day = randint(0, 4)
            meeting2_day = randint(0, 4)
            meeting3_day = randint(0, 4)
            meeting4_day = randint(0, 4)
            meeting_time_1 = '11:00:00'
            meeting_time_2 = '10:00:00'
            meeting_time_3 = '13:30:00'
            meeting_time_4 = '14:30:00'
            arrival = '08:00:00'
            departure = '16:30:00'
            lunch = '11:30:00'

        #worker = pd.Series(0, index=self.time_vector[self.time_vector.dayofweek < 5])
        worker = pd.Series(0, index=self.time_vector)

        for day in range(self.days):
            day_count = pd.to_datetime(self.start_date) + delta_day * day
            if day_count.dayofweek < 5:
                arr_time_var = random_time_delta(10, t)
                arr_lunch = random_time_delta(3, t)
                dep_lunch = random_time_delta(3, t)
                dep_time_var = random_time_delta(10, t)
                rand_arrival = pd.to_datetime(self.start_date + ' ' + arrival) + arr_time_var + delta_day * day
                rand_arr_lunch = pd.to_datetime(self.start_date + ' ' + lunch) + arr_lunch + delta_day*day
                rand_dep_lunch = pd.to_datetime(self.start_date + ' ' + lunch) + delta_hour + dep_lunch + delta_day*day
                rand_dep_time = pd.to_datetime(self.start_date + ' ' + departure) + dep_time_var + delta_day*day
                worker[rand_arrival:rand_arr_lunch] = 1
                worker[rand_dep_lunch:rand_dep_time] = 1
                #print(meeting1_day,meeting2_day,meeting3_day,meeting4_day)
                #print(rand_arrival.dayofweek)
                if rand_arrival.dayofweek == meeting1_day:
                    meeting_hour = pd.to_datetime(self.start_date + ' ' + meeting_time_1) + delta_day * day
                    worker[meeting_hour:meeting_hour+delta_hour] = 0
                if rand_arrival.dayofweek == meeting2_day:
                    meeting_hour = pd.to_datetime(self.start_date + ' ' + meeting_time_2) + delta_day * day
                    worker[meeting_hour:meeting_hour+delta_hour] = 0
                if worker_role == 'MiddleManager' or 'SeniorManager':
                    if rand_arrival.dayofweek == meeting3_day:
                        meeting_hour = pd.to_datetime(self.start_date + ' ' + meeting_time_3) + delta_day * day
                        worker[meeting_hour:meeting_hour+delta_hour] = 0
                    if worker_role == 'SeniorManager':
                        if rand_arrival.dayofweek == meeting4_day:
                            meeting_hour = pd.to_datetime(self.start_date + ' ' + meeting_time_4) + delta_day * day
                            worker[meeting_hour:meeting_hour+delta_hour] = 0
                if worker_role == 'AdministrativeStaff':
                    rand_work_1 = pd.to_datetime(self.start_date + ' ' + meeting_time_1) + random_time_delta(30, t) + \
                                  delta_day * day
                    rand_work_2 = pd.to_datetime(self.start_date + ' ' + meeting_time_2) + random_time_delta(30, t) + \
                                  delta_day * day
                    rand_work_3 = pd.to_datetime(self.start_date + ' ' + meeting_time_3) + random_time_delta(30, t) + \
                                  delta_day * day
                    rand_work_4 = pd.to_datetime(self.start_date + ' ' + meeting_time_4) + random_time_delta(30, t) + \
                                  delta_day * day
                    worker[rand_work_1:rand_work_1 + delta_10min] = 0
                    worker[rand_work_2:rand_work_1 + delta_10min] = 0
                    worker[rand_work_3:rand_work_1 + delta_10min] = 0
                    worker[rand_work_4:rand_work_1 + delta_10min] = 0
        return worker

    def write_out(self, file_name):
        self.simulation.fillna(0.0)
        self.simulation.to_csv(file_name)



def myround(x, base=5):
    return int(base * round(float(x) / base))  # A function for rounding the variable time


def random_time_delta(std_dev, rounding):
    neg = 0
    time_var_int = myround(np.random.normal(0, std_dev), rounding)  # this needs to be adjusted manually
                                                                        # for the time sample
    if time_var_int < 0:
        time_var_int = time_var_int*-1
        neg = 1
    if time_var_int < 10:
        time_var_string = '0'+str(time_var_int)  # If this is called, it's because we need to pad the value
    else:
        time_var_string = str(time_var_int)
    if neg == 1:
        time_var = -pd.to_timedelta('00:'+time_var_string+':00')
    else:
        time_var = pd.to_timedelta('00:'+time_var_string+':00')
    #print(time_var)
    return time_var


if __name__ == "__main__":
    with open('setup.csv', mode='r') as infile:
        reader = csv.reader(infile)
        setup_variables = {rows[0]:rows[1] for rows in reader}
    simulator = OccSim(setup_variables)
    simulator.simulate()
    simulator.write_out('all_rooms.csv')