from django.shortcuts import render,redirect
import json


def home(request):
    if request.method == 'POST':
        job_count = request.POST.get('job_count')
        previously_served = request.POST.get('previously_served', '')
        starting_position = request.POST.get('starting_position', '')
        starting_track = request.POST.get('starting_track', '')
        ending_track = request.POST.get('ending_track', '')
        arm_movement = request.POST.get('arm_movement', '')
        selected_algorithm = request.POST.get('fifoalgorithm')
        
        if job_count and job_count.isdigit():
            job_count = int(job_count)
            input_values = {}
            
            for i in range(1, job_count + 1):
                input_name = f'job_{i}'
                input_value = request.POST.get(input_name)
                input_values[input_name] = input_value
            
            input_values['previously_served'] = previously_served
            input_values['starting_position'] = starting_position
            input_values['starting_track'] = starting_track
            input_values['ending_track'] = ending_track
            input_values['arm_movement'] = arm_movement
            
            if selected_algorithm == 'FIFO':
                return redirect('fifo', job_count=job_count, **input_values)
            elif selected_algorithm == 'SSTF':
                return redirect('sstf', job_count=job_count, **input_values)
            elif selected_algorithm == 'SCAN':
                return redirect('scan', job_count=job_count, **input_values)
            elif selected_algorithm == 'C-SCAN':
                return redirect('cscan', job_count=job_count, **input_values)
            elif selected_algorithm == 'LOOK':
                return redirect('look', job_count=job_count, **input_values)
            elif selected_algorithm == 'C-LOOK':
                return redirect('clook', job_count=job_count, **input_values)
       
    return render(request, 'diskscheduling/home.html')


#FIFO CALCULATIONS
def fifo(request, job_count=None, previously_served='', starting_position='', starting_track='', ending_track='', arm_movement=''):
    input_values = {}  # Dictionary to store the inputted values

    if request.method == 'POST':
        job_count = request.POST.get('job_count')
        previously_served = request.POST.get('previously_served', '')
        starting_position = request.POST.get('starting_position', '')
        starting_track = request.POST.get('starting_track', '')
        ending_track = request.POST.get('ending_track', '')
        arm_movement = request.POST.get('arm_movement', '')
        
        if job_count and job_count.isdigit():
            job_count = int(job_count)

            for i in range(1, job_count + 1):
                input_name = f'job_{i}'
                input_value = request.POST.get(input_name)
                input_values[input_name] = input_value

        input_values['previously_served'] = previously_served
        input_values['starting_position'] = starting_position
        input_values['starting_track'] = starting_track
        input_values['ending_track'] = ending_track
        input_values['arm_movement'] = arm_movement

    else:
        # Handle GET request or initial rendering
        # Populate input_values dictionary with previous values if available
        job_count = request.GET.get('job_count')
        previously_served = request.GET.get('previously_served', '')
        starting_position = request.GET.get('starting_position', '')
        starting_track = request.GET.get('starting_track', '')
        ending_track = request.GET.get('ending_track', '')
        arm_movement = request.GET.get('arm_movement', '')
        
        if job_count and job_count.isdigit():
            job_count = int(job_count)

            for i in range(1, job_count + 1):
                input_name = f'job_{i}'
                input_value = request.GET.get(input_name)
                input_values[input_name] = input_value

        input_values['previously_served'] = previously_served
        input_values['starting_position'] = starting_position
        input_values['starting_track'] = starting_track
        input_values['ending_track'] = ending_track
        input_values['arm_movement'] = arm_movement
    
    y_values_arranged = []
    previously_served_value = input_values.get('previously_served')

    # Append the starting position if it exists
    starting_position = input_values.get('starting_position')
    current_position = int(starting_position)

   # Append all other input values
    for i in range(1, job_count + 1):
        input_name = f'job_{i}'
        input_value = input_values.get(input_name)
        if input_value is not None:
            # Check if the previously served value falls between the current position and the previous position
            # Check if the previously served value falls between the current position and the previous position
            for index, value in enumerate(y_values_arranged):
                if index > 0:
                    current_position = int(value)
                    previous_job_value = int(y_values_arranged[index - 1])
                    if previously_served_value is not None:
                        if previous_job_value < int(previously_served_value) < current_position:
                            y_values_arranged.insert(index, str(previously_served_value))
                            previously_served_value = None
                            break
                        elif current_position < int(previously_served_value) < previous_job_value:
                            y_values_arranged.insert(index, str(previously_served_value))
                            previously_served_value = None
                            break


            y_values_arranged.append(str(input_value))

    # Append the previously served value if it hasn't been inserted yet
    if previously_served_value is not None and previously_served_value not in y_values_arranged:
        y_values_arranged.insert(-1, str(previously_served_value))

    # Append the starting position
    y_values_arranged.insert(0, str(starting_position))

    print(y_values_arranged)



    # previously_served_value = input_values.get('previously_served')

    # # Append the starting position if it exists
    # starting_position = input_values.get('starting_position')
    # current_position = int(starting_position)

    # # Append all other input values
    # for i in range(1, job_count + 1):
    #     input_name = f'job_{i}'
    #     input_value = input_values.get(input_name)
    #     if input_value is not None:
    #         if previously_served_value is not None and int(current_position) < int(previously_served_value) < int(input_value):
    #             y_values_arranged.append(str(previously_served_value))
    #             y_values_arranged.append(str(input_value))
    #             previously_served_value = None
    #         y_values_arranged.append(str(input_value))
    #         current_position = int(input_value)

    # # Append the previously served value if it falls within the range of the current position and next job request
    # if previously_served_value is not None and int(current_position) < int(previously_served_value):
    #     y_values_arranged.append(str(previously_served_value))

    # # Append the starting position at the beginning of the list
    # y_values_arranged.insert(0, str(starting_position))


    # print(y_values_arranged)







    # # Set job_count to a default value of 0 if it is None
    # job_count = job_count or 0
    
    # # Append the job values
    # for i in range(1, job_count + 1):
    #     input_name = f'job_{i}'
    #     input_value = input_values.get(input_name)
    
    
    #     if input_value is not None:
    #             if previously_served_value is not None and int(input_value) > int(previously_served_value):
    #                 y_values_arranged.append(str(previously_served_value))
    #                 previously_served_value = None
    #             y_values_arranged.append(str(input_value))

    # # Append the previously served value if it exists
    # if previously_served_value is not None:
    #     y_values_arranged.append(str(previously_served_value))

    x_values = []

    # Append the starting position if it exists
    starting_position = input_values.get('starting_position')
    if starting_position is not None:
        x_values.append("Starting Position")

    # Append the job names based on the values in y_values_arranged
    previously_served_value = input_values.get('previously_served')
    previously_served_added = False  # Flag to track if the previously_served job has been added

    for job_value in y_values_arranged:
        if previously_served_value is not None and job_value == int(previously_served_value) and not previously_served_added:
            x_values.append("Previously Served")
            previously_served_added = True
            previously_served_value = None
        else:
            job_names = [k for k, v in input_values.items() if v == str(job_value) and k != 'starting_position']
            if job_names:
                job_name = next((name for name in job_names if name not in x_values), '')
                x_values.append(job_name)

    # Check if the previously served job is the last job in the list
    if previously_served_value is not None and int(previously_served_value) == y_values_arranged[-1] and not previously_served_added:
        x_values.append("Previously Served")

    print(x_values)


    # print(x_values)

    
    # Convert the yValues to JSON
    x_values_json = json.dumps(x_values)
    y_values_json = json.dumps(y_values_arranged)
    
    
    # Calculate THM
    # Parse JSON string to obtain the list of values
    y_values = json.loads(y_values_json)  

    thm = 0
    for i in range(len(y_values) - 1):
        diff = abs(int(y_values[i]) - int(y_values[i+1]))
        thm += diff
    # print(thm)
    
