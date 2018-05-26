'''Your task is to find the angle of the sun above the horizon knowing the time of the day.
Input data: the sun rises in the East at 6:00 AM, which corresponds to the angle of 0 degrees.
 At 12:00 PM the sun reaches its zenith, which means that the angle equals 90 degrees.
 6:00 PM is the time of the sunset so the angle is 180 degrees.
 If the input will be the time of the night (before 6:00 AM or after 6:00 PM),
your function should return - "I don't see the sun!".
'''


def sun_angle(time: str):
    #replace this for solution
    hour,mint = time.split(":")
    hour = int(hour)
    mint = int(mint)
    if hour > 6 and hour <18:
        angle = float(((hour-6)*60 + mint)*(90/360))
        if angle.is_integer():
            return int(angle)
        else:
            return angle
    else:
        return "I don't see the sun!"

if __name__ == '__main__':
    print("Example:")
    print(sun_angle("07:00"))

    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert sun_angle("07:00") == 15
    assert sun_angle("01:23") == "I don't see the sun!"
    print("Coding complete? Click 'Check' to earn cool rewards!")