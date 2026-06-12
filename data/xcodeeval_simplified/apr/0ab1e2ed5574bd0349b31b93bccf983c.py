time_input = input().split(":")
if int(time_input[0][::-1]) >= int(time_input[1]):
    print(int(time_input[0][::-1]) - int(time_input[1]))
else:
    minutes = int(time_input[1])
    hours = int(time_input[0])
    answer = 0
    while True:
        minutes += 1
        answer += 1
        if minutes == 60:
            minutes = 0
            hours += 1
            if hours == 24:
                hours = 0
                time_str = "00:00"
            else:
                if len(str(hours)) == 1:
                    time_str = "0" + str(hours) + "00"
                else:
                    time_str = str(hours) + "00"
        else:
            if len(str(minutes)) == 1:
                if len(str(hours)) == 1:
                    time_str = "0" + str(hours) + "0" + str(minutes)
                else:
                    time_str = str(hours) + "0" + str(minutes)
            else:
                if len(str(hours) == 1):
                    time_str = "0" + str(hours) + str(minutes)
                else:
                    time_str = str(hours) + str(minutes)
        if time_str == time_str[::-1]:
            print(answer)
            break
