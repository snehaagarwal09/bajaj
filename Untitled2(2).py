#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd


# In[ ]:


from datetime import datetime



# In[ ]:


file_path = r"C:\Users\SOC-S-608\Downloads\Untitled spreadsheet - Sheet1.csv"


# In[ ]:


df = pd.read_csv(file_path)


# In[ ]:


df['attendance_date'] = pd.to_datetime(df['attendance_date'], format='%m/%d/%Y')


# In[ ]:


df = df.sort_values(by=['student_id', 'attendance_date'])


# In[5]:


def find_absence_streaks(df):
    result = []
    for student_id, group in df.groupby('student_id'):
        streak_start = None
        streak_end = None
        streak_days = 0
        prev_day = None
        
        for idx, row in group.iterrows():
            if row['status'] == 'Absent':
                if prev_day is None or (row['attendance_date'] - prev_day).days == 1:
                    streak_days += 1
                    streak_end = row['attendance_date']
                else:
                    if streak_days > 3:
                        result.append([student_id, streak_start, streak_end, streak_days])
                    streak_start = row['attendance_date']
                    streak_end = row['attendance_date']
                    streak_days = 1
            else:
                if streak_days > 3:
                    result.append([student_id, streak_start, streak_end, streak_days])
                streak_start = None
                streak_end = None
                streak_days = 0
            prev_day = row['attendance_date']

        if streak_days > 3:
            result.append([student_id, streak_start, streak_end, streak_days])

    return pd.DataFrame(result, columns=['student_id', 'absence_start_date', 'absence_end_date', 'total_absent_days'])

absence_streaks = find_absence_streaks(df)

print(absence_streaks)


# In[6]:


import re


# In[9]:


def validate_email(email):
    email_pattern = r'^[A-Za-z0-9_]+@[A-Za-z0-9]+\.[a-z]{2,}$'
    
    if re.match(email_pattern, email):
        return email
    return None


# In[10]:


absence_streaks_data = [
    [107, None, '2024-03-25', 4],  # Student 107 has an absence streak but no start date
    [108, '2024-11-02', '2024-11-05', 4]  # Student 108 has a valid absence streak
]


# In[11]:


students_data = [
    [108, 'John Doe', 'john.doe_parent@gmail.com'],
    [107, 'Jane Smith', 'jane.smith_parent@domaincom'],  # Invalid email
    [101, 'Mark Johnson', 'mark.johnson_parent@gmail.com']
]


# In[12]:


students_df = pd.DataFrame(students_data, columns=['student_id', 'student_name', 'parent_email'])


# In[15]:


merged_df = pd.merge(absence_streaks, students_df, on='student_id', how='left')


# In[16]:


merged_df['email'] = merged_df['parent_email'].apply(validate_email)


# In[17]:


merged_df['msg'] = merged_df.apply(
    lambda row: f"Dear Parent, your child {row['student_name']} was absent from {row['absence_start_date']} to {row['absence_end_date']} for {row['total_absent_days']} days. Please ensure their attendance improves." 
    if pd.notna(row['email']) else None, axis=1
)


# In[18]:


final_df = merged_df[['student_id', 'student_name', 'absence_start_date', 'absence_end_date', 'total_absent_days', 'email', 'msg']]


# In[19]:


print(final_df)


# In[ ]:




