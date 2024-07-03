"""
File: the_internet.py
Author: Josh Ventura
Date: 12/02/2021
Section: 35
E-mail: j246@umbc.edu
Description: This python closely resembles the build of the internet


"""

def run_the_internet():
    websites = {}
    connection = {}
    user_input = input(">>> ")
    while user_input.lower() != "quit":
            #split user input into a list
        user_input = user_input.split(" ")
            #creating server

        # CREATES A SERVER
        if user_input[0] == "create-server":
            websites[user_input[1]] = user_input[2]
            print("Success: A server with the name", user_input[1], "was created at ip", user_input[2])
            print(websites)

        if user_input[1]in websites and user_input[2] in websites:
        ## CREATES A CONNECTION
            if user_input[0] == "create-connection":
                if user_input[1] and user_input[2] in websites:

                    if user_input[1] in connection:
                        connection[user_input[1]].append([user_input[2],int(user_input[3])])

                    if user_input[2] in connection:
                        connection[user_input[2]].append([user_input[1],int(user_input[3])])

                    if user_input[1] not in connection:
                        connection[user_input[1]] = [[user_input[2],int(user_input[3])]]

                    if user_input[2] not in connection:
                        connection[user_input[2]] = [[user_input[1],int(user_input[3])]]

                    print("Success: A server with the name",user_input[1],"is now connected to",user_input[2])
                    print(connection)

                else:
                    print("One or more servers are not reachable")

        # SETS SERVERS
        elif user_input[0] == "set-server":
            for element in websites.keys():
                if websites[element] == user_input[1]:
                    server_home = element
                else:
                    server_home = user_input[1]
            print("Server", server_home,"selected.")


        # PINGS SITES VISITED
        elif user_input[0] == "ping":
            if user_input[0] == "ping":
                ping_flag = 0

                if server_home:

                    if len(user_input[1].split(".")) == 4:

                        for element in websites.keys():
                            if websites[element] == user_input[1]:
                                landing_server = element
                                ping_flag = 1

                    elif len(user_input[1].split(".")) == 2:
                        landing_server = user_input[1]
                        ping_flag = 1

                    else:
                        print("Destination unrecognizable")

                    if ping_flag == 1:

                        if landing_server not in websites:
                            print("Unable to find server")

                        else:
                            ping_time = ping(connection, server_home, landing_server)
                            print("Reply from", websites[server_home], "time =", ping_time, "ms")
                else:
                    print("Please set home-server first")

        #TRACES ROUTES
        elif user_input[0] == "traceroute":
            route_check = 0

            if server_home:

                if len(user_input[1].split(".")) == 4:

                    for element in websites.keys():

                        if websites[element] == user_input[1]:
                            landing_server = element
                            route_check = 1

                    print("Tracing route to", landing_server, [user_input[1]])

                elif len(user_input[1].split(".")) == 2:
                    landing_server = user_input[1]
                    route_check = 1
                    print("Tracing route to", landing_server, [user_input[1]])

                else:
                    print("Unable to resolve target system name", user_input[1])

                if route_check == 1:
                    if landing_server not in websites:
                        print("Unable to find path to server")

                    else:
                         trace(connection, server_home, landing_server, websites)

            else:
                print("Please set home-server first")


        elif user_input[0] == "ip-config":

            if user_input[0] == 'ip-config':
                if server_home:
                    print(server_home, '  ', websites[server_home])
                else:
                    print("Home server not yet defined")

        elif user_input[0] == "display-servers":
            user_input = input(">>> ")


def ping(web_connections, home_site, landing_page):

    ping = 0

    for node in web_connections[home_site]:


        visited = [home_site]

        if node[0] not in visited:
            found = recursion(web_connections, node[0], landing_page, visited)

            if found == True:
                visited.append(landing_page)

                for i in range(1, len(visited)):
                    for node in web_connections[visited[i - 1]]:
                        if visited[i] == node[0]:
                            ping += node[1]

                return ping


def trace(web_connections, home_site, landing_page, websites):

    found = False

    for webnode in web_connections[home_site]:

        path = [home_site]

        if webnode[0] not in path:
            found = recursion(web_connections, webnode[0], landing_page, path)

            if found == True:
                path.append(landing_page)
                print(path)
                for i in range(len(path)):
                    if i == 0:
                        print(0, "   ", 0, "   ", websites[path[i]], "   ", path[i])
                    else:
                        for webnode in web_connections[path[i - 1]]:
                            if path[i] == webnode[0]:
                                print(i, "   ", webnode[1], "   ", websites[webnode[0]], "   ", webnode[0])
                print("Trace Complete")
                return path

    if found == False:
        print("Unable to resolve target system name", landing_page)

def recursion(web_connections, home_site, landing_page, visited):

    if home_site == landing_page:

        return True

    if home_site in visited:
        return False

    visited.append(home_site)

    # recursive case
    result = False
    print([home_site])
    for node in web_connections[home_site]:
        if node[0] not in visited:
            if recursion(web_connections, node[0], landing_page, visited):
                result = True
                return True
    return result

if __name__ == '__main__':
   run_the_internet()