# Calculate ST
   # Calculate ST
    st = 0
    ending_track = int(ending_track)
    if thm != 0:
        st = ending_track * int(arm_movement) / thm
    st = round(st, 2)
        # print(st)
    return render(request, 'diskscheduling/fcfschart.html', {'input_values': input_values,'y_values_json': y_values_json,'x_values_json': x_values_json,'starting_track': starting_track,'ending_track': ending_track,'arm_movement':arm_movement,'thm': thm,'st':st})


#SSTF CALCULATIONS
def sstf(request, job_count=None, previously_served='', starting_position='', starting_track='', ending_track='', arm_movement=''):
    input_values = {}  # Dictionary to store the inputted values

    if request.method == 'POST':
        job_count = request.POST.get('job_count')
        previously_served = request.POST.get('previously_served', '')
        starting_position = request.POST.get('starting_position', '')
        starting_track = request.POST.get('starting_track', '')
        ending_track = request.POST.get('ending_track', '')
        arm_movement = request.POST.get('arm_movement', '')
        
        if job_count and job_count.isdigit():
            job_count = int(job_count)

            for i in range(1, job_count + 1):
                input_name = f'job_{i}'
                input_value = request.POST.get(input_name)
                input_values[input_name] = input_value

        input_values['previously_served'] = previously_served
        input_values['starting_position'] = starting_position
        input_values['starting_track'] = starting_track
        input_values['ending_track'] = ending_track
        input_values['arm_movement'] = arm_movement

    else:
        # Handle GET request or initial rendering
        # Populate input_values dictionary with previous values if available
        job_count = request.GET.get('job_count')
        previously_served = request.GET.get('previously_served', '')
        starting_position = request.GET.get('starting_position', '')
        starting_track = request.GET.get('starting_track', '')
        ending_track = request.GET.get('ending_track', '')
        arm_movement = request.GET.get('arm_movement', '')
        
        if job_count and job_count.isdigit():
            job_count = int(job_count)

            for i in range(1, job_count + 1):
                input_name = f'job_{i}'
                input_value = request.GET.get(input_name)
                input_values[input_name] = input_value

        input_values['previously_served'] = previously_served
        input_values['starting_position'] = starting_position
        input_values['starting_track'] = starting_track
        input_values['ending_track'] = ending_track
        input_values['arm_movement'] = arm_movement
    
    
    y_values_arranged = []

    # Set job_count to a default value of 0 if it is None
    job_count = job_count or 0

    # Create a list to hold the job values
    jobs = []

    # Append the job values
    for i in range(1, job_count + 1):
        input_name = f'job_{i}'
        input_value = input_values.get(input_name)
        if input_value is not None:
            jobs.append(int(input_value))

    # Sort the jobs in ascending order
    jobs.sort()
   
    # Start at the starting position
    starting_position = input_values.get('starting_position')
    current_position = int(starting_position)

    # Add the starting position to y_values_arranged
    y_values_arranged.append(current_position)

    # Compare the first two job requests
    first_job = jobs[0]
    second_job = jobs[1]

    # Calculate the seek time from the starting position to the first job
    seek_time_first = abs(first_job - current_position)

    # Calculate the seek time from the starting position to the second job
    seek_time_second = abs(second_job - current_position)

    # Determine which job is closer to the starting position
    if seek_time_first <= seek_time_second:
        next_job = first_job
    else:
        next_job = second_job

    # Check if the previously_served job is on the path to the next job request
    previously_served_value = input_values.get('previously_served')
    previously_served_added = False  # Flag to track if the previously_served job has been added

    # Check if the previously_served job is on the path to the next job request
    if previously_served_value is not None and min(current_position, next_job) <= int(previously_served_value) <= max(current_position, next_job):
        y_values_arranged.append(int(previously_served_value))
        previously_served_added = True

    # Add the next job to y_values_arranged
    y_values_arranged.append(next_job)
    current_position = next_job

    # Remove the processed job from the jobs list
    jobs.remove(next_job)

    # Continue with the remaining jobs
    while jobs:
        # Find the job with the shortest seek time from the current position
        min_seek_time = float('inf')
        next_job = None

        for job in jobs:
            seek_time = abs(job - current_position)
            if seek_time < min_seek_time:
                min_seek_time = seek_time
                next_job = job

        # Check if the previously_served job is on the path to the next job request
        if not previously_served_added and previously_served_value is not None and min(current_position, next_job) <= int(previously_served_value) <= max(current_position, next_job):
            y_values_arranged.append(int(previously_served_value))
            previously_served_added = True

        # Append the next_job to y_values_arranged
        y_values_arranged.append(next_job)

        # Update the current_position to the next_job
        current_position = next_job

        # Remove the processed job from the jobs list
        jobs.remove(next_job)

    print(y_values_arranged)



    # Print y_values_arranged for reference
    # print(y_values_arranged)

    x_values = []

    # Append the starting position if it exists
    starting_position = input_values.get('starting_position')
    if starting_position is not None:
        x_values.append("Starting Position")

    # Append the job names based on the values in y_values_arranged
    previously_served_value = input_values.get('previously_served')
    previously_served_added = False  # Flag to track if the previously_served job has been added

    for job_value in y_values_arranged:
        if previously_served_value is not None and job_value == int(previously_served_value) and not previously_served_added:
            x_values.append("Previously Served")
            previously_served_added = True
            previously_served_value = None
        else:
            job_names = [k for k, v in input_values.items() if v == str(job_value) and k != 'starting_position']
            if job_names:
                job_name = next((name for name in job_names if name not in x_values), '')
                x_values.append(job_name)

    # Check if the previously served job is the last job in the list
    if previously_served_value is not None and int(previously_served_value) == y_values_arranged[-1] and not previously_served_added:
        x_values.append("Previously Served")

    print(x_values)







    
    # Convert the yValues to JSON
    x_values_json = json.dumps(x_values)
    y_values_json = json.dumps(y_values_arranged)
    
    # Calculate THM
    # Parse JSON string to obtain the list of values
    y_values = json.loads(y_values_json)  

    thm = 0
    for i in range(len(y_values) - 1):
        diff = abs(int(y_values[i]) - int(y_values[i+1]))
        thm += diff
    
   # Calculate ST
    st = 0
    ending_track = int(ending_track)
    starting_track = int(starting_track)
    # total_track = int(ending_track) 
    total_track = ending_track - starting_track +1
    if thm != 0:
        # st = total_track * int(arm_movement) / thm
        st = total_track * int(arm_movement) / thm
    st = round(st, 2)
    
        
    return render(request, 'diskscheduling/sstfchart.html', {'input_values': input_values,'y_values_json': y_values_json,'x_values_json': x_values_json,'starting_track': starting_track,'ending_track': ending_track,'arm_movement':arm_movement,'thm': thm,'st':st,'jobs':jobs})



