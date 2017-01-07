# Spy包
# mySql工厂函数：

# S = Spy.mySql("127.0.0.1","root","toor","myDb")


# S("users").


class Spy(object):
    def __init__(self, table):
        self.table = table
        self.sql = ["from ", str(self.table), " where 1=1 "]
        self.fieldAdded = False
        self.pageAdded = False
        pass

    """
    :param columns 要查询的列 为空则跳过

    """
    def field(self, columns=[]):
        if columns == []:
            #抛出异常
            pass
        else:
            columns = ["select ",",".join(columns)]
        self.fieldAdded = True
        return self

    """
        @param dict 条件
            dict {key:value}  {"age":15}  查询age=15的数据
            dict {key:(operator,value)}	  {"age":(">",15)} 查询age>15的数据
        @return SpyObject 用于连贯操作

    """

    def where(self, conditions):
        for k,v in conditions.items():
            if type(v) == type(("tuple",123)):
                self.sql += [" and ",str(k),str(v[0]),'"'+str(v[1])+'"']
            #if type(v) == type("string"):
            else:
                self.sql += [" and ",str(k),"=",'"'+str(v)+'"',""]
        return self
    """
        :param num
    """
    def page(self, num=1, size=15):
        #if self.pageAdded == True:
        self.page = [" limit ",str(int(num)),",",str(int(size))]
        self.pageAdded = True
        return self
    # end method

    """
        终结操作预处理
        @param
    """
    def _terminate(self):
        if self.fieldAdded == False:
            self.sql = ["select * "] + self.sql
        if self.pageAdded == True:
            self.sql += self.page
        pass
    """
        @param rows 行数（可选）-1为不选
        @return Dataframe？ 用于显示结果
    """

    def select(self, rows=-1):
        self._terminate()
        print(" ".join(self.sql))
        pass



Spy("users").where({"age":15}).select()
Spy("users").where({"age":'1000000'}).page(15).select()
Spy("users").where({"age":(">",15)}).page(15).select()
Spy("users").select()
Spy("users").where({"age":15}).select()