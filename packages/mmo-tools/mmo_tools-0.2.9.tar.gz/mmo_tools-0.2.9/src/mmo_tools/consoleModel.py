from datetime import datetime
from enum import Enum
import time
class status:
    SUCCESS = '\x1b[96m'
    WARNING = '\x1b[93m'
    ERROR   = '\x1b[91m'
    LOADING = '\x1b[94m'
    TIME    = '\x1b[95m'
    RESET   = '\x1b[0m'


class FormatTime:
    """
    Args:
    :A: H:M:S
    :B: d/m/Y
    """
    A =  datetime.now().strftime("%H:%M:%S")
    B =  datetime.now().strftime("%d/%m/%Y")

class console:

    
    def wait(number : int ):
        """
            Args:
            :number: Số thời gian đếm ngược
        """
        for _ in range(number,1,-1):
            print(f"continue {_}s ..." , end="                                             \r")
            time.sleep(1)

    def log(text : str , type : status):
        """
            Args:
            :text: Dạng văn bản hiển thị
            :type: Trạng thái màu sắc
        
        """
        __ =  "[" + text.split("[")[1].split("]")[0] + "]"
        text =  text.split("(")[0] + status.TIME + "(" +text.split("(")[1].split(")")[0] +  ")" +type +  text.split(")")[1] +  status.RESET
        text = text.replace(__ ,  status.TIME + __ + type)


        if type == status.SUCCESS:
            print(status.SUCCESS + text)
        elif type == status.WARNING:
            print(status.WARNING + text)
        elif type == status.LOADING:
            print(status.LOADING + text)
        elif type == status.ERROR:
            print(status.ERROR + text)





            
