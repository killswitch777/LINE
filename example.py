#-*- coding: utf-8 -*-
from LineClient import *
import time

#/* QrCode Login:
client = LINE(appType='ANDROIDLITE')
#/* accessToken Login:
#client = LINE("Your accessToken", appType='IOSIPAD')
client.callback.default("accessToken: %s" % client.accessToken)

def bot(op):
    if op.type == 0:
        return
    elif op.type == 25:
        msg = op.message
        text = str(msg.text)
        to = msg.to
        if text.lower() == 'speed':
            start = time.time()
            client.sendMessage(to, '....')
            client.sendMessage(to, '%.5f Second..' % (time.time()-start))
    elif op.type == 26:
        msg = op.message
        to = msg.to
        text = str(msg.text)
        if msg.toType == 0 and msg._from != client.profile.mid:
            to = msg._from
        else: to = msg.to
        if text.lower() == 'hi':
            client.sendMessage(to, 'Hi juga')

def fetch():
    while True:
        try:
            operations = client.poll.fetchOperations(client.revision, 50)
            for op in operations:
                if (op.type != OpType.END_OF_OPERATION):
                    client.revision = max(op.revision, client.revision)
                    bot(op)
        except KeyboardInterrupt:
            sys.exit('Keyboard Interrupt')
        except TalkException:
            client.lookError()
        except ShouldSyncException:
            client.revision = max(op.revision, client.revision)
        except Exception as e:
            client.lookError()

if __name__ == '__main__':
    fetch()
