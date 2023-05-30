from flask import Flask, render_template
import psutil

app = Flask(__name__)


@app.route('/')
def home():
    cpu_temp = psutil.sensors_temperatures()['cpu_thermal'][0].current
    gpu_temp = psutil.sensors_temperatures()['gpu_thermal'][0].current
    memory_info = psutil.virtual_memory()
    memory_total = memory_info.total
    memory_used = memory_info.used
    memory_percentage = memory_info.percent

    return render_template('/index.html', cpu_temp=cpu_temp, memory_total=memory_total, memory_used=memory_used, memory_percentage=memory_percentage)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