# SCAN CALCULATIONS
def scan(request, job_count=None, previously_served='', starting_position='', starting_track='', ending_track='', arm_movement=''):
    input_values = {}  # Dictionary to store the inputted values

    if request.method == 'POST':
        job_count = request.POST.get('job_count')
        previously_served = request.POST.get('previously_served', '')
        starting_position = request.POST.get('starting_position', '')
        starting_track = request.POST.get('starting_track', '')
        ending_track = request.POST.get('ending_track', '')
        arm_movement = request.POST.get('arm_movement', '')
        
        if job_count and job_count.isdigit():
            job_count = int(job_count)

            for i in range(1, job_count + 1):
                input_name = f'job_{i}'
                input_value = request.POST.get(input_name)
                input_values[input_name] = input_value

        input_values['previously_served'] = previously_served
        input_values['starting_position'] = starting_position
        input_values['starting_track'] = starting_track
        input_values['ending_track'] = ending_track
        input_values['arm_movement'] = arm_movement

    else:
        # Handle GET request or initial rendering
        # Populate input_values dictionary with previous values if available
        job_count = request.GET.get('job_count')
        previously_served = request.GET.get('previously_served', '')
        starting_position = request.GET.get('starting_position', '')
        starting_track = request.GET.get('starting_track', '')
        ending_track = request.GET.get('ending_track', '')
        arm_movement = request.GET.get('arm_movement', '')
        
        if job_count and job_count.isdigit():
            job_count = int(job_count)

            for i in range(1, job_count + 1):
                input_name = f'job_{i}'
                input_value = request.GET.get(input_name)
                input_values[input_name] = input_value

        input_values['previously_served'] = previously_served
        input_values['starting_position'] = starting_position
        input_values['starting_track'] = starting_track
        input_values['ending_track'] = ending_track
        input_values['arm_movement'] = arm_movement

    y_values_arranged = []

    # Set job_count to a default value of 0 if it is None
    job_count = job_count or 0

    # Create a list to hold the job values
    jobs = []

    # Append the job values
    for i in range(1, job_count + 1):
        input_name = f'job_{i}'
        input_value = input_values.get(input_name)
        if input_value is not None:
            jobs.append(int(input_value))

     # Sort the jobs in ascending order
    # Sort the jobs in ascending order
    jobs.sort()
    # print(jobs)

    # Start at the starting position
    starting_position = input_values.get('starting_position')
    current_position = int(starting_position)
    

    # Add the starting position to y_values_arranged
    y_values_arranged.append(current_position)

    if starting_position and previously_served:
        starting_position_value = int(starting_position)
        previously_served_value = int(previously_served)

        if starting_position_value > previously_served_value:
            direction = "UP"
        else:
            direction = "DOWN"
    else:
        direction = "NONE"

    if direction == "DOWN":
        # Append the job requests lower than the starting position in descending order
        for job in jobs:
            if job < current_position:
                y_values_arranged.append(job)

        # Sort the job requests in descending order
        y_values_arranged.sort(reverse=True)

        # Append the starting_position value
        y_values_arranged.append(starting_track)

        #Para makuha ang natitirang job request
        remaining_jobs = [job for job in jobs if job >= current_position]
        remaining_jobs.sort()

       # Check if there is a previously served value
        previously_served_value = input_values.get('previously_served')
        if previously_served_value is not None:
            previously_served_value = int(previously_served_value)
            # Find the index where the previously served value should be inserted
            insert_index = 0
            for i, job in enumerate(remaining_jobs):
                if job > previously_served_value:
                    insert_index = i
                    break
            # Insert the previously served value at the appropriate position
            remaining_jobs.insert(insert_index, previously_served_value)

        
        #Para maadd sa array na y_values_arranged yung natitirang job
        for job in remaining_jobs:
            y_values_arranged.append(job)
        
        # print("Down")
    else:
        # Append the job requests higher than the starting position in ascending order
        for job in jobs:
            if job > current_position:
                y_values_arranged.append(job)

        # Sort the job requests in ascending order
        y_values_arranged.sort()

        # Append the ending_track value minus 1 if it's not already in the list
        ending_track = input_values.get('ending_track')
        ending_track_value = int(ending_track)
        y_values_arranged.append(ending_track_value )

        # Append the remaining job requests in descending order
        remaining_jobs = [job for job in jobs if job <= current_position]
        remaining_jobs.sort(reverse=True)

        # Check if there is a previously served value
        previously_served_value = input_values.get('previously_served')
        if previously_served_value is not None:
            previously_served_value = int(previously_served_value)
            # Find the index where the previously served value should be inserted
            insert_index = 0
            for i, job in enumerate(remaining_jobs):
                if job < previously_served_value:
                    insert_index = i
                    break
            # Insert the previously served value at the appropriate position
            remaining_jobs.insert(insert_index, previously_served_value)

        # Extend the remaining jobs to y_values_arranged
        y_values_arranged.extend(remaining_jobs)



        # print("UP")

    
    print(direction)
    print(jobs)
    print(y_values_arranged)

    x_values = []

    # Append the starting position if it exists
    starting_position = input_values.get('starting_position')
    if starting_position is not None:
        x_values.append("Starting Position")

    # Append the job names based on the values in y_values_arranged
    previously_served_value = input_values.get('previously_served')
    previously_served_added = False  # Flag to track if the previously_served job has been added

    for job_value in y_values_arranged:
        if previously_served_value is not None and job_value == int(previously_served_value) and not previously_served_added:
            x_values.append("Previously Served")
            previously_served_added = True
            previously_served_value = None
        else:
            job_names = [k for k, v in input_values.items() if v == str(job_value) and k != 'starting_position']
            if job_names:
                job_name = next((name for name in job_names if name not in x_values), '')
                x_values.append(job_name)

    # Check if the previously served job is the last job in the list
    if previously_served_value is not None and int(previously_served_value) == y_values_arranged[-1] and not previously_served_added:
        x_values.append("Previously Served")

    print(x_values)

    # print(x_values)


    
    # Convert the yValues to JSON
    x_values_json = json.dumps(x_values)
    y_values_json = json.dumps(y_values_arranged)
    
    # Calculate THM
    # Parse JSON string to obtain the list of values
    y_values = json.loads(y_values_json)  

    thm = 0
    for i in range(len(y_values) - 1):
        diff = abs(int(y_values[i]) - int(y_values[i+1]))
        thm += diff
    
    # Calculate ST
   # Calculate ST
    st = 0
    ending_track = int(ending_track)
    starting_track = int(starting_track)
    # total_track = int(ending_track) 
    total_track = ending_track - starting_track +1
    if thm != 0:
        # st = total_track * int(arm_movement) / thm
        st = total_track * int(arm_movement) / thm
    st = round(st, 2)
    return render(request, 'diskscheduling/scanchart.html', {'input_values': input_values,'y_values_json': y_values_json,'x_values_json': x_values_json,'starting_track': starting_track,'ending_track': ending_track,'arm_movement':arm_movement,'thm': thm,'st':st,'jobs':jobs,'direction':direction})





