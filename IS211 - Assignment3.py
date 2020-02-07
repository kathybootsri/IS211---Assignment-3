# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 16:55:40 2020

@author: kbootsri
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 15:52:18 2020

@author: kbootsri
"""




def main():
    import argparse
    import sys
 
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default = "http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv", type=str)
    args = parser.parse_args()
    if (args.input == None and args.length == None):
        sys.exit()    

        
if __name__ == "__main__":
    
    """PART II: DOWNLOAD DATA FUNCTION"""
        
    def downloadData(url):
        import urllib.request
        import pandas as pd
        from io import StringIO
        import re
        import datetime
        
        global df
        
        response = urllib.request.urlopen(url)
        html = response.read()
        
        s=str(html,'utf-8')
        
        data = StringIO(s) 
        
        df=pd.read_csv(data, names = ['File Name', 'Date/Time', 'Web ID', 'Status', 'Bytes'])
        
        df['Count'] = 1
#        print(df)
        for x in range(len(df)):
            file_name = df.iloc[x]['File Name']
            if re.search(r"\.[Jj][Pp][Gg]$", file_name) or re.search(r"\.[Jj][Pp][Ee][Gg]$", file_name) or re.search(r"\.[Pp][Nn][Gg]$", file_name) or re.search(r"\.[Gg][Ii][Ff]$", file_name):
                df.at[x, 'Photo Type'] = 1

        
        """PARSE WEB ID"""
        split = df['Web ID'].str.split("/")
        
        raw_web = split.to_list()
        
        df[['Parse1', 'Parse2', 'Parse3', 'Parse4', 'Parse 5', 'Parse 6']] = pd.DataFrame(raw_web)
        
        
        
        for x in range(len(df)):  
            file_name = str(df.iloc[x]['Parse2'])
            if re.search(" msie ", file_name, re.IGNORECASE):
                df.at[x, 'Browser'] = 'Internet Explorer'  
                
        for x in range(len(df)):    
            file_name = str(df.iloc[x]['Parse4'])
            if re.search("safari", file_name, re.IGNORECASE):
                df.at[x, 'Browser'] = 'Safari'  

        for x in range(len(df)):
            file_name = str(df.iloc[x]['Parse3'])
            if re.search("firefox", file_name, re.IGNORECASE):
                df.at[x, 'Browser'] = 'Firefox'
            if re.search("chrome", file_name, re.IGNORECASE):
                df.at[x, 'Browser'] = 'Chrome'                    
        
        for x in range(len(df)):
            file_name = df.iloc[x]['Date/Time']
            hour = datetime.datetime.strptime(file_name, "%Y-%m-%d %X").hour
            df.at[x, 'Hour of Day'] = hour
        
        

        """COUNT PERCENTAGE OF HITS AS IMAGES"""
        
        df['Hour of Day'] = df['Hour of Day'].astype(int)
        
        perc_photo = df['Photo Type'].sum()/df['File Name'].count()
        
        format_perc = "{:.2%}".format(perc_photo)
    
        print("Image requests account for {} of all requests.".format(format_perc))
        print( "\n")
        
        """COUNT BROWSER SUMMARY"""
        
        df_piv = df.pivot_table(index = ['Browser'], values = ['Count'], aggfunc='sum')
        
        df_piv.sort_values(by='Count', ascending=False)

        print("Here are the browser counts, with Chrome being most popular:")
        print(df_piv)
        print( "\n")
        
        """COUNT HOURLY ACTIVITY"""
        
        df_hr = df.pivot_table(index = ['Hour of Day'], values = ['Count'], aggfunc='sum')
        
        for hour in range(len(df_hr)):
            hr_count = df_hr.iloc[hour]['Count']
            print ("Hour {} has {} hits".format(hour, hr_count))

        
url = "http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv"

downloadData(url)