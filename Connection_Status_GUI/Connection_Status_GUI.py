from definitions import checkPing
from os import path
from subprocess import check_output
import csv
import time

#Connection Status GUI v1.0.1
#Samuel Bravo
#02/06/2020

while(True):
    ####################################################################################################
    #Extract the hosts information
    hosts_info = []
    print("Getting hosts information")
    #make sure the host file exists
    if path.exists("hosts.csv") == False:
        print("Error: hosts.csv not found. Create the file and add it to the same directory as main.py")
        os.system("pause")
        exit()
    else:
        with open("hosts.csv") as csvFile:
            csvReader = csv.reader(csvFile, delimiter=',')
            for row in csvReader:
                #if the line contains data AND doesnt start with #, append it
                #List elements format: ipaddress,hostname,boolean
                if row:
                    hosts_info.append(row)
            csvFile.close()
    print("host info extracted successfully\nBeginning connection tests...\n")
    ####################################################################################################
    #Check the connection periodically to each host, track the results forever
    for host in hosts_info:
        if host[0].find("#") == -1:
            connection_status = checkPing(host[0])
            if connection_status == True:
                host[3] = "UP"
            else:
                host[3] = "DOWN"

    ####################################################################################################
    #Start generating the HTML file
    current_time = check_output("time /T", shell=True).decode()
    current_time = current_time[0:len(current_time) -2 ] #removes the \r\n from the end of the output
    out_file = open("index.html","w")
    print("Writting HTML file...\n")
    out_file.write('<!DOCTYPE html>\n' + 
                   '<html lang="en" xmlns="http://www.w3.org/1999/xhtml">\n' +
                   '<head>\n' + 
                   '<meta http-equiv="refresh" content="5"; URL="index.html" />\n' + 
                   '<title>Somerset Connection Status</title>\n' +
                   '<style>\n' + 
                   '.masonary{\ncolumn-count: 5;\ncolumn-gap: 1em;\nwidth: 20%;\n}\n' +
                   '.item{\nbackground-color: #eee;\ndisplay: inline-block;\nmargin: 0 0 1em;\nwidth: 30;\nfont-size: .75em;\n}\n' + 
                   '.normal_font{\nfont-weight: normal;\n}\n' + 
                   '</style>\n' + 
                   '</head>\n<body>\n' + 
                   '<p align="center"><strong>Somerset Connection Status: Updated@ ' + current_time + '</strong></p>\n' + 
                   '<div class="masonry">\n')

    ####################################################################################################
    #generate the html file
    counter = 0              #controls the number of rows in each table
    first_table = True       #
    color_controller = True  #controls the transition between 2 cell colors
    color_failed = ' bgcolor="red" '
    max_rows = 21            #controls the number of rows in each table plus the header (table_size = max_rows+headers)

    for line in hosts_info:
        #Control the cells color so that each new table set transitions between white and grey.
        if color_controller == True:
            cell_color = ' bgcolor="cyan" '
        else:
            cell_color = ' bgcolor="khaki" '

    ####################################################################################################
        #every n rows, create a new table.
        if counter == 0:
            counter = counter + 1
            #if this is the first table, do this
            if first_table:
                out_file.write('<table class="item" border="1" valign="top">\n')
                first_table = False
            else:
                out_file.write('</table>\n')
                out_file.write('<table class="item" border="1" valign="top">\n')

            #Now create the tables header using the current line of hosts_info
            #If the current line begins with a '#' make the header bold
            if line[0].find("#") > -1:
                out_file.write("<tr>\n")
                out_file.write("<th bgcolor='orange'>" + line[0][1:] + "</th>\n")
                out_file.write("<th bgcolor='orange' width='6'>Status</th>\n")
                out_file.write("</tr>\n")
            else:
                #Determine if the hosts connection was UP or DOWN. if its DOWN set cell color to color_failed (red)
                if line[3] == "DOWN":
                    out_file.write('<tr><th ' + color_failed + ' align="left" class="normal_font">' + line[2] + '</th>\n')
                    out_file.write('<th ' + color_failed + 'align="left" class="normal_font">' + line[3] + '</th></tr>\n')
                else:
                    out_file.write('<tr><th ' + cell_color + ' align="left" class="normal_font">' + line[2] + '</th>\n')
                    out_file.write('<th ' + cell_color + 'align="left" class="normal_font">' + line[3] + '</th></tr>\n')
    
    ####################################################################################################
        #If max_rows hasn't been reached yet, create a new row
        else:
            #Every time a line comment is hit make those cells bold and change the color for the preceeding cells.
            if line[0].find("#") > -1:
                #switch the color_controller
                if color_controller == True:
                    color_controller = False
                else:
                    color_controller = True
                #Control the cells color so that each new table set transitions between white and grey.
                if color_controller == True:
                    cell_color = ' bgcolor="orange" '
                else:
                    cell_color = ' bgcolor="orange" '
                #create the row with bold font and the cell color
                out_file.write("<tr>\n")
                out_file.write("<td" + cell_color + "><strong>" + line[0][1:] + "</strong></td>\n")
                out_file.write("<td " + cell_color + "width='6'><strong>Status</strong></td>\n")
                out_file.write("</tr>\n")

            else:
                if line[3] == "DOWN":
                    out_file.write('<tr><td' + color_failed + '>' + line[2] + '</td>\n')
                    out_file.write('<td ' + color_failed + 'width="6">' + line[3] + '</td></tr>\n')
                else:
                    out_file.write('<tr><td' + cell_color + '>' + line[2] + '</td>\n')
                    out_file.write('<td ' + cell_color + 'width="6">' + line[3] + '</td></tr>\n')

            #if max_rows rows have been reached, reset the counter to create a new table
            if counter >= max_rows:
                counter = 0
            else:
                counter = counter+1

    out_file.write("</table>\n")
    out_file.write("</div>\n</body>\n</html>\n")
    out_file.close()

    print("Beginning timer for 10 seconds\n")
    time.sleep(10)








