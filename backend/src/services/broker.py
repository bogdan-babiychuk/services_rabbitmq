import aio_pika

class ProduceMessageInRabbit:
    def __init__(self, url:str, login:str, password:str)-> None:
        self.url = url
        self.login = login
        self.password  = password
        
    async def get_connection(self):
        return await aio_pika.connect_robust(self.url,
                                      login=self.login,
                                      password=self.password)

    async def publish_message(self,
                        name_queue:str,
                        name_exchange:str,
                        routing_key:str,
                        body:str):
        
        connection = await self.get_connection()
        async with connection:
            async with connection.channel() as channel:
                exchange = await channel.declare_exchange(name_exchange, type=aio_pika.ExchangeType.DIRECT)
                queue = await channel.declare_queue(name_queue, durable=True)

                await queue.bind(exchange, routing_key=routing_key)

                await exchange.publish(aio_pika.Message(body.encode(),content_type="application/json",),
                                       routing_key=routing_key)


