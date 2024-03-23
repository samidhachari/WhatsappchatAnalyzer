
# updated code 
import pandas as pd
import re

def preprocessing_data(data):
    patternDate = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s(?:am|pm)\s-\s'

    messages = re.split(patternDate, data)[3:]
    dates = re.findall(patternDate, data)[2:]

    # Create DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    
    # Convert message_date type
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M\u202f%p - ')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Separate user and messages
    users = []
    messages = []
    
    for m in df['user_message']:
        entry = re.split('([\w\W]+?):\s', m)
        if entry[1:]:
            # Check if the entry is a phone number
            if re.match(r'\+\d{2} \d{5} \d{5}', entry[1]):
                users.append(entry[1])  # Append phone number as user identifier
                messages.append(entry[2])  # Append the message to the messages list
            else:
                # If name is found where a phone number is expected, use the name as user identifier
                users.append(entry[1])  
                messages.append(entry[2])  # Append the message to the messages list
        elif not m.startswith('group_notification'):  # Check if the message is not a group notification
            users.append('group_notification')
            messages.append(m)  # Append the whole message if user is not found
    
    # Add user and message columns to the DataFrame
    df['user'] = users
    df['message'] = messages

    # Drop the original user_message column
    df.drop(columns=['user_message'], inplace=True)

    # Extract additional date-time features
    df['onlyDate'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute


    period = []
    for hour in df[['day_name','hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00')+ "-"+ str(hour+1))
        else:
            period.append(str(hour)+"-"+str(hour+1))
            
    df['period'] = period
    return df