def cscan(request, job_count=None, previously_served='', starting_position='', starting_track='', ending_track='', arm_movement=''):
    input_values = {}  # Dictionary to store the inputted values

    if request.method == 'POST':
        job_count = request.POST.get('job_count')
        previously_served = request.POST.get('previously_served', '')
        starting_position = request.POST.get('starting_position', '')
        starting_track = request.POST.get('starting_track', '')
        ending_track = request.POST.get('ending_track', '')
        arm_movement = request.POST.get('arm_movement', '')
        
        if job_count and job_count.isdigit():
            job_count = int(job_count)

            for i in range(1, job_count + 1):
                input_name = f'job_{i}'
                input_value = request.POST.get(input_name)
                input_values[input_name] = input_value

        input_values['previously_served'] = previously_served
        input_values['starting_position'] = starting_position
        input_values['starting_track'] = starting_track
        input_values['ending_track'] = ending_track
        input_values['arm_movement'] = arm_movement

    else:
        # Handle GET request or initial rendering
        # Populate input_values dictionary with previous values if available
        job_count = request.GET.get('job_count')
        previously_served = request.GET.get('previously_served', '')
        starting_position = request.GET.get('starting_position', '')
        starting_track = request.GET.get('starting_track', '')
        ending_track = request.GET.get('ending_track', '')
        arm_movement = request.GET.get('arm_movement', '')
        
        if job_count and job_count.isdigit():
            job_count = int(job_count)

            for i in range(1, job_count + 1):
                input_name = f'job_{i}'
                input_value = request.GET.get(input_name)
                input_values[input_name] = input_value

        input_values['previously_served'] = previously_served
        input_values['starting_position'] = starting_position
        input_values['starting_track'] = starting_track
        input_values['ending_track'] = ending_track
        input_values['arm_movement'] = arm_movement

    y_values_arranged = []

    # Set job_count to a default value of 0 if it is None
    job_count = job_count or 0

    # Create a list to hold the job values
    jobs = []

    # Append the job values
    for i in range(1, job_count + 1):
        input_name = f'job_{i}'
        input_value = input_values.get(input_name)
        if input_value is not None:
            jobs.append(int(input_value))

     # Sort the jobs in ascending order
    # Sort the jobs in ascending order
    jobs.sort()
    # print(jobs)

    # Start at the starting position
    starting_position = input_values.get('starting_position')
    current_position = int(starting_position)
    

    # Add the starting position to y_values_arranged
    y_values_arranged.append(current_position)

    if starting_position and previously_served:
        starting_position_value = int(starting_position)
        previously_served_value = int(previously_served)

        if starting_position_value > previously_served_value:
            direction = "UP"
        else:
            direction = "DOWN"
    else:
        direction = "NONE"

    if direction == "DOWN":
        # Append the job requests lower than the starting position in descending order
        for job in jobs:
            if job < current_position:
                y_values_arranged.append(job)

        # Sort the job requests in descending order
        y_values_arranged.sort(reverse=True)

        # Append the starting_position value
        y_values_arranged.append(starting_track)

        #PS MUNA BAGO IBA
        y_values_arranged.append(previously_served_value )
        
        #diretso ending track walang dadaanan na iba
        ending_track = input_values.get('ending_track')
        ending_track_value = int(ending_track)   # Decrease the value by 1
        y_values_arranged.append(ending_track_value)

        #Para makuha ang natitirang job request
        remaining_jobs = [job for job in jobs if job >= current_position]
        remaining_jobs.sort(reverse=True)
        
        #Para maadd sa array na y_values_arranged yung natitirang job
        for job in remaining_jobs:
            y_values_arranged.append(job)
        
        # print("Down")
    else:
        # Append the job requests higher than the starting position in ascending order
        for job in jobs:
            if job > current_position:
                y_values_arranged.append(job)

        # Sort the job requests in ascending order
        y_values_arranged.sort()

        # Append the ending_track value minus 1 if it's not already in the list
        ending_track = input_values.get('ending_track')
        ending_track_value = int(ending_track)  # Decrease the value by 1
        y_values_arranged.append(ending_track_value)

         #PS MUNA BAGO IBA
        y_values_arranged.append(previously_served_value )
        
        #diretso starting track walang dadaanan na iba
        y_values_arranged.append(starting_track)
        
        # Append the remaining job requests in descending order
        remaining_jobs = [job for job in jobs if job <= current_position]
        remaining_jobs.sort()

        # Extend the remaining jobs to y_values_arranged
        y_values_arranged.extend(remaining_jobs)



        # print("UP")

    
    # print(direction)
    # print(jobs)
    # print(y_values_arranged)

    x_values = []

    # Append the starting position if it exists
    starting_position = input_values.get('starting_position')
    if starting_position is not None:
        x_values.append("Starting Position")

    # Append the job names based on the values in y_values_arranged
    previously_served_value = input_values.get('previously_served')
    previously_served_added = False  # Flag to track if the previously_served job has been added

    for job_value in y_values_arranged:
        if previously_served_value is not None and job_value == int(previously_served_value) and not previously_served_added:
            x_values.append("Previously Served")
            previously_served_added = True
            previously_served_value = None
        else:
            job_names = [k for k, v in input_values.items() if v == str(job_value) and k != 'starting_position']
            if job_names:
                job_name = next((name for name in job_names if name not in x_values), '')
                x_values.append(job_name)

    # Check if the previously served job is the last job in the list
    if previously_served_value is not None and int(previously_served_value) == y_values_arranged[-1] and not previously_served_added:
        x_values.append("Previously Served")

    print(x_values)
    


    
    # Convert the yValues to JSON
    x_values_json = json.dumps(x_values)
    y_values_json = json.dumps(y_values_arranged)
    
    # Calculate THM
    # Parse JSON string to obtain the list of values
    y_values = json.loads(y_values_json)  

    thm = 0
    for i in range(len(y_values) - 1):
        diff = abs(int(y_values[i]) - int(y_values[i+1]))
        thm += diff
    
   # Calculate ST
    st = 0
    ending_track = int(ending_track)
    starting_track = int(starting_track)
    # total_track = int(ending_track) 
    total_track = ending_track - starting_track +1
    if thm != 0:
        # st = total_track * int(arm_movement) / thm
        st = total_track * int(arm_movement) / thm
    st = round(st, 2)
    return render(request, 'diskscheduling/cscanchart.html', {'input_values': input_values,'y_values_json': y_values_json,'x_values_json': x_values_json,'starting_track': starting_track,'ending_track': ending_track,'arm_movement':arm_movement,'thm': thm,'st':st,'jobs':jobs,'direction':direction})



