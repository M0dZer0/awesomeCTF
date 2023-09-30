from django.shortcuts import render
from datetime import datetime, timezone, timedelta

def beijing_time(request):
    # 获取当前的UTC时间
    utc_time = datetime.now(timezone.utc)
    # 计算北京时间
    beijing_time = utc_time + timedelta(hours=8)
    # 构造上下文数据
    context = {
        'beijing_time': beijing_time
    }
    # 渲染模板并返回响应
    return render(request, 'beijing_time.html', context)
