from motion import df
from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool, ColumnDataSource

df["Start_time"]=df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["End_time"]=df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")

cd=ColumnDataSource(df)

plt=figure(x_axis_type="datetime",width=800,height=300,title="Motion graph")

p=plt.quad(left="Start",right="End",bottom=0,top=2,color="purple", source=cd)

plt.ygrid[0].ticker.desired_num_ticks=1
plt.yaxis.minor_tick_line_color=None

hover=HoverTool(tooltips=[("Entered","@Start_time"),("Left","@End_time")])
plt.add_tools(hover)

output_file("Motion.html",mode='absolute')
show(plt)