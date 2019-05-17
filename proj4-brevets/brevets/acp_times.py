"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow

#  Note for CIS 322 Fall 2016:
#  You MUST provide the following two functions
#  with these signatures, so that I can write
#  automated tests for grading.  You must keep
#  these signatures even if you don't use all the
#  same arguments.  Arguments are explained in the
#  javadoc comments.

# Brevet Calculation Based Table of the format: [maximum speed, minimum speed, control location difference
SPEED_CONTROLS = [[34,15,200],[32,15,200],[30,15,200],[28,11.428,400],[26,13.333,300]]
# Overall time limits vary for each brevet according to the distance. These are [hours,minutes,distance (km)]
TIME_LIMITS = {200:[13,30],400:[27,0],600:[40,0],1000:[75,0]}
# The last controle distance should be between the brevet distance and that distance plus 10%.
ACCEPTABLE_RANGE = 1.10


def get_time(control_dist_km, brevet_dist_km, brevet_start_time,index):
  """
  Args:
     control_dist_km:  number, the control distance in kilometers
     brevet_dist_km: number, the nominal distance of the brevet
         in kilometers, which must be one of 200, 300, 400, 600,
         or 1000 (the only official ACP brevet distances)
     brevet_start_time:  An ISO 8601 format date-time string indicating
         the official start time of the brevet
     index: used to grab maximumn and minimum speeds from the SPEED_CONTROLS table, the index value will be 0 for open times
         and 1 for close times
  Returns:
     An ISO 8601 format date string indicating the control open time.
     This will be in the same time zone as the brevet start time.
  """
  # Special Case: the control distance entered is the starting point (0 km)
  if (control_dist_km == 0):
    return arrow.get(brevet_start_time).shift(hours=+index).isoformat()
  # The control distance is outside the regulated acceptable range
  if (control_dist_km > brevet_dist_km * ACCEPTABLE_RANGE):
      return None
  # The Control distance is within the regulated acceptable range
  if (control_dist_km >= brevet_dist_km):
    control_dist_km = brevet_dist_km
    if (index == 1):
      h = TIME_LIMITS[control_dist_km][0]
      m = TIME_LIMITS[control_dist_km][1]
      return arrow.get(brevet_start_time).shift(hours=+h,minutes=+m).isoformat()

  time_shift = 0.0
  for row in SPEED_CONTROLS:
    if control_dist_km <= 0:
      continue
    if control_dist_km > row[2]:
      time_shift += row[2] / row[index]
    else:
      time_shift += (control_dist_km / row[index])
    control_dist_km -= row[2]

  h = int(time_shift)
  m = round(time_shift * 60) % 60
  print("Hours: ",h," Minutes: ",m)
  return arrow.get(brevet_start_time).shift(hours=+h,minutes=+m).isoformat()


def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    return get_time(control_dist_km,brevet_dist_km,brevet_start_time,0)


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet
       in kilometers, which must be one of 200, 300, 400, 600, or 1000
       (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    return get_time(control_dist_km,brevet_dist_km,brevet_start_time,1)
