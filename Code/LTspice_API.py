import subprocess
import ltspice
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, url_for
import os

app = Flask(__name__,static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_ltspice', methods=['POST'])
def run_ltspice():
    R1 = float(request.form['R1'])
    R = float(request.form['R'])
    Z1 = float(request.form['Z1'])
    Z = float(request.form['Z'])
    L1 = float(request.form['L1'])
    L = float(request.form['L'])
    dielectric_constant = float(request.form['dielectric_constant'])

    TD1 = L1 * np.sqrt(dielectric_constant) * 1e6 / 299792458
    TD = L * np.sqrt(dielectric_constant) * 1e6 / 299792458

    # Define netlist string
    netlist_string =    '../Simulations/Star.asc\n' \
                        'V1 N008 0 PULSE(0 3.3 0 2e-9 1.5e-9 0.8e-8 2e-8)\n' \
                        'R1 N004 N008 14\n' \
                        'C1 N004 0 20e-12\n' \
                        'R2 N005 N004 {R1}\n' \
                        'T1 N005 0 N001 0 Td={L1} Z0={Z1}\n' \
                        'T2 N002 0 N003 0 Td={L} Z0={Z}\n' \
                        'T3 N006 0 N007 0 Td={L} Z0={Z}\n' \
                        'T4 N009 0 N010 0 Td={L} Z0={Z}\n' \
                        'R3 N002 N001 {R}\n' \
                        'R4 N006 N001 {R}\n' \
                        'R5 N009 N001 {R}\n' \
                        'R6 N003 0 1e6\n' \
                        'R7 N007 0 1e6\n' \
                        'R8 N010 0 1e6\n' \
                        '.tran 4e-8\n' \
                        '.params R1 = '+str(R1)+'\n' \
                        '.params R = '+str(R)+'\n' \
                        '.params Z1 = '+str(Z1)+'\n' \
                        '.params Z = '+str(Z)+'\n' \
                        '.params L1 = '+str(TD1)+'n\n' \
                        '.params L = '+str(TD)+'n\n' \
                        '.backanno' \
                        '.end'
    
    filepath_netlist = "../Simulations/Star.net"
    filepath_raw = "../Simulations/Star.raw"
    filepath_cir = "../Simulations/Star.cir"

    # Update netlist with netlist string
    with open(filepath_netlist, "w") as netlist:
        netlist.write(netlist_string)

    # Convert netlist to *.cir file
    with open(filepath_netlist, "r") as netlist:
        netlist_content = netlist.read()
    with open(filepath_cir, "w") as cir:
        cir.write(netlist_content)

    # Run simulation and application to create raw file
    subprocess.run(['C:\\Program Files\\LTC\\LTspiceXVII\\XVIIx64.exe', '-b', '-Run', '-cir', filepath_cir])

    # Read raw file using ltspice
    l = ltspice.Ltspice(filepath_raw)
    l.parse()
    time = l.get_time()
    value = l.get_data('V(n003)')

    # Plotting
    plt.clf()   
    plt.plot(time, value)
    plt.grid()
    plt.xlabel("Time")
    plt.ylabel("Voltage")
    
    # Save plot image
    plot_dir = os.path.join(app.root_path, 'static')  # Get the path to the static directory
    plot_path = os.path.join(plot_dir, 'plot.png')  # Define the path to the plot image
    plt.savefig(plot_path)

    return render_template('index.html', plot_generated=True, plot_path=url_for('static', filename='plot.png'))

@app.route('/run_ltspice2', methods=['POST'])
def run_ltspice2():
    RT = float(request.form['RT'])
    L1 = float(request.form['L1'])
    L2 = float(request.form['L2'])
    L3 = float(request.form['L3'])
    L4 = float(request.form['L4'])
    L5 = float(request.form['L5'])
    Z = float(request.form['Z'])
    dielectric_constant = float(request.form['dielectric_constant'])
    c0 = 299792458 

    TD1 = L1*np.sqrt(dielectric_constant)*1e6/c0
    TD2 = L2*np.sqrt(dielectric_constant)*1e6/c0
    TD3 = L3*np.sqrt(dielectric_constant)*1e6/c0
    TD4 = L4*np.sqrt(dielectric_constant)*1e6/c0
    TD5 = L5*np.sqrt(dielectric_constant)*1e6/c0

    # Array for data processing
    data_temp = np.zeros((8000,2))
    data = np.zeros((8000,0))

    # Define netlist string
    netlist_string =    '\n' \
                        'V1 N007 0 PULSE(0 1.5 0 2e-9 1.5e-9 0.875e-8 2e-8)\n' \
                        'R1 N002 N007 31\n' \
                        'C1 N002 0 20e-12\n' \
                        'T1 N002 0 N003 0 Td={TD1} Z0={Z}\n' \
                        'T3 N003 0 N004 0 Td={TD2} Z0={Z}\n' \
                        'T4 N003 0 N008 0 Td={TD5} Z0={Z}\n' \
                        'R8 N008 0 1e6\n' \
                        'T2 N004 0 N009 0 Td={TD5} Z0={Z}\n' \
                        'R2 N009 0 1e6\n' \
                        'T5 N004 0 N005 0 Td={TD3} Z0={Z}\n' \
                        'T6 N005 0 N006 0 Td={TD4} Z0={Z}\n' \
                        'T7 N005 0 N010 0 Td={TD5} Z0={Z}\n' \
                        'R3 N010 0 1e6\n' \
                        'V2 N001 0 0.75\n' \
                        'R4 N001 N006 {RT}\n' \
                        '.tran 4e-8\n' \
                        '.params RT = '+str(RT)+'\n' \
                        '.params L1 = '+str(TD1)+'n\n' \
                        '.params L2 = '+str(TD2)+'n\n' \
                        '.params L3 = '+str(TD3)+'n\n' \
                        '.params L4 = '+str(TD5)+'n\n' \
                        '.params L5 = '+str(TD4)+'n\n' \
                        '.params Z = '+str(Z)+'\n' \
                        '.backanno' \
                        '.end'
    
    filepath_netlist = "../Simulations/DaisyChain.net"
    filepath_raw = "../Simulations/DaisyChain.raw"
    filepath_cir = "../Simulations/DaisyChain.cir"
    filepath_asc = "../Simulations/DaisyChain.asc"
    filepath_save_data = "../Data/Simulation_Data.csv"

    # Update netlist with netlist string
    netlist = open(filepath_netlist,"w")
    netlist.write(netlist_string)
    netlist.close()

    # Convert netlist to *.cir file
    netlist = open(filepath_netlist,"r")
    netlist_content = netlist.read()
    netlist.close()
    cir = open(filepath_cir,"w")
    cir.write(netlist_content)
    cir.close()

    # Run simulation and application to create raw file
    simulation_run = subprocess.Popen('"C:\Program Files\LTC\LTspiceXVII\XVIIx64.exe" -b -Run -cir ""../Simulations/DaisyChain.cir"')
    
    # Wait for completion
    checker = True
    while checker:
        poll = simulation_run.poll()
        if poll is None:
            pass
        else:
            checker=False

    # Read raw file using ltspice
    l = ltspice.Ltspice(filepath_raw)
    l.parse()
    time = l.get_time()
    value = l.get_data('V(n008)')
    value2 = l.get_data('V(n009)')
    value3 = l.get_data('V(n010)')

    # Plotting
    plt.clf()   
    plt.plot(time, value, label="IC2")
    plt.plot(time,value2, label="IC3")
    plt.plot(time,value3, label="IC4")
    plt.grid()
    plt.legend(loc="upper right")
    plt.xlabel("Time")
    plt.ylabel("Voltage")

    # Write data to variable
    for x in range (len(time)):
        data_temp[x][0] = time[x]
        data_temp[x][1] = value[x]
    data = np.append(data,data_temp,axis=1)
    #print(data_temp)
                
    # Kill simulation and application   
    simulation_run.kill()    
    
    # Save plot image
    plot2_dir = os.path.join(app.root_path, 'static')  # Get the path to the static directory
    plot2_path = os.path.join(plot2_dir, 'plot2.png')  # Define the path to the plot image
    plt.savefig(plot2_path)

    return render_template('index.html', plot2_generated=True, plot2_path=url_for('static', filename='plot2.png'))

if __name__ == '__main__':
    app.run(debug=True)





# =====================================================================================

# import subprocess
# import ltspice
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt

# # Define directories
# filepath_netlist = "../Simulations/Star.net"
# filepath_raw = "../Simulations/Star.raw"
# filepath_asc = "../Simulations/Star.asc"
# filepath_cir = "../Simulations/Star.cir"

# filepath_save_data = ""

# # Parameters values input
# R1 = 15                                         # Value for resistor R1 [Ohm] (INPUT)
# R = 50                                          # Value for resistor R [Ohm] (INPUT)
# Z1 = 50                                         # Value for characteristic impedance Z1 [Ohm] (INPUT)
# Z = 50                                          # Value for characteristic impedance Z [Ohm] (INPUT)
# L1 = 100                                        # Value for transmission line length L1 [mm] (INPUT)
# L = 50                                          # Value for transmission line length L [mm] (INPUT)
# dielectric_constant = 4.5                       # Dielectric constant of the PCB material [Dimensionless] (INPUT)
# c0 = 299792458                                  # Speed of light (constant)

# TD1 = L1*np.sqrt(dielectric_constant)*1e6/c0
# TD = L*np.sqrt(dielectric_constant)*1e6/c0

# # Array for data processing
# data_temp = np.zeros((8000,2))
# data = np.zeros((8000,0))
    
# # Define netlist string
# netlist_string =    'C:\\Users\\julia\\Documents\\Projektgruppe2324\\ChatBot\\ChatBot-240130\\Simulations\\Star.asc\n' \
#                     'V1 N008 0 PULSE(0 3.3 0 2e-9 1.5e-9 0.8e-8 2e-8)\n' \
#                     'R1 N004 N008 14\n' \
#                     'C1 N004 0 20e-12\n' \
#                     'R2 N005 N004 {R1}\n' \
#                     'T1 N005 0 N001 0 Td={L1} Z0={Z1}\n' \
#                     'T2 N002 0 N003 0 Td={L} Z0={Z}\n' \
#                     'T3 N006 0 N007 0 Td={L} Z0={Z}\n' \
#                     'T4 N009 0 N010 0 Td={L} Z0={Z}\n' \
#                     'R3 N002 N001 {R}\n' \
#                     'R4 N006 N001 {R}\n' \
#                     'R5 N009 N001 {R}\n' \
#                     'R6 N003 0 1e6\n' \
#                     'R7 N007 0 1e6\n' \
#                     'R8 N010 0 1e6\n' \
#                     '.tran 4e-8\n' \
#                     '.params R1 = '+str(R1)+'\n' \
#                     '.params R = '+str(R)+'\n' \
#                     '.params Z1 = '+str(Z1)+'\n' \
#                     '.params Z = '+str(Z)+'\n' \
#                     '.params L1 = '+str(TD1)+'n\n' \
#                     '.params L = '+str(TD)+'n\n' \
#                     '.backanno' \
#                     '.end'
                                                
#  # Update netlist with netlist string
# netlist = open(filepath_netlist,"w")
# netlist.write(netlist_string)
# netlist.close()

# # Convert netlist to *.cir file
# netlist = open(filepath_netlist,"r")
# netlist_content = netlist.read()
# netlist.close()
# cir = open(filepath_cir,"w")
# cir.write(netlist_content)
# cir.close()

# # Run simulation and application to create raw file
# simulation_run = subprocess.Popen('"C:\Program Files\LTC\LTspiceXVII\XVIIx64.exe" -b -Run -cir ""../Simulations/Star.cir"')

# # Wait for completion
# checker = True
# while checker==True:
#     poll = simulation_run.poll()
#     if poll is None:
#         pass
#     else:
#         checker=False
    
# # Read raw file using ltspice
# l = ltspice.Ltspice(filepath_raw)
# l.parse()
# time = l.get_time()
# value = l.get_data('V(n003)')
# #print(time)
# #print(value)

# # Plotting
# plt.plot(time, value)
# plt.grid()
# plt.xlabel("Time")
# plt.ylabel("Voltage")
  
# # Write data to variable
# #for x in range (len(time)):
# #    data_temp[x][0] = time[x]
# #    data_temp[x][1] = value[x]
# #data = np.append(data,data_temp,axis=1)
# #print(data_temp)
            
# # Kill simulation and application   
# simulation_run.kill()

# # Show plot
# # plt.show()
# plt.savefig("plot.png")

# # Export data to *.csv file
# #df = pd.DataFrame(data)
# #print(df)
# #df.to_csv(filepath_save_data, index=False, header=False)