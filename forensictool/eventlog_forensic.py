import win32evtlog
import win32evtlogutil
server = 'localhost' 
logtype = 'System' # 'Application' # 'Security' # 'System' # 'Setup'
hand = win32evtlog.OpenEventLog(server,logtype)
flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
total = win32evtlog.GetNumberOfEventLogRecords(hand)


count = 0
while True:
    events = win32evtlog.ReadEventLog(hand, flags,0) #하루 단위로 불러옴
    if not events:
        break
    if events: #그 날짜에 이벤트가있으면
        for event in events: # 그날의 모든 이벤트 출력
            count+=1
            print('────────────────────────────────────────────')
            print('Event Category:', event.EventCategory)
            print('Time Generated:', event.TimeGenerated)
            print('Source Name:', event.SourceName)
            print('Event ID:', event.EventID)
            print('Event Type:', event.EventType)
            data = event.StringInserts
            if data:
                print ('Event Data:')
                for msg in data:
                    print(' ',msg)
                binary_data = win32evtlogutil.SafeFormatMessage(event, logtype)

            binary_data = win32evtlogutil.SafeFormatMessage(event, logtype)
            binary_data = binary_data.split('\n')
            if binary_data:
                print ('Binary Data:')
                for bmsg in binary_data:
                    print(' ',bmsg)
            print('────────────────────────────────────────────')
        
print('\n개수: ', count)

class EventlogForensicTool:
    def __init__(self):
        pass


    def GetLogFiles(self):
        pass