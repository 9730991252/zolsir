from channels.consumer import SyncConsumer ,AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
class MySyncConsumer(SyncConsumer):
    def websocket_connect(self,event):
        print('connect')
        async_to_sync(self.channel_layer.group_add)(
            'programmers',#group Name
            self.channel_name
            )
        self.send({
            'type':'websocket.accept'
        })
        
    def websocket_receive(self,event):
        print('massege receive',event)
        async_to_sync(self.channel_layer.group_send)(
            'programmers',
            {
                'type':'chat.message',
                'message':event['text']
            })
    
    def chat_message(self, event):
        print('event ......', event['message'] )
        self.send({
            'type':'websocket.send',
            'text': event['message']
        })
        
    def websocket_disconnect(self,event):
        print('disconnect',event)
        async_to_sync(self.channel_layer.group_discard)(
            'programmers',#group Name
            self.channel_name
            )
        raise StopConsumer()