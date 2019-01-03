import udp_host


def user_input():
    while 1:
        msg= input("input msg:")
        udp_host.tx2_udp_send(msg)


user_input()