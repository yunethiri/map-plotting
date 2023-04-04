import pandas as pd
import numpy as np
import folium
import os
from branca.element import Template, MacroElement

# set workingpath
path = "/Users/yunethirikhin/School/Y2 Winter - Research"
os.chdir(path)

### READ IN DATA AND FORMATTING ###

# read in data
df = pd.read_excel('map_plotting/Industries for plotting_Hui Xin\'s task.xlsx')

# Dataframe for sampling site, steel mill, power plants, incineration plants
df1 = df[0:59]

# Dataframe for refineries
df2 = df[60:78]
df2 = df2.rename(columns = {'Capacity (MW)':'Capacity (thousand bbl/d)'})

# Dataframe for ports
df_exact = df[79:303]
df_exact = df_exact.rename(columns = {'Capacity (MW)':'Capacity (TEU)'})

# Dataframe for landfills
df3 = df[304:]
df3 = df3.rename(columns = {'Capacity (MW)':'Capacity'})

# the estimated size excel file and dataframe 
df_est = pd.read_excel('map_plotting/Industries for plotting_Hui Xin\'s task ESTIMATED.xlsx')
df_est = df_est[59:]
df_est = df_est.rename(columns = {'Capacity (MW)':'Size range'})

# read in icons from icons folder and processing
def load_images_from_folder(folder): 
    images_dict = {}
    for filename in os.listdir(folder): 
        img = os.path.join(folder,filename)
        images_dict[filename[:-4]] = img
    return images_dict

icons_dict = load_images_from_folder("map_plotting/icons")
#print(icons_dict)

### MAP PLOTTING ###
p_scale = 4
r_scale = 7
sampling_scale = 30
port_scale = 2

n = folium.Map(location=[1,0], tiles="OpenStreetMap", zoom_start=2)
#{'green', 'darkblue', 'darkred', 'pink', 'lightblue', 'beige', \
#'white', 'lightred', 'black', 'lightgray', 'cadetblue', 'gray', 'purple', 'orange', 'darkgreen', 'darkpurple', 'lightgreen', 'blue', 'red'}.


# REFINERIES
for i in range(0,len(df2)):
    if df2.iloc[i]['Coordinates']!=0: #and df2.iloc[i]['Country']=='Singapore':
      html=f"""
          <h1> {df2.iloc[i]['Name']}</h1>
          <p>{df2.iloc[i]['Type of plant']}</p>
          <p>Capacity: {df2.iloc[i]['Capacity (thousand bbl/d)']} (thousand bbl/d)</p>
          <ul>
          </ul>
          </p>
          """
      
      iframe = folium.IFrame(html=html, width=200, height=200)
      popup = folium.Popup(iframe, max_width=2650)
      folium.Marker(
        location=[float(df2.iloc[i]['Coordinates'].split(sep=', ')[0]),float(df2.iloc[i]['Coordinates'].split(sep=', ')[1])],
        popup=popup,
        #icon=folium.Icon(color='gray',prefix='fa',icon="fa-solid fa-diamond",radius=500)).add_to(n)
        icon = folium.features.CustomIcon(icons_dict['diamond'],
                                          icon_size=(np.log(float(df2.iloc[i]['Normalised Capacity']))*r_scale,np.log(float(df2.iloc[i]['Normalised Capacity']))*r_scale))).add_to(n)

#check if it is Nan
#numpy.isnan(number)

# PORTS
for i in range(0,len(df_est)):
    size = np.log(float(100000))*port_scale,np.log(float(100000))*port_scale
    if type(df_est.iloc[i]['Coordinates'])==str:
      html=f"""
          <h1> {df_est.iloc[i]['Name']}</h1>
          <p>{df_exact.iloc[i]['Type of plant']}</p>
          <p>Port Size: {df_est.iloc[i]['Size range']} </p>
          <ul>
          </ul>
          </p>
          """
      if df_est.iloc[i]['Size range'] == 'very small':
        port = icons_dict['verysmall']
      elif df_est.iloc[i]['Size range'] == 'small':
        port= icons_dict['small']
      elif df_est.iloc[i]['Size range'] == 'medium':
       port = icons_dict['medium']

      elif df_est.iloc[i]['Size range'] == 'large':
        port = icons_dict['large']
      elif df_est.iloc[i]['Size range'] == 'very large':
        port = icons_dict['verylarge']

      else:
        print(df_est.iloc[i])

      iframe = folium.IFrame(html=html, width=200, height=200)
      popup = folium.Popup(iframe, max_width=2650)
      folium.Marker(
          location=[float(df_est.iloc[i]['Coordinates'].split(sep=', ')[0]),float(df_est.iloc[i]['Coordinates'].split(sep=', ')[1])],
          popup=popup,
          icon = folium.features.CustomIcon(port,icon_size=(size))).add_to(n)