#LOOK CALCULATIONS
def look(request, job_count=None, previously_served='', starting_position='', starting_track='', ending_track='', arm_movement=''):
    input_values = {}  # Dictionary to store the inputted values

    if request.method == 'POST':
        job_count = request.POST.get('job_count')
        previously_served = request.POST.get('previously_served', '')
        starting_position = request.POST.get('starting_position', '')
        starting_track = request.POST.get('starting_track', '')
        ending_track = request.POST.get('ending_track', '')
        arm_movement = request.POST.get('arm_movement', '')
        
        if job_count and job_count.isdigit():
            job_count = int(job_count)

            for i in range(1, job_count + 1):
                input_name = f'job_{i}'
                input_value = request.POST.get(input_name)
                input_values[input_name] = input_value

        input_values['previously_served'] = previously_served
        input_values['starting_position'] = starting_position
        input_values['starting_track'] = starting_track
        input_values['ending_track'] = ending_track
        input_values['arm_movement'] = arm_movement

    else:
        # Handle GET request or initial rendering
        # Populate input_values dictionary with previous values if available
        job_count = request.GET.get('job_count')
        previously_served = request.GET.get('previously_served', '')
        starting_position = request.GET.get('starting_position', '')
        starting_track = request.GET.get('starting_track', '')
        ending_track = request.GET.get('ending_track', '')
        arm_movement = request.GET.get('arm_movement', '')
        
        if job_count and job_count.isdigit():
            job_count = int(job_count)

            for i in range(1, job_count + 1):
                input_name = f'job_{i}'
                input_value = request.GET.get(input_name)
                input_values[input_name] = input_value

        input_values['previously_served'] = previously_served
        input_values['starting_position'] = starting_position
        input_values['starting_track'] = starting_track
        input_values['ending_track'] = ending_track
        input_values['arm_movement'] = arm_movement

    y_values_arranged = []

    # Set job_count to a default value of 0 if it is None
    job_count = job_count or 0

    # Create a list to hold the job values
    jobs = []

    # Append the job values
    for i in range(1, job_count + 1):
        input_name = f'job_{i}'
        input_value = input_values.get(input_name)
        if input_value is not None:
            jobs.append(int(input_value))

     # Sort the jobs in ascending order
    # Sort the jobs in ascending order
    jobs.sort()
    # print(jobs)

    # Start at the starting position
    starting_position = input_values.get('starting_position')
    current_position = int(starting_position)
    

    # Add the starting position to y_values_arranged
    y_values_arranged.append(current_position)

    if starting_position and previously_served:
        starting_position_value = int(starting_position)
        previously_served_value = int(previously_served)

        if starting_position_value > previously_served_value:
            direction = "UP"
        else:
            direction = "DOWN"
    else:
        direction = "NONE"

    if direction == "DOWN":
        # Append the job requests lower than the starting position in descending order
        for job in jobs:
            if job < current_position:
                y_values_arranged.append(job)

        # Sort the job requests in descending order
        y_values_arranged.sort(reverse=True)

        #Para makuha ang natitirang job request
        remaining_jobs = [job for job in jobs if job >= current_position]
        remaining_jobs.sort()

       # Check if there is a previously served value
        previously_served_value = input_values.get('previously_served')
        if previously_served_value is not None:
            previously_served_value = int(previously_served_value)
            # Find the index where the previously served value should be inserted
            insert_index = 0
            for i, job in enumerate(remaining_jobs):
                if job > previously_served_value:
                    insert_index = i
                    break
            # Insert the previously served value at the appropriate position
            remaining_jobs.insert(insert_index, previously_served_value)

        
        #Para maadd sa array na y_values_arranged yung natitirang job
        for job in remaining_jobs:
            y_values_arranged.append(job)
        
        # print("Down")
    else:
        # Append the job requests higher than the starting position in ascending order
        for job in jobs:
            if job > current_position:
                y_values_arranged.append(job)

        # Sort the job requests in ascending order
        y_values_arranged.sort()



        # Append the remaining job requests in descending order
        remaining_jobs = [job for job in jobs if job <= current_position]
        remaining_jobs.sort(reverse=True)

        # Check if there is a previously served value
        previously_served_value = input_values.get('previously_served')
        if previously_served_value is not None:
            previously_served_value = int(previously_served_value)
            # Find the index where the previously served value should be inserted
            insert_index = 0
            for i, job in enumerate(remaining_jobs):
                if job < previously_served_value:
                    insert_index = i
                    break
            # Insert the previously served value at the appropriate position
            remaining_jobs.insert(insert_index, previously_served_value)

        # Extend the remaining jobs to y_values_arranged
        y_values_arranged.extend(remaining_jobs)



        # print("UP")

    
    # print(direction)
    # print(jobs)
    # print(y_values_arranged)

    x_values = []

    # Append the starting position if it exists
    starting_position = input_values.get('starting_position')
    if starting_position is not None:
        x_values.append("Starting Position")

    # Append the job names based on the values in y_values_arranged
    previously_served_value = input_values.get('previously_served')
    previously_served_added = False  # Flag to track if the previously_served job has been added

    for job_value in y_values_arranged:
        if previously_served_value is not None and job_value == int(previously_served_value) and not previously_served_added:
            x_values.append("Previously Served")
            previously_served_added = True
            previously_served_value = None
        else:
            job_names = [k for k, v in input_values.items() if v == str(job_value) and k != 'starting_position']
            if job_names:
                job_name = next((name for name in job_names if name not in x_values), '')
                x_values.append(job_name)

    # Check if the previously served job is the last job in the list
    if previously_served_value is not None and int(previously_served_value) == y_values_arranged[-1] and not previously_served_added:
        x_values.append("Previously Served")

    print(x_values)


    
    # Convert the yValues to JSON
    x_values_json = json.dumps(x_values)
    y_values_json = json.dumps(y_values_arranged)
    
    # Calculate THM
    # Parse JSON string to obtain the list of values
    y_values = json.loads(y_values_json)  

    thm = 0
    for i in range(len(y_values) - 1):
        diff = abs(int(y_values[i]) - int(y_values[i+1]))
        thm += diff
    
   # Calculate ST
    st = 0
    ending_track = int(ending_track)
    starting_track = int(starting_track)
    # total_track = int(ending_track) 
    total_track = ending_track - starting_track +1
    if thm != 0:
        # st = total_track * int(arm_movement) / thm
        st = total_track * int(arm_movement) / thm
    st = round(st, 2)
    return render(request, 'diskscheduling/lookchart.html', {'input_values': input_values,'y_values_json': y_values_json,'x_values_json': x_values_json,'starting_track': starting_track,'ending_track': ending_track,'arm_movement':arm_movement,'thm': thm,'st':st,'jobs':jobs,'direction':direction})



