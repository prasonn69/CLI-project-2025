temperature=input('Enter the temperature: ')
humidity=input('Enter the humidity')
if temperature=='Warm' and humidity=='Dry':
    print('Play Basketball')
elif temperature=='Warm' and humidity=='Humid':
     print('Play tennis')
elif temperature=='Cold' and humidity=='Dry':
     print('Play Cricket')
else:
     print('Go swim')      