for i in range(0,len(df1)):
      
      # SAMPLING SITE 
      if df1.iloc[i]['Type of plant'] == 'Sampling site':
        html=f"""
            <h1> {df1.iloc[i]['Name']}</h1>
            <p>{df1.iloc[i]['Type of plant']}</p>
            <ul>
            </ul>
            </p>
            """

        iframe = folium.IFrame(html=html, width=200, height=200)
        popup = folium.Popup(iframe, max_width=2650)
        folium.Marker(
            location=[float(df1.iloc[i]['Coordinates'].split(sep=', ')[0]),float(df1.iloc[i]['Coordinates'].split(sep=', ')[1])],
            popup=popup,
            icon=folium.Icon(color='red',prefix='fa',icon="exclamation",radius=500)).add_to(n)
      
      # STEEL MILL 
      elif df1.iloc[i]['Type of plant'] == 'Steel mill':
        html=f"""
            <h1> {df1.iloc[i]['Name']}</h1>
            <p>{df1.iloc[i]['Type of plant']}</p>
            <ul>
            </ul>
            </p>
            """

        iframe = folium.IFrame(html=html, width=200, height=200)
        popup = folium.Popup(iframe, max_width=2650)
        folium.Marker(
            location=[float(df1.iloc[i]['Coordinates'].split(sep=', ')[0]),float(df1.iloc[i]['Coordinates'].split(sep=', ')[1])],
            popup=popup,
            icon = folium.features.CustomIcon(icons_dict['triangle'],icon_size=(sampling_scale,sampling_scale))).add_to(n)

      # INCINERATION PLANTS 
      elif df1.iloc[i]['Type of plant'] == 'Incineration plants':
        html=f"""
            <h1> {df1.iloc[i]['Name']}</h1>
            <p>{df1.iloc[i]['Type of plant']}</p>
            <p>Capacity: {df1.iloc[i]['Capacity (MW)']} (MW)</p>
            <ul>
            </ul>
            </p>
            """  
        
        iframe = folium.IFrame(html=html, width=200, height=200)
        popup = folium.Popup(iframe, max_width=2650)
        
        if df1.iloc[i]['Normalised Capacity'] == 0 or pd.isna(df1.iloc[i]['Capacity (MW)']):
           folium.Marker(
            location=[float(df1.iloc[i]['Coordinates'].split(sep=', ')[0]),float(df1.iloc[i]['Coordinates'].split(sep=', ')[1])],
            popup=popup,
            #icon = folium.features.CustomIcon(,icon_size=(28, 30))).add_to(n)
            icon = folium.features.CustomIcon(icons_dict['star2'],icon_size=(sampling_scale,sampling_scale))).add_to(n)
        else:
          folium.Marker(
              location=[float(df1.iloc[i]['Coordinates'].split(sep=', ')[0]),float(df1.iloc[i]['Coordinates'].split(sep=', ')[1])],
              popup=popup,
              #icon = folium.features.CustomIcon(,icon_size=(28, 30))).add_to(n)
              icon = folium.features.CustomIcon(icons_dict['star'],icon_size=(np.log(float(df1.iloc[i]['Capacity (MW)']))*r_scale,np.log(float(df1.iloc[i]['Capacity (MW)']))*r_scale))).add_to(n)
            
    
      # POWER PLANTS 
      if df1.iloc[i]['Type of plant'] == 'Power plants' and df1.iloc[i]['Country'] == 'Singapore':
          html=f"""
                <h1> {df1.iloc[i]['Name']}</h1>
                <p>{df1.iloc[i]['Type of plant']}</p>
                <p>Capacity: {df1.iloc[i]['Capacity (MW)']} (MW)</p>
                <ul>
                </ul>
                </p>
                """
  
          if df1.iloc[i]['Name'] == 'Senoko Power Station':
            html=f"""
                <h1> {df1.iloc[i]['Name']}</h1>
                <p>{df1.iloc[i]['Type of plant']}</p>
                <p>Capacity: 3300 (MW)</p>
                <ul>
                </ul>
                </p>
                """

            iframe = folium.IFrame(html=html, width=200, height=200)
            popup = folium.Popup(iframe, max_width=2650)
            folium.Marker(
                location=[float(df1.iloc[i]['Coordinates'].split(sep=', ')[0]),float(df1.iloc[i]['Coordinates'].split(sep=', ')[1])],
                popup=popup,
                #icon=folium.Icon(color='gray',prefix='fa',icon="fa-solid fa-diamond",radius=500)).add_to(n)
                icon = folium.features.CustomIcon(icons_dict['senoko'],icon_size=(np.log(3300)*p_scale,np.log(3300)*p_scale))).add_to(n)
                  

          elif df1.iloc[i]['Name'] == 'Tuas Power Station':
            html=f"""
                <h1> {df1.iloc[i]['Name']}</h1>
                <p>{df1.iloc[i]['Type of plant']}</p>
                <p>Capacity: 2475.9 (MW)</p>
                <ul>
                </ul>
                </p>
                """

            iframe = folium.IFrame(html=html, width=200, height=200)
            popup = folium.Popup(iframe, max_width=2650)
            folium.Marker(
                location=[float(df1.iloc[i]['Coordinates'].split(sep=', ')[0]),float(df1.iloc[i]['Coordinates'].split(sep=', ')[1])],
                popup=popup,
                #icon=folium.Icon(color='gray',prefix='fa',icon="fa-solid fa-diamond",radius=500)).add_to(n)
                icon = folium.features.CustomIcon(icons_dict['tuas'],icon_size=(np.log(2475.9)*p_scale,np.log(2475.9)*p_scale ))).add_to(n)
                  

          elif df1.iloc[i]['Name'] == 'Pulau Seraya Power Station': 
            html=f"""
                <h1> {df1.iloc[i]['Name']}</h1>
                <p>{df1.iloc[i]['Type of plant']}</p>
                <p>Capacity: {df1.iloc[i]['Capacity (MW)']} (MW)</p>
                <ul>
                </ul>
                </p>
                """

            iframe = folium.IFrame(html=html, width=200, height=200)
            popup = folium.Popup(iframe, max_width=2650)
            folium.Marker(
                location=[float(df1.iloc[i]['Coordinates'].split(sep=', ')[0]),float(df1.iloc[i]['Coordinates'].split(sep=', ')[1])],
                popup=popup,
                #icon=folium.Icon(color='gray',prefix='fa',icon="fa-solid fa-diamond",radius=500)).add_to(n)
                icon = folium.features.CustomIcon(icons_dict['pulau'],icon_size=(np.log(3040)*p_scale,np.log(3040)*p_scale))).add_to(n)
                  

          elif df1.iloc[i]['Type'] == 'Gas':
            iframe = folium.IFrame(html=html, width=200, height=200)
            popup = folium.Popup(iframe, max_width=2650)
            folium.Marker(
                location=[float(df1.iloc[i]['Coordinates'].split(sep=', ')[0]),float(df1.iloc[i]['Coordinates'].split(sep=', ')[1])],
                popup=popup,
                icon = folium.features.CustomIcon(icons_dict['blue_circle'],icon_size=(np.log(float(df1.iloc[i]['Capacity (MW)']))*p_scale,np.log(float(df1.iloc[i]['Capacity (MW)']))*p_scale))).add_to(n)
  
      # POWER PLANTS FOR MALAYSIA & INDONESIA
      if df1.iloc[i]['Type of plant'] == 'Power plants' and df1.iloc[i]['Country'] != 'Singapore':

        
          html=f"""
                  <h1> {df1.iloc[i]['Name']}</h1>
                  <p>{df1.iloc[i]['Type of plant']}</p>
                  <p>Capacity: {df1.iloc[i]['Capacity (MW)']} (MW)</p>
                  <ul>
                  </ul>
                  </p>
                  """

          if df1.iloc[i]['Type'] == 'Gas':
            iframe = folium.IFrame(html=html, width=200, height=200)
            popup = folium.Popup(iframe, max_width=2650)
            folium.Marker(
                location=[float(df1.iloc[i]['Coordinates'].split(sep=', ')[0]),float(df1.iloc[i]['Coordinates'].split(sep=', ')[1])],
                popup=popup,
                icon = folium.features.CustomIcon(icons_dict['blue_circle'],icon_size=(np.log(float(df1.iloc[i]['Capacity (MW)']))*p_scale,np.log(float(df1.iloc[i]['Capacity (MW)']))*p_scale))).add_to(n)
      
          elif df1.iloc[i]['Type'] == 'Coal-fired':
            iframe = folium.IFrame(html=html, width=200, height=200)
            popup = folium.Popup(iframe, max_width=2650)
            folium.Marker(
                location=[float(df1.iloc[i]['Coordinates'].split(sep=', ')[0]),float(df1.iloc[i]['Coordinates'].split(sep=', ')[1])],
                popup=popup,
                icon = folium.features.CustomIcon(icons_dict['orange_circle'],icon_size=(np.log(float(df1.iloc[i]['Capacity (MW)']))*p_scale,np.log(float(df1.iloc[i]['Capacity (MW)']))*p_scale))).add_to(n)