#LOOK CALCULATIONS
def clook(request, job_count=None, previously_served='', starting_position='', starting_track='', ending_track='', arm_movement=''):
    input_values = {}  # Dictionary to store the inputted values

    if request.method == 'POST':
        job_count = request.POST.get('job_count')
        previously_served = request.POST.get('previously_served', '')
        starting_position = request.POST.get('starting_position', '')
        starting_track = request.POST.get('starting_track', '')
        ending_track = request.POST.get('ending_track', '')
        arm_movement = request.POST.get('arm_movement', '')
        
        if job_count and job_count.isdigit():
            job_count = int(job_count)

            for i in range(1, job_count + 1):
                input_name = f'job_{i}'
                input_value = request.POST.get(input_name)
                input_values[input_name] = input_value

        input_values['previously_served'] = previously_served
        input_values['starting_position'] = starting_position
        input_values['starting_track'] = starting_track
        input_values['ending_track'] = ending_track
        input_values['arm_movement'] = arm_movement

    else:
        # Handle GET request or initial rendering
        # Populate input_values dictionary with previous values if available
        job_count = request.GET.get('job_count')
        previously_served = request.GET.get('previously_served', '')
        starting_position = request.GET.get('starting_position', '')
        starting_track = request.GET.get('starting_track', '')
        ending_track = request.GET.get('ending_track', '')
        arm_movement = request.GET.get('arm_movement', '')
        
        if job_count and job_count.isdigit():
            job_count = int(job_count)

            for i in range(1, job_count + 1):
                input_name = f'job_{i}'
                input_value = request.GET.get(input_name)
                input_values[input_name] = input_value

        input_values['previously_served'] = previously_served
        input_values['starting_position'] = starting_position
        input_values['starting_track'] = starting_track
        input_values['ending_track'] = ending_track
        input_values['arm_movement'] = arm_movement

    y_values_arranged = []

    # Set job_count to a default value of 0 if it is None
    job_count = job_count or 0

    # Create a list to hold the job values
    jobs = []

    # Append the job values
    for i in range(1, job_count + 1):
        input_name = f'job_{i}'
        input_value = input_values.get(input_name)
        if input_value is not None:
            jobs.append(int(input_value))

     # Sort the jobs in ascending order
    # Sort the jobs in ascending order
    jobs.sort()
    # print(jobs)

    # Start at the starting position
    starting_position = input_values.get('starting_position')
    current_position = int(starting_position)
    

    # Add the starting position to y_values_arranged
    y_values_arranged.append(current_position)

    if starting_position and previously_served:
        starting_position_value = int(starting_position)
        previously_served_value = int(previously_served)

        if starting_position_value > previously_served_value:
            direction = "UP"
        else:
            direction = "DOWN"
    else:
        direction = "NONE"

    if direction == "DOWN":
        # Append the job requests lower than the starting position in descending order
        for job in jobs:
            if job < current_position:
                y_values_arranged.append(job)

        # Sort the job requests in descending order
        y_values_arranged.sort(reverse=True)

        # Find the highest job request
        highest_job = max(jobs)

        # Append the highest job request
        y_values_arranged.append(highest_job)

        # Retrieve the remaining job requests greater than or equal to the current position
        remaining_jobs = [job for job in jobs if job >= current_position]
        y_values_arranged.remove(highest_job)
        remaining_jobs.sort(reverse=True)
    
        # # Add the remaining job requests to y_values_arranged
        # y_values_arranged.extend(remaining_jobs)
        
       # Check if there is a previously served value
        previously_served_value = input_values.get('previously_served')
        if previously_served_value is not None:
            previously_served_value = int(previously_served_value)
            # Find the index where the previously served value should be inserted
            insert_index = 0
            for i, job in enumerate(remaining_jobs):
                if job == highest_job:
                    insert_index = i+1
                    break
            # Insert the previously served value at the appropriate position
            remaining_jobs.insert(insert_index, previously_served_value)
            remaining_jobs.sort(reverse=True)
        
        #Para maadd sa array na y_values_arranged yung natitirang job
        for job in remaining_jobs:
            y_values_arranged.append(job)
        
        # print("Down")
    else:
        # Append the job requests higher than the starting position in ascending order
        for job in jobs:
            if job > current_position:
                y_values_arranged.append(job)

        # Sort the job requests in ascending order
        y_values_arranged.sort()

        # Find the lowest job request
        lowest_job = min(jobs)
        # # Find the highest job request
        # highest_job = max(jobs)

        # Append the lowest job request
        y_values_arranged.append(lowest_job)

        # Retrieve the remaining job requests
        remaining_jobs = [job for job in jobs if job != lowest_job and job <= current_position]

        # Sort the remaining job requests in ascending order
        remaining_jobs.sort()
        
        # Check if there is a previously served value
        previously_served_value = input_values.get('previously_served')
        if previously_served_value is not None:
            previously_served_value = int(previously_served_value)
            # Find the index where the previously served value should be inserted
            insert_index = 0
            for i, job in enumerate(remaining_jobs):
                if job == lowest_job:
                    insert_index = i+1
                    break
            # Insert the previously served value at the appropriate position
            remaining_jobs.insert(insert_index, previously_served_value)
            remaining_jobs.sort()
        
        #Para maadd sa array na y_values_arranged yung natitirang job
        for job in remaining_jobs:
            y_values_arranged.append(job)
        # # Retrieve the remaining job requests greater than or equal to the current position
        # remaining_jobs = [job for job in jobs if job >= current_position]
        # remaining_jobs.sort(reverse=True)
        

        # # Check if there is a previously served value
        # previously_served_value = input_values.get('previously_served')
        # if previously_served_value is not None:
        #     previously_served_value = int(previously_served_value)
        #     # Check if the previously served value should be inserted
        #     if previously_served_value in remaining_jobs:
        #         # Find the index where the previously served value should be inserted
        #         insert_index = remaining_jobs.index(previously_served_value)
        #         # Insert the previously served value at the appropriate position
        #         remaining_jobs.insert(insert_index, previously_served_value)

        # # Iterate over the remaining jobs and remove them from the list as they are served
        # for job in remaining_jobs:
        #     y_values_arranged.append(job)
        #     remaining_jobs.remove(job)

        # print(remaining_jobs)
        # Check if there is a previously served value
        # previously_served_value = input_values.get('previously_served')
        # if previously_served_value is not None:
        #     previously_served_value = int(previously_served_value)
        #     # Find the index where the previously served value should be inserted
        #     insert_index = 0
        #     for i, job in enumerate(remaining_jobs):
        #         if job < previously_served_value:
        #             insert_index = i
        #             break
        #     # Insert the previously served value at the appropriate position
        #     remaining_jobs.insert(insert_index, previously_served_value)

        # # Extend the remaining jobs to y_values_arranged
        # y_values_arranged.extend(remaining_jobs)


        # print("UP")

    print(direction)
    print(jobs)
    print(y_values_arranged)

    x_values = []

    # Append the starting position if it exists
    starting_position = input_values.get('starting_position')
    if starting_position is not None:
        x_values.append("Starting Position")

    # Append the job names based on the values in y_values_arranged
    previously_served_value = input_values.get('previously_served')
    previously_served_added = False  # Flag to track if the previously_served job has been added

    for job_value in y_values_arranged:
        if previously_served_value is not None and job_value == int(previously_served_value) and not previously_served_added:
            x_values.append("Previously Served")
            previously_served_added = True
            previously_served_value = None
        else:
            job_names = [k for k, v in input_values.items() if v == str(job_value) and k != 'starting_position']
            if job_names:
                job_name = next((name for name in job_names if name not in x_values), '')
                x_values.append(job_name)

    # Check if the previously served job is the last job in the list
    if previously_served_value is not None and int(previously_served_value) == y_values_arranged[-1] and not previously_served_added:
        x_values.append("Previously Served")

    print(x_values)


    
    # Convert the yValues to JSON
    x_values_json = json.dumps(x_values)
    y_values_json = json.dumps(y_values_arranged)
    
    # Calculate THM
    # Parse JSON string to obtain the list of values
    y_values = json.loads(y_values_json)  

    thm = 0
    for i in range(len(y_values) - 1):
        diff = abs(int(y_values[i]) - int(y_values[i+1]))
        thm += diff
    
   # Calculate ST
    st = 0
    ending_track = int(ending_track)
    starting_track = int(starting_track)
    # total_track = int(ending_track) 
    total_track = ending_track - starting_track +1
    if thm != 0:
        # st = total_track * int(arm_movement) / thm
        st = total_track * int(arm_movement) / thm
    st = round(st, 2)
    return render(request, 'diskscheduling/clookchart.html', {'input_values': input_values,'y_values_json': y_values_json,'x_values_json': x_values_json,'starting_track': starting_track,'ending_track': ending_track,'arm_movement':arm_movement,'thm': thm,'st':st,'jobs':jobs,'direction':direction})
