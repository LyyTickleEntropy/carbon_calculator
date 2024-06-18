from flask import render_template, request, flash
from app import app
from datetime import datetime

@app.route("/", methods=["GET", "POST"])
def index():
    carbon_emission = None
    current_date = datetime.now().strftime("%Y-%m-%d")
    show_result = False
    error_message = None

    if request.method == "POST":
        try:
            # 获取用户输入数据
            transportation = request.form.get("transportation", "0").strip()
            energy = request.form.get("energy", "0").strip()
            dietary = request.form.get("dietary", "0").strip()
            goods = request.form.get("goods", "0").strip()
            waste = request.form.get("waste", "0").strip()
            other = request.form.get("other", "0").strip()

            # 将输入转换为浮点数
            transportation = float(transportation) if transportation else 0.0
            energy = float(energy) if energy else 0.0
            dietary = float(dietary) if dietary else 0.0
            goods = float(goods) if goods else 0.0
            waste = float(waste) if waste else 0.0
            other = float(other) if other else 0.0

            # 确保所有输入值都是非负数
            if transportation < 0 or energy < 0 or dietary < 0 or goods < 0 or waste < 0 or other < 0:
                raise ValueError("All values must be non-negative.")

            # 计算碳排放量
            carbon_emission = (
                transportation * 0.21 +  # 运输碳排放因子
                energy * 0.5 +           # 家庭能源使用碳排放因子
                dietary * 0.003 +        # 饮食碳排放因子
                goods * 2.5 +            # 商品消费碳排放因子
                waste * 0.1 +            # 废物管理碳排放因子
                other                    # 其他碳排放量（直接输入）
            )
            show_result = True
        except ValueError as e:
            error_message = str(e)

    return render_template("index.html", carbon_emission=carbon_emission, current_date=current_date, show_result=show_result, error_message=error_message)