# LANDFILLS 
for i in range(0,len(df3)):
    if df3.iloc[i]['Coordinates']!=0:
      html=f"""
          <h1> {df3.iloc[i]['Name']}</h1>
          <p>{df3.iloc[i]['Type of plant']}</p>
          <p>Capacity: {df3.iloc[i]['Capacity']}</p>
          <ul>
          </ul>
          </p>
          """
      
      iframe = folium.IFrame(html=html, width=200, height=200)
      popup = folium.Popup(iframe, max_width=2650)

      if df3.iloc[i]['Capacity'] == 0 or pd.isna(df3.iloc[i]['Capacity']):
        continue
      else:
          folium.Marker(
              location=[float(df3.iloc[i]['Coordinates'].split(sep=', ')[0]),float(df3.iloc[i]['Coordinates'].split(sep=', ')[1])],
              popup=popup,
              #icon = folium.features.CustomIcon(,icon_size=(28, 30))).add_to(n)
              icon = folium.features.CustomIcon(icons_dict['trash'],icon_size=(sampling_scale,sampling_scale))).add_to(n)

## LEGENDS ##

main_legend = """
{% macro html(this, kwargs) %}

<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Map Plotting</title>
  <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
  
  <script>
  $( function() {
    $( "#maplegend" ).draggable({
                    start: function (event, ui) {
                        $(this).css({
                            right: "auto",
                            top: "auto",
                            bottom: "auto"
                        });
                    }
                });
});

  </script>
</head>
<body>

 
<div id='maplegend' class='maplegend' 
    style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
     border-radius:6px; padding: 10px; font-size:14px; left: 20px; bottom: 20px;'>
     
<div class='legend-title'>Legend</div>
<div class='legend-scale'>
  <ul class='legend-labels'>
    <li><img src= "icons/sampling_site.png" 
    style="width:auto; height:25px">
            </img> <span> </span> Sampling Site </li>

    <li><img src= "icons/triangle.png" 
    style="width:auto; height:20px">
            </img> <span> </span> Steel Mill </li>

    <li><img src= "icons/diamond.png" 
    style="width:auto; height:20px">
            </img> <span> </span> Refineries </li>

    <li><img src= "icons/star.png" 
    style="width:auto; height:20px">
            </img> <span> </span> Incineration Plant </li>

    <li><img src= "icons/port.png" 
    style="width:auto; height:20px">
            </img> <span> </span> Port </li>

    <li><img src= "icons/blue_circle.png" 
    style="width:auto; height:20px">
            </img> <span> </span> Power Plant (Gas) </li>

    <li><img src= "icons/green_circle.png" 
    style="width:auto; height:20px">
            </img> <span> </span> Power Plant (Oil) </li>

    <li><img src= "icons/pulau.png" 
    style="width:auto; height:20px">
            </img> <span> </span> Power Plant (Gas-Oil) </li>

    <li><img src= "icons/orange_circle.png" 
    style="width:auto; height:20px">
            </img> <span> </span> Power Plant (Coal) </li>

    <li><img src= "icons/trash.png" 
    style="width:auto; height:20px">
            </img> <span> </span> Landfill </li>
    

  </ul>
</div>
</div>
 
</body>
</html>

<style type='text/css'>
  .maplegend .legend-title {
    text-align: left;
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 90%;
    }
  .maplegend .legend-scale ul {
    margin: 0;
    margin-bottom: 5px;
    padding: 0;
    float: left;
    list-style: none;
    }
  .maplegend .legend-scale ul li {
    font-size: 80%;
    list-style: none;
    margin-left: 0;
    line-height: 18px;
    margin-bottom: 2px;
    }
  .maplegend ul.legend-labels li span {
    display: block;
    float: left;
    height: 1px;
    width: 1px;
    margin-right: 5px;
    margin-left: 0;
    border: 1px solid #999;
    }
  .maplegend .legend-source {
    font-size: 80%;
    color: #777;
    clear: both;
    }
  .maplegend a {
    color: #777;
    }
</style>
{% endmacro %}"""


