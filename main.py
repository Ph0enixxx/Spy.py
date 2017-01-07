# Spy包
# mySql工厂函数：

# S = Spy.mySql("127.0.0.1","root","toor","myDb")


# S("users").
"""
where ok
group
order
join
distinct
query
having
page ok


增：add(dict) ok
删除：remove(condition)
     remove_unsafe(condition)
改：save(dict)
   save_unsafe(condition)
查：select(row) 返回dataframe？list？
    json(row) 返回json
    count() 计数 ok
    getSql() 获取sql语句 ok
    query(sql) ok

防止注入
"""


class Spy(object):
    def __init__(self, table):
        if table == False:
            #抛出异常
            pass
        self.table = table
        self.sql = ["from ", str(self.table), " where 1=1 "]
        self.whereAdded = False
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
            self.columns = ["select ",",".join(columns)]
        self.fieldAdded = True
        return self

    """
        @param dict 条件
            dict {key:value}  {"age":15}  查询age=15的数据
            dict {key:(operator,value)}	  {"age":(">",15)} 查询age>15的数据
        @return SpyObject 用于连贯操作

    """

    def where(self, conditions):
        self.whereAdded = True
        self.whereS = []
        for k,v in conditions.items():
            if type(v) == type(("tuple",123)):
                self.whereS += [" and ",str(k),str(v[0]),'"'+str(v[1])+'"']
            #if type(v) == type("string"):
            else:
                self.whereS += [" and ",str(k),"=",'"'+str(v)+'"',""]
            self.sql += self.whereS
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
        if self.fieldAdded == True:
            self.sql = self.columns + self.sql
        else:
            self.sql = ["select * "] + self.sql

        if self.pageAdded == True:
            self.sql += self.page
        pass

    """
        执行sql语句
    """
    def _execute(self):
        print(" ".join(self.sql))
        # print(self.sql)
        pass
    """
        @param rows 行数（可选）-1为不选
        @return Dataframe？ 用于显示结果
    """

    def select(self):
        self._terminate()
        print(" ".join(self.sql))
        pass
    """
        @直接执行sql语句
    """
    def query(self,sql):
        sql = self.sql
        pass
    """
        @获取sql语句
    """
    def getSql(self):
        self._terminate()
        return str(self.sql)
    """
        @统计查询结果行数
    """
    def count(self):#SELECT COUNT(*)
        self.field(["count(*) as num"])
        self.page(1,1)
        self.select()

    """
        @param content dict 添加的内容
    """
    def add(self,content={}):
        if content == {}:
            return True
        self.sql = ["insert into ", self.table, " ("]
        for k,v in content.items():
            self.sql += [str(k),","]
        self.sql = self.sql[:-1] + [") values ("]
        for k,v in content.items():
            self.sql += [str(v),","]
        self.sql = self.sql[:-1] + [");"]
        self._execute()

    """
        删
    """
    def remove(self):
        if self.whereAdded == False:
            #抛出异常
            return
        self.sql = ["delete from ", self.table,"where 1=1"] + self.whereS
        self._execute()


Spy("users").where({"age":15}).select()
Spy("users").where({"age":'1000000'}).page(15).select()
Spy("users").where({"age":(">",15)}).page(15).select()
Spy("users").count()
Spy("users").where({"age":15}).select()
Spy("users").add({"aa":"bbbb","bbb":"oooo"})
Spy("users").remove()
Spy("users").where({"age":(">",15)}).remove()