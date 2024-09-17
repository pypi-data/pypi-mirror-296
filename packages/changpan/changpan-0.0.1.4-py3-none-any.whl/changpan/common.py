import sys
import argparse


# 根据dict生成长选项与短选项（用于用getopt解析cmd参数）

class CPparser(argparse.ArgumentParser):
    """
    dict_args每一项的格式：'变量名字':{'opts':这个变量要绑定的选项opt(元组),"value":默认值},
    输入字典格式示例：
    dict_args={  
        'file':{'args':("--file","-f","--house"),"value":None,"help":"this is the file"},
        'path':{'args':("--path","-p"),"value":None,"help":"this is a path"},
    }
    """

    def __init__(self,dict_args={}, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dict_args = dict_args
        self.dict_to_args(self.dict_args)
    
    # 重写__getattr__方法，使得可以通过对象.变量名的方式访问变量的值
    def __getattr__(self, name):
        try:
            return self.dict_args[name]['value']
        except KeyError:
            raise AttributeError(name)

    # 设置输入参数
    def set_args(self, dict_args):
        # 设置输入参数
        self.dict_args = dict_args
        # 将字典传入argparse
        self.dict_to_args(self.dict_args)
    
    # 将字典dict_args参数传入argparse
    def dict_to_args(self, dict_args):
        for var_name, v in self.dict_args.items():
            self.add_argument(*v['args'], default=v['value'], help=v['help'])

    # 从argparse读取值到dict_args
    def args_to_dict(self):
        # 从命令行中解析参数
        args = self.parse_args()
        # 遍历args中的所有属性
        for arg in args.__dict__.keys():
            # 遍历dict_args中的所有键值对
            for varName,dict_arg in self.dict_args.items():
                args_list = [i.strip('-') for i in dict_arg['args']]
                # 如果当前属性在args_list中，则将其赋值给对应的dict_arg
                if arg in args_list:
                    self.dict_args[varName]['value'] = args.__dict__[arg]
        return self.dict_args
    
    # 解析参数,返回字典
    def parse(self):
        self.dict_args = self.args_to_dict()
        # 遍历dict_args中的所有键值对,用创建属性并赋值给self
        for var_name, v in self.dict_args.items():
            setattr(self, var_name, v['value'])
        return self.dict_args
    
   
    # 打印所有参数
    def print_args(self):
        print(self.dict_args)
    
    # 将字典解析成全局变量,变量名与字典的key相同
    def to_globals(self,globals = globals()):
        for var_name, v in self.dict_args.items():
            globals[var_name] = v['value']
    
    @classmethod
    def help(self):
        string = """
示例：
#  0.定义输出选项的字典
dict_args={  
    'file':{'args':("--file","-f","--house"),"value":None,"help":"this is the file"},
    'path':{'args':("--path","-p"),"value":None,"help":"this is a path"},
}
# 1.创建参数解析器
parser = CPparser(dict_args=dict_args,
                prog='ProgramNameCP',                  # 程序名称
                description='What the program does',   # 程序描述
                epilog='Text at the bottom of help')   # 程序结尾
# 2.解析参数
parser.parse()
# 3.所有参数转全局变量
parser.to_globals()
# # 3.将字典解析成全局变量,变量名与字典的key相同
# dict_to_global(dict_args,lambda x:x['value'])

# 4.打印/使用参数
print(file)
print(path)
print(parser.file)
print(parser.path)
        """
        print(string)
        return string

# 将字典解析成全局变量,变量名与字典的key相同
def dict_to_globals(dict_args,globals=globals(),func=None):
    '''
    将字典解析成全局变量,变量名与字典的key相同
    '''
    if func is None:
        for var_name, value in dict_args.items():
            globals[var_name] = value
    else:
        for var_name, value in dict_args.items():
            globals[var_name] = func(value)



if __name__ == "__main__":
    # 输入参数的默认值
    # dict_args每一项的格式：'变量名字':{'opts':这个变量要绑定的选项opt(元组),"value":默认值},
    # opts的值是长选项与短选项的元组，选项前面必须有-或者--
    # 0.定义输出选项的字典
    dict_args={  
        'file':{'args':("--file","-f","--house"),"value":None,"help":"this is the file"},
        'path':{'args':("--path","-p"),"value":None,"help":"this is a path"},
    }
    # 1.创建参数解析器
    parser = CPparser(dict_args=dict_args,
                    prog='ProgramNameCP',                  # 程序名称
                    description='What the program does',   # 程序描述
                    epilog='Text at the bottom of help')   # 程序结尾
    # 2.解析参数
    parser.parse()
    # # 3.所有参数转全局变量
    # parser.to_globals()
    # 3.将字典解析成全局变量,变量名与字典的key相同
    dict_to_globals(dict_args,globals(),lambda x:x['value'])

    # 4.打印/使用参数
    print(file)
    print(path)
    print(parser.file)
    print(parser.path)


    # 打印方法与用法
    # help(CPargparse)