ports_legend = """
{% macro html(this, kwargs) %}

<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Map Plotting</title>
  <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
  
  <script>
  $( function() {
    $( "#maplegend" ).draggable({
                    start: function (event, ui) {
                        $(this).css({
                            right: "auto",
                            top: "auto",
                            bottom: "auto"
                        });
                    }
                });
});

  </script>
</head>
<body>

 
<div id='maplegend' class='maplegend' 
    style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
     border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>
     
<div class='legend-title'> Ports (Normalised Capacity) </div>
<div class='legend-scale'>
  <ul class='legend-labels'>

    <li><img src= "icons/verysmall.png" 
    style="width:auto; height:20px">
            </img> <span> </span> 0.00 - 0.005 </li>

    <li><img src= "icons/small.png" 
    style="width:auto; height:20px">
            </img> <span> </span> 0.005 - 0.05 </li>
    
    <li><img src= "icons/medium.png" 
    style="width:auto; height:20px">
            </img> <span> </span> 0.05 - 0.5 </li>   

    <li><img src= "icons/large.png" 
    style="width:auto; height:20px">
            </img> <span> </span> 0.5 - 1.0 </li>  
              
    <li><img src= "icons/verylarge.png" 
    style="width:auto; height:20px">
            </img> <span> </span> 1.0 </li>  

  </ul>
</div>
</div>
 
</body>
</html>

<style type='text/css'>
  .maplegend .legend-title {
    text-align: left;
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 90%;
    }
  .maplegend .legend-scale ul {
    margin: 0;
    margin-bottom: 5px;
    padding: 0;
    float: left;
    list-style: none;
    }
  .maplegend .legend-scale ul li {
    font-size: 80%;
    list-style: none;
    margin-left: 0;
    line-height: 18px;
    margin-bottom: 2px;
    }
  .maplegend ul.legend-labels li span {
    display: block;
    float: left;
    height: 1px;
    width: 1px;
    margin-right: 5px;
    margin-left: 0;
    border: 1px solid #999;
    }
  .maplegend .legend-source {
    font-size: 80%;
    color: #777;
    clear: both;
    }
  .maplegend a {
    color: #777;
    }
</style>
{% endmacro %}"""


