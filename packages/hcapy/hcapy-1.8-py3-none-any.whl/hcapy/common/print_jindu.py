def print_jindu(jindu, total, per: int = 20, dot: int = 5):
    if not per:
        # 若未指定per，则所有进度都输出
        progress_percentage = round(jindu / total * 100, dot)
        print("进度： ", progress_percentage, " %")
    else:
        # 若指定了per，则将进度五等分
        progress_percentage = round(jindu / total * 100, dot)
        steps = [i * (100 / per) for i in range(1, per + 1)]

        for step in steps:
            deta = 1 / total
            if abs(step - progress_percentage) < deta:
                print("进度： ", round(progress_percentage, dot), " %")
            elif progress_percentage == 100:
                print("进度： ", round(progress_percentage, dot), " %")