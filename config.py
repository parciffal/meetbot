"""Token of telegram bot you can change it to another bot token"""
TOKEN = ''


"""Your telegram group id"""
GROUP_ID = ''


"""White list file name """
FILENAME = 'userbase.csw'


"""Welcome message"""
WELCOME_MESSAGE = 'welcome message'
WELCOME_ERROR_WHITELIST = 'Sorry your not in white list'
WELCOME_ERROR_GROUPCHAT = 'Bot works only in private chat'


"""Welcome message murkup names """
WEllBUTT1 = '1'
WELLBUTT2 = '2'
WELLBUTTCUSTOM = 'custom'

"""Repit message"""
REPIT_MESSAGE = 'repit message'
"""price enter like number not string"""
X = 12


"""Date step"""
CONFIRMBUTT = 'Confirm'
REPITBUTT = 'Repit'
ADDNEW = 'New Order'
CONFIRMMESSAGE_ALERT = 'order is proccesing'
CONFIRMMESSAGE_TEXT = 'You have ordered {quantity}\nPrice is {price}\nAt {todey} {date} \nIn {latitude} {longitude}'
DATE_ERROR_WRONG = "Wrong date!!\nSend me date like in exemple\nDD.MM 00:00 - 23:59 pm\nExemple'12.12 4:15"


"""Location step"""
DATE_ERROR_LOC_STEP = "Today is {date}\nSend me date like in exemple\nDD.MM 00:00 - 23:59 pm\nExemple'12.12 4:15"


"""Quantity step"""
QUANTITY_ERROR = 'Wrong quantity Try new'


"""Same as every where we ask location"""
LOCATION_MESSAGE_TEXT = 'Send me location with map in telegram'


"""Messange send to group"""
GROUP_SEND_MESSAGE = '{username} have ordered {quantity}\nPrice is {price}\nAt {todey} {date} \nIn {latitude} {longitude}'
ORDER_IS_IN_PROC = 'Order is in process'
ACCEPTBUTTONTEXT = 'Accept'


"""Acception message from group"""
ACCEPTION_MESSAGE_FROM_GROUP = 'Order is accepted'