refineries_legend = """
{% macro html(this, kwargs) %}

<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Map Plotting</title>
  <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
  
  <script>
  $( function() {
    $( "#maplegend" ).draggable({
                    start: function (event, ui) {
                        $(this).css({
                            right: "auto",
                            top: "auto",
                            bottom: "auto"
                        });
                    }
                });
});

  </script>
</head>
<body>

 
<div id='maplegend' class='maplegend' 
    style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
     border-radius:6px; padding: 10px; font-size:14px; right: 20px; top: 20px;'>
     
<div class='legend-title'> Refineries <br> (Normalised Capacity) </div>
<div class='legend-scale'>
  <ul class='legend-labels'>

    <li><img src= "icons/diamond.png" 
    style="width:auto; height:11px">
            </img> <span> </span> 0.00 - 0.01 </li> 

    <li><img src= "icons/diamond.png" 
    style="width:auto; height:14px">
            </img> <span> </span> 0.01 - 0.1 </li> 

    <li><img src= "icons/diamond.png" 
    style="width:auto; height:17px">
            </img> <span> </span> 0.1 - 1.0 </li>
    
    <li><img src= "icons/diamond.png" 
    style="width:auto; height:20px">
            </img> <span> </span> 1.0 </li>

  </ul>
</div>
</div>
 
</body>
</html>

<style type='text/css'>
  .maplegend .legend-title {
    text-align: left;
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 90%;
    }
  .maplegend .legend-scale ul {
    margin: 0;
    margin-bottom: 5px;
    padding: 0;
    float: left;
    list-style: none;
    }
  .maplegend .legend-scale ul li {
    font-size: 80%;
    list-style: none;
    margin-left: 0;
    line-height: 18px;
    margin-bottom: 2px;
    }
  .maplegend ul.legend-labels li span {
    display: block;
    float: left;
    height: 1px;
    width: 1px;
    margin-right: 5px;
    margin-left: 0;
    border: 1px solid #999;
    }
  .maplegend .legend-source {
    font-size: 80%;
    color: #777;
    clear: both;
    }
  .maplegend a {
    color: #777;
    }
</style>
{% endmacro %}"""

