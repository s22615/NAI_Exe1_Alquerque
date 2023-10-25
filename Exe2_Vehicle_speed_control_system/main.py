import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
import math
from skfuzzy import control as ctrl

"""
==========================================
Fuzzy Logic: Vehicle speed control system
==========================================

Author
    Sebastian Mackiewicz - PJAIT student

Let's create a fuzzy control system which models how fast your vehicle should go to provide the greatest safety for driver.
When driving, you consider humidity, air clarity and traffic congestion
rated between 1% and 100%. After calculation you get information about how fast you going and what should do next? 
Reduce your current speed(and by how much) or nothing because your speed is just fine

We would formulate this problem as:

* Antecednets (Inputs)
   - `humidity`
      * Universe: What humidity value is? (from 1 to 100 %)
      * Fuzzy set: low, medium, high
   - `air_clarity`
      * Universe: What air clarity value is? (from 1 to 100 %)
      * Fuzzy set: low, medium, high
   - `traffic_congestion`
      * Universe: What traffic congestion value is? (from 1 to 100 %)
      * Fuzzy set: low, medium, high
   - `traffic_congestion`
      * What is your current speed? (in km/h)
* Consequents (Outputs)
   - `safe_speed`
      * Universe: How fast should vehicle move from 60 to 120 km/h
      * Fuzzy set: low, medium, high
* Rules
   - If the humidity is poor OR air clarity is poor OR traffic congestion is poor, 
   then the safe speed will be low
   - If the humidity is average OR air clarity is average OR traffic congestion is average,
   then the safe speed will be medium
   - If the humidity is good OR air clarity is good OR traffic congestion is good,
   then the safe speed will be high.
* Usage
   - If I tell this controller that I rated:
      * the humidity as 25, and
      * the air_clarity as 50, and
      * the traffic_congestion as 75,
   - it would recommend that you should reduce speed by around:
      * 25 km/h. Because your current speed is 120 km/h and safe speed is around 94 km/h
    
To run program install
pip install scikit-fuzzy
pip install matplotlib
"""

# New Antecedent/Consequent objects hold universe variables and membership
# functions
humidity = ctrl.Antecedent(np.arange(0, 101, 1), 'humidity')
air_clarity = ctrl.Antecedent(np.arange(0, 101, 1), 'air_clarity')
traffic_congestion = ctrl.Antecedent(np.arange(0, 101, 1), 'traffic_congestion')
safe_speed = ctrl.Consequent(np.arange(61, 121, 1), 'safe_speed')

# Auto-membership function population is possible with .automf(3, 5, or 7)
humidity.automf(3)
air_clarity.automf(3)
traffic_congestion.automf(3)

# Custom membership functions can be built interactively with a familiar,
# Pythonic API
safe_speed['low'] = fuzz.trimf(safe_speed.universe, [61, 81, 81])
safe_speed['medium'] = fuzz.trimf(safe_speed.universe, [81, 101, 121])
safe_speed['high'] = fuzz.trimf(safe_speed.universe, [101, 121, 121])

"""
Making plots for data visualization
"""
humidity['average'].view()
air_clarity['average'].view()
traffic_congestion['average'].view()
safe_speed.view()

"""
Setting rules for fuzzy logic
"""
rule1 = ctrl.Rule(humidity['poor'] | air_clarity['poor'] | traffic_congestion['poor'], safe_speed['high'])
rule2 = ctrl.Rule(humidity['average'] | air_clarity['average'] | traffic_congestion['average'], safe_speed['medium'])
rule3 = ctrl.Rule(humidity['good'] | air_clarity['good'] | traffic_congestion['good'], safe_speed['low'])

"""
Creating control system with previous defined rules
"""
speed_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])

"""
Creating control system simulation
"""
final_speed = ctrl.ControlSystemSimulation(speed_ctrl)

"""
Declaring our inputs and calling compute method
"""
final_speed.input['humidity'] = 25
final_speed.input['air_clarity'] = 50
final_speed.input['traffic_congestion'] = 75
car_speed = 120

final_speed.compute()

"""
Based on final speed number displaying message
"""
message_reduce = 'You should reduce your speed by %d km/h.' % (car_speed - math.ceil(final_speed.output['safe_speed']))
message_ok = 'Your speed is just fine. Safe speed was %d km/h.' % math.ceil(final_speed.output['safe_speed'])
final_mess = message_reduce if car_speed > final_speed.output['safe_speed'] else message_ok

"""
Once computed, we can view the result as well as visualize it.
"""
print('Your current speed is %s km/h. \n%s' % (car_speed, final_mess))
safe_speed.view(sim=final_speed)
plt.show()