from sqltools.parser import *
from tests.testclass import SqltoolsTest

import sqlparse

class ParserTest(SqltoolsTest):
    def test_handle_pair1(self):
        node = TreeNode(State.ROOT)
        node.children.append(TreeNode(State.COL, value="a"))
        node.children[0].children.append(TreeNode(State.OP, value="="))
        node.children[0].children[0].children.append(TreeNode(State.TERMINAL, value="2"))

        tn = TreeNode(State.ROOT)
        tokens= sqlparse.parse('a = 2')[0].tokens[0].tokens

        Parser.handle_pair(tn, tokens)

        self.print_tree(tn)

        self.assertTreeEqual(tn, node)

    def test_handle_pair2(self):
        node = TreeNode(State.ROOT)
        node.children.append(TreeNode(State.COL, value="a"))
        node.children[0].children.append(TreeNode(State.AGG, value="min"))
        node.children[0].children.append(TreeNode(State.OP, value="="))
        node.children[0].children[1].children.append(TreeNode(State.TERMINAL, value="2"))

        tn = TreeNode(State.ROOT)
        Parser.handle_pair(tn, sqlparse.parse('min(a) = 2')[0].tokens[0])

        self.print_tree(tn)

        self.assertTreeEqual(tn, node)

    def test_handle_pair3(self):
        node = TreeNode(State.ROOT)
        node.children.append(TreeNode(State.COL, value="a"))
        node.children[0].children.append(TreeNode(State.OP, value="="))
        node.children[0].children[0].children.append(TreeNode(State.TERMINAL, value="'2'"))

        tn = TreeNode(State.ROOT)
        Parser.handle_pair(tn, sqlparse.parse("a = '2'")[0].tokens[0])

        self.assertTreeEqual(tn, node)

    def test_select1(self):
        node = TreeNode(State.SELECT)
        node.children.append(TreeNode(State.COL, value="salary"))
        node.children[0].children.append(TreeNode(State.AGG, value="max"))
        node.children.append(TreeNode(State.COL, value="department_name"))

        node.attr['tables']= ['instructor']

        sql = "SELECT max(salary), department_name FROM instructor"
        token = sqlparse.parse(sql)[0]

        tn = TreeNode(State.SELECT)
        Parser.handle_select(tn, token)

        self.print_tree(tn)

        self.assertTreeEqual(tn, node)

    def test_select2(self):
        node = TreeNode(State.ROOT)
        node.children.append(TreeNode(State.NONE))
        node.children[0].children.append(TreeNode(State.SELECT))
        node.children[0].children[0].children.append(TreeNode(State.COL, value="salary"))
        node.children[0].children.append(TreeNode(State.LIMIT, value='1'))

        node.children[0].children[0].attr['tables']= ['instructor']

        sql = "SELECT salary FROM instructor LIMIT 1"
        token = sqlparse.parse(sql)[0]

        tn = TreeNode(State.ROOT)
        Parser.handle(tn, token)

        self.print_tree(tn)

        self.assertTreeEqual(tn, node)

    def test_root2(self):
        node = TreeNode(State.ROOT)
        node.children.append(TreeNode(State.NONE))
        node.children[0].children.append(TreeNode(State.SELECT))
        node.children[0].children[0].children.append(TreeNode(State.COL, value="salary"))
        node.children[0].children[0].children[0].children.append(TreeNode(State.AGG, value="max"))
        node.children[0].children[0].children.append(TreeNode(State.COL, value="department_name"))
        node.children[0].children.append(TreeNode(State.WHERE))
        node.children[0].children[1].children.append(TreeNode(State.COL, value="a"))
        node.children[0].children[1].children[0].children.append(TreeNode(State.OP, value="="))
        node.children[0].children[1].children[0].children[0].children.append(TreeNode(State.TERMINAL, value="2"))

        node.children[0].children[0].attr['tables']= ['instructor']

        sql = "SELECT max(salary), department_name FROM instructor WHERE a = 2"
        token = sqlparse.parse(sql)[0]

        tn = TreeNode(State.ROOT)
        Parser.handle(tn, token)

        self.print_tree(tn)

        self.assertTreeEqual(tn, node)

    def test_root1(self):
        node = TreeNode(State.ROOT)
        node.children.append(TreeNode(State.NONE))
        node.children[0].children.append(TreeNode(State.SELECT))
        node.children[0].children[0].children.append(TreeNode(State.COL, value="salary"))
        node.children[0].children[0].children[0].children.append(TreeNode(State.AGG, value="max"))
        node.children[0].children[0].children.append(TreeNode(State.COL, value="department_name"))

        node.children[0].children[0].attr['tables']= ['instructor']

        sql = "SELECT max(salary), department_name FROM instructor"
        token = sqlparse.parse(sql)[0]

        tn = TreeNode(State.ROOT)
        Parser.handle(tn, token)

        self.assertTreeEqual(tn, node)

    def test_root3(self):
        node = TreeNode(State.ROOT)
        node.children.append(TreeNode(State.NONE))
        node.children[0].children.append(TreeNode(State.SELECT))
        node.children[0].children[0].children.append(TreeNode(State.COL, value="salary"))
        node.children[0].children[0].children[0].children.append(TreeNode(State.AGG, value="max"))
        node.children[0].children[0].children.append(TreeNode(State.COL, value="department_name"))
        node.children[0].children.append(TreeNode(State.GROUP_BY))
        node.children[0].children[1].children.append(TreeNode(State.COL, value="department_name"))

        node.children[0].children[0].attr['tables']= ['instructor']

        sql = "SELECT max(salary), department_name FROM instructor GROUP BY department_name"
        token = sqlparse.parse(sql)[0]

        tn = TreeNode(State.ROOT)
        Parser.handle(tn, token)

        self.assertTreeEqual(tn, node)

    def test_group1(self):
        node = TreeNode(State.GROUP_BY)
        node.children.append(TreeNode(State.COL, value="department_name"))

        sql = "GROUP BY department_name LIMIT 1"
        token = sqlparse.parse(sql)[0]
        tn = TreeNode(State.GROUP_BY)

        Parser.handle_group(tn, token)

        self.assertTreeEqual(tn, node)

    def test_select4(self):
        node = TreeNode(State.SELECT)
        node.children.append(TreeNode(State.COL, value="*"))

        node.attr['tables']= ['instructor']

        sql = "SELECT * FROM instructor"
        token = sqlparse.parse(sql)[0]

        tn = TreeNode(State.SELECT)
        Parser.handle_select(tn, token)

        self.print_tree(tn)

        self.assertTreeEqual(tn, node)

    def test_select3(self):
        node = TreeNode(State.SELECT)
        node.children.append(TreeNode(State.COL, value="*"))
        node.children.append(TreeNode(State.COL, value="department_name"))

        node.attr['tables']= ['instructor']

        sql = "SELECT *, department_name FROM instructor"
        token = sqlparse.parse(sql)[0]

        tn = TreeNode(State.SELECT)
        Parser.handle_select(tn, token)

        self.print_tree(tn)

        self.assertTreeEqual(tn, node)

    def test_group2(self):
        node = TreeNode(State.GROUP_BY)
        node.children.append(TreeNode(State.COL, value="department_name"))
        node.children.append(TreeNode(State.HAVING))
        node.children[1].children.append(TreeNode(State.COL, value="salary"))
        node.children[1].children[0].children.append(TreeNode(State.AGG, value="avg"))
        node.children[1].children[0].children.append(TreeNode(State.OP, value=">"))
        node.children[1].children[0].children[1].children.append(TreeNode(State.TERMINAL, value="1"))

        sql = "GROUP BY department_name HAVING avg(salary) > 1"
        token = sqlparse.parse(sql)[0]
        tn = TreeNode(State.GROUP_BY)
        Parser.handle_group(tn, token)

        self.assertTreeEqual(tn, node)

    def test_group3(self):
        node = TreeNode(State.GROUP_BY)
        node.children.append(TreeNode(State.COL, value="department_name"))
        node.children.append(TreeNode(State.HAVING))
        node.children[1].children.append(TreeNode(State.COL, value="salary"))
        node.children[1].children[0].children.append(TreeNode(State.AGG, value="avg"))
        node.children[1].children[0].children.append(TreeNode(State.OP, value=">"))

        newroot = TreeNode(State.ROOT)
        node.children[1].children[0].children[1].children.append(newroot)

        newroot.children.append(TreeNode(State.NONE))
        newroot.children[0].children.append(TreeNode(State.SELECT))
        newroot.children[0].children[0].children.append(TreeNode(State.COL, value="salary"))
        newroot.children[0].children[0].children[0].children.append(TreeNode(State.AGG, value="avg"))

        newroot.children[0].children[0].attr['tables']=  ['instructor']

        sql = "GROUP BY department_name HAVING avg(salary) > (SELECT avg(salary) FROM instructor)"
        token = sqlparse.parse(sql)[0]
        tn = TreeNode(State.GROUP_BY)
        Parser.handle_group(tn, token)

        self.assertTreeEqual(tn, node)

    def test_or(self):
        node = TreeNode(State.WHERE)
        node.children.append(TreeNode(State.LOGIC, value="or"))
        node.children[0].children.append(TreeNode(State.COL, value="city"))
        node.children[0].children[0].children.append(TreeNode(State.OP, value="="))
        node.children[0].children[0].children[0].children.append(TreeNode(State.TERMINAL, value='"Aberdeen"'))
        node.children[0].children.append(TreeNode(State.COL, value="city"))
        node.children[0].children[1].children.append(TreeNode(State.OP, value="="))
        node.children[0].children[1].children[0].children.append(TreeNode(State.TERMINAL, value='"Abilene"'))

        sql = 'WHERE city  =  "Aberdeen" OR city  =  "Abilene"'
        token = sqlparse.parse(sql)[0]
        tn = TreeNode(State.WHERE)
        Parser.handle_where(tn, token)

        self.assertTreeEqual(tn, node)

    def test_union(self):
        node = TreeNode(State.ROOT)
        node.children.append(TreeNode(State.IUE, value="union"))
        node.children[0].children.append(TreeNode(State.ROOT))
        node.children[0].children[0].children.append(TreeNode(State.NONE))
        node.children[0].children[0].children[0].children.append(TreeNode(State.SELECT))
        node.children[0].children[0].children[0].children[0].children.append(TreeNode(State.COL, value="sourceairport"))
        node.children[0].children.append(TreeNode(State.ROOT))
        node.children[0].children[1].children.append(TreeNode(State.NONE))
        node.children[0].children[1].children[0].children.append(TreeNode(State.SELECT))
        node.children[0].children[1].children[0].children[0].children.append(TreeNode(State.COL, value="destairport"))

        node.children[0].children[0].children[0].children[0].attr['tables']= ['flights']
        node.children[0].children[1].children[0].children[0].attr['tables']= ['flights']

        sql = "SELECT SourceAirport FROM Flights UNION SELECT DestAirport FROM Flights"
        token = sqlparse.parse(sql)[0]

        tn = TreeNode(State.ROOT)
        Parser.handle(tn, token)

        self.print_tree(tn)

        self.assertTreeEqual(tn, node)

    def test_complex(self):
        root = TreeNode(State.ROOT)
        root.children.append(TreeNode(State.NONE))
        root.children[0].children.append(TreeNode(State.SELECT))
        root.children[0].children[0].children.append(TreeNode(State.COL, value="airportname"))
        root.children[0].children.append(TreeNode(State.WHERE))
        root.children[0].children[1].children.append(TreeNode(State.COL, value="airportcode"))
        root.children[0].children[1].children[0].children.append(TreeNode(State.OP, value="not in"))

        node = TreeNode(State.ROOT)
        node.children.append(TreeNode(State.IUE, value="union"))
        node.children[0].children.append(TreeNode(State.ROOT))
        node.children[0].children[0].children.append(TreeNode(State.NONE))
        node.children[0].children[0].children[0].children.append(TreeNode(State.SELECT))
        node.children[0].children[0].children[0].children[0].children.append(TreeNode(State.COL, value="sourceairport"))
        node.children[0].children.append(TreeNode(State.ROOT))
        node.children[0].children[1].children.append(TreeNode(State.NONE))
        node.children[0].children[1].children[0].children.append(TreeNode(State.SELECT))
        node.children[0].children[1].children[0].children[0].children.append(TreeNode(State.COL, value="destairport"))

        root.children[0].children[1].children[0].children[0].children.append(node)

        root.children[0].children[0].attr['tables']= ['airports']
        node.children[0].children[0].children[0].children[0].attr['tables']= ['flights']
        node.children[0].children[1].children[0].children[0].attr['tables']= ['flights']

        sql = "SELECT AirportName FROM Airports WHERE AirportCode NOT IN (SELECT SourceAirport FROM Flights UNION SELECT DestAirport FROM Flights)"
        token = sqlparse.parse(sql)[0]

        tn = TreeNode(State.ROOT)
        Parser.handle(tn, token)

        self.assertTreeEqual(tn, root)

    def test_tables_1(self):
        node = TreeNode(State.ROOT)
        node.children.append(TreeNode(State.NONE))
        node.children[0].children.append(TreeNode(State.SELECT))
        node.children[0].children[0].children.append(TreeNode(State.COL, value="instructor.salary"))
        node.children[0].children.append(TreeNode(State.LIMIT, value='1'))

        node.children[0].children[0].attr['tables']= ['instructor']

        sql = "SELECT salary FROM instructor LIMIT 1"
        token = sqlparse.parse(sql)[0]

        tn = TreeNode(State.ROOT)
        Parser.handle(tn, token, col_map={'salary': 'instructor.salary'})

        self.print_tree(tn)

        self.assertTreeEqual(tn, node)

    def test_tables_2(self):
        node = TreeNode(State.ROOT)
        node.children.append(TreeNode(State.NONE))
        node.children[0].children.append(TreeNode(State.SELECT))
        node.children[0].children[0].children.append(TreeNode(State.COL, value="instructor.salary"))
        node.children[0].children.append(TreeNode(State.LIMIT, value='1'))

        node.children[0].children[0].attr['tables']= ['instructor']

        sql = "SELECT t1.salary FROM instructor AS t1 LIMIT 1"
        token = sqlparse.parse(sql)[0]

        tn = TreeNode(State.ROOT)
        Parser.handle(tn, token, col_map={'t1.salary': 'instructor.salary'})

        self.print_tree(tn)

        self.assertTreeEqual(tn, node)

    def test_tables_3(self):
        node = TreeNode(State.ROOT)
        node.children.append(TreeNode(State.NONE))
        node.children[0].children.append(TreeNode(State.SELECT))
        node.children[0].children[0].children.append(TreeNode(State.COL, value="instructor.salary"))
        node.children[0].children.append(TreeNode(State.LIMIT, value='1'))

        node.children[0].children[0].attr['tables']= ['instructor', 'othertable']

        sql = "SELECT t1.salary FROM instructor AS t1 JOIN othertable AS t2 LIMIT 1"
        token = sqlparse.parse(sql)[0]

        tn = TreeNode(State.ROOT)
        Parser.handle(tn, token, col_map={'t1.salary': 'instructor.salary'})

        self.print_tree(tn)

        self.assertTreeEqual(tn, node)

    def test_tables_3(self):
        node = TreeNode(State.ROOT)
        node.children.append(TreeNode(State.NONE))
        node.children[0].children.append(TreeNode(State.SELECT))
        node.children[0].children[0].children.append(TreeNode(State.COL, value="instructor.salary"))
        node.children[0].children.append(TreeNode(State.LIMIT, value='1'))

        node.children[0].children[0].attr['tables']= ['instructor', 'othertable']

        sql = "SELECT salary FROM instructor AS t1 JOIN othertable AS t2 LIMIT 1"

        table_info = {
            'instructor': ['salary', 'hours'],
            'othertable': ['abc']
        }

        tn = to_tree(sql, table_info)

        self.print_tree(tn)

        self.assertTreeEqual(tn, node)

    def test_tables_4(self):
        node = TreeNode(State.ROOT)
        node.children.append(TreeNode(State.NONE))
        node.children[0].children.append(TreeNode(State.SELECT))
        node.children[0].children[0].children.append(TreeNode(State.COL, value="instructor.salary"))
        node.children[0].children.append(TreeNode(State.LIMIT, value='1'))

        node.children[0].children[0].attr['tables']= ['instructor', 'othertable']

        sql = "SELECT instructor.salary FROM instructor AS t1 JOIN othertable AS t2 LIMIT 1"

        table_info = {
            'instructor': ['salary', 'hours'],
            'othertable': ['abc']
        }

        tn = to_tree(sql, table_info)

        self.print_tree(tn)

        self.assertTreeEqual(tn, node)

    def test_tables_5(self):
        node = TreeNode(State.ROOT)
        node.children.append(TreeNode(State.NONE))
        node.children[0].children.append(TreeNode(State.SELECT))
        node.children[0].children[0].children.append(TreeNode(State.COL, value="instructor.salary"))
        node.children[0].children.append(TreeNode(State.LIMIT, value='1'))

        node.children[0].children[0].attr['tables']= ['instructor', 'othertable']

        sql = "SELECT t1.salary FROM instructor AS t1 JOIN othertable AS t2 LIMIT 1"

        table_info = {
            'instructor': ['salary', 'hours'],
            'othertable': ['abc']
        }

        tn = to_tree(sql, table_info)

        self.print_tree(tn)

        self.assertTreeEqual(tn, node)

    def test_tables_6(self):
        node = TreeNode(State.ROOT)
        node.children.append(TreeNode(State.NONE))
        node.children[0].children.append(TreeNode(State.SELECT))
        node.children[0].children[0].children.append(TreeNode(State.COL, value="instructor.salary"))
        node.children[0].children[0].children.append(TreeNode(State.COL, value="instructor.hours"))
        node.children[0].children.append(TreeNode(State.LIMIT, value='1'))

        node.children[0].children[0].attr['tables']= ['instructor', 'othertable']

        sql = "SELECT t1.salary, hours FROM insTructor AS t1 JOIN othertable AS t2 LIMIT 1"

        table_info = {
            'Instructor': ['salary', 'hours'],
            'othertable': ['abc']
        }

        tn = to_tree(sql, table_info)

        self.print_tree(tn)

        self.assertTreeEqual(tn, node)