incineration_legend = """
{% macro html(this, kwargs) %}

<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Map Plotting</title>
  <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
  
  <script>
  $( function() {
    $( "#maplegend" ).draggable({
                    start: function (event, ui) {
                        $(this).css({
                            right: "auto",
                            top: "auto",
                            bottom: "auto"
                        });
                    }
                });
});

  </script>
</head>
<body>

 
<div id='maplegend' class='maplegend' 
    style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
     border-radius:6px; padding: 10px; font-size:14px; left: 20px; top: 20px;'>
     
<div class='legend-title'> Incineration Plants <br>
                          (Normalised Capacity) </div>
<div class='legend-scale'>
  <ul class='legend-labels'>

    <li><img src= "icons/star.png" 
    style="width:auto; height:11px">
            </img> <span> </span> 0.00 - 0.01 </li> 

    <li><img src= "icons/star.png" 
    style="width:auto; height:14px">
            </img> <span> </span> 0.01 - 0.1 </li> 

    <li><img src= "icons/star.png" 
    style="width:auto; height:17px">
            </img> <span> </span> 0.1 - 1.0 </li>
    
    <li><img src= "icons/star.png" 
    style="width:auto; height:20px">
            </img> <span> </span> 1.0 </li>

  </ul>
</div>
</div>
 
</body>
</html>

<style type='text/css'>
  .maplegend .legend-title {
    text-align: left;
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 90%;
    }
  .maplegend .legend-scale ul {
    margin: 0;
    margin-bottom: 5px;
    padding: 0;
    float: left;
    list-style: none;
    }
  .maplegend .legend-scale ul li {
    font-size: 80%;
    list-style: none;
    margin-left: 0;
    line-height: 18px;
    margin-bottom: 2px;
    }
  .maplegend ul.legend-labels li span {
    display: block;
    float: left;
    height: 1px;
    width: 1px;
    margin-right: 5px;
    margin-left: 0;
    border: 1px solid #999;
    }
  .maplegend .legend-source {
    font-size: 80%;
    color: #777;
    clear: both;
    }
  .maplegend a {
    color: #777;
    }
</style>
{% endmacro %}"""


macro = MacroElement()
macro._template = Template(main_legend)

macro2 = MacroElement()
macro2._template = Template(ports_legend)

macro3 = MacroElement()
macro3._template = Template(refineries_legend)

macro4 = MacroElement()
macro4._template = Template(incineration_legend)

n.get_root().add_child(macro)
n.get_root().add_child(macro2)
n.get_root().add_child(macro3)
n.get_root().add_child(macro4)

# Show the map again
n.fit_bounds(n.get_bounds(), padding=(30, 30))
n.save('map_plotting/map.